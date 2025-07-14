import os
from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model

def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """
    Loads a chat model based on a fully specified provider/model string.
    
    Supports both OpenAI and OpenRouter providers, automatically handling required API keys from environment variables. Raises a ValueError if the necessary API key is missing.
    
    Parameters:
        fully_specified_name (str): The provider and model name in the format "provider/model" (e.g., "openai/gpt-4.1-mini" or "openrouter/anthropic/claude-3.5-sonnet").
    
    Returns:
        BaseChatModel: An initialized chat model instance.
    
    Raises:
        ValueError: If the required API key for the specified provider is not found in environment variables.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    
    kwargs = {}

    # Check for required API keys
    if provider == "openrouter":
        if not os.getenv("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        print(f"Loading OpenRouter model: {model}")
        provider = "openai"
        kwargs["base_url"] = "https://openrouter.ai/api/v1"
        kwargs["openai_api_key"] = os.getenv("OPENROUTER_API_KEY")

    elif provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        print(f"Loading OpenAI model: {model}")
    
    

    return init_chat_model(model, model_provider=provider, **kwargs)