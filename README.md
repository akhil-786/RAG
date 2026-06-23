# 🤖 ReAct Multi-Tool AI Agent

An intelligent AI Agent built using **Streamlit**, **Gemini**, and the **ReAct (Reasoning + Acting)** framework.

The agent can autonomously reason, choose tools, execute actions, observe results, and generate responses.

---

## 🚀 Features

### 🧠 ReAct Agent Architecture

The agent follows:

```text
User Query
    ↓
Plan
    ↓
Action
    ↓
Tool Execution
    ↓
Observation
    ↓
Final Answer
```

---

## 🛠️ Integrated Tools

### 🌦️ Weather Tool

Fetches real-time weather information.

Example:

```text
Weather in Hyderabad
Weather in London
```

---

### 🌐 Web Search Tool

Searches the internet for up-to-date information.

Example:

```text
Who is the PM of India?
Latest AI News
Current CEO of Microsoft
```

---

### 📈 Finance Tool

Retrieves live stock market information using Finnhub.

Example:

```text
AAPL stock price
MSFT stock price
NVDA stock price
```

Returns:

* Current Price
* Open Price
* High
* Low
* Previous Close

---

### 💻 Command Execution Tool

Executes system commands safely.

Example:

```text
ipconfig
dir
whoami
```

---

## 🏗️ Project Structure

```bash
project/
│
├── app.py
├── .env
├── requirements.txt
│
├── tools/
│   ├── weather.py
│   ├── finance.py
│   ├── search.py
│   └── command.py
│
├── README.md
└── .gitignore
```

---

## ⚙️ Tech Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| Python     | Backend               |
| Streamlit  | UI                    |
| Gemini     | LLM                   |
| OpenAI SDK | Gemini Wrapper        |
| Finnhub    | Stock Market Data     |
| Requests   | API Calls             |
| dotenv     | Environment Variables |

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/react-multi-tool-agent.git

cd react-multi-tool-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key

FIN_HUB_API=your_finnhub_api_key

SEARCH_API_KEY=your_search_api_key
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## 💬 Example Queries

### Weather

```text
What is the weather in Hyderabad?
```

### Finance

```text
AAPL stock price
```

### Search

```text
Who is the Prime Minister of India?
```

### Commands

```text
ipconfig
```

---

## 📊 Current Capabilities

✅ ReAct Reasoning Loop

✅ Gemini Integration

✅ Weather Tool

✅ Finance Tool

✅ Web Search Tool

✅ Command Execution Tool

✅ Streamlit Interface

---

## 🔮 Future Improvements

* RAG Integration
* PDF Chat
* Vector Database Support
* ChromaDB / FAISS
* Memory Support
* Multi-Agent Workflows
* Portfolio Analysis
* Stock News & Sentiment Analysis
* Conversation Export

---

## 🔒 Security

API keys are stored in:

```env
.env
```

and excluded using:

```gitignore
.env
```

Never commit secrets to GitHub.

---

## 👨‍💻 Author

**Akhil Nakka**

Cloud Engineering | MERN Stack Development | AI & LLM Applications | Competitive Programming

---

⭐ If you found this project useful, please consider giving it a star.
