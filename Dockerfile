FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY Data/ ./Data/
COPY Reports/ ./Reports/
COPY Scripts/ ./Scripts/
COPY README.md .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit","run","app/main.py","--server.address=0.0.0.0","--server.port=8501"]