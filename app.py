import os
import json
import requests
import streamlit as st
import serpapi
from dotenv import load_dotenv
from openai import OpenAI
import finnhub
from tools.weather import get_weather
from tools.finance import get_stock_price
from tools.search import web_search
from tools.command import run_command
from pathlib import Path
# Load environment variables
load_dotenv(Path(__file__).parent / ".env")


# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="ReAct Agent Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean UI styling
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .stChatMessage { border-radius: 12px; margin-bottom: 10px; }
    .tool-box { 
        background-color: #f0f2f6; 
        border-left: 5px solid #ff4b4b; 
        padding: 10px; 
        border-radius: 4px;
        font-family: monospace;
        margin: 5px 0;
    }
    .plan-box {
        background-color: #e8f4f8;
        border-left: 5px solid #00a0db;
        padding: 10px;
        border-radius: 4px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration Sidebar ---
with st.sidebar:
    st.title("⚙️ Agent Settings")
    st.markdown("Configure your LLM credentials and endpoints below.")
    
    # Allow fallback to env variables if not filled in UI
    openai_api_key = st.text_input(
        "RAG Application"
        
    )
    base_url = st.text_input(
        "Akhil"
    )
    
    st.divider()
    if st.button("Clear Conversation History", type="primary"):
        st.session_state.messages = []
        st.session_state.ui_history = []
        st.rerun()

# --- Initialize Client & State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ui_history" not in st.session_state:
    # Keeps track of stylized visual updates for the user chat view
    st.session_state.ui_history = []

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
import os
import finnhub

finnhub_client = finnhub.Client(
    api_key=os.getenv("FIN_HUB_API")
)



# --- Tools Definitions ---




def web_search(query):
    try:
        response = requests.post(
            "https://search-router.com/api/search",
            headers={"X-API-Key": os.getenv("SERPAPI_KEY")},
            json={"query": query, "num_results": 7},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return f"Search routing failed: {str(e)}"


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "web_search": web_search,
    "get_stock_price": get_stock_price
}

# --- System Prompt Definition ---
SYSTEM_PROMPT = """
IMPORTANT:
You MUST NEVER answer a weather question directly.
If a tool exists for a task, you MUST call the tool first.
You are not allowed to use your own knowledge when a tool is available.

For weather questions:
1. plan
2. action(get_weather)
3. wait for observation
4. output

Never skip the action step.

You are a helpful AI Assistant specialized in resolving user queries.
You work in start, plan, action, observe mode.

For the given user query and available tools, plan the step-by-step execution. Based on the planning, select the relevant tool from the available tools. Perform an action to call the tool. Wait for the observation, and based on that observation, resolve the user query.

Rules:
- Follow the Output JSON Format perfectly.
- Generate one single step object container per turn. 
- Always perform one step at a time and wait for next input/observation.
- Don't do all steps at once, go one-by-one.

Output JSON Format:
{
    "step": "plan" | "action" | "output",
    "content": "Description of thought process or final output answer",
    "function": "The name of function (ONLY if step is 'action')",
    "input": "The exact input parameter string or argument for the function (ONLY if step is 'action')"
}

Available Tools:
- "get_weather": Takes a city name as an input and returns the current weather for the city.
- "run_command": Takes a system command as a string, executes it, and returns the console response.
- "web_search": Searches the internet and returns relevant information.
- "get_stock_price": Takes a stock ticker symbol and returns current stock market information.
"""

# --- Main Application Interface ---
st.title("🧠 Automated ReAct Loop Agent")
st.caption("An interactive agent leveraging structured execution steps (Plan ➡️ Action ➡️ Observe ➡️ Output).")

# Display permanent conversation logs cleanly
for interaction in st.session_state.ui_history:
    if interaction["type"] == "user":
        st.chat_message("user").write(interaction["text"])
    elif interaction["type"] == "plan":
        st.markdown(f"<div class='plan-box'>🧠 <b>Plan:</b> {interaction['text']}</div>", unsafe_allow_html=True)
    elif interaction["type"] == "action":
        st.markdown(f"<div class='tool-box'>🛠️ <b>Calling Tool:</b> {interaction['name']} with input <code>{interaction['input']}</code></div>", unsafe_allow_html=True)
    elif interaction["type"] == "observation":
        st.info(f"👀 **Observation:** {interaction['text']}")
    elif interaction["type"] == "assistant":
        st.chat_message("assistant").write(interaction["text"])

# Handle text input chat box
if user_query := st.chat_input("Ask me about the weather, stocks, commands, or web searches..."):
    
    # Append User Input to layout state tracking
    st.chat_message("user").write(user_query)
    st.session_state.ui_history.append({"type": "user", "text": user_query})
    
    # Reinitialize message history framing for model state tracking if empty
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Create status containers for visual feedback while thinking
    with st.spinner("Agent is reasoning..."):
        max_iterations = 8  # Prevents infinite loop runaways
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                # LLM execution step
                response = client.chat.completions.create(
                    model="gemini-3.5-flash",
                    messages=st.session_state.messages,
                    response_format={"type": "json_object"}
                )
                
                raw_json = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": raw_json})
                parsed_response = json.loads(raw_json)
                
                step_type = parsed_response.get("step")
                
                # Handle Planning Steps
                if step_type == "plan":
                    plan_content = parsed_response.get("content")
                    st.markdown(f"<div class='plan-box'>🧠 <b>Plan:</b> {plan_content}</div>", unsafe_allow_html=True)
                    st.session_state.ui_history.append({"type": "plan", "text": plan_content})
                    # Advance the context prompt to keep the model moving instead of stalling out on stale loops
                    st.session_state.messages.append({"role": "user", "content": "Proceed to your next step or action based on this plan."})
                    continue
                
                # Handle Action / Tool-execution Steps
                elif step_type == "action":
                    tool_name = parsed_response.get("function")
                    tool_input = parsed_response.get("input")
                    
                    st.markdown(f"<div class='tool-box'>🛠️ <b>Calling Tool:</b> {tool_name} with input <code>{tool_input}</code></div>", unsafe_allow_html=True)
                    st.session_state.ui_history.append({"type": "action", "name": tool_name, "input": tool_input})
                    
                    if tool_name in available_tools:
                        tool_output = available_tools[tool_name](tool_input)
                    else:
                        tool_output = f"Error: Tool '{tool_name}' is not registered."
                        
                    st.info(f"👀 **Observation:** {tool_output}")
                    st.session_state.ui_history.append({"type": "observation", "text": str(tool_output)})
                    
                    # Feed observation back to the model
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": json.dumps({"step": "observe", "output": str(tool_output)})
                    })
                    continue
                    
                # Handle Final Output Steps
                elif step_type == "output":
                    final_text = parsed_response.get("content")
                    st.chat_message("assistant").write(final_text)
                    st.session_state.ui_history.append({"type": "assistant", "text": final_text})
                    break
                    
                else:
                    st.warning("Received unexpected JSON payload format.")
                    st.json(parsed_response)
                    break
                    
            except Exception as ex:
                st.error(f"Execution Error occurred: {str(ex)}")
                break
        else:
            st.error("Reached maximum reasoning loop limits without resolving an output answer.")