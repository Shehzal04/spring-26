from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import faiss
import re
import os
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ─── CONFIG ─────────────────────────────────────────────────────────────────
MODEL_NAME = 'paraphrase-MiniLM-L6-v2'
DATA_FILE  = 'data/qna_data.csv'
INDEX_FILE = 'qna_faiss.index'

# ─── HELPERS ────────────────────────────────────────────────────────────────
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z0-9\s?.!,]', '', text)
        text = text.lower().strip()
    else:
        text = ''
    return text

def load_data():
    df = pd.read_csv(DATA_FILE)
    df.dropna(subset=['question', 'answer'], inplace=True)
    df['clean_question'] = df['question'].apply(clean_text)
    df = df[df['clean_question'].str.len() > 0].reset_index(drop=True)
    return df

def build_index(df, model):
    print("Building FAISS index...")
    embeddings = model.encode(df['clean_question'].tolist(), show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    print(f"Index saved → {INDEX_FILE}")
    return index, embeddings

def load_or_build(df, model):
    if os.path.exists(INDEX_FILE):
        print("Loading existing FAISS index...")
        index = faiss.read_index(INDEX_FILE)
    else:
        index, _ = build_index(df, model)
    return index

# ─── INIT ────────────────────────────────────────────────────────────────────
print("Loading model...")
model = SentenceTransformer(MODEL_NAME)
df    = load_data()
index = load_or_build(df, model)
print(f"Ready! {len(df)} QnA pairs loaded.")

# ─── ROUTES ──────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data  = request.get_json()
    query = data.get('query', '').strip()
    k     = int(data.get('k', 5))

    if not query:
        return jsonify({'error': 'Empty query'}), 400

    clean_q   = clean_text(query)
    query_emb = model.encode([clean_q]).astype('float32')
    distances, indices = index.search(query_emb, k)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), 1):
        row = df.iloc[idx]
        results.append({
            'rank':     rank,
            'question': row['question'],
            'answer':   row['answer'],
            'distance': round(float(dist), 4),
            'topic':    row.get('topic', 'General')
        })

    return jsonify({'query': query, 'results': results})

if __name__ == '__main__':
    app.run(debug=True)
