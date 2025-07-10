# Supervisor Agent Configuration
# This module defines the configuration schema for the Supervisor multi-agent system.
# The Supervisor pattern orchestrates multiple specialized sub-agents to handle complex tasks.
# Each sub-agent has specific capabilities and tools optimized for their domain.

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

# Current date for dynamic prompt injection
today = datetime.now().strftime("%Y-%m-%d")

# Supervisor agent's main system prompt
# This prompt defines the supervisor's role as an orchestrator of specialized sub-agents
DEFAULT_SUPERVISOR_PROMPT = f"""today's date is {today}

You are the Executive Content Director orchestrating a team of specialized AI agents to produce exceptional content for clients.

Available agents:
- scrape_agent: Specialized web scraping specialist that extracts and processes data from websites, APIs, and online sources
- general_research_agent: Expert at comprehensive web research on any topic using advanced search tools
- writing_agent: Professional content writer that creates final polished content in any format

Your workflow:
1. Analyze the user's request to understand what type of content they need
2. Route to appropriate research agents to gather information
3. Once you have sufficient research, route to the writing agent to create the final content
4. When the task is complete, you can end the conversation

Example workflow:
- User asks find and organize information on the top 5 popular winter coats and their prices from Musinsa
- You route: ROUTE_TO: scrape_agent (to scrape product data from Musinsa website)
- Agent returns with research
- You route: ROUTE_TO: writing_agent (to create the LinkedIn post)
- Agent returns with final content
- You respond: COMPLETE

Always be strategic about which agents to use and in what order to produce the best possible content.
"""

# Scrape agent's system prompt
# This agent specializes in web scraping and data extraction using Firecrawl tools
DEFAULT_SCRAPE_SYSTEM_PROMPT = f"""today's date is {today}, You are an expert web scraping and data extraction assistant for a digital content agency.
You have access to the following tools: scrape_with_firecrawl, crawl_with_firecrawl, map_with_firecrawl, and get_todays_date.
First get today's date then continue.
The scrape_with_firecrawl tool is used to scrape single web pages and extract clean, structured content from URLs.
The crawl_with_firecrawl tool is used to crawl multiple pages from a website systematically and extract content from all discovered pages.
The map_with_firecrawl tool is used to map and discover the structure of a website, including all available pages and their relationships.
The get_todays_date tool is used to get today's date.
when you are done with your scraping and data extraction, return the processed data to the supervisor agent.
"""

# Research agent's system prompt
# This agent specializes in comprehensive web research using advanced search tools
DEFAULT_RESEARCH_SYSTEM_PROMPT = f"""today's date is {today}, You are an general research agent. 
You have access to the following tools: advanced_research and get_todays_date. 
First get today's date then continue to use the advanced_research tool to search for general information on the topic you are given to research, when your done you return the research to the supervisor agent. 
YOU MUST USE THE ADVANCED_RESEARCH TOOL TO SEARCH FOR INFORMATION YOU NEED.
"""

# Writing agent's system prompt
# This agent specializes in creating polished, final content from research data
DEFAULT_WRITING_SYSTEM_PROMPT = f"""You are an expert writing assistant.
Your primary responsibility is to help draft, edit,  and improve written content to ensure clarity,
correctness, and engagement. You are strictly supposed to take in the content you are given and write the
final content based on the requested format for the user, then return the final content to the supervisor agent.
"""

class Configuration(BaseModel):
    """Configuration schema for the Supervisor multi-agent system.
    
    This class defines all configurable parameters for the supervisor and its sub-agents.
    The supervisor coordinates between specialized agents:
    - Scrape agent: Web scraping and data extraction
    - Research agent: General web research and information gathering
    - Writing agent: Content creation and formatting
    """
    
    # === SUPERVISOR CONFIGURATION ===
    supervisor_system_prompt: str = Field(
        default=DEFAULT_SUPERVISOR_PROMPT,
        description="The system prompt to use for the supervisor agent's interactions. "
        "This prompt defines the supervisor's role as an orchestrator of sub-agents.",
        json_schema_extra={"langgraph_nodes": ["supervisor"], "langgraph_type": "prompt"}
    )

    supervisor_model: Annotated[
        Literal[
            # OpenAI Models
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
            
            # OpenRouter Models
            "openrouter/x-ai/grok-4",
            "openrouter/google/gemini-pro-1.5",
        ], 
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",  # Good default for most supervisor tasks
        description="The name of the language model to use for the supervisor agent. "
        "Supervisor needs good reasoning for agent coordination. "
        "grok-4 recommended for complex orchestration.",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )

    # === SCRAPE AGENT CONFIGURATION ===
    scrape_system_prompt: str = Field(
        default=DEFAULT_SCRAPE_SYSTEM_PROMPT,
        description="The system prompt for the scraping sub-agent. "
        "This agent specializes in web scraping and data extraction using Firecrawl.",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}
    )

    scrape_model: Annotated[
        Literal[
            # OpenAI Models
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
            
            # OpenRouter Models - Good for Scraping
            "openrouter/grok-4",
            "openrouter/anthropic/claude-3-haiku",
            "openrouter/meta-llama/llama-3.1-8b-instruct",
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",  # Good balance for scraping tasks
        description="The name of the language model to use for the scrape sub-agent. "
        "Scraping requires good reasoning for data extraction.",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}            
    )

    scrape_tools: list[Literal[
        "scrape_with_firecrawl",  # Single page scraping
        "crawl_with_firecrawl",   # Multi-page crawling
        "map_with_firecrawl",     # Site structure mapping
        "get_todays_date"         # Date utility
    ]] = Field(
        default=["scrape_with_firecrawl", "crawl_with_firecrawl", "get_todays_date"],
        description="The list of tools to make available to the scrape sub-agent. "
        "These tools provide comprehensive web scraping capabilities.",
        json_schema_extra={"langgraph_nodes": ["scrape_agent"]}
    )

    # === RESEARCH AGENT CONFIGURATION ===
    research_system_prompt: str = Field(
        default=DEFAULT_RESEARCH_SYSTEM_PROMPT,
        description="The system prompt for the research sub-agent. "
        "This agent specializes in comprehensive web research and information gathering.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    research_model: Annotated[
        Literal[
            # OpenAI Models
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
            
            # OpenRouter Models - Good for Research
            "openrouter/grok-4",
            "openrouter/google/gemini-pro-1.5",
            "openrouter/anthropic/claude-3-haiku",
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",  # Good balance for research tasks
        description="The name of the language model to use for the research sub-agent. "
        "Research requires good reasoning for information synthesis.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    research_tools : list[Literal[
        "basic_research",     # Simple web search
        "advanced_research",  # Multi-source research
        "get_todays_date"     # Date utility
    ]] = Field(
        default=["advanced_research", "get_todays_date"],
        description="The list of tools to make available to the research sub-agent. "
        "Advanced research provides comprehensive information gathering capabilities.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    # === WRITING AGENT CONFIGURATION ===
    writing_system_prompt: str = Field(
        default=DEFAULT_WRITING_SYSTEM_PROMPT,
        description="The system prompt for the writing sub-agent. "
        "This agent specializes in creating polished, final content from research data.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )

    writing_model: Annotated[
        Literal[
            # OpenAI Models
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
            
            # OpenRouter Models - Good for Writing
            "openrouter/grok-4",
            "openrouter/google/gemini-pro-1.5",
            "openrouter/anthropic/claude-3-haiku",
        ],
        {"__template_metadata__": {"kind": "llm"}}
    ] = Field(
        default="openai/gpt-4.1-mini",  # Good balance for writing tasks
        description="The name of the language model to use for the writing sub-agent. "
        "Writing requires good language skills for content creation.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )

    writing_tools: list[Literal[
        "advanced_research",  # Additional research if needed
        "basic_research",     # Simple fact-checking
        "get_todays_date"     # Date utility
    ]] = Field(
        default = ["advanced_research", "get_todays_date"],
        description="The list of tools to make available to the writing sub-agent. "
        "Writing agent can do additional research if needed for content creation.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )
