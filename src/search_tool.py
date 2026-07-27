import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_web(query, max_results=3):
    """Search the web using Tavily and return a list of result summaries."""
    response = client.search(query=query, max_results=max_results)
    results = response.get("results", [])
    return [
        {"title": r["title"], "content": r["content"], "url": r["url"]}
        for r in results
    ]


if __name__ == "__main__":
    # Test with a query derived from a caption that names something specific
    test_query = "Eiffel Tower history facts"
    results = search_web(test_query)
    for r in results:
        print(f"- {r['title']}: {r['content'][:150]}...")
        print(f"  Source: {r['url']}\n")
