"""
Finance-related tools for market research and financial data retrieval.
"""

from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_core.tools import tool


@tool
async def finance_research(ticker_symbol: str):
    """
    Search for financial research and news using stock ticker symbols.
    
    Args:
        ticker_symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
        
    Returns:
        Financial news and research data
    """
    yahoo_tool = YahooFinanceNewsTool()
    result = await yahoo_tool.ainvoke(ticker_symbol)
    print(f"finance_research result for {ticker_symbol}: {result}")
    return result