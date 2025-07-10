# Agent Playground - Shopping Assistant with LangGraph

A comprehensive multi-agent shopping system built with LangGraph, LangChain, and Firecrawl for web scraping and product research. Features extensive OpenRouter model support and comprehensive testing infrastructure.

## ✨ Key Features

- **Multi-Agent Architecture**: Supervisor and ReAct agent patterns with specialized sub-agents
- **OpenRouter Integration**: Support for 8+ models including Claude, Gemini, Grok, and Llama
- **Web Scraping**: Integrated Firecrawl for product data extraction and analysis
- **Interactive Chat UI**: Streamlit-based interface with real-time streaming and tool visualization
- **Comprehensive Testing**: pytest framework with model validation and performance testing
- **Dynamic Configuration**: Automatic API key handling and model routing
- **LangSmith Integration**: Prompt management with dynamic date injection
- **MCP Tools**: Advanced search, scraping, and utility tools

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- uv package manager
- API keys for OpenAI and/or OpenRouter

### Installation

```bash
# Clone and install dependencies
uv sync --dev --native-tls

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### Environment Setup

Required environment variables:
```bash
# Core API Keys
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Web Tools
FIRECRAWL_API_KEY=your_firecrawl_key_here
TAVILY_API_KEY=your_tavily_key_here

# Optional: LangSmith tracing
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_TRACING=true
```

## 🎯 Usage

### Interactive Chat UI

Run the Streamlit interface:

```bash
# Using the run script
uv run python run_streamlit.py

# Or directly with streamlit
uv run streamlit run main.py
```

Available at `http://localhost:8501`

### Programmatic Usage

#### ReAct Agent with OpenRouter
```python
from playground.agents.react.graph import make_graph
from langchain_core.runnables import RunnableConfig

# Create ReAct agent with Claude model
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
    "messages": [{"role": "user", "content": "Find wireless headphones under $200"}]
})
```

#### Supervisor Multi-Agent
```python
from playground.agents.supervisor.graph import make_supervisor_graph
from langchain_core.runnables import RunnableConfig

# Create supervisor with mixed models
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
    "messages": [{"role": "user", "content": "Research and compare gaming laptops"}]
})
```

## 🧪 Testing

### Model Testing Framework

```bash
# Run all model tests
uv run --native-tls --dev python run_tests.py all

# Test specific providers
uv run --native-tls --dev python run_tests.py openai
uv run --native-tls --dev python run_tests.py openrouter

# Quick validation tests
uv run --native-tls --dev python run_tests.py quick

# Direct pytest usage
uv run --native-tls pytest tests/test_openrouter_models.py -m openai_only -v -s
```

### Test Features
- **Model Validation**: API key verification and response testing
- **Performance Testing**: Response time measurement across models
- **Configuration Testing**: Agent setup and model option validation
- **Marker-based Filtering**: Selective test execution with pytest markers

## 🏗️ Architecture

### Agent Types

#### ReAct Agent (`playground/agents/react/`)
- Single-agent pattern with reasoning and acting
- Configurable with OpenAI or OpenRouter models
- Direct tool integration for scraping and research

#### Supervisor Agent (`playground/agents/supervisor/`)
- Multi-agent coordination system
- Three specialized sub-agents:
  - **Scrape Agent**: Web scraping with Firecrawl
  - **Research Agent**: Information gathering with Tavily
  - **Writing Agent**: Content creation and formatting

### Supported Models

#### OpenAI Models
- `gpt-4.1` - Most capable, highest cost
- `gpt-4.1-mini` - Balanced performance/cost (default)
- `gpt-4.1-nano` - Fastest, lowest cost

#### OpenRouter Models
- **Anthropic**: `claude-3.5-sonnet`, `claude-3-haiku`
- **Google**: `gemini-pro-1.5`
- **Meta**: `llama-3.1-8b-instruct`
- **X.AI**: `grok-4`
- **Qwen**: `qwen-2.5-72b-instruct`
- **Mistral**: `mistral-large`

## 📁 Project Structure

```
playground/
├── agents/
│   ├── react/                  # ReAct agent implementation
│   │   ├── configuration.py    # Model and tool configuration
│   │   └── graph.py           # LangGraph implementation
│   └── supervisor/            # Supervisor multi-agent system
│       ├── configuration.py   # Supervisor and sub-agent configs
│       ├── graph.py          # Main orchestration logic
│       └── subagents.py      # Specialized agent creation
├── tools/                     # MCP tool integrations
│   ├── crawl.py             # Firecrawl web scraping
│   ├── search.py            # Tavily search integration
│   └── utility.py           # Date and utility tools
└── utils/
    ├── langsmith.py         # Prompt management with date injection
    └── model.py             # Enhanced model loader with OpenRouter

tests/
├── conftest.py              # Pytest configuration and fixtures
└── test_openrouter_models.py # Comprehensive model testing

# Configuration
pytest.ini                   # Pytest settings and markers
run_tests.py                # Test runner with scenarios
pyproject.toml              # Dependencies and dev tools
```

## 🎨 Chat Interface Features

- **Real-time Streaming**: See responses as they're generated
- **Tool Call Visibility**: Toggle detailed tool execution logs
- **Session Management**: Persistent chat history

## 🔧 Development

### Adding New Models

Add to configuration files:
```python
# In playground/agents/react/configuration.py or supervisor/configuration.py
model: Annotated[
    Literal[
        # Existing models...
        "openrouter/your-new/model-name",
    ],
    {"__template_metadata__": {"kind": "llm"}}
]
```

### Creating Custom Agents

1. Create agent directory in `playground/agents/`
2. Implement configuration schema with Pydantic
3. Create LangGraph implementation
4. Add comprehensive documentation and docstrings

### Testing New Features

1. Add tests to `tests/test_openrouter_models.py`
2. Use appropriate pytest markers
3. Update `run_tests.py` if needed
4. Ensure clean test output with proper fixtures

## 📊 Validation Framework

### Firecrawl Testing Focus
- **Product Information Extraction**: Structured data from e-commerce sites
- **Price Monitoring**: Track changes across platforms
- **Review Scraping**: Customer feedback analysis
- **Multi-Site Coverage**: Amazon, eBay, and specialized retailers
- **Performance Metrics**: Speed, accuracy, and reliability

### Agent Integration Testing
- **Model Performance**: Response time and quality across providers
- **Tool Coordination**: Multi-agent task distribution
- **Error Recovery**: Handling API failures and retries
- **Configuration Validation**: Model and tool compatibility

## 🛠️ Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure all required keys are in `.env`
2. **Model Access**: Verify OpenRouter credits and model availability
3. **Network Issues**: Use `--native-tls` flag with uv commands
4. **Test Failures**: Check API key permissions and rate limits

### Debug Mode

Enable detailed logging:
```bash
LANGSMITH_TRACING=true uv run python run_streamlit.py
```

## 🚀 Future Enhancements

- **Advanced Tool Integration**: Custom scraping patterns
- **Multi-Modal Support**: Image-based product analysis
- **Experiment Framework**: A/B testing across models

## 📄 License

MIT License - see LICENSE file for details.

---

This project serves as a comprehensive testbed for multi-agent shopping systems, enabling systematic comparison of different architectural approaches and model providers.