#!/usr/bin/env python3
"""
테스트 실행 스크립트
다양한 테스트 시나리오를 위한 편의 스크립트
"""

import subprocess
import sys
import os

def check_env_vars():
    """환경 변수 체크"""
    required_vars = ["OPENAI_API_KEY", "OPENROUTER_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("Some tests may be skipped.")
    else:
        print("✅ All required environment variables are set.")

def run_command(cmd, description):
    """명령어 실행"""
    print(f"\n🧪 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_tests.py all          # 모든 테스트 실행")
        print("  python run_tests.py quick        # 빠른 테스트만 실행")
        print("  python run_tests.py openai       # OpenAI 모델만 테스트")
        print("  python run_tests.py openrouter   # OpenRouter 모델만 테스트")
        return
    
    test_type = sys.argv[1]
    
    # 환경 변수 체크
    check_env_vars()
    
    # 기본 pytest 명령어 (print 출력 보이도록 설정, 경고 억제)
    base_cmd = ["uv", "run", "--native-tls", "pytest", "-v", "-s", "--capture=no", "--disable-warnings"]
    
    # 테스트 타입별 명령어 설정
    if test_type == "all":
        cmd = base_cmd + ["tests/test_openrouter_models.py"]
        description = "Running all OpenRouter model tests"
        
    elif test_type == "quick":
        cmd = base_cmd + [
            "tests/test_openrouter_models.py::TestModelLoading::test_openai_model_loading",
            "tests/test_openrouter_models.py::TestModelResponses::test_openai_simple_response"
        ]
        description = "Running quick tests (OpenAI only)"
        
    elif test_type == "openai":
        cmd = base_cmd + ["tests/test_openrouter_models.py", "-m", "openai_only"]
        description = "Running OpenAI model tests"
        
    elif test_type == "openrouter":
        cmd = base_cmd + ["tests/test_openrouter_models.py", "-m", "openrouter_only"]
        description = "Running OpenRouter model tests"
        
    else:
        print(f"Unknown test type: {test_type}")
        return
    
    # 테스트 실행
    success = run_command(cmd, description)
    
    if success:
        print("\n✅ Tests completed successfully!")
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()