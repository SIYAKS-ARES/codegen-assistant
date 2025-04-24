from flask import Blueprint, render_template, request, jsonify
from app.ollama_client import OllamaClient
from app.utils import format_code_for_html
from s4e.job import Job

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
    data = request.json or {}
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Prompt boş olamaz'}), 400
    
    # Job sınıfını kullanarak kod üret
    code_job = CodeGenerationJob({'prompt': prompt, 'max_score': 10})
    code_job.run()
    
    # Çıktıları kontrol et
    detail = code_job.output.get('detail', [])
    compact = code_job.output.get('compact', [])
    
    # Sonuç oluştur
    result = {
        'code': detail[0] if detail else '',
        'title': compact[0] if compact else 'Kod Başlığı'
    }
    
    return jsonify(result)

class CodeGenerationJob(Job):
    """Job sınıfını miras alan kod üretme işi."""
    
    def __init__(self, param=None):
        """Constructor
        
        Args:
            param (dict): İş parametreleri {'prompt': 'istek metni', 'max_score': 10}
        """
        super().__init__(param)
    
    def run(self):
        """İşi çalıştır."""
        # Önce parent'ın run metodunu çağır
        # Bu, output dict'ini oluşturur ve içindeki listeleri başlatır
        super().run()
        
        # Parametreleri al
        prompt = self.param.get('prompt', '')
        
        # Ollama API'sini kullanarak kod üret
        result = ollama_client.generate_code(prompt)
        
        if result and result.get('code'):
            # Kod üretimi başarılı oldu
            self.output['detail'].append(result['code'])
            self.output['compact'].append(result['title'])
            
            # İş adımlarını kaydet
            self.output['video'].extend([
                f"1. Prompt alındı: '{prompt}'",
                "2. LLM modeline istek gönderildi",
                "3. Kod ve başlık ayrıştırıldı",
                "4. Sonuç döndürüldü"
            ])
            
            # Başarılı - tam puan
            self.calculate_score()
        else:
            # Kod üretilemedi
            self.output['detail'].append("Kod üretilemedi")
            self.output['compact'].append("Hata: Kod üretimi başarısız")
            self.output['video'].append("Hata: LLM modeline istek gönderildi ancak sonuç alınamadı")
            
            # Başarısız - 0 puan
            self.score = 0 