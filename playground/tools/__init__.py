"""
Tools module for the Agent Playground.

This module provides a collection of tools used by all agent architectures
for various tasks including financial research, web search, and utility functions.
"""

from typing import Callable, List, Any

# Import all tools
from .search import advanced_research_tool, basic_research_tool
from .utility import get_todays_date
from .crawl import crawl_with_firecrawl, map_with_firecrawl, scrape_with_firecrawl


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

        "scrape_with_firecrawl": scrape_with_firecrawl,
        "crawl_with_firecrawl": crawl_with_firecrawl,
        "map_with_firecrawl": map_with_firecrawl,
    }
    
    tools = []
    for tool_name in selected_tools:
        if tool_name in tool_map:
            tools.append(tool_map[tool_name])
    
    return tools


__all__ = [
    "advanced_research_tool", 
    "basic_research_tool",
    "scrape_with_firecrawl",
    "crawl_with_firecrawl",
    "map_with_firecrawl",
    "get_todays_date",
    "get_tools",
]