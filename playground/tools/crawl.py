import os

from firecrawl import FirecrawlApp, ScrapeOptions
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def scrape_with_firecrawl(url: str) -> str:
    """
    Extracts the main content from a single webpage using Firecrawl's standard scraping.
    
    Use this function to quickly retrieve readable content (such as articles, product details, or page text) from a specific URL. Returns the extracted content in markdown format, or an error message if scraping fails.
    
    Parameters:
        url (str): The full URL of the webpage to scrape, including the protocol (http:// or https://).
    
    Returns:
        str: Scraped content in markdown format, or an error message if the operation fails.
    """
    try:
        scrape_status = firecrawl.scrape_url(
            url, 
            scrape_options=ScrapeOptions(formats=["markdown"])
        )
        print(f"scrape_with_firecrawl: {scrape_status}")
        return scrape_status
    except Exception as e:
        return f"Error scrapping website: {e}"
    
@tool
def scrape_with_fireagent(url: str) -> str:
    """
    Scrape complex or dynamic websites using Firecrawl's FIRE-1 AI agent for advanced data extraction.
    
    This tool is suitable for pages with dynamic content, JavaScript interactions, complex navigation, or when standard scraping methods are insufficient. The FIRE-1 agent can interact with web elements and extract detailed content in both markdown and HTML formats.
    
    Parameters:
        url (str): The full URL of the webpage to be scraped.
    
    Returns:
        str: The scraped content in markdown and HTML formats, or an error message if scraping fails.
    """
    try:
        scrape_result = firecrawl.scrape_url(
            url, 
            scrape_options=ScrapeOptions(
                formats=["markdown", "html"],
                agent={
                    'model': 'FIRE-1',
                    "prompt": "Search until you get detailed results that satisfy your user requests."
                }
            )
        )
        print(f"scrape_with_fire1: {scrape_result}")
        return scrape_result
    except Exception as e:
        return f"Error scrapping website: {e}"


@tool
def crawl_with_firecrawl(url: str) -> str:
    """
    Crawls a website starting from the given URL to discover and scrape multiple pages.
    
    This function systematically follows links from the provided URL, collecting content from all reachable pages. It is useful for building datasets, extracting all articles or products, or mapping the structure of a website. The result is returned in markdown format. For large sites, the output may be extensive.
    
    Parameters:
        url (str): The starting URL for the crawl.
    
    Returns:
        str: Combined content from all discovered pages in markdown format, or an error message if crawling fails.
    """
    try:
        crawl_status = firecrawl.crawl_url(
            url, 
            scrape_options=ScrapeOptions(formats=["markdown"])
        )
        print(f"crawl_with_firecrawl: {crawl_status}")
        return crawl_status
    except Exception as e:
        return f"Error crawling website: {e}"

@tool
def search_with_firecrawl(query: str, limit: int = 5) -> str:
    """
    Perform a web search using Firecrawl to find relevant pages for a given query.
    
    Searches the web based on the provided query and returns a list of URLs with brief descriptions. Useful for discovering sources, competitor sites, or relevant content before scraping specific pages.
    
    Parameters:
        query (str): The search terms to use.
        limit (int): The maximum number of results to return (default is 5).
    
    Returns:
        str: A formatted list of search results with URLs and descriptions, or an error message if the search fails.
    """
    try:
        search_result = firecrawl.search(query=query, limit=limit)
        print(f"search_with_firecrawl: {search_result}")
        return search_result
    except Exception as e:
        return f"Error searching website: {e}"

@tool
def map_with_firecrawl(url: str) -> str:
    """
    Generate a hierarchical map of all discoverable pages on a website without scraping their content.
    
    Parameters:
        url (str): The base URL of the website to map.
    
    Returns:
        str: A markdown-formatted site map showing the structure and URLs of the website, or an error message if mapping fails.
    """
    try:
        map_status = firecrawl.map_url(url)
        print(f"map_with_firecrawl: {map_status}")
        return map_status
    except Exception as e:
        return f"Error mapping website: {e}"
