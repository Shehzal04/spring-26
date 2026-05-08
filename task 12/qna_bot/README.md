# AI QnA Bot — Lab 12 Task
**Stack:** Flask · Hugging Face MiniLM · FAISS · HTML/CSS/JS

## Project Structure
```
qna_bot/
├── app.py                  ← Flask backend
├── requirements.txt        ← Python dependencies
├── data/
│   └── qna_data.csv        ← Your QnA dataset (replace with your own)
└── templates/
    └── index.html          ← Frontend UI
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your own dataset
Replace `data/qna_data.csv` with your topic's data.  
Required columns: `topic`, `question`, `answer`

### 3. Run the app
```bash
python app.py
```

Open browser at: **http://127.0.0.1:5000**

---

## How it works

1. **Preprocessing** — CSV loaded, nulls removed, text cleaned with regex
2. **Embedding** — Questions embedded using `paraphrase-MiniLM-L6-v2`
3. **FAISS Index** — Vectors stored in `IndexFlatL2` (Euclidean distance)
4. **Search** — User query embedded → top-K similar questions retrieved
5. **UI** — Flask serves results via `/search` POST endpoint → displayed in HTML

## To use a different topic
Just replace `qna_data.csv` with your own CSV having `topic`, `question`, `answer` columns.  
Delete `qna_faiss.index` so it rebuilds automatically on next run.
