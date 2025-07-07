
from langchain_core.runnables import RunnableConfig


from playground.agents.react.graph import make_graph
from playground.agents.supervisor.configuration import Configuration


UNEDITABLE_SYSTEM_PROMPT = """UNEDITABLE_SYSTEM_PROMPT """

supervisor_config = Configuration()
    
async def create_subagents(configurable: dict = None):
    """Create all subagents using the make_graph pattern from react_agent."""

    print(f"create_subagents configurable: {configurable}")

    if configurable is None:
        configurable = {}

    scrape_config = RunnableConfig(
        configurable={
            "model": configurable.get("scrape_model", supervisor_config.scrape_model),
            "system_prompt": configurable.get("scrape_system_prompt", supervisor_config.scrape_system_prompt),
            "selected_tools": configurable.get("scrape_tools", supervisor_config.scrape_tools),
            "name": "scrape_agent"
        }
    )

    scrape_agent = await make_graph(scrape_config)

    # Create general research agent using make_graph  
    research_config = RunnableConfig(
        configurable={
            "model": configurable.get("research_model", supervisor_config.research_model),
            "system_prompt": configurable.get("research_system_prompt", supervisor_config.research_system_prompt),
            "selected_tools": configurable.get("research_tools", supervisor_config.research_tools),
            "name": "general_research_agent"
        }
    )
    general_research_agent = await make_graph(research_config)

    # Create writing agent using make_graph
    writing_config = RunnableConfig(
        configurable={
            "model": configurable.get("writing_model", supervisor_config.writing_model),
            "system_prompt": configurable.get("writing_system_prompt", supervisor_config.writing_system_prompt),
            "selected_tools": configurable.get("writing_tools", supervisor_config.writing_tools),
            "name": "writing_agent"
        }
    )
    writing_agent = await make_graph(writing_config)
    
    return [
        scrape_agent, 
        general_research_agent, 
        writing_agent
    ]