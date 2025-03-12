from mcps import SearchMCP
from structlog.contextvars import (
    bind_contextvars,
)
import asyncio
import functools
import signal
import enum

import structlog

logger = structlog.get_logger()


class State(enum.Enum):
    INIT = 1
    COLLECTED = 2
    EVALUATED = 3
    METADATA_STORED = 4
    RESOURCE_PARSED = 5
    RESOURCE_STORED = 6


class Transition(enum.Enum):
    SEARCHING = 1
    EVALUATING = 2
    STORING_METADATA = 3
    PARSING = 4
    STORING_RESOURCE = 5


class Agent:
    """
    Agent orchestrates all of the actions for ragdoll
    """

    def __init__(self, prompt: str):
        self.prompt = prompt
        self.mcp = {"search": SearchMCP()}

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
        # State Machine Loop
        state = State.INIT
        while True:
            match state:
                case State.INIT:
                    new_state = State.COLLECTED
                    transition = Transition.SEARCHING
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")

                    self.results = await self.search()

                    state = new_state
                case State.COLLECTED:
                    new_state = State.EVALUATED
                    transition = Transition.EVALUATING
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")
                    await asyncio.sleep(5)
                    state = new_state
                case State.EVALUATED:
                    new_state = State.METADATA_STORED
                    transition = Transition.STORING_METADATA
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")
                    await asyncio.sleep(5)
                    state = new_state
                case State.METADATA_STORED:
                    new_state = State.RESOURCE_PARSED
                    transition = Transition.PARSING
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")
                    await asyncio.sleep(5)
                    state = new_state
                case State.RESOURCE_PARSED:
                    new_state = State.RESOURCE_STORED
                    transition = Transition.STORING_RESOURCE
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")
                    await asyncio.sleep(5)
                    state = new_state
                case State.RESOURCE_STORED:
                    new_state = State.COLLECTED
                    transition = Transition.SEARCHING
                    bind_contextvars(transition=transition.name, state=state.name)
                    logger.info(f"Transitioning to {new_state} through {transition}")
                    await asyncio.sleep(5)
                    state = new_state

    def stop(self, signame, loop):
        logger.info("Stoping agent")
        loop.stop()

    async def search(self):
        """
        Use MCP to Search for results
        """
        return await self.mcp["search"].run(self.prompt)
