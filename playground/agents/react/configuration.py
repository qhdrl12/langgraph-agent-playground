from typing import Annotated, Literal
from pydantic import BaseModel, Field

class Configuration(BaseModel):
    """The configuration for the agent."""

    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        description="The system prompt to use for the agent's interactions. "
        "This prompt sets the context and behavior for the agent."
    )

    model: Annotated[
            Literal[
                "openai/gpt-4.1",
                "openai/gpt-4.1-mini",
                "openai/gpt-4.1-nano",
            ],
            {"__template_metadata__": {"kind": "llm"}},
        ] = Field(
            default="openai/gpt-4.1-mini",
            description="The name of the language model to use for the agent's main interactions. "
        "Should be in the form: provider/model-name."
    )

    selected_tools: list[Literal["finance_research", "advanced_research_tool", "basic_research_tool", "get_todays_date"]] = Field(
        default = ["get_todays_date"],
        description="The list of tools to use for the agent's interactions. "
        "This list should contain the names of the tools to use."
    )