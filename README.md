# 👶 BabyCare Chat-Bot

A conversational AI assistant designed to provide general information and guidance on **baby care**, such as feeding, milestones, and development.  
The chatbot retrieves accurate responses from a **JSON knowledge base** using **semantic similarity** powered by the **SentenceTransformer** model (`all-MiniLM-L6-v2`).

---

## 🧠 Overview

The BabyCare Chatbot allows parents and caregivers to ask natural language questions like:

> "What should a 13-month-old be able to do?"  
> "How much milk should my baby drink?"  
> "What food is safe for a 13-month-old?"

It then searches the knowledge base for the **most relevant question** and provides a clear, detailed answer — including a gentle reminder that it is not a substitute for professional medical advice.

---

## 📂 Project Structure

babycare-chatbot/
│
├── baby_qa_data.json # Knowledge base of baby-related Q&A
├── chatbot.py # Core chatbot logic (semantic search + response)
├── app.py # Streamlit front-end UI
├── requirements.txt # Dependencies
└── README.md # Documentation


---

## ⚙️ How It Works

1. **Knowledge Base:**  
   The bot uses a `baby_qa_data.json` file formatted as:
   ```json
   [
     {
       "question": "What should a 13-month-old be able to do?",
       "answer": "A 13-month-old baby will be able to do all sorts of exciting new things..."
     },
     {
       "question": "How many words should a 13-month-old say?",
       "answer": "Most 12- to 13-month-olds can say one word and about half of them say two words."
     }
   ]


Semantic Search:
The chatbot encodes all questions from the JSON file and compares user input with them using cosine similarity to find the most relevant response.

Streamlit UI:
Provides a friendly chat interface where users can type questions or click sample prompts.

🧩 Features

✅ Semantic understanding of user questions
✅ JSON-based knowledge base for easy updates
✅ Real-time chat interface using Streamlit
✅ Includes disclaimer for safe medical communication
✅ Lightweight model for fast local inference

🚀 Installation and Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/babycare-chatbot.git
cd babycare-chatbot

2️⃣ Install dependencies
pip install -r requirements.txt


requirements.txt

streamlit
sentence-transformers
scikit-learn
numpy

3️⃣ Add the Knowledge Base

Create a file named baby_qa_data.json and paste your baby care Q&A dataset in the same format shown above.

4️⃣ Run the App
streamlit run app.py


Open the app in your browser at http://localhost:8501

💬 Example Questions

“What can a 13-month-old eat?”

“How many words should my 1-year-old say?”

“How much milk does a 13-month-old need?”

“What are 13-month-old milestones?”

🧠 Model Details

Embedding Model: all-MiniLM-L6-v2

Similarity Metric: Cosine Similarity

Language: English

Purpose: Local semantic retrieval (not connected to external APIs)

🧷 Disclaimer

⚠️ This chatbot provides general informational guidance only.
It is not a substitute for professional medical or pediatric advice.
Always consult your pediatrician for any medical concerns.

👨‍💻 Author

Sheon Shibu
🎓 MCA Graduate | 💡 AI & Data Enthusiast


🏷️ License

This project is licensed under the MIT License — feel free to modify and use it for educational or personal projects.

⭐ Future Enhancements

Add voice-based Q&A using SpeechRecognition

Expand knowledge base for multiple baby age groups

Integrate with OpenAI API for fallback responses

Add image upload for symptom-based queries

🍼 Making baby care knowledge simple, safe, and accessible for everyone.
