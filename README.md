# Pak-Law-AI


**Law-Bot** (PakLawAI) is an **AI-powered legal information assistant** specialized in **Pakistani law**.  
It combines **RAG (Retrieval-Augmented Generation)** with **LLMs** to provide structured, citation-backed answers.  
The project also benchmarks multiple **Ollama models** against your own **RAG system** using evaluation metrics.

---

## 🚀 Features
- 📚 **RAG pipeline** with Qdrant vector store + local embeddings  
- 🧾 **Custom legal prompt** for trustworthy, structured answers  
- 🤖 **Model benchmarking** against PakLawAI (Ollama, OpenAI, etc.)  
- 📊 **Evaluation metrics**: BLEU, semantic similarity, jurisdiction accuracy, composite score  
- 💾 Auto-saves results to **JSON** after each query  
- 🔄 Resumable: skips queries already processed  

---

## 📂 Project Structure
```

law-bot/
│── main.py                # Entry point (evaluation loop)
│── config.py              # Configurations (paths, models, timeouts)
│── metrics.py             # Scoring functions (BLEU, semantic, etc.)
│── utils.py               # Ollama helpers
│
│── rag/
│   │── **init**.py
│   │── rag\_core.py        # RAG setup (PDFs, embeddings, vector store)
│   │── prompts.py         # System prompt (Pakistani law specialization)
│   │── rag\_query.py       # ask\_rag() function
│
│── data/
│   │── queries\_all.txt    # Input queries
│   │── result.json        # Output results
│   │── processed\_files.pkl
│   │── All\_laws\_categories/   # PDF law documents
│
│── .env                   # API keys (OPENAI\_API\_KEY=...)
│── requirements.txt       # Dependencies
│── README.md              # Project documentation

````

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/law-bot.git
cd law-bot
````

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key_here
```

> ⚠️ You also need **Ollama** installed locally for running models like `llama3`, `mistral`, etc.

---

## ▶️ Usage

### Run RAG + Evaluation

```bash
python main.py
```

* Reads queries from `data/queries_all.txt`
* Gets answers from:

  * **PakLawAI (RAG system)**
  * **Multiple Ollama models**
* Evaluates with BLEU, semantic similarity, jurisdiction accuracy
* Saves results in `data/result.json`

---

## 📊 Evaluation Metrics

| Metric              | Description                                          |
| ------------------- | ---------------------------------------------------- |
| **BLEU**            | Compares overlap of words with reference answer      |
| **Semantic Score**  | Cosine similarity of embeddings (semantic closeness) |
| **Jurisdiction**    | Binary check for presence of Pakistani legal terms   |
| **Length Penalty**  | Prevents overly short answers scoring too high       |
| **Composite Score** | Weighted combination of all metrics                  |

---

## 📌 Example Workflow

1. Add your queries in `data/queries_all.txt`
2. Run `python main.py`
3. Check results in `data/result.json`

---

## 🛠 Requirements

* Python 3.9+
* [Ollama](https://ollama.ai) (for running local models)
* Qdrant (local or cloud) for vector storage

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

PakLawAI is an **informational assistant only**.
It does **not provide legal advice** and is **not a substitute for a qualified lawyer**.
Always consult a licensed advocate for legal matters.

---

