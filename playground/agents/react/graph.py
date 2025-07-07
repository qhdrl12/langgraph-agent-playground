
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

from playground.tools import get_tools
from playground.utils.model import load_chat_model
from playground.agents.react.configuration import Configuration

react_config = Configuration()

async def make_graph(config: RunnableConfig):
    
    # Get name from config or use default
    configurable = config.get("configurable", {})

    # get values from configuration
    llm = configurable.get("model", react_config.model)
    selected_tools = configurable.get("selected_tools", react_config.selected_tools)
    prompt = configurable.get("system_prompt", react_config.system_prompt)
    
    # specify the name for use in supervisor architecture
    name = configurable.get("name", "react_agent")

    # Compile the builder into an executable graph
    # You can customize this by adding interrupt points for state updates
    graph = create_react_agent(
        model=load_chat_model(llm), 
        tools=get_tools(selected_tools),
        prompt=prompt, 
        config_schema=Configuration,
        name=name
    )

    return graph