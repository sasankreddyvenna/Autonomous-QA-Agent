# 🤖 Autonomous QA Agent

An AI-powered system that automates **Test Case Generation** and
**Selenium Script Generation** from uploaded requirement documents.

Perfect for QA engineers, testers, and teams looking to speed up test
authoring using LLMs.

------------------------------------------------------------------------

## ✅ What This Tool Does

✔️ Upload requirement documents\
✔️ Extract & store knowledge in a vector database\
✔️ Generate test cases grounded in context\
✔️ Select a test case & auto-generate Selenium scripts\
✔️ View scripts on screen & download as `.py`

------------------------------------------------------------------------

## 🗂 Project Structure

    Autonomous-QA-Agent/
    │
    ├── backend/
    │   ├── app.py
    │   ├── routes/
    │   │     ├── ingest_routes.py
    │   │     ├── testcase_routes.py
    │   │     ├── script_routes.py
    │   ├── services/
    │   │    ├── knowledge_base/
    │   │         ├── chroma_client.py 
    │   │         └── embedder.py 
    │   │
    │   ├── groq_client/
    │   │         ├── generator.py 
    │   │         └── prompts/
    │   │              ├── testcase_prompt.txt
    │   │              └── script_prompt.txt
    │   │
    │   └── selenium/
    │   │      └── script_generator.py
    │   │      
    │   ├── storage/  
    │   │      └── chroma_db/
    │   │
    │   │
    │   │
    │   ├── utils/    
    │   │  
    ├── ui/
    │   ├── app.py
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md

------------------------------------------------------------------------

## ✅ System Requirements

  Requirement    Version
  -------------- --------------------------
  Python         3.9+
  Pip            Latest
  Chrome         Latest
  ChromeDriver   Matching browser version
  Groq API Key   Required

------------------------------------------------------------------------

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/sasankreddyvenna/Autonomous-QA-Agent.git
cd Autonomous-QA-Agent
```

### 2️⃣ Create & Activate Virtual Environment

**Windows**

``` bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Configure Environment Variables

Create a `.env` file inside the **backend** folder:

    GROQ_API_KEY=YOUR_KEY_HERE

✅ Do NOT commit this file\
✅ `.env` is ignored by git

------------------------------------------------------------------------

## ▶️ Start the Backend (FastAPI)

``` bash
cd backend
uvicorn app:app --reload
```

Backend runs at: 👉 http://127.0.0.1:8000

------------------------------------------------------------------------

## 🖥️ Start the UI (Streamlit)

Open a new terminal:

``` bash
cd ui
streamlit run app.py
```

UI opens in your browser ✅

------------------------------------------------------------------------

## 🧪 How to Use

### ✅ Step 1: Upload Documents

-   Upload PDF, TXT, MD, JSON, or HTML
-   System ingests & stores content in vector DB

### ✅ Step 2: Generate Test Cases

-   Enter a query (e.g., "Generate test cases for login")
-   View results in a table

### ✅ Step 3: Generate Selenium Script

-   Select a test case
-   Click **Generate Script**
-   View script on screen
-   Download `.py` file

------------------------------------------------------------------------

## ⚙️ API Endpoints

  Endpoint                Method   Description
  ----------------------- -------- ---------------------------
  `/ingest/upload`        POST     Upload & ingest documents
  `/testcases/generate`   POST     Generate test cases
  `/script/generate`      POST     Generate Selenium script

------------------------------------------------------------------------

## 📌 Example Selenium Output

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
```

------------------------------------------------------------------------

## 🔒 Security Notes

✅ No secrets are committed to the repo\
✅ GitHub push protection is enabled\
✅ Always store API keys in `.env`

------------------------------------------------------------------------

## 🚀 Roadmap

-   Playwright support
-   Test execution engine
-   CI/CD integration
-   Multi-user workspace

------------------------------------------------------------------------

## 🤝 Contributing

Pull requests are welcome!

------------------------------------------------------------------------

## 📜 License

MIT License

------------------------------------------------------------------------

## ⭐ Support

If you find this project helpful: ✅ Star ⭐ the repository\
✅ Share with others



