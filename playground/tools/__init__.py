"""
Tools module for the Agent Playground.

This module provides a collection of tools used by all agent architectures
for various tasks including financial research, web search, and utility functions.
"""

from typing import Callable, List, Any

# Import all tools
from .search import advanced_research_tool, basic_research_tool
from .utility import get_todays_date
from .crawl import web_crawl, web_scrape, web_search
from .scrap import search_basic_products,fetch_product_benefits,search_detailed_products,fetch_product_reviews,enrich_products_with_details


def get_tools(selected_tools: List[str]) -> List[Callable[..., Any]]:
    """
    Get tools by name for any agent architecture.
    
    Args:
        selected_tools: List of tool names to retrieve
        
    Returns:
        List of tool functions
    """
    tool_map = {
        "advanced_research": advanced_research_tool,
        "basic_research": basic_research_tool,
        "get_todays_date": get_todays_date,
        "web_scrape": web_scrape,
        "web_crawl": web_crawl,
        "web_search": web_search,
        "search_basic_products": search_basic_products,
        "fetch_product_benefits": fetch_product_benefits,
        "search_detailed_products" : search_detailed_products,
        "fetch_product_reviews": fetch_product_reviews,
        "enrich_products_with_details": enrich_products_with_details,
        
    }

    tools = []
    for tool_name in selected_tools:
        if tool_name in tool_map:
            tools.append(tool_map[tool_name])
    
    return tools


__all__ = [
    "advanced_research_tool", 
    "basic_research_tool",
    "web_scrape",
    "search_basic_products",
    "fetch_product_benefits",
    "search_detailed_products",
    "fetch_product_reviews",
    "enrich_products_with_details",
    "web_crawl",
    "web_search",
    "get_todays_date",
    "get_tools",
]