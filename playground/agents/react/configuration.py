# React Agent Configuration
# This module defines the configuration schema for the React (ReAct) agent.
# ReAct agents follow a "Reasoning and Acting" pattern where they:
# 1. Reason about the problem
# 2. Take actions using tools
# 3. Observe the results
# 4. Repeat until the task is complete

from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, Field

from playground.utils.langsmith import get_prompt_with_fallback

# Fallback system prompt when LangSmith prompt is unavailable
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."

class Configuration(BaseModel):
    """Configuration schema for the React agent.
    
    This class defines all configurable parameters for the React agent,
    including system prompts, model selection, and available tools.
    """

    system_prompt: str = Field(
        default_factory=lambda: get_prompt_with_fallback(
              "shopping_advisor",  # LangSmith prompt name
              DEFAULT_SYSTEM_PROMPT,  # Fallback if LangSmith unavailable
            #   "d2a18e1e"  # Optional: specific prompt version
          ).format(today=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        description="The system prompt to use for the agent's interactions. "
        "This prompt sets the context and behavior for the agent. "
        "Automatically injects current date/time into {today} placeholder."
    )

    model: Annotated[
            Literal[
                # OpenAI Models
                "openai/gpt-4.1",
                "openai/gpt-4.1-mini",
                "openai/gpt-4.1-nano",
                
                "openrouter/x-ai/grok-4",
                "openrouter/google/gemini-pro-1.5",
                
                "openrouter/qwen/qwen-2.5-72b-instruct",
                "openrouter/mistral/mistral-large",
            ],
            {"__template_metadata__": {"kind": "llm"}},  # LangGraph metadata
        ] = Field(
            default="openai/gpt-4.1-mini",  # Good balance for most use cases
            description="The name of the language model to use for the agent's main interactions. "
        "Should be in the form: provider/model-name. "
        "OpenAI models for reliability, OpenRouter models for variety and cost options."
    )

    selected_tools: list[Literal[
        "advanced_research_tool",  # Advanced web research with multiple sources
        "basic_research_tool",     # Basic web search functionality
        "scrape_with_firecrawl",   # Web scraping using Firecrawl API
        "get_todays_date"          # Get current date/time
    ]] = Field(
        default = ["scrape_with_firecrawl", "get_todays_date"],  # Default tools for shopping tasks
        description="The list of tools to use for the agent's interactions. "
        "Tools define the actions the agent can take. "
        "Select tools based on the agent's intended use case."
    )