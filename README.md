#Healthcare Advice Chatbot

An AI-powered **Healthcare Advice Chatbot** that provides basic healthcare guidance based on user questions.
The chatbot uses **LangGraph workflow orchestration**, **LangChain tools**, and the **Groq LLM** to generate helpful responses.

The application is built with **Streamlit** to provide a simple and interactive web interface.

---

#Features

* Ask healthcare-related questions
* AI-generated responses using Groq LLM
* Tool-based reasoning with LangChain
* Workflow management using LangGraph
* Context-based healthcare guideline retrieval
* Simple and interactive Streamlit interface
* Conversation history tracking

---

#Example Topics Covered

The chatbot currently provides guidelines for:

* Diabetes
* Hypertension
* Mental Health

If a specific guideline is not found, the chatbot suggests consulting a healthcare professional.

---

#Project Architecture

The chatbot follows a **LangGraph workflow** consisting of three main nodes:

1️⃣ **Retrieve Context Node**
Retrieves healthcare guidelines related to the user's question.

2️⃣ **Create Prompt Node**
Builds a structured prompt combining:

* user query
* retrieved healthcare context

3️⃣ **Generate Response Node**
Uses a **ReAct Agent** to generate a response with the help of tools.

Workflow:

START → Retrieve Context → Create Prompt → Generate Response → END

---

# Technologies Used

* Python
* Streamlit (UI framework)
* LangChain (tool integration)
* LangGraph (workflow orchestration)
* Groq LLM (AI response generation)

---

# Project Structure

```
project-folder
│
├── day4.py          # Main chatbot application
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

# Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/healthcare-chatbot.git
cd healthcare-chatbot
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Set Groq API Key

Set your API key as an environment variable:

Windows:

```
set GROQ_API_KEY=your_api_key_here
```

Linux / Mac:

```
export GROQ_API_KEY=your_api_key_here
```

---

# Run the Application

```
streamlit run day4.py
```

Then open the browser at:

```
http://localhost:8501
```

