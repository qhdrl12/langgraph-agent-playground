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

## Agent Architectures for Firwl Testing

### 1. ReAct Agent (Single Agent)
- **Location**: `playground/agents/shopping_agent.py`
- **Purpose**: Test Firecrawl integration in single-agent ReAct pattern
- **Firecrawl Use Cases**: Direct tool calls for product scraping, price checking, review extraction

### 2. Supervisor Multi-Agent System
- **Location**: `playground/agents/supervisor_agent.py`
- **Purpose**: Test Firecrawl under multi-agent coordination scenarios
- **Firecrawl Distribution**: Different sub-agents using Firecrawl for specialized tasks
- **Validation**: Concurrent Firecrawl usage, task distribution efficiency

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
- **OpenAI**: GPT-4o-mini, GPT-4o
- **Anthropic**: Claude-3-haiku, Claude-3-sonnet
- **OpenRouter**: Various models through unified API

### Configuration
- **Environment**: `.env` file with API keys and configuration
- **Models**: Configurable model selection per agent type
- **MCP**: Firecrawl and Tavily API configuration

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
│   ├── shopping_agent.py       # ReAct shopping agent
│   ├── supervisor_agent.py     # Supervisor multi-agent system
│   ├── hierarchical_agent.py   # Hierarchical agents (planned)
│   └── workflow_agent.py       # Workflow-based agent (planned)
├── tools/                      # (planned)
│   ├── product_search.py       # Firecrawl product extraction
│   ├── price_comparison.py     # Firecrawl price monitoring
│   ├── review_analysis.py      # Firecrawl review scraping
│   ├── firecrawl_benchmark.py  # Firecrawl performance testing
│   └── tavily_search.py        # Backup search tool
├── workflows/                  # (planned)
│   ├── firecrawl_workflow.py   # Firecrawl-specific workflows
│   └── validation_workflow.py  # Tool validation workflows
├── utils/
│   ├── config.py              # Configuration management (planned)
│   ├── firecrawl_metrics.py   # Firecrawl performance metrics (planned)
│   └── validation_utils.py    # Validation utilities (planned)
└── experiments/                # (planned)
    ├── firecrawl_validation.py # Comprehensive Firecrawl testing
    ├── agent_firecrawl_test.py # Agent-specific Firecrawl tests
    └── performance_benchmark.py # Performance benchmarking

# Root files
main.py                         # Streamlit chat UI
run_streamlit.py               # Streamlit runner script
pyproject.toml                 # Project configuration
CLAUDE.md                     # This file
README.md                     # Project documentation
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
from playground.agents.shopping_agent import graph

# Create and use ReAct agent
agent = await graph({})
result = await agent.ainvoke({
    "messages": [{"role": "user", "content": "Find wireless bluetooth headphones"}]
})
```

### Supervisor Multi-Agent
```python
from playground.agents.supervisor_agent import graph

# Create and use supervisor agent
supervisor = await graph({})
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
```bash
# Run all tests (when implemented)
uv run pytest

# Run specific agent tests
uv run pytest tests/agents/

# Run performance benchmarks (when implemented)
uv run python playground/experiments/agent_comparison.py

# Run Streamlit UI
uv run python run_streamlit.py
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
- **Supervisor Agent**: Multi-agent coordination system with Firecrawl integration
- **ReAct Agent**: Single-agent pattern with reasoning and acting
- **Tool Call Visualization**: Real-time tool execution display
- **Package Structure**: Clean `playground/` organization
- **MCP Integration**: Firecrawl and Tavily API support

### 🚧 In Progress
- **Firecrawl Tool Validation**: Comprehensive testing framework
- **Performance Benchmarking**: Metrics collection and analysis

### 📋 Planned
- **Hierarchical Agent**: Complex agent hierarchies
- **Workflow Agent**: Structured workflow sequences
- **Additional Tools**: Price comparison, review analysis
- **Experiment Framework**: Systematic validation testing
- **Multi-Modal Support**: Image-based product analysis

---

This project serves as a comprehensive testbed for multi-agent shopping systems, enabling systematic comparison of different architectural approaches and Firecrawl validation strategies.