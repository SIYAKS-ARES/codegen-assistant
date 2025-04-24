from flask import Blueprint, render_template, request, jsonify
from app.ollama_client import OllamaClient
from app.utils import format_code_for_html

# Blueprint tanımı
main = Blueprint('main', __name__)

# Ollama istemcisi
ollama_client = OllamaClient()

@main.route('/', methods=['GET'])
def index():
    """Ana sayfa."""
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate_code():
    """Kod üretmek için API endpoint'i."""
    # İstek verilerini al
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Prompt boş olamaz'}), 400
    
    # Ollama API'sini kullanarak kod üret
    result = ollama_client.generate_code(prompt)
    
    # Sonucu döndür
    return jsonify(result) 