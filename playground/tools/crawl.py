import os

from firecrawl import FirecrawlApp
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def scrape_with_firecrawl(url: str) -> str:
    """Use this to scrape a website with firecrawl"""
    try:
        scrape_status = firecrawl.scrape_url(url, formats=["markdown"])
        print(f"scrape_with_firecrawl: {scrape_status}")
        return scrape_status
    except Exception as e:
        return f"Error scrapping website: {e}"
    
@tool
def scrape_with_fireagent(url: str) -> str:
    """
    Use this to scrape a website with firecrawl(Fire-1).
    For difficult collection requests, use that tool.
    """
    try:
        scrape_result = firecrawl.scrape_url(url, 
            formats=["markdown", "html"],
            agent={
                'model': 'FIRE-1',
                "prompt": "Search until you get detailed results that satisfy your user requests."
            }
        )
        print(f"scrape_with_fire1: {scrape_result}")
        return scrape_result
    except Exception as e:
        return f"Error scrapping website: {e}"


@tool
def crawl_with_firecrawl(url: str) -> str:
    """Use this to crawl a website with firecrawl"""
    try:
        crawl_status = firecrawl.crawl_url(url, formats=["markdown"])
        print(f"crawl_with_firecrawl: {crawl_status}")
        return crawl_status
    except Exception as e:
        return f"Error crawling website: {e}"
    
@tool
def map_with_firecrawl(url: str) -> str:
    """Use this to map a website with firecrawl"""
    try:
        map_status = firecrawl.map_url(url, formats=["markdown"])
        print(f"map_with_firecrawl: {map_status}")
        return map_status
    except Exception as e:
        return f"Error mapping website: {e}"

