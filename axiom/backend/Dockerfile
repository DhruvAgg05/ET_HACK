FROM python:3.11-slim

WORKDIR /app

# System dependencies for PaddleOCR + Tesseract fallback
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download the embedding model and the spaCy NER model.
# Without en_core_web_sm, entity_extractor.py falls back to spacy.blank("en")
# (no NER component) — it won't crash, but entity/relationship extraction
# quietly degrades to regex-only patterns.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python -m spacy download en_core_web_sm

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]