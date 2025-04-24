FROM python:3.9-slim

WORKDIR /app

# Bağımlılık dosyasını kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Ollama ile iletişim için port açılımı
ENV OLLAMA_HOST="http://host.docker.internal:11434"

# Flask uygulaması için port
EXPOSE 5000

# Gunicorn ile çalıştır
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"] 