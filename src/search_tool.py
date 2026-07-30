'''
search_tool.py

- the research step of the agent
- if an images is worth further search, this tools takes a text query and runs a web search
  via Tavily API, returning a short list of real, sourced results so the final report
  includes genuine external context
'''

#IMPORTS
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

'''
Search the web using Tavily and return a list of result summaries.

- Tavily has a hard 400 character limit on queries.
- queries exceeding the limit therefore crashed the pipeline
- the query truncation below is a defensive fix so this function is safe regardless of
  how long the input text is.
'''

def search_web(query, max_results=3):
    # Tavily's hard limit is 400 chars; leave a safety margin
    query = query[:380]
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
        #print each result's title, plus a short preview of its content [150 chars]
        print(f"- {r['title']}: {r['content'][:150]}...")
        #print source url so result can be traced back to its origin
        print(f"  Source: {r['url']}\n")
