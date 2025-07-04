
from typing import List, Optional
from langgraph.pregel.remote import RemoteGraph
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph_supervisor import create_supervisor
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


class OAPRemoteGraph(RemoteGraph):
    def _sanitize_config(self, config: RunnableConfig) -> RunnableConfig:
        """Sanitize the config to remove non-serializable fields."""
        sanitized = super()._sanitize_config(config)

        # Filter out keys that are already defined in GraphConfigPydantic
        # to avoid the child graph inheriting config from the supervisor
        # (e.g. system_prompt)
        graph_config_fields = set(GraphConfigPydantic.model_fields.keys())

        if "configurable" in sanitized:
            sanitized["configurable"] = {
                k: v
                for k, v in sanitized["configurable"].items()
                if k not in graph_config_fields
            }

        if "metadata" in sanitized:
            sanitized["metadata"] = {
                k: v
                for k, v in sanitized["metadata"].items()
                if k not in graph_config_fields
            }

        return sanitized
    

def make_child_graphs(cfg: GraphConfigPydantic):
    """
    Instantiate a list of RemoteGraph nodes based on the configuration.

    Args:
        cfg: The configuration for the graph

    Returns:
        A list of RemoteGraph instances
    """
    import re

    def sanitize_name(name):
        # Replace spaces with underscores
        sanitized = name.replace(" ", "_")
        # Remove any other disallowed characters (<, >, |, \, /)
        sanitized = re.sub(r"[<|\\/>]", "", sanitized)
        return sanitized

    # If no agents in config, return empty list
    if not cfg.agents:
        return []

    # If access_token is None, create headers without token
    headers = {}

    def create_remote_graph_wrapper(agent: AgentsConfig):
        return OAPRemoteGraph(
            agent.agent_id,
            url=agent.deployment_url,
            name=sanitize_name(agent.name),
            headers=headers,
        )

    return [create_remote_graph_wrapper(a) for a in cfg.agents]



def make_model(cfg: GraphConfigPydantic):
    """Create the appropriate model based on model_name."""
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

    child_graphs = make_child_graphs(cfg)

    graph = create_supervisor(
        child_graphs,
        model=model,
        tools=tools,
        prompt=cfg.system_prompt + UNEDITABLE_SYSTEM_PROMPT,
        config_schema=GraphConfigPydantic,
        handoff_tool_prefix="delegate_to_",
        output_mode="last_message"
    )

    return graph.compile()
