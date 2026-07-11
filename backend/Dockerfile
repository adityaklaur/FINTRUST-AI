FROM python:3.13-slim

WORKDIR /app

# System deps for pdfplumber/onnxruntime wheels are already provided as wheels;
# keep the image slim.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ships the prebuilt registry + vector store under data/ so the API is queryable
# immediately (the ONNX embedding model downloads on first query).
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
