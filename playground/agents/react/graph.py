# React Agent Graph Construction
# This module creates the LangGraph execution graph for the React agent.
# The React pattern enables agents to reason about problems and take actions iteratively.

from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

from playground.tools import get_tools
from playground.utils.model import load_chat_model
from playground.agents.react.configuration import Configuration

# Default configuration instance
react_config = Configuration()

async def make_graph(config: RunnableConfig):
    """Create a React agent graph with the given configuration.
    
    This function constructs a React (ReAct) agent that can reason about problems
    and take actions using available tools. The agent follows this pattern:
    1. Receives a user query
    2. Reasons about what actions to take
    3. Executes tools to gather information
    4. Reflects on the results
    5. Continues until the task is complete
    
    Args:
        config (RunnableConfig): Configuration containing agent parameters
        
    Returns:
        CompiledGraph: The executable React agent graph
    """
    
    # Extract configurable parameters from the provided config
    configurable = config.get("configurable", {})

    # Get configuration values with fallbacks to defaults
    llm = configurable.get("model", react_config.model)
    selected_tools = configurable.get("selected_tools", react_config.selected_tools)
    prompt = configurable.get("system_prompt", react_config.system_prompt)
    print(f"prompt={prompt}")  # Debug: show the actual prompt being used
    
    # Agent name for identification (especially useful in supervisor architectures)
    name = configurable.get("name", "react_agent")

    # Create the React agent using LangGraph's prebuilt function
    # This automatically handles the ReAct pattern implementation
    graph = create_react_agent(
        model=load_chat_model(llm),           # Load the specified LLM
        tools=get_tools(selected_tools),      # Get the requested tools
        prompt=prompt,                        # System prompt with instructions
        config_schema=Configuration,          # Schema for configuration validation
        name=name                            # Agent identifier
    )

    return graph