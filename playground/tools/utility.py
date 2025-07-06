"""
Utility tools for common tasks and helper functions.
"""

from datetime import datetime
from langchain_core.tools import tool


@tool
async def get_todays_date() -> str:
    """
    Get the current date in YYYY-MM-DD format.
    
    Returns:
        Current date as string
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date