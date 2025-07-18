import os

from firecrawl import FirecrawlApp, ScrapeOptions
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def web_scrape(url: str) -> str:
    """
    Scrape a single webpage using Firecrawl's basic scraping functionality.
    
    Use this tool when you need to extract content from a specific webpage URL.
    This is ideal for:
    - Getting product details from a product page
    - Extracting article content from news sites
    - Reading content from any single webpage
    - Quick data extraction that doesn't require complex navigation
    
    Args:
        url (str): The complete URL of the webpage to scrape (must include http:// or https://)
    
    Returns:
        str: The scraped content in markdown format, or error message if scraping fails
    """
    try:
        scrape_status = firecrawl.scrape_url(
            url, 
            formats=["markdown"],
            only_main_content=True,
            wait_for=1000
        )
        print(f"web_scrape: {scrape_status}")
        return scrape_status
    except Exception as e:
        return f"Error scrapping website: {e}"
    
@tool
def web_crawl(url: str) -> str:
    """
    Crawl an entire website or domain to discover and scrape multiple pages systematically.
    
    Use this tool when you need to:
    - Discover all pages on a website or specific subdirectory
    - Scrape multiple related pages (e.g., all products in a category)
    - Build a comprehensive dataset from a website
    - Find all blog posts, articles, or product pages on a site
    - Map out website structure and content hierarchy
    
    This will follow links and crawl multiple pages starting from the provided URL.
    Be careful with large websites as this can return substantial amounts of data.
    
    Args:
        url (str): The base URL to start crawling from (can be domain root or specific path)
    
    Returns:
        str: Content from all discovered pages in markdown format, 
             or error message if crawling fails
    """
    try:
        crawl_status = firecrawl.crawl_url(
            url, 
            scrape_options=ScrapeOptions(formats=["markdown"])
        )
        print(f"web_crawl: {crawl_status}")
        return crawl_status
    except Exception as e:
        return f"Error crawling website: {e}"

@tool
def web_search(query: str, limit: int = 5) -> str:
    """
    Search the web using Firecrawl's search functionality to find relevant pages.
    
    Use this tool when you need to:
    - Find websites or pages related to a specific topic or product
    - Discover relevant sources before scraping specific content
    - Search for competitor analysis or market research
    - Find multiple sources for price comparison
    - Locate specific types of content across the web
    
    This performs a web search and returns URLs and basic information about found pages.
    Use the results to identify specific URLs for further scraping.
    
    Args:
        query (str): Search query terms (e.g., "wireless bluetooth headphones reviews")
        limit (int): Maximum number of search results to return (default: 5, recommended: 5~10)
    
    Returns:
        str: Search results with URLs and page descriptions, 
             or error message if search fails
    """
    try:
        search_result = firecrawl.search(query=query, limit=limit)
        print(f"web_search: {search_result}")
        return search_result
    except Exception as e:
        return f"Error searching website: {e}"


if __name__ == "__main__":
    # response = web_scrape.invoke("https://www.musinsa.com/goods/3187853")
    # response = web_scrape.invoke("https://www.musinsa.com/app/goods/3187853")
    response = web_search.invoke("마크모크 통굽 샌들 site:musinsa.com")