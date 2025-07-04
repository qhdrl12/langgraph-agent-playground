"""KShop Streamlit Chat UI - Main application file."""

from typing import Any, Dict, Union, List
import asyncio

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph.state import CompiledStateGraph
from src.kshop.agents.shopping_agent import graph


# Page config
st.set_page_config(
    page_title="KShop - Shopping Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean, modern styling
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    /* Clean header styling */
    .header-container {
        text-align: center;
        padding: 1.5rem 0;
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .header-container h1 {
        color: #2d3748;
        font-size: 2rem;
        margin: 0;
    }
    
    .header-container p {
        color: #718096;
        margin: 0.5rem 0 0 0;
    }
    
    /* Clean chat messages */
    .user-message {
        background: #4a5568;
        color: white;
        padding: 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 1rem 0;
        width: 100%;
        display: block;
    }
    
    .assistant-message {
        background: #f7fafc;
        color: #2d3748;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        border-radius: 18px 18px 18px 4px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: 0;
        margin-right: auto;
    }
    
    /* Tool call styling - collapsible */
    .tool-section {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .tool-header {
        background: #edf2f7;
        padding: 0.5rem 1rem;
        cursor: pointer;
        border-bottom: 1px solid #e2e8f0;
        font-size: 0.9rem;
        font-weight: 500;
        color: #4a5568;
    }
    
    .tool-header:hover {
        background: #e2e8f0;
    }
    
    .tool-content {
        padding: 1rem;
        display: none;
    }
    
    .tool-content.expanded {
        display: block;
    }
    
    .tool-call {
        background: #ebf8ff;
        color: #2b6cb0;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3182ce;
        font-size: 0.9rem;
    }
    
    .tool-result {
        background: #f0fff4;
        color: #22543d;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #38a169;
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: #f8f9fa;
        color: #2d3748;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Clean button styling */
    .stButton > button {
        background: #4a5568;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #2d3748;
        transform: translateY(-1px);
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
        margin-top: 2rem;
    }
    
    /* Hide default streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "show_tools" not in st.session_state:
        st.session_state.show_tools = True
    if "streaming_active" not in st.session_state:
        st.session_state.streaming_active = False
    if "tool_calls" not in st.session_state:
        st.session_state.tool_calls = []
    if "tool_results" not in st.session_state:
        st.session_state.tool_results = []

async def create_agent() -> CompiledStateGraph:
    """Create a shopping agent."""
    return await graph({})

def render_tool_call(tool_call: Dict[str, Any], tool_id: str, is_live: bool = False) -> None:
    """Render a tool call with collapsible formatting."""
    tool_name = tool_call.get('name', 'Unknown')
    
    # Create collapsible section with status indicator
    status_indicator = "🔄" if is_live else "🔧"
    status_text = "Calling" if is_live else "Tool Call"
    
    with st.expander(f"{status_indicator} {status_text}: {tool_name}", expanded=False):
        st.markdown(f"""
        <div class="tool-call">
            <strong>Tool:</strong> {tool_name}<br>
            <strong>ID:</strong> {tool_call.get('id', 'N/A')}<br>
            <strong>Status:</strong> {'🔄 Running...' if is_live else '✅ Completed'}
        </div>
        """, unsafe_allow_html=True)
        
        if tool_call.get('args'):
            st.markdown("**Arguments:**")
            st.json(tool_call['args'])

def render_tool_result(tool_result: Dict[str, Any], tool_id: str) -> None:
    """Render a tool result with collapsible formatting."""
    
    # Create collapsible section
    with st.expander(f"✅ Tool Result: {tool_result.get('tool_call_id', 'N/A')}", expanded=False):
        st.markdown(f"""
        <div class="tool-result">
            <strong>Result ID:</strong> {tool_result.get('tool_call_id', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
        
        if tool_result.get('content'):
            st.markdown("**Content:**")
            if isinstance(tool_result['content'], (dict, list)):
                st.json(tool_result['content'])
            else:
                # Truncate very long text content
                content = str(tool_result['content'])
                if len(content) > 2000:
                    st.text(content[:2000] + "...")
                    st.markdown("*Content truncated - expand to see full result*")
                else:
                    st.text(content)

def render_message(message: Union[HumanMessage, AIMessage, ToolMessage], message_data: Dict[str, Any] = None) -> None:
    """Render a message with appropriate styling."""
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{message.content}</div>', unsafe_allow_html=True)
    
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(f'<div class="assistant-message">{message.content}</div>', unsafe_allow_html=True)
            
            # Render tool calls if present and tools are enabled
            if st.session_state.get('show_tools', True) and message_data and message_data.get('tool_calls'):
                for i, tool_call in enumerate(message_data['tool_calls']):
                    render_tool_call(tool_call, f"call_{i}")
            
            # Render tool results if present and tools are enabled
            if st.session_state.get('show_tools', True) and message_data and message_data.get('tool_results'):
                for i, tool_result in enumerate(message_data['tool_results']):
                    render_tool_result(tool_result, f"result_{i}")
    
    elif isinstance(message, ToolMessage):
        # Tool messages are handled within AI messages
        pass

async def stream_agent_response(agent: CompiledStateGraph, user_input: str, conversation_history: List, 
                                 tool_call_containers: List = None, tool_result_containers: List = None):
    """Stream the agent response with real-time tool calls and results."""
    try:
        # Prepare messages with conversation history
        messages = conversation_history + [HumanMessage(content=user_input)]
        
        # Initialize response tracking
        final_response = ""
        tool_calls = []
        tool_results = []
        
        # Stream the response
        async for event in agent.astream({"messages": messages}):
            print(f"event : {event}")
            # Handle different types of events
            if "agent" in event:
                event_data = event.get("agent")
                if "messages" in event_data:
                    for msg in event_data["messages"]:
                        if isinstance(msg, AIMessage):
                            if msg.content:
                                final_response = msg.content
                            
                            # Handle tool calls in real-time
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    if tool_call not in tool_calls:
                                        tool_calls.append(tool_call)
                                        # Display tool call immediately with "running" status
                                        if (tool_call_containers is not None and 
                                            len(tool_calls) <= len(tool_call_containers) and 
                                            st.session_state.show_tools):
                                            with tool_call_containers[len(tool_calls) - 1]:
                                                render_tool_call(tool_call, f"streaming_call_{len(tool_calls) - 1}", is_live=True)
                        
            elif "tools" in event:
                event_data = event.get("tools")
                if "messages" in event_data:
                    for msg in event_data["messages"]:
                        if isinstance(msg, ToolMessage):
                            tool_result = {
                                "tool_call_id": msg.tool_call_id,
                                "content": msg.content
                            }
                            tool_results.append(tool_result)
                            
                            # Display tool result immediately and update corresponding tool call status
                            if (tool_result_containers is not None and 
                                len(tool_results) <= len(tool_result_containers) and 
                                st.session_state.show_tools):
                                # Update tool call to completed status
                                tool_call_index = len(tool_results) - 1
                                if tool_call_index < len(tool_calls) and tool_call_containers is not None:
                                    with tool_call_containers[tool_call_index]:
                                        render_tool_call(tool_calls[tool_call_index], f"completed_call_{tool_call_index}", is_live=False)
                                
                                # Display tool result
                                with tool_result_containers[len(tool_results) - 1]:
                                    render_tool_result(tool_result, f"streaming_result_{len(tool_results) - 1}")
        
        return {
            "response": final_response,
            "tool_calls": tool_calls,
            "tool_results": tool_results
        }
        
    except Exception as e:
        st.error(f"Error during streaming: {str(e)}")
        return {
            "response": f"Error: {str(e)}",
            "tool_calls": [],
            "tool_results": []
        }

async def main():
    """Main application function."""
    init_session_state()
    
    # Initialize agent automatically
    if st.session_state.agent is None:
        try:
            st.session_state.agent = await create_agent()
        except Exception as e:
            st.error(f"Failed to initialize agent: {str(e)}")
            return
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🛒 KShop - Shopping Agent</h1>
        <p>Chat with your AI shopping assistant powered by LangGraph</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration (minimal)
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("⚙️ Settings")
        
        # Tool visibility toggle
        st.session_state.show_tools = st.checkbox(
            "Show Tool Calls",
            value=st.session_state.show_tools,
            help="Toggle visibility of tool calls and results"
        )
        
        # Clear chat history
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            if hasattr(st.session_state, 'message_data'):
                st.session_state.message_data = {}
            st.rerun()
        
        # Agent status
        st.markdown("---")
        st.markdown("**Agent Status:** ✅ Ready")
        st.markdown("**Model:** Built-in Shopping Agent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display all chat history first
    for i, message in enumerate(st.session_state.messages):
        message_data = None
        if isinstance(message, AIMessage) and hasattr(st.session_state, 'message_data'):
            message_data = st.session_state.message_data.get(i, {})
        render_message(message, message_data)
    
    # Chat input at the bottom
    if prompt := st.chat_input("Ask me anything about shopping..."):
        if not st.session_state.agent:
            st.warning("Agent is not ready. Please refresh the page.")
            return
        
        # Add user message to history
        user_message = HumanMessage(content=prompt)
        st.session_state.messages.append(user_message)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
        
        # Stream agent response
        with st.chat_message("assistant"):
            try:
                # Get conversation history (only messages)
                conversation_history = [msg for msg in st.session_state.messages[:-1]]
                
                # Create placeholder containers for tool calls and results
                tool_call_containers = []
                tool_result_containers = []
                
                # Prepare containers for up to 5 tool calls/results (adjust as needed)
                for i in range(5):
                    tool_call_containers.append(st.empty())
                    tool_result_containers.append(st.empty())
                
                # Container for the final response
                response_container = st.empty()
                
                # Start with thinking indicator
                with response_container:
                    st.markdown("🤔 **Thinking...**")
                
                # Stream the response
                response_data = await stream_agent_response(
                    st.session_state.agent, 
                    prompt, 
                    conversation_history,
                    tool_call_containers,
                    tool_result_containers
                )
                
                # Display final assistant response with streaming effect
                if response_data["response"]:
                    with response_container:
                        # Create a placeholder for streaming text
                        streaming_text = ""
                        text_container = st.empty()
                        
                        # Simulate streaming by revealing text progressively
                        full_response = response_data["response"]
                        words = full_response.split()
                        
                        for i, word in enumerate(words):
                            streaming_text += word + " "
                            with text_container:
                                st.markdown(f'<div class="assistant-message">{streaming_text}▊</div>', 
                                          unsafe_allow_html=True)
                            await asyncio.sleep(0.05)  # Small delay between words
                        
                        # Final text without cursor
                        with text_container:
                            st.markdown(f'<div class="assistant-message">{full_response}</div>', 
                                      unsafe_allow_html=True)
                else:
                    with response_container:
                        st.markdown("_No response generated_")
                
                # Add assistant message to history with metadata
                ai_message = AIMessage(content=response_data["response"])
                st.session_state.messages.append(ai_message)
                
                # Store message data for rendering
                if not hasattr(st.session_state, 'message_data'):
                    st.session_state.message_data = {}
                
                st.session_state.message_data[len(st.session_state.messages) - 1] = {
                    "tool_calls": response_data["tool_calls"],
                    "tool_results": response_data["tool_results"]
                }
                
                # Clear only the tool containers to prevent duplicate display
                # Keep the response container with final text
                for container in tool_call_containers:
                    container.empty()
                for container in tool_result_containers:
                    container.empty()
                
                # Force rerun to refresh the display with the new message
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                # Add error message to history
                error_message = AIMessage(content=f"Sorry, I encountered an error: {str(e)}")
                st.session_state.messages.append(error_message)
                st.rerun()
    
    # Simple footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem 0;'>"
        "KShop - Firecrawl Tool Validation Platform"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())