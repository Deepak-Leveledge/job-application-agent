# 💼 AI Job Application Agent

An intelligent multi-agent AI system that analyzes job descriptions, matches them against your resume, and automatically generates a tailored cover letter and resume improvement suggestions — all in one click.

🚀 **Live Demo** → [https://job-application-agent.onrender.com](https://job-application-agent.onrender.com)

---

## 📌 What It Does

Paste a job description and upload your resume — the AI agents will:

- 🔍 Analyze the job description deeply
- 📄 Analyze your resume and extract key information
- 🌐 Research the company and market online
- 🎯 Calculate your match score with skill gaps and strengths
- ✍️ Write a personalized tailored cover letter
- 📝 Give specific resume improvement suggestions
- ✅ Run a quality check on all outputs

---

## 🏗️ Architecture — Multi Agent System

```
User Input (Job Description + Resume PDF)
              ↓
     [Supervisor — LangGraph]
      /       |        \
     ↓        ↓         ↓
[JD          [Resume    [Market
Analyzer]    Analyzer]  Researcher]
     \          |        /
      ↓         ↓       ↓
      [Match Analyzer Agent]
              ↓
      [Cover Letter Writer]
              ↓
      [Resume Improver Agent]
              ↓
      [Quality Checker Agent]
         ↓           ↓
      APPROVED    REVISE (loop back)
         ↓
    Final Output
```

---

## 🤖 Agents

| Agent                   | Role                                                                 |
| ----------------------- | -------------------------------------------------------------------- |
| **JD Analyzer**         | Extracts skills, requirements, responsibilities from job description |
| **Resume Analyzer**     | Extracts skills, experience, achievements from resume                |
| **Market Researcher**   | Searches web for company info, news, culture using Tavily            |
| **Match Analyzer**      | Compares JD vs Resume, calculates match score, finds gaps            |
| **Cover Letter Writer** | Writes a personalized cover letter using all context                 |
| **Resume Improver**     | Suggests specific keyword and content improvements                   |
| **Quality Checker**     | Reviews all outputs and approves or sends back for revision          |

---

## 🛠️ Tech Stack

| Tool                  | Purpose                                  |
| --------------------- | ---------------------------------------- |
| **Python**            | Core programming language                |
| **LangGraph**         | Multi-agent workflow orchestration       |
| **LangChain**         | LLM integration layer                    |
| **Gemini 2.0 Flash**  | LLM brain for all agents                 |
| **Tavily Search API** | Real-time web search for market research |
| **LangSmith**         | Agent tracing and observability          |
| **PyPDF2**            | Resume PDF text extraction               |
| **Streamlit**         | Web UI                                   |
| **Render**            | Cloud deployment                         |

---

## ⚙️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/job-application-agent.git
cd job-application-agent
```

### 2. Install uv and create virtual environment

```bash
pip install uv
uv venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Create `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=job-application-agent
```

### 5. Run the app

```bash
streamlit run app.py
```

Open → [http://localhost:8501](http://localhost:8501)

---

## 🔑 API Keys Required

| API           | Where to Get                                       | Cost      |
| ------------- | -------------------------------------------------- | --------- |
| **Gemini**    | [aistudio.google.com](https://aistudio.google.com) | Free      |
| **Tavily**    | [tavily.com](https://tavily.com)                   | Free tier |
| **LangSmith** | [smith.langchain.com](https://smith.langchain.com) | Free tier |

---

## 🖥️ How to Use

1. Open the app at the live URL or locally
2. Paste the full job description in the left panel
3. Upload your resume as a PDF
4. Click **🚀 Generate Application**
5. Wait ~1 minute for all agents to complete
6. View results across 5 tabs:
   - 🎯 Match Score and Analysis
   - ✍️ Tailored Cover Letter (downloadable)
   - 📝 Resume Improvement Tips
   - 🔍 Full JD Analysis
   - ✅ Quality Report

---

## 📊 Output Example

```
Match Score        : 78/100
Strong Matches     : Python, FastAPI, REST APIs
Skill Gaps         : Docker, AWS
Cover Letter       : Personalized, 4 paragraphs
Resume Tips        : 6 specific improvements
Quality Check      : ✅ APPROVED
```

---

## 🔭 Observability

All agent runs are fully traced in **LangSmith**:

- Every LLM call with input and output
- Every Tavily search query and result
- Full graph execution timeline
- Token usage per agent

---
