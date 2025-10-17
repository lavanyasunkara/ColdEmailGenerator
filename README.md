
---

# Cold Email Generator
AI-powered Streamlit app that generates personalized cold emails using LangChain and OpenAI.
Absolutely 💪 — here’s a **professional, GitHub-ready README.md** for your **Cold Email Generator** project.
It’s designed to look clean on GitHub, explain setup, and impress recruiters or collaborators.

---


---

## 🚀 Features

- 📄 Upload PDF or text resume and preview extracted content  
- 🔗 Fetch job descriptions directly from URLs (using `WebBaseLoader`)  
- 🧠 Uses LangChain-powered prompt pipelines for context extraction and email generation  
- ✉️ Automatically generates personalized cold emails based on skills and job fit  
- 🌐 Streamlit interface for simple, interactive use  
- ☁️ Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/Lavanyasunkara26/coldemailgenerator)

---

## 🧠 Tech Stack

| Category | Technologies |
|-----------|---------------|
| Frontend | [Streamlit](https://streamlit.io/) |
| AI Framework | [LangChain](https://www.langchain.com/), [LangChain-Community](https://pypi.org/project/langchain-community/) |
| Parsing | [PyPDF2](https://pypi.org/project/PyPDF2/) |
| Environment | Python 3.10+, [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Hosting | [Hugging Face Spaces](https://huggingface.co/spaces) |

---

## 🧩 Folder Structure

```

coldemailgenerator/
├── app/
|----resource/
│       ├── main.py             # Streamlit entry file
│       ├── chain.py            # LangChain logic
│       ├── portfolio.py        # Portfolio data interface
│       ├── utils.py            # Cleaning & helper functions
├── requirements.txt        # Dependencies
├── README.md               # This file

````

---

## ⚙️ Installation (Run Locally)

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/coldemailgenerator.git
   cd coldemailgenerator
````

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file in the project root:

   OPENAI_API_KEY=your_openai_key

5. **Run the app**

   ```bash
   streamlit run app/resource/main.py
   ```

6. Visit the app in your browser at
   👉 [http://localhost:8501](http://localhost:8501)

---


4. Commit → build → your Space will be live.

---

## 🧠 Example Usage

1. Upload a resume (PDF or text)
2. Paste a job posting link
3. Click **Generate Cold Email**
4. The AI generates a personalized outreach email

---

## 📦 Requirements

```
streamlit
langchain
langchain-community
PyPDF2
python-dotenv
```

---




