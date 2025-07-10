"""
OpenRouter 모델 테스트
pytest를 사용한 체계적인 모델 테스트 및 성능 비교
"""

import pytest
import os
import time
from playground.utils.model import load_chat_model

# 테스트 설정
TEST_MODELS_OPENAI = [
    "openai/gpt-4.1-mini",
    "openai/gpt-4.1-nano",
]

TEST_MODELS_OPENROUTER = [
    "openrouter/x-ai/grok-4",
    "openrouter/openai/gpt-4o-mini",
]

# 전체 테스트용
TEST_MODELS = TEST_MODELS_OPENAI + TEST_MODELS_OPENROUTER

# 테스트 프롬프트들
SIMPLE_PROMPT = "What is 2+2? Answer briefly."

@pytest.fixture
def response_timeout():
    """응답 시간 제한"""
    return 10.0


class TestModelResponses:
    """모델 응답 테스트"""
    
    @pytest.mark.asyncio
    @pytest.mark.openai_only
    async def test_openai_simple_response(self):
        """OpenAI 모델 간단 응답 테스트"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        model = load_chat_model("openai/gpt-4.1-mini")
        response = await model.ainvoke(SIMPLE_PROMPT)
        
        assert response is not None
        assert hasattr(response, 'content')
        assert "4" in response.content
    
    @pytest.mark.asyncio
    @pytest.mark.openrouter_only
    async def test_openrouter_simple_response(self):
        """OpenRouter 모델 간단 응답 테스트"""
        if not os.getenv("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not set")
        
        # 더 안전한 모델로 변경
        model = load_chat_model("openrouter/anthropic/claude-3-haiku")
        response = await model.ainvoke(SIMPLE_PROMPT)
        
        assert response is not None
        assert hasattr(response, 'content')
        assert "4" in response.content
    


class TestModelPerformance:
    """모델 성능 테스트"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("model_name", TEST_MODELS_OPENAI)
    @pytest.mark.openai_only
    async def test_openai_response_time(self, model_name, response_timeout):
        """OpenAI 모델 응답 시간 테스트"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        model = load_chat_model(model_name)
        
        start_time = time.time()
        response = await model.ainvoke(SIMPLE_PROMPT)
        response_time = time.time() - start_time
        
        assert response is not None
        assert response_time < response_timeout
        
        print(f"\n{model_name} response time: {response_time:.2f}s")
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("model_name", TEST_MODELS_OPENROUTER)
    @pytest.mark.openrouter_only
    async def test_openrouter_response_time(self, model_name, response_timeout):
        """OpenRouter 모델 응답 시간 테스트"""
        if not os.getenv("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not set")
        
        model = load_chat_model(model_name)
        
        start_time = time.time()
        response = await model.ainvoke(SIMPLE_PROMPT)
        response_time = time.time() - start_time
        
        assert response is not None
        assert response_time < response_timeout
        
        print(f"\n{model_name} response time: {response_time:.2f}s")
    


class TestAgentConfiguration:
    """Agent 설정 테스트"""
    
    def test_react_agent_model_options(self):
        """React Agent 모델 옵션 테스트"""
        from playground.agents.react.configuration import Configuration
        
        config = Configuration()
        
        # 기본값 확인
        assert config.model == "openai/gpt-4.1-mini"
        
        # 모델 타입 확인 (클래스에서 접근)
        model_field = Configuration.model_fields['model']
        assert model_field is not None
        
        # 모델 필드의 annotation 확인
        assert hasattr(model_field, 'annotation')