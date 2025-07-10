"""
pytest 설정 및 공통 픽스처
"""

import pytest
import warnings
import os
from typing import Dict, List

# 전역 경고 억제
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", message=".*PydanticDeprecatedSince.*")
warnings.filterwarnings("ignore", message=".*__fields__.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope="session")
def api_keys() -> Dict[str, bool]:
    """API 키 존재 여부 확인 픽스처"""
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
    }

@pytest.fixture(scope="session")
def available_models(api_keys) -> List[str]:
    """사용 가능한 모델 목록 픽스처"""
    models = []
    
    if api_keys["openai"]:
        models.extend([
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1-nano",
        ])
    
    if api_keys["openrouter"]:
        models.extend([
            "openrouter/x-ai/grok-4",
            # 다른 OpenRouter 모델들을 필요에 따라 추가
        ])
    
    return models


def pytest_configure(config):
    """pytest 설정"""
    # 추가 마커 등록
    config.addinivalue_line(
        "markers", "requires_openai: mark test as requiring OpenAI API key"
    )
    config.addinivalue_line(
        "markers", "requires_openrouter: mark test as requiring OpenRouter API key"
    )

# def pytest_collection_modifyitems(config, items):
#     """테스트 수집 후 수정"""
#     # API 키가 없으면 해당 테스트를 자동으로 skip
#     openai_available = bool(os.getenv("OPENAI_API_KEY"))
#     openrouter_available = bool(os.getenv("OPENROUTER_API_KEY"))
    
#     skip_openai = pytest.mark.skip(reason="OPENAI_API_KEY not available")
#     skip_openrouter = pytest.mark.skip(reason="OPENROUTER_API_KEY not available")
    
#     for item in items:
#         if "openai" in item.name.lower() and not openai_available:
#             item.add_marker(skip_openai)
#         if "openrouter" in item.name.lower() and not openrouter_available:
#             item.add_marker(skip_openrouter)