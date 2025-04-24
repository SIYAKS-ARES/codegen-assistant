# Task sınıfı tanımı
class Task:
    def __init__(self, param=None):
        self.param = param or {}
        self.output = {}
        self.score = 0
        
    def run(self):
        # Bu method alt sınıflar tarafından override edilmelidir
        raise NotImplementedError("Alt sınıflar bu metodu uygulamalıdır")
    
    def calculate_score(self):
        # Bu method alt sınıflar tarafından override edilmelidir
        raise NotImplementedError("Alt sınıflar bu metodu uygulamalıdır") 