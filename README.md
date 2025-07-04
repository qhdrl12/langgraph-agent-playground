# Agent Playground - Firecrawl Tool Validation

A comprehensive testing platform for validating Firecrawl's capabilities using various agent architectures for shopping-related tasks.

## Project Overview

Agent Playground is primarily a validation project for testing Firecrawl's capabilities in shopping-related information retrieval and web scraping tasks. The project uses various agent architectures as test frameworks to comprehensively evaluate Firecrawl's performance, reliability, and utility for building effective shopping agents.

## Key Features

- **Firecrawl Tool Validation**: Comprehensive testing of web scraping capabilities
- **Multiple Agent Architectures**: ReAct, Supervisor, Hierarchical, and Workflow agents
- **Shopping Context Testing**: Product information, pricing, and review data extraction
- **Performance Benchmarking**: Speed, accuracy, and reliability metrics
- **Interactive Chat UI**: Real-time streaming with tool call visibility

## Installation

```bash
uv sync --dev
```

## Usage

### Streamlit Chat UI

Run the interactive Streamlit chat interface:

```bash
# Using the run script
uv run python run_streamlit.py

# Or directly with streamlit
uv run streamlit run main.py
```

The web interface will be available at `http://localhost:8501`

### Programmatic Usage

```python
from playground.agents.supervisor_agent import graph

# Create and use supervisor agent
agent = await graph({})
result = await agent.ainvoke({"messages": [{"role": "user", "content": "Find laptops under $1000"}]})
```

## Features

### Chat Interface
- **Real-time Streaming**: See agent responses as they're generated
- **Tool Call Visibility**: Toggle to show/hide tool execution details
- **Multiple Models**: Support for OpenAI GPT and Anthropic Claude models
- **Session Management**: Persistent chat history during session

### Agent Architectures
- **ReAct Agent**: Single-agent pattern with reasoning and acting
- **Supervisor Agent**: Multi-agent coordination with specialized sub-agents
- **Hierarchical Agent**: Complex agent hierarchies for task delegation
- **Workflow Agent**: Structured workflow sequences with state management

### Firecrawl Integration
- **Product Information Extraction**: Structured product data from e-commerce sites
- **Price Monitoring**: Track price changes across multiple platforms
- **Review Scraping**: Extract and analyze customer reviews
- **Multi-Site Coverage**: Testing across Amazon, eBay, and other major platforms

### Configuration
- **Model Selection**: Choose between different LLM models
- **API Key Management**: Set API keys through UI or environment variables
- **Tool Visibility**: Control what information is displayed

## Environment Setup

Create a `.env` file with your API keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `OPENAI_API_KEY` - For GPT models
- `ANTHROPIC_API_KEY` - For Claude models
- `MCP_FIRECRAWL_API_KEY` - For Firecrawl web scraping
- `MCP_TAVILY_API_KEY` - For Tavily web search

## Project Structure

```
playground/
├── agents/
│   ├── supervisor_agent.py     # Supervisor multi-agent system
│   └── shopping_agent.py       # ReAct shopping agent
├── utils/
│   └── __init__.py            # Utility functions
main.py                        # Streamlit chat UI
pyproject.toml                 # Project configuration
CLAUDE.md                     # Detailed project instructions
```

## Testing and Validation

The project focuses on comprehensive Firecrawl validation through:

1. **Extraction Accuracy**: How well Firecrawl extracts product data
2. **Performance Metrics**: Response time and reliability measurements
3. **Multi-Platform Testing**: Coverage across different e-commerce sites
4. **Agent Integration**: How different agent patterns utilize Firecrawl
5. **Error Handling**: Resilience testing and failure recovery

## Future Enhancements

- **Reinforcement Learning**: Agent optimization through feedback
- **Multi-Modal**: Image-based product analysis
- **Real-Time Monitoring**: Live price tracking and alerts
- **Personalization**: User preference learning
- **Voice Interface**: Voice-based shopping assistance