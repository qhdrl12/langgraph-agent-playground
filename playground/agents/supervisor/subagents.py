# Supervisor Sub-Agents Creation
# This module creates specialized sub-agents for the Supervisor multi-agent system.
# Each sub-agent is a React agent with specific tools and prompts for their domain.

from langchain_core.runnables import RunnableConfig

from playground.agents.react.graph import make_graph
from playground.agents.supervisor.configuration import Configuration

# Legacy constant - not currently used but kept for compatibility
UNEDITABLE_SYSTEM_PROMPT = """UNEDITABLE_SYSTEM_PROMPT """

# Default configuration instance for the supervisor system
supervisor_config = Configuration()
    
async def create_subagents(configurable: dict = None):
    """Create all specialized sub-agents for the Supervisor system.
    
    This function creates three specialized React agents:
    1. Scrape Agent: Web scraping and data extraction using Firecrawl
    2. Research Agent: Comprehensive web research and information gathering
    3. Writing Agent: Content creation and formatting from research data
    
    Each sub-agent is configured with specific tools and prompts optimized
    for their domain expertise.
    
    Args:
        configurable (dict, optional): Configuration overrides for sub-agents
        
    Returns:
        list: List of compiled sub-agent graphs ready for use by supervisor
    """

    print(f"create_subagents configurable: {configurable}")

    if configurable is None:
        configurable = {}

    # === CREATE SCRAPE AGENT ===
    # Specialized for web scraping and data extraction using Firecrawl tools
    scrape_config = RunnableConfig(
        configurable={
            "model": configurable.get("scrape_model", supervisor_config.scrape_model),
            "system_prompt": configurable.get("scrape_system_prompt", supervisor_config.scrape_system_prompt),
            "selected_tools": configurable.get("scrape_tools", supervisor_config.scrape_tools),
            "name": "scrape_agent"  # Agent identifier for supervisor routing
        }
    )

    scrape_agent = await make_graph(scrape_config)

    # === CREATE RESEARCH AGENT ===
    # Specialized for comprehensive web research and information gathering
    research_config = RunnableConfig(
        configurable={
            "model": configurable.get("research_model", supervisor_config.research_model),
            "system_prompt": configurable.get("research_system_prompt", supervisor_config.research_system_prompt),
            "selected_tools": configurable.get("research_tools", supervisor_config.research_tools),
            "name": "general_research_agent"  # Agent identifier for supervisor routing
        }
    )
    general_research_agent = await make_graph(research_config)

    # === CREATE WRITING AGENT ===
    # Specialized for content creation and formatting from research data
    writing_config = RunnableConfig(
        configurable={
            "model": configurable.get("writing_model", supervisor_config.writing_model),
            "system_prompt": configurable.get("writing_system_prompt", supervisor_config.writing_system_prompt),
            "selected_tools": configurable.get("writing_tools", supervisor_config.writing_tools),
            "name": "writing_agent"  # Agent identifier for supervisor routing
        }
    )
    writing_agent = await make_graph(writing_config)
    
    # Return all sub-agents for supervisor orchestration
    return [
        scrape_agent,           # Web scraping and data extraction
        general_research_agent, # Comprehensive web research
        writing_agent           # Content creation and formatting
    ]