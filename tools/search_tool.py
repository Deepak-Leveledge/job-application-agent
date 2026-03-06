from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()
import os 

def search_web(query:str ,max_result :int = 5)-> str:
    print(f"🔎 Searching the web for: {query}")

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = client.search(
        query=query,
        max_results=max_result,
        search_depth="advanced"
    )

    # extract and format results

    results =""
    for i , result in enumerate(response["results"]):
        results += f"""
Result {i+1}:
Title: {result["title"]}
URL: {result["url"]}
Content: {result["content"]}
---
"""


    print(f"✅ Search completed! {len(response['results'])} results found.")
    return results
