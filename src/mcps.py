from arxiv_mcp_server.tools import handle_search
import json
from structlog import get_logger

logger = get_logger()


class SearchMCP:
    async def run(self, prompt: str):
        results = await handle_search({"query": prompt, "max_results": 5})
        logger.info(f"Found {len(results)}")
        for result in results:
            content = json.loads(result.text)
            if content["total_results"] > 0:
                for paper in content["papers"]:
                    logger.info(f"Result: {paper['title']}")
        return results
