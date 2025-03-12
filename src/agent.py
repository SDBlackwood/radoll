import structlog
import asyncio
import functools
import signal

logger = structlog.get_logger()


class Agent:
    """
    Agent orchestrates all of the actions for ragdoll
    """

    def __init__(self, prompt: str):
        self.prompt = prompt

    async def run(self):
        """
        Runs a loop until we send an exit signal
        """
        loop = asyncio.get_running_loop()

        for signame in {"SIGINT", "SIGTERM"}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self.stop, signame, loop),
            )

        logger.info("Beginning agent loop")
        logger.info(f"Prompt: {self.prompt}")
        while True:
            await asyncio.sleep(5)
            logger.info("Looping")

    def stop(self, signame, loop):
        logger.info("Stoping agent")
        loop.stop()
