import requests
import json
import re

class OllamaClient:
    """Ollama API ile iletişim kuran istemci sınıfı."""
    
    def __init__(self, base_url="http://localhost:11434"):
        """Ollama istemcisini başlatır.
        
        Args:
            base_url (str): Ollama API'nin URL'i
        """
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        
    def generate_code(self, prompt, model="mistral"):
        """Verilen prompt'a göre kod üretir.
        
        Args:
            prompt (str): Kullanıcı isteği
            model (str): Kullanılacak model adı
            
        Returns:
            dict: {"code": "üretilen kod", "title": "kod başlığı"}
        """
        # Sistem promptu hazırla - daha net yönergelerle
        system_prompt = """
        Sen yüksek kaliteli bir Python kod asistanısın. Kullanıcıdan gelen isteğe göre hem kod hem başlık üretmelisin:
        
        1. Önce isteğe uygun çalışan bir Python kodu yaz
        2. Sonra bu kodun amacını özetleyen kısa bir başlık ekle
        
        Yanıtını TAM OLARAK aşağıdaki formatta vermelisin. Bu format ZORUNLUDUR:
        
        ---CODE---
        def example_function():
            # kod örneği
            return "sonuç"
        ---TITLE---
        Örnek Başlık: Bu fonksiyon ne yapar
        
        Hem kod hem başlık kısmını mutlaka doldur. Başka açıklama ekleme.
        """
        
        # İstek gövdesi
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "temperature": 0.3,  # Daha tutarlı yanıtlar için
            "max_tokens": 2000   # Yeterince uzun yanıt için
        }
        
        try:
            # API isteği gönder
            response = requests.post(self.generate_url, json=payload)
            response.raise_for_status()
            
            # Yanıtı al
            result = response.json()
            response_text = result.get("response", "")
            
            # Yanıtı ayrıştır
            code_part = ""
            title_part = "Başlık bulunamadı"  # Varsayılan değer
            
            # Regex ile bölümleri bul
            code_match = re.search(r'---CODE---(.*?)(?:---TITLE---|$)', response_text, re.DOTALL)
            title_match = re.search(r'---TITLE---(.*?)$', response_text, re.DOTALL)
            
            if code_match:
                code_part = code_match.group(1).strip()
            
            if title_match:
                title_part = title_match.group(1).strip()
            
            # Başlık yoksa, alternatif yöntem
            if not title_part or title_part == "Başlık bulunamadı":
                # Başlık üretmek için yeni bir istek gönder
                title_prompt = f"Aşağıdaki Python kodunun ne yaptığını bir başlık olarak özetle (30 karakterden kısa):\n\n```python\n{code_part}\n```"
                title_payload = {
                    "model": model,
                    "prompt": title_prompt,
                    "system": "Verilen kodun ne yaptığını çok kısa bir başlıkla özetle.",
                    "stream": False,
                    "max_tokens": 100
                }
                
                title_response = requests.post(self.generate_url, json=title_payload)
                if title_response.status_code == 200:
                    title_part = title_response.json().get("response", "").strip()
            
            return {"code": code_part, "title": title_part}
            
        except Exception as e:
            print(f"Ollama API hatası: {str(e)}")
            return {"code": "", "title": f"Hata: {str(e)}"} 