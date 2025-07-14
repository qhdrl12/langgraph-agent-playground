import os

from firecrawl import FirecrawlApp, ScrapeOptions
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def scrape_with_firecrawl(url: str) -> str:
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
            scrape_options=ScrapeOptions(formats=["markdown"])
        )
        print(f"scrape_with_firecrawl: {scrape_status}")
        return scrape_status
    except Exception as e:
        return f"Error scrapping website: {e}"
    
@tool
def scrape_with_fireagent(url: str) -> str:
    """
    Scrape complex websites using Firecrawl's AI-powered FIRE-1 agent for intelligent data extraction.
    
    Use this tool when basic scraping fails or when dealing with:
    - JavaScript-heavy websites that require interaction
    - Sites with complex navigation or authentication
    - Pages where specific data is hard to locate
    - Dynamic content that loads after page initialization
    - Shopping sites with complex product catalogs
    - Sites that block standard scraping attempts
    
    The FIRE-1 agent can intelligently navigate pages, click buttons, fill forms,
    and extract specific data based on natural language instructions.
    
    Args:
        url (str): The complete URL of the webpage to scrape with AI assistance
    
    Returns:
        str: Detailed scraped content in both markdown and HTML formats, 
             or error message if scraping fails
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
        print(f"crawl_with_firecrawl: {crawl_status}")
        return crawl_status
    except Exception as e:
        return f"Error crawling website: {e}"

@tool
def search_with_firecrawl(query: str, limit: int = 5) -> str:
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
        limit (int): Maximum number of search results to return (default: 5, recommended: 5-20)
    
    Returns:
        str: Search results with URLs and page descriptions, 
             or error message if search fails
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
    Map a website's structure to discover all available pages and their relationships.
    
    Use this tool when you need to:
    - Understand the complete structure of a website before scraping
    - Find all available pages, categories, and sections on a site
    - Discover hidden or hard-to-find pages
    - Plan a comprehensive crawling strategy
    - Analyze website architecture for competitive research
    - Find all product categories or content sections
    
    This returns a site map showing all discoverable URLs and their hierarchy
    without actually scraping the content of each page.
    
    Args:
        url (str): The base URL of the website to map (typically the domain root)
    
    Returns:
        str: Website structure map in markdown format showing all discoverable URLs,
             or error message if mapping fails
    """
    try:
        map_status = firecrawl.map_url(url)
        print(f"map_with_firecrawl: {map_status}")
        return map_status
    except Exception as e:
        return f"Error mapping website: {e}"
