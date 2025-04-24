import requests
import json

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
        # Sistem promptu hazırla
        system_prompt = """
        Sen bir Python kod üretici asistansın. Kullanıcıdan gelen isteğe göre:
        1. Sadece çalışır bir Python kod bloğu üret.
        2. Kodun ne işe yaradığını özetleyen kısa bir başlık döndür.
        Cevabını şu formatta ver:
        ---CODE---
        <python kodu buraya>
        ---TITLE---
        <başlık buraya>
        """
        
        # İstek gövdesi
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
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
            title_part = ""
            
            if "---CODE---" in response_text and "---TITLE---" in response_text:
                code_section = response_text.split("---CODE---")[1].split("---TITLE---")[0].strip()
                title_section = response_text.split("---TITLE---")[1].strip()
                
                code_part = code_section
                title_part = title_section
            
            return {"code": code_part, "title": title_part}
            
        except Exception as e:
            print(f"Ollama API hatası: {str(e)}")
            return {"code": "", "title": f"Hata: {str(e)}"} 