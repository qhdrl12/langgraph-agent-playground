import os
from typing import Optional
from functools import lru_cache
from langsmith import Client

langsmith_client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))


def pull_prompt(prompt_name: str, version: Optional[str] = None) -> str:
    """Pull prompt from LangSmith Hub"""
    try:
        # 버전 지정 시 포함
        full_name = f"{prompt_name}:{version}" if version else prompt_name

        prompt = langsmith_client.pull_prompt(full_name)
        print(f"pulled prompt: {prompt}")
        return prompt.format_messages()[0].content

    except Exception as e:
        print(f"Failed to pull prompt {prompt_name}: {e}")
        return None

def get_prompt_with_fallback(prompt_name: str, fallback_prompt: str, version: Optional[str] = None) -> str:
    """Pull prompt with fallback to default if failed"""
    langsmith_prompt = pull_prompt(prompt_name, version)
    return langsmith_prompt if langsmith_prompt else fallback_prompt