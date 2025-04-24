# Yapay Zeka Destekli Kod Üretici

Bu proje, Ollama ile çalışan yerel bir yapay zeka modeli (LLM) kullanarak kullanıcı tarafından verilen promptlara göre Python kodu üreten bir web uygulamasıdır.

## Özellikler

- Yerel çalışan Ollama LLM (Mistral gibi) entegrasyonu
- Kullanıcı promptlarından Python kodu üretimi
- Üretilen kod için otomatik başlık oluşturma
- Basit ve kullanıcı dostu web arayüzü
- Docker ile containerization
- Kubernetes ile deployment desteği

## Gereksinimler

- Python 3.9+
- Flask
- Requests
- Ollama (yerel olarak çalışan)
- Docker (opsiyonel)
- Kubernetes / Minikube (opsiyonel)

## Kurulum ve Çalıştırma

### Yerel Kurulum

1. Repository'i klonlayın:
   ```
   git clone https://github.com/kullanici/codegen-assistant.git
   cd codegen-assistant
   ```

2. Sanal ortam oluşturun ve bağımlılıkları yükleyin:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ollama'yı yükleyin ve çalıştırın:
   ```
   # Ollama'yı https://ollama.ai/ adresinden indirin
   # Mistral modelini yükleyin:
   ollama pull mistral
   ```

4. Uygulamayı çalıştırın:
   ```
   python run.py
   ```

5. Tarayıcınızda [http://localhost:5000](http://localhost:5000) adresine gidin.

### Docker ile Çalıştırma

1. Docker imajını oluşturun:
   ```
   docker build -t codegen-assistant .
   ```

2. Ollama'nın çalıştığından emin olun.

3. Container'ı çalıştırın:
   ```
   docker run -p 5000:5000 -e OLLAMA_HOST=http://host.docker.internal:11434 codegen-assistant
   ```

4. Tarayıcınızda [http://localhost:5000](http://localhost:5000) adresine gidin.

### Kubernetes ile Deployment

1. Docker imajını oluşturun ve registry'ye push edin:
   ```
   docker build -t KULLANICI_ADI/codegen-assistant:latest .
   docker push KULLANICI_ADI/codegen-assistant:latest
   ```

2. `deployment.yaml` ve `service.yaml` dosyalarında "USERNAME" değerini kendi Docker Hub kullanıcı adınızla değiştirin.

3. Minikube'u başlatın:
   ```
   minikube start
   ```

4. Deployment ve Service oluşturun:
   ```
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

5. Service'e erişin:
   ```
   minikube service codegen-assistant-service
   ```

## Proje Yapısı

```
codegen-assistant/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── ollama_client.py
│   ├── utils.py
│   └── templates/
│       └── index.html
├── s4e/
│   ├── __init__.py
│   ├── config.py
│   ├── task.py
│   └── job.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── deployment.yaml
├── service.yaml
├── README.md
└── run.py
```

## Docker Hub'a Yükleme

Docker imajını Docker Hub'a yüklemek için:

```
docker login
docker build -t KULLANICI_ADI/codegen-assistant:latest .
docker push KULLANICI_ADI/codegen-assistant:latest
```

## Lisans

MIT

## Katkıda Bulunanlar

- Yapımcı: [İsim] 