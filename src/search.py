from typing import Dict, Any
import arxiv
from structlog import get_logger

logger = get_logger()
client = arxiv.Client()


class Arxiv:
    async def run(self, prompt: str):
        # Search for the 10 most recent articles matching the prompt
        search = arxiv.Search(
            query=prompt, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate
        )

        results = []
        for paper in client.results(search):
            processed = self._process_paper(paper)
            logger.info(f"Found paper: {processed['title']}, {processed['id']}")
            results.append(processed)

        return results

    def _process_paper(self, paper: arxiv.Result) -> Dict[str, Any]:
        """Process paper information with resource URI."""
        return {
            "id": paper.get_short_id(),
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "abstract": paper.summary,
            "categories": paper.categories,
            "published": paper.published.isoformat(),
            "url": paper.pdf_url,
            "resource_uri": f"arxiv://{paper.get_short_id()}",
        }

    def download(self, id_list: list):
        pass
