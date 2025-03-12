import asyncio

from agent import Agent
from structlog import get_logger

logger = get_logger()


def main():
    agent = Agent("Search for research papers on LLMs and Machine Learning")
    asyncio.run(agent.run())


if __name__ == "__main__":
    try:
        main()
    except RuntimeError:
        logger.info("Agent stopped")
