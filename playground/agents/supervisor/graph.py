# Supervisor Agent Graph Construction
# This module creates the LangGraph execution graph for the Supervisor multi-agent system.
# The Supervisor pattern orchestrates multiple specialized sub-agents to handle complex tasks.

from langchain_core.runnables import RunnableConfig
from playground.agents.supervisor.configuration import Configuration
from playground.agents.supervisor.subagents import create_subagents
from playground.utils.model import load_chat_model

from langgraph_supervisor import create_supervisor

async def make_supervisor_graph(config: RunnableConfig):
    """Create a Supervisor multi-agent graph with specialized sub-agents.
    
    This function constructs a Supervisor agent system that orchestrates multiple
    specialized sub-agents to handle complex tasks requiring different capabilities:
    
    - Scrape Agent: Web scraping and data extraction using Firecrawl
    - Research Agent: Comprehensive web research and information gathering
    - Writing Agent: Content creation and formatting from research data
    
    The supervisor analyzes user requests and routes them to appropriate sub-agents,
    coordinating their work to produce comprehensive results.
    
    Args:
        config (RunnableConfig): Configuration containing supervisor and sub-agent parameters
        
    Returns:
        CompiledGraph: The executable supervisor multi-agent graph
    """
    # Extract configuration values from the provided config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful supervisor agent.")
    
    # Create all sub-agents with their specialized configurations
    # This includes scrape_agent, research_agent, and writing_agent
    subagents = await create_subagents(configurable)

    # Create the supervisor graph that orchestrates the sub-agents
    supervisor_graph = create_supervisor(
        agents=subagents,                         # List of specialized sub-agents
        model=load_chat_model(supervisor_model),  # LLM for supervisor reasoning
        prompt=supervisor_system_prompt,          # Instructions for coordination
        config_schema=Configuration               # Configuration schema validation
    )

    # Compile the graph into an executable format
    compiled_graph = supervisor_graph.compile()
    return compiled_graph