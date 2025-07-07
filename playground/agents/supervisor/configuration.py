from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field


today = datetime.now().strftime("%Y-%m-%d")

DEFAULT_SUPERVISOR_PROMPT = f"""today's date is {today}

You are the Executive Content Director orchestrating a team of specialized AI agents to produce exceptional content for clients.

Available agents:
- finance_research_agent: Specialized in financial data research and analysis using Yahoo Finance and other financial sources
- general_research_agent: Expert at comprehensive web research on any topic using advanced search tools
- writing_agent: Professional content writer that creates final polished content in any format

Your workflow:
1. Analyze the user's request to understand what type of content they need
2. Route to appropriate research agents to gather information
3. Once you have sufficient research, route to the writing agent to create the final content
4. When the task is complete, you can end the conversation

Example workflow:
- User asks for LinkedIn post about Tesla's latest earnings
- You route: ROUTE_TO: finance_research_agent (to get Tesla financial data)
- Agent returns with research
- You route: ROUTE_TO: writing_agent (to create the LinkedIn post)
- Agent returns with final content
- You respond: COMPLETE

Always be strategic about which agents to use and in what order to produce the best possible content.
"""

DEFAULT_SCRAPE_SYSTEM_PROMPT = f"""today's date is {today}, You are an expert web scraping and data extraction assistant for a digital content agency.
You have access to the following tools: scrape_with_firecrawl, crawl_with_firecrawl, map_with_firecrawl, and get_todays_date.
First get today's date then continue.
The scrape_with_firecrawl tool is used to scrape single web pages and extract clean, structured content from URLs.
The crawl_with_firecrawl tool is used to crawl multiple pages from a website systematically and extract content from all discovered pages.
The map_with_firecrawl tool is used to map and discover the structure of a website, including all available pages and their relationships.
The get_todays_date tool is used to get today's date.
when you are done with your scraping and data extraction, return the processed data to the supervisor agent.
"""

DEFAULT_RESEARCH_SYSTEM_PROMPT = f"""today's date is {today}, You are an general research agent. 
You have access to the following tools: advanced_research and get_todays_date. 
First get today's date then continue to use the advanced_research tool to search for general information on the topic you are given to research, when your done you return the research to the supervisor agent. 
YOU MUST USE THE ADVANCED_RESEARCH TOOL TO SEARCH FOR INFORMATION YOU NEED.
"""

DEFAULT_WRITING_SYSTEM_PROMPT = f"""You are an expert writing assistant.
Your primary responsibility is to help draft, edit,  and improve written content to ensure clarity,
correctness, and engagement. You are strictly supposed to take in the content you are given and write the
final content based on the requested format for the user, then return the final content to the supervisor agent.
"""

class Configuration(BaseModel):
    supervisor_system_prompt: str = Field(
        default=DEFAULT_SUPERVISOR_PROMPT,
        description="The system prompt to use for the supervisor agent's interactions",
        json_schema_extra={"langgraph_nodes": ["supervisor"], "langgraph_type": "prompt"}
    )

    supervisor_model: Annotated[
        Literal[
            "openai/gpt-4.1", 
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
        ], 
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",
        description="The name of the language model to use for the supervisor agent.",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )

    scrape_system_prompt: str = Field(
        default=DEFAULT_SCRAPE_SYSTEM_PROMPT,
        description="The system prompt for the scrapping sub-agent",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}
    )

    scrape_model: Annotated[
        Literal[
            "openai/gpt-4.1", 
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",                
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",
        description="The name of the language model to use for the scrape sub-agent.",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}            
    )

    scrape_tools: list[Literal["scrape_with_firecrawl", "crawl_with_firecrawl", "map_with_firecrawl", "get_todays_date"]] = Field(
        default=["scrape_with_firecrawl", "crawl_with_firecrawl", "get_todays_date"],
        description="The list of tools to make available to the general scrape sub-agent.",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}
    )

    research_system_prompt: str = Field(
        default=DEFAULT_RESEARCH_SYSTEM_PROMPT,
        description="The system prompt for the research sub-agent",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    research_model: Annotated[
        Literal[
            "openai/gpt-4.1", 
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",
        description="The name of the language model to use for the research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    research_tools : list[Literal["finance_research", "basic_research", "advanced_research", "get_todays_date"]] = Field(
        default=["advanced_research", "get_todays_date"],
        description="The list of tools to make available to the general research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    writing_system_prompt: str = Field(
        default=DEFAULT_WRITING_SYSTEM_PROMPT,
        description="The system prompt for the writing sub-agent",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )

    writing_model: Annotated[
        Literal[
            "openai/gpt-4.1", 
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",
        description="The name of the language model to use for the research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )

    writing_tools: list[Literal["finance_research", "advanced_research", "basic_research", "get_todays_date"]] = Field(
        default = ["advanced_research", "get_todays_date"],
        description="The list of tools to make available to the general research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )
