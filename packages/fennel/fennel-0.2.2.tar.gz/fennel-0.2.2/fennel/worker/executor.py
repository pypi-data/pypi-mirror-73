import asyncio
import logging
import signal
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from functools import partial
from logging.handlers import QueueHandler
from multiprocessing import Queue
from typing import Optional

import structlog
import uvloop

from fennel.exceptions import UnknownTask
from fennel.job import Job
from fennel.utils import base64uuid, duration
from fennel.worker.broker import Broker

logger = structlog.get_logger("fennel.worker")


EXIT_SIGNAL = "signal"
EXIT_COMPLETE = "complete"


class Executor:
    def __init__(self, app):
        """
        The `Executor` is responsible for reading jobs from the Redis queue and execute
        them.

        Heartbeats are sent from the executor periodically (controlled by
        :attr:`fennel.settings.Settings.heartbeat_interval`). If they are missing for
        more than :attr:`fennel.settings.Settings.heartbeat_timeout` seconds, the
        executor will be assumed dead and all of its pending messages will be reinserted
        to the stream by another worker's maintenance function.

        Parameters
        ----------
        app : fennel.App
            The application instance for which to start an `Executor`.
        """
        self.app = app
        self.settings = app.settings
        self.executor_id: str = base64uuid()
        self.must_stop = False
        self.broker: Optional[Broker] = None  # Set on .start()

    def start(self, exit: str = EXIT_SIGNAL, queue: Queue = None) -> None:
        """
        Begin the main executor loop.

        Parameters
        ----------
        exit : str
            The exit strategy. `EXIT_SIGNAL` is used when the worker should only stop on
            receipt of a interrupt or termination signal. `EXIT_COMPLETE` is used in tests
            to exit when all tasks from the queue have completed.
        queue : multiprocessing.Queue
            A `QueueHandler` will be used to send logs to this queue to avoid
            interleaving from multiple processes.

        Notes
        -----
        Intended to run via :func:`fennel.worker.worker.start` which will supervise
        multiple `Executor` processes.

        `signal.SIGINT` and `signal.SIGTERM` are handled by gracefully shutting down,
        which means giving the executor processes a chance to finish their current
        tasks.
        """
        if queue:
            # To prevent interleaved logging.
            logging.getLogger("fennel.worker").addHandler(QueueHandler(queue))

        uvloop.install()
        asyncio.run(self._start(exit=exit))

    def stop(self):
        """
        Gracefully stop all running coroutines, giving them a chance to complete execution
        of their current task.
        """
        if not self.must_stop:
            logger.warning("shutting-down", executor=self.executor_id)
            self.must_stop = True

    async def _start(self, exit) -> None:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.add_signal_handler(signal.SIGTERM, self.stop)

        n = self.settings.concurrency
        self.broker = await Broker.for_app(self.app)

        consumers = [self._loop(f"{self.executor_id}:{i}", exit) for i in range(n)]
        maintainers = [self._heartbeat(), self._scheduler(), self._maintenance()]

        logger.warning("executor-started", executor=self.executor_id)
        await asyncio.gather(*consumers + maintainers)
        logger.warning("executor-stopped", executor=self.executor_id)

    async def _loop(self, consumer_id: str, exit: str) -> None:
        """
        The main consumer loop: read data from the stream and handle processing.
        """
        while not self.must_stop:
            results = await self.broker.read(
                consumer=consumer_id,
                count=self.settings.prefetch_count,
                recover=False,
                timeout=self.settings.read_timeout,
            )

            if exit == EXIT_COMPLETE and not results:
                self.stop()
                return

            for xid, fields in results:
                job = await self.broker.executing(fields["uuid"])
                await self._handle(xid, job, consumer_id)

    async def _handle(self, xid: str, job: Job, consumer_id: str) -> None:
        """
        Handle the given job. All jobs are acknowledged and deleted after processing.
        Depending on the outcome, they will also be scheduled for reprocessing, their
        result will be stored, or they will be put in the dead-letter queue.
        """
        with duration(logger, "executing", xid=xid, job=asdict(job), con=consumer_id):
            job = await self._execute(job)
            job = job.increment()

            if job.exception:
                if job.tries <= job.max_retries:
                    await self.broker.ack_and_schedule(xid, job)
                    logger.debug("ack-schedule", xid=xid, job=asdict(job))
                else:
                    await self.broker.ack_and_dead(xid, job)
                    logger.debug("ack-dead", xid=xid, job=asdict(job))
            else:
                if not self.settings.results_enabled:
                    await self.broker.ack(xid, job)
                    logger.debug("ack", xid=xid, job=asdict(job))
                else:
                    await self.broker.ack_and_store(xid, job)
                    logger.debug("ack-store", xid=xid, job=asdict(job))

    async def _execute(self, job: Job) -> Job:
        """
        Attempt execution of a task. If the task is a coroutine function, then await it
        in our current event loop, otherwise run the task in a thread pool executor so
        as not to block the loop.
        """
        try:
            f = self.app.task_map[job.task]
            args, kwargs = job.args, job.kwargs
        except KeyError:
            raise UnknownTask(f"Could not find function: {job.task}")

        try:
            if asyncio.iscoroutinefunction(f):
                val = await f(*args, **kwargs)
            else:
                with ThreadPoolExecutor(max_workers=1) as pool:
                    loop = asyncio.get_running_loop()
                    val = await loop.run_in_executor(pool, partial(f, *args, **kwargs))
        except BaseException as e:
            logger.exception("execution-failed", job=asdict(job))
            return job.replace(
                exception={
                    "original_type": type(e).__name__,
                    "original_args": list(e.args),
                },
                return_value=None,
            )
        else:
            return job.replace(exception={}, return_value=val)

    async def _heartbeat(self) -> None:
        """
        Publish a heartbeat for this executor. If heartbeats are missing for more than
        settings.heartbeat_timeout seconds, the executor will be considered dead and all
        its consumers' messages will be deleted and added to the stream for
        reprocessing.
        """
        while not self.must_stop:
            await self.broker.heartbeat(self.executor_id)
            logger.info("heartbeat", executor=self.executor_id)
            await asyncio.sleep(self.settings.heartbeat_interval)

    async def _scheduler(self) -> None:
        """
        Find any jobs whose ETA has passed and add them to the stream. Jobs are stored
        in a sorted set by their expected time of arrival and we find tasks whose value
        is less than 'now'.
        """
        while not self.must_stop:
            results = await self.broker.process_schedule()
            logger.info("poll-schedule", executor=self.executor_id, results=results)
            await asyncio.sleep(self.settings.schedule_interval)

    async def _maintenance(self) -> None:
        """
        The maintenance script performs the following:
            1. Find dead consumers (their executor heartbeats are missing for greater
            than settings.heartbeat_timeout).
            2. Delete their pending messages and put them back in the stream for other
            consumers to process.
            3. Delete the dead consumers (and the executor's last heartbeat).
        """
        while not self.must_stop:
            results = await self.broker.maintenance(self.settings.heartbeat_timeout)
            logger.info("maintenance", executor=self.executor_id, results=results)
            await asyncio.sleep(self.settings.maintenance_interval)
