# Agent Playground - Firecrawl Tool Validation for Shopping Agents

## Project Overview
Agent Playground is primarily a validation project for testing Firecrawl's capabilities in shopping-related information retrieval and web scraping tasks. The project uses various agent architectures as test frameworks to comprehensively evaluate Firecrawl's performance, reliability, and utility for building effective shopping agents.

## Primary Goals
- **Firecrawl Tool Validation**: Comprehensive testing of Firecrawl's web scraping and data extraction capabilities
- **Shopping Context Testing**: Evaluate Firecrawl's effectiveness for product information, pricing, and review data extraction
- **Agent Architecture Testing**: Use different agent patterns to stress-test Firecrawl in various usage scenarios
- **Performance Benchmarking**: Measure Firecrawl's speed, accuracy, and reliability across different shopping websites

## Firecrawl Validation Focus Areas
- **Product Information Extraction**: How well can Firecrawl extract structured product data?
- **Price Monitoring**: Can Firecrawl reliably track price changes across different e-commerce sites?
- **Review Scraping**: How effectively can Firecrawl extract and structure customer reviews?
- **Multi-Site Coverage**: Testing across major shopping platforms (Amazon, eBay, etc.)
- **Rate Limiting & Reliability**: Understanding Firecrawl's limits and error handling
- **Data Quality**: Evaluating the accuracy and completeness of extracted data

## Agent Architectures for Firecrawl Testing

### 1. ReAct Agent (Single Agent)
- **Location**: `playground/agents/react/`
- **Purpose**: Test Firecrawl integration in single-agent ReAct pattern
- **Firecrawl Use Cases**: Direct tool calls for product scraping, price checking, review extraction
- **Configuration**: Supports both OpenAI and OpenRouter models with dynamic date injection

### 2. Supervisor Multi-Agent System
- **Location**: `playground/agents/supervisor/`
- **Purpose**: Test Firecrawl under multi-agent coordination scenarios
- **Firecrawl Distribution**: Different sub-agents using Firecrawl for specialized tasks
- **Validation**: Concurrent Firecrawl usage, task distribution efficiency
- **Sub-Agents**: Scrape, Research, and Writing agents with specialized model configurations

### 3. Hierarchical Agent System
- **Location**: `playground/agents/hierarchical_agent.py` (planned)
- **Purpose**: Test Firecrawl in complex agent hierarchies
- **Firecrawl Cascade**: Higher-level agents delegating Firecrawl tasks to lower levels
- **Validation**: Task complexity handling, error propagation

### 4. Workflow-Based Agent
- **Location**: `playground/agents/workflow_agent.py` (planned)
- **Purpose**: Test Firecrawl in structured workflow sequences
- **Firecrawl Integration**: Sequential Firecrawl calls across workflow states
- **Validation**: State management, data persistence between Firecrawl calls

## Key Components

### Firecrawl Testing Tools
- **ProductSearchTool**: Primary Firecrawl integration for product data extraction
- **PriceComparisonTool**: Firecrawl-based price monitoring and comparison across sites
- **ReviewAnalysisTool**: Firecrawl-powered review extraction and sentiment analysis
- **FirecrawlBenchmarkTool**: Performance and reliability testing tool for Firecrawl
- **TavilySearchTool**: Backup/comparison tool to validate Firecrawl results

### Models
- **OpenAI**: GPT-4.1, GPT-4.1-mini, GPT-4.1-nano
- **OpenRouter**: 
  - Anthropic models: claude-3.5-sonnet, claude-3-haiku
  - Google models: gemini-pro-1.5
  - Meta models: llama-3.1-8b-instruct
  - X.AI models: grok-4
  - Qwen models: qwen-2.5-72b-instruct
  - Mistral models: mistral-large

### Configuration
- **Environment**: `.env` file with API keys (OpenAI, OpenRouter, Firecrawl, Tavily, LangSmith)
- **Models**: Dynamic model selection with automatic API key validation
- **MCP**: Firecrawl and Tavily API configuration
- **System Prompts**: LangSmith integration with dynamic date injection via {today} placeholder
- **Agent Configuration**: Pydantic-based configuration with comprehensive model options

## Development Setup

### Prerequisites
- Python 3.12+
- uv package manager
- API keys for OpenAI/Anthropic/OpenRouter
- MCP Firecrawl and Tavily API keys

### Installation
```bash
uv sync --dev --native-tls
```

### Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Firecrawl Validation Framework

### Firecrawl Performance Metrics
- **Extraction Accuracy**: How accurately does Firecrawl extract product data?
- **Speed**: Response time for different types of scraping tasks
- **Reliability**: Success rate across different websites and scenarios
- **Rate Limits**: Understanding and testing Firecrawl's usage limits
- **Data Completeness**: Percentage of expected data fields successfully extracted
- **Error Handling**: How well does Firecrawl handle failed requests or blocked sites?

### Firecrawl Test Scenarios
1. **Single Product Extraction**: Extract detailed product info from individual product pages
2. **Bulk Product Scraping**: Extract multiple products from category/search pages
3. **Price Monitoring**: Track price changes across multiple sites over time
4. **Review Extraction**: Extract customer reviews and ratings from various platforms
5. **Multi-Platform Testing**: Test Firecrawl across Amazon, eBay, Walmart, etc.
6. **Anti-Bot Resilience**: Test how Firecrawl handles sites with anti-scraping measures

### Agent-Firecrawl Integration Tests
- **ReAct Agent**: How effectively can a single agent use Firecrawl for complex shopping tasks?
- **Multi-Agent Coordination**: Can multiple agents share Firecrawl resources efficiently?
- **Error Recovery**: How do different agent architectures handle Firecrawl failures?
- **Task Complexity**: Which agent patterns best utilize Firecrawl's capabilities?

## Project Structure
```
playground/
├── agents/
│   ├── react/                  # ReAct agent implementation
│   │   ├── configuration.py    # React agent configuration with OpenAI/OpenRouter models
│   │   └── graph.py           # LangGraph implementation with comprehensive documentation
│   ├── supervisor/            # Supervisor multi-agent system
│   │   ├── configuration.py   # Supervisor and sub-agent configurations
│   │   ├── graph.py          # Main supervisor orchestration logic
│   │   └── subagents.py      # Specialized sub-agent creation (scrape, research, writing)
│   └── __init__.py           # Agent module exports
├── tools/                     # MCP tool integrations
│   ├── __init__.py           # Tool exports and management
│   ├── crawl.py             # Firecrawl web scraping tools
│   ├── search.py            # Tavily search integration
│   └── utility.py           # Date and utility tools
├── utils/
│   ├── __init__.py          # Utility exports
│   ├── langsmith.py         # LangSmith prompt management with date injection
│   └── model.py             # Enhanced model loader with OpenRouter support
└── experiments/             # (planned)
    ├── firecrawl_validation.py # Comprehensive Firecrawl testing
    ├── agent_firecrawl_test.py # Agent-specific Firecrawl tests
    └── performance_benchmark.py # Performance benchmarking

# Testing Infrastructure
tests/
├── conftest.py              # Pytest configuration and fixtures
└── test_openrouter_models.py # Comprehensive model testing suite

# Root files
main.py                      # Streamlit chat UI
run_streamlit.py            # Streamlit runner script
run_tests.py               # Convenient test runner with multiple scenarios
pytest.ini                 # Pytest configuration with markers and warning filters
pyproject.toml             # Project configuration with dev dependencies
CLAUDE.md                  # This file
README.md                 # Project documentation
.env.example              # Environment variable template
```

## Usage Examples

### Streamlit Chat UI
```bash
# Run the interactive chat interface
uv run python run_streamlit.py

# Or directly with streamlit
uv run streamlit run main.py
```

### Basic ReAct Agent
```python
from playground.agents.react.graph import make_graph
from langchain_core.runnables import RunnableConfig

# Create ReAct agent with OpenRouter model
config = RunnableConfig(
    configurable={
        "model": "openrouter/anthropic/claude-3.5-sonnet",
        "system_prompt": "You are a shopping assistant.",
        "selected_tools": ["scrape_with_firecrawl", "get_todays_date"],
        "name": "shopping_agent"
    }
)

agent = await make_graph(config)
result = await agent.ainvoke({
    "messages": [{"role": "user", "content": "Find wireless bluetooth headphones"}]
})
```

### Supervisor Multi-Agent
```python
from playground.agents.supervisor.graph import make_supervisor_graph
from langchain_core.runnables import RunnableConfig

# Create supervisor with specialized sub-agents
config = RunnableConfig(
    configurable={
        "supervisor_model": "openrouter/x-ai/grok-4",
        "scrape_model": "openrouter/anthropic/claude-3-haiku",
        "research_model": "openai/gpt-4.1-mini",
        "writing_model": "openrouter/anthropic/claude-3.5-sonnet"
    }
)

supervisor = await make_supervisor_graph(config)
result = await supervisor.ainvoke({
    "messages": [{"role": "user", "content": "Find best laptop for programming"}]
})
```

## Development Guidelines

### Adding New Agents
1. Create agent class in `playground/agents/`
2. Implement LangGraph state graph structure
3. Add to `__init__.py` exports
4. Create test in `tests/agents/` (planned)

### Adding New Tools
1. Create tool class in `playground/tools/` (planned)
2. Implement MCP integration
3. Add to tools `__init__.py`
4. Update agent configurations

### Experiment Design
1. Define clear hypothesis
2. Set measurable metrics
3. Create controlled test scenarios
4. Document results in `experiments/`

## Testing

### Model Testing Framework
```bash
# Run all model tests
uv run --native-tls --dev python run_tests.py all

# Test only OpenAI models
uv run --native-tls --dev python run_tests.py openai

# Test only OpenRouter models  
uv run --native-tls --dev python run_tests.py openrouter

# Quick tests (OpenAI only)
uv run --native-tls --dev python run_tests.py quick

# Direct pytest usage
uv run --native-tls pytest tests/test_openrouter_models.py -m openai_only -v -s --disable-warnings
```

### Pytest Configuration
- **Markers**: `openai_only`, `openrouter_only` for selective testing
- **Fixtures**: Shared configuration and timeout settings
- **Warning Suppression**: Clean test output without deprecation warnings
- **Async Support**: Full async/await testing with pytest-asyncio

### Test Coverage
- **Model Loading**: API key validation and provider routing
- **Response Testing**: Basic model functionality verification  
- **Performance Testing**: Response time measurement across models
- **Configuration Testing**: Agent configuration validation

### Application Testing
```bash
# Run Streamlit UI
uv run python run_streamlit.py

# Performance benchmarks (planned)
uv run python playground/experiments/agent_comparison.py
```

## Monitoring
- **LangSmith**: Trace agent execution and performance
- **Supabase**: Store experiment results and metrics
- **Local Logs**: Detailed execution logs for debugging

## Future Enhancements
- **Reinforcement Learning**: Agent optimization through feedback
- **Multi-Modal**: Image-based product analysis
- **Real-Time**: Live price monitoring and alerts
- **Personalization**: User preference learning
- **Voice Interface**: Voice-based shopping assistance

## Current Implementation Status

### ✅ Completed
- **Streamlit Chat UI**: Interactive chat interface with real-time streaming
- **Supervisor Agent**: Multi-agent coordination system with specialized sub-agents
- **ReAct Agent**: Single-agent pattern with comprehensive documentation
- **OpenRouter Integration**: Support for 8+ OpenRouter models with automatic API routing
- **Model Testing Framework**: Comprehensive pytest suite with marker-based filtering
- **Enhanced Model Loader**: API key validation and OpenRouter base URL configuration
- **Dynamic System Prompts**: LangSmith integration with automatic date injection
- **Tool Call Visualization**: Real-time tool execution display
- **Package Structure**: Clean `playground/` organization with detailed documentation
- **MCP Integration**: Firecrawl and Tavily API support
- **Configuration Management**: Pydantic-based configuration with comprehensive model options

### 🚧 In Progress
- **Firecrawl Tool Validation**: Comprehensive testing framework using new model infrastructure
- **Performance Benchmarking**: Cross-model performance analysis and metrics collection

### 📋 Planned
- **Hierarchical Agent**: Complex agent hierarchies
- **Workflow Agent**: Structured workflow sequences
- **Additional Tools**: Price comparison, review analysis
- **Experiment Framework**: Systematic validation testing
- **Multi-Modal Support**: Image-based product analysis

---

This project serves as a comprehensive testbed for multi-agent shopping systems, enabling systematic comparison of different architectural approaches and Firecrawl validation strategies.