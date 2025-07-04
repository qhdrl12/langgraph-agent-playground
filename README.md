# KShop - Shopping Agent

A shopping agent built with LangGraph and LangChain for automated shopping tasks.

## Features

- Multi-agent shopping workflows
- Product search and comparison
- Price monitoring
- Purchase automation
- Review analysis

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
from kshop.agents import ShoppingAgent

agent = ShoppingAgent()
result = agent.search_product("laptop")
```

## Features

### Chat Interface
- **Real-time Streaming**: See agent responses as they're generated
- **Tool Call Visibility**: Toggle to show/hide tool execution details
- **Multiple Models**: Support for OpenAI GPT and Anthropic Claude models
- **Session Management**: Persistent chat history during session

### Shopping Tools
- **Product Search**: Find products across multiple platforms
- **Price Comparison**: Compare prices and find best deals
- **Review Analysis**: Analyze customer reviews and sentiment

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
- `MCP_FIRECRAWL_API_KEY` - For web scraping (future implementation)
- `MCP_TAVILY_API_KEY` - For web search (future implementation)