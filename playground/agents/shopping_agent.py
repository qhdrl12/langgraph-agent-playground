"""Main shopping agent implementation."""

from typing import List, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
import os

from pydantic import BaseModel, Field


UNEDITABLE_SYSTEM_PROMPT = """UNEDITABLE_SYSTEM_PROMPT """

DEFAULT_SUPERVISOR_PROMPT = """You are a shopping assistant powered by Firecrawl web scraping capabilities. Help users find products, compare prices, and analyze reviews by extracting information from shopping websites.

Available tools:
1. product_search: Extract detailed product information from a specific product page URL
2. firecrawl_scraper: General web scraping for any shopping website 
3. price_comparison: Compare prices across different sources
4. review_analysis: Analyze product reviews and ratings

When helping users:
- Ask for specific product URLs when they want detailed product information
- Use firecrawl_scraper for general web page content extraction
- Use product_search for structured product data extraction
- Always provide clear, helpful recommendations based on scraped data
- Explain what information was extracted and from which sources

Be thorough and accurate in your analysis of scraped content.
"""

class AgentsConfig(BaseModel):
    deployment_url: str
    """The URL of the LangGraph deployment"""
    agent_id: str
    """The ID of the agent to use"""
    name: str
    """The name of the agent"""


class GraphConfigPydantic(BaseModel):
    agents: List[AgentsConfig] = Field(
        default=[],
        metadata={"x_oap_ui_config": {"type": "agents"}},
    )
    system_prompt: Optional[str] = Field(
        default=DEFAULT_SUPERVISOR_PROMPT,
        metadata={
            "x_oap_ui_config": {
                "type": "textarea",
                "placeholder": "Enter a system prompt...",
                "description": f"The system prompt to use in all generations. The following prompt will always be included at the end of the system prompt:\n---{UNEDITABLE_SYSTEM_PROMPT}---",
                "default": DEFAULT_SUPERVISOR_PROMPT,
            }
        },
    )




def make_model(cfg: GraphConfigPydantic):
    """Create the appropriate model based on model_name."""
    # if model_name.startswith("gpt-"):
    #     return ChatOpenAI(
    #         model=model_name,
    #         temperature=0.1,
    #         api_key=os.getenv("OPENAI_API_KEY")
    #     )
    # else:
    #     # Default to OpenAI
    #     return ChatOpenAI(
    #         model=model_name,
    #         base_url="https://openrouter.ai/api/v1",
    #         temperature=0.1,
    #         api_key=os.getenv("OPENROUTER_API_KEY")
    #     )
    return ChatOpenAI(model="gpt-4.1-mini", temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))


async def make_tool(cfg: GraphConfigPydantic):
    client = MultiServerMCPClient(
        {
            "firecrawl": {
                "command": "npx",
                "args": ["-y", "firecrawl-mcp"],
                "env": {"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
                "transport": "stdio", 
            }
        }
    )

    return await client.get_tools()


async def graph(config: RunnableConfig):
    cfg = GraphConfigPydantic(**config.get("configurable", {}))
    model = make_model(cfg)
    tools = await make_tool(cfg)

    return create_react_agent(
        model=model,
        tools=tools,
        prompt=cfg.system_prompt + UNEDITABLE_SYSTEM_PROMPT
    )
