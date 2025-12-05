---
title: BGE-M3 Embedding Service
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# 🧠 BGE-M3 Embedding Service

A FastAPI-based embedding service that generates 1024-dimensional vectors using the BGE-M3 model.

## 🚀 Quick Start

This Space provides a simple REST API for generating text embeddings.

### API Endpoints

- **Health Check**: `/health`
- **Generate Embedding**: `/embed` (POST)
- **Interactive Docs**: `/docs`

### Example Usage

```python
import requests

response = requests.post(
    "https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/embed",
    json={"text": "Hello, world!"}
)

embedding = response.json()["embedding"]
print(f"Embedding dimension: {len(embedding)}")
```

### Try It Out

Click the "View App" button above to access the interactive API documentation!

## 📝 Features

- ✅ High-quality multilingual embeddings
- ✅ Fast inference on CPU
- ✅ Ready-to-use REST API
- ✅ Automatic model downloading
- ✅ Interactive Swagger docs

## 🔧 Technical Details

- **Model**: BAAI/bge-m3
- **Framework**: FastAPI + Uvicorn
- **Embedding Dimension**: 1024
- **Device**: CPU
