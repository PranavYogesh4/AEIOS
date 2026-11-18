
import requests


class WebSearchTool:

    def search(self, query):

        url = f"https://duckduckgo.com/?q={query}"

        return f"""
        LIVE WEB SEARCH RESULTS
        Search Query:
        {query}

        Search URL:
        {url}

        NOTE:
        Real-time cybersecurity intelligence retrieval
        can be integrated here using APIs later.
        """

