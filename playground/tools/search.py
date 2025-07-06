"""
Search tools for web research and information retrieval.
"""

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool


@tool
async def advanced_research_tool(query: str):
    """
    Perform comprehensive web searches for detailed research.
    
    Args:
        query: The search query string
        
    Returns:
        Search results with detailed information
    """
    tavily_tool = TavilySearchResults(
        max_results=10,
        search_depth="advanced"
    )
    result = await tavily_tool.ainvoke({"query": query})
    print(f"advanced_research_tool result: {result}")
    return result


@tool
async def basic_research_tool(query: str):
    """
    Research trending topics for social media content.
    
    Args:
        query: The search query string
        
    Returns:
        Trending search results
    """
    tavily_tool = TavilySearchResults(
        max_results=5,
        search_depth="basic",
        include_raw_content=False,
        include_images=True
    )
    enhanced_query = f"trending {query}"
    result = await tavily_tool.ainvoke({"query": enhanced_query})
    print(f"basic_research_tool result: {result}")
    return result