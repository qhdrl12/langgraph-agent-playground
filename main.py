"""KShop Streamlit Chat UI - Main application file."""

from typing import Any, Dict, Union, List
import asyncio

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph.state import CompiledStateGraph
from playground.agents.supervisor.graph import make_supervisor_graph as graph
# from playground.agents.supervisor_agent import graph
# from src.kshop.agents.shopping_agent import graph
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Agent Playground",
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
    if "message_tools" not in st.session_state:
        st.session_state.message_tools = {}  # {message_index: {"tool_calls": [], "tool_results": []}}

async def create_agent() -> CompiledStateGraph:
    """Create a shopping agent."""
    return await graph({})

def render_tool_call(tool_call: Dict[str, Any], tool_id: str, is_live: bool = False) -> None:
    """Render a tool call with collapsible formatting."""
    tool_name = tool_call.get('tool_name', 'Unknown')
    tool_args = tool_call.get('tool_args', {})
    tool_call_id = tool_call.get('tool_call_id', '')
    
    # Skip rendering if tool_name is empty or meaningless
    if not tool_name or tool_name in ['Unknown', '']:
        return
    
    # Create collapsible section with status indicator
    status_indicator = "🔄" if is_live else "🔧"
    
    with st.expander(f"{status_indicator} {tool_name} ({tool_call_id})", expanded=False):
        st.markdown(f"""
        <div class="tool-call">
            <strong>Tool:</strong> {tool_name}<br>
            <strong>Status:</strong> {'🔄 Running...' if is_live else '✅ Completed'}
        </div>
        """, unsafe_allow_html=True)
        
        if tool_args:
            st.markdown("**Parameters:**")
            st.json(tool_args)

def render_tool_result(tool_result: Dict[str, Any], tool_id: str) -> None:
    """Render a tool result with collapsible formatting."""
    
    # Create collapsible section with tool name if available
    tool_name = tool_result.get('tool_name', 'Unknown Tool')
    tool_call_id = tool_result.get('tool_call_id', 'N/A')
    
    with st.expander(f"✅ Tool Result: {tool_name} ({tool_call_id})", expanded=False):
        st.markdown(f"""
        <div class="tool-result">
            <strong>Tool:</strong> {tool_name}<br>
            <strong>Result ID:</strong> {tool_call_id}
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

def render_message(message: Union[HumanMessage, AIMessage, ToolMessage], message_index: int = None) -> None:
    """Render a message with appropriate styling."""
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{message.content}</div>', unsafe_allow_html=True)
    
    elif isinstance(message, AIMessage):
        # Render everything within the assistant chat message area
        with st.chat_message("assistant"):
            # First render tool calls and results (they happen before the AI response)
            if (message_index is not None and 
                message_index in st.session_state.message_tools and 
                st.session_state.show_tools and
                not st.session_state.streaming_active):
                
                message_tools = st.session_state.message_tools[message_index]
                
                # Render tool calls first
                for i, tool_call in enumerate(message_tools.get("tool_calls", [])):
                    if tool_call:
                        render_tool_call(tool_call, f"msg_{message_index}_call_{i}", is_live=False)
                
                # Then render tool results
                for i, tool_result in enumerate(message_tools.get("tool_results", [])):
                    if tool_result:
                        render_tool_result(tool_result, f"msg_{message_index}_result_{i}")
            
            # Finally render the AI message text
            st.markdown(f'<div class="assistant-message">{message.content}</div>', unsafe_allow_html=True)
    
    elif isinstance(message, ToolMessage):
        # Tool messages are handled within AI messages
        pass

async def stream_agent_response(agent: CompiledStateGraph, user_input: str, conversation_history: List, 
                                 tool_call_containers: List = None, tool_result_containers: List = None,
                                 response_container = None):
    """Stream the agent response with real-time tool calls and results."""
    try:
        # Prepare messages with conversation history
        messages = conversation_history + [HumanMessage(content=user_input)]
        
        # Initialize response tracking
        final_response = ""
        tool_calls = []
        tool_results = []
        
        # Stream the response using astream_events for better event handling
        async for event in agent.astream_events({"messages": messages}, version="v1"):
            event_type = event.get("event", "")
            
            if event_type == "on_chain_stream":
                print(f"event : {event}")

            # Handle AI message events (including tool calls)
            if event_type == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk", {})
                if hasattr(chunk, 'content') and chunk.content:
                    final_response += chunk.content
                    # Update response container in real-time
                    if response_container:
                        with response_container:
                            st.markdown(f'<div class="assistant-message">{final_response}▊</div>', 
                                      unsafe_allow_html=True)
                    
            # Handle tool start events
            elif event_type == "on_tool_start":
                tool_name = event.get("name", "")
                tool_input = event.get("data", {}).get("input", {})
                tool_id = event.get("run_id", "")
                
                # Create tool call object for better display
                tool_call = {
                    "tool_name": tool_name,
                    "tool_args": tool_input,
                    "tool_call_id": tool_id
                }
                
                # Only add if not already exists and has meaningful name
                tool_calls.append(tool_call)
                
                # Display tool call immediately with "running" status
                if (tool_call_containers is not None and 
                    len(tool_calls) <= len(tool_call_containers) and 
                    st.session_state.show_tools):
                    with tool_call_containers[len(tool_calls) - 1]:
                        render_tool_call(tool_call, f"streaming_call_{len(tool_calls) - 1}", is_live=True)
            
            # Handle tool end events (tool results)
            elif event_type == "on_tool_end":
                tool_name = event.get("name", "")
                tool_output = event.get("data", {}).get("output", {})
                tool_id = event.get("run_id", "")
                
                # Create tool result from the output
                tool_result = {
                    "tool_call_id": tool_id,
                    "content": tool_output,
                    "tool_name": tool_name
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
            
            # Handle chain/node end events for final responses
            elif event_type == "on_chain_end":
                chain_output = event.get("data", {}).get("output", {})
                if isinstance(chain_output, dict) and "messages" in chain_output:
                    messages_output = chain_output["messages"]
                    if messages_output and isinstance(messages_output[-1], AIMessage):
                        final_msg = messages_output[-1]
                        if final_msg.content and not final_response:
                            final_response = final_msg.content
        
        # Remove cursor from final response
        if response_container and final_response:
            with response_container:
                st.markdown(f'<div class="assistant-message">{final_response}</div>', 
                          unsafe_allow_html=True)
        
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
            st.session_state.message_tools = {}
            st.rerun()
        
        # Agent status
        st.markdown("---")
        st.markdown("**Agent Status:** ✅ Ready")
        st.markdown("**Model:** Built-in Shopping Agent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display all chat history first
    for i, message in enumerate(st.session_state.messages):
        render_message(message, message_index=i)
    
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
        
        # Set streaming active flag
        st.session_state.streaming_active = True
        
        # Get conversation history (only messages)
        conversation_history = [msg for msg in st.session_state.messages[:-1]]
        
        # Create assistant message container and put everything inside it
        with st.chat_message("assistant"):
            try:
                # Create placeholder containers for tool calls and results FIRST
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
                    tool_result_containers,
                    response_container
                )
                
                # Final response is already handled in stream_agent_response
                # Just ensure we have a response for empty cases
                if not response_data["response"]:
                    with response_container:
                        st.markdown("_No response generated_")
                
                # Add assistant message to history
                ai_message = AIMessage(content=response_data["response"])
                st.session_state.messages.append(ai_message)
                
                # Store tool calls and results for this message
                message_index = len(st.session_state.messages) - 1
                st.session_state.message_tools[message_index] = {
                    "tool_calls": response_data["tool_calls"],
                    "tool_results": response_data["tool_results"]
                }
                
                # Disable streaming flag
                st.session_state.streaming_active = False
                
                # Clear streaming containers and rerun to switch to history mode
                # This prevents duplication while maintaining tool call positions
                response_container.empty()
                for container in tool_call_containers:
                    container.empty()
                for container in tool_result_containers:
                    container.empty()
                
                # Rerun to render from message history (which includes tools)
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                # Add error message to history
                error_message = AIMessage(content=f"Sorry, I encountered an error: {str(e)}")
                st.session_state.messages.append(error_message)
                # Disable streaming flag
                st.session_state.streaming_active = False
                st.rerun()
    
    # Simple footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem 0;'>"
        "Agent Playground UI"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())