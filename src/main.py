import asyncio

from agent import Agent
from database import setup_database
from structlog import get_logger

logger = get_logger()


def main():
    # Setup the database first
    if setup_database():
        logger.info("Database setup completed successfully")
    else:
        logger.error("Database setup failed")
        return

    agent = Agent("Search for research papers on LLMs and Machine Learning")
    asyncio.run(agent.run())


if __name__ == "__main__":
    try:
        main()
    except RuntimeError:
        logger.info("Agent stopped")
