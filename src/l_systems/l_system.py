"""
Простой модуль L-систем для совместимости
"""

class SimpleLSystem:
    """Простая L-система"""
    def __init__(self):
        self.axiom = ""
        self.rules = {}
        self.angle = 0
        self.distance = 10
    
    def load_from_file(self, filename):
        """Загрузка из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if not lines:
                return False
                
            parts = lines[0].split()
            self.axiom = parts[0]
            self.angle = float(parts[1])
            if len(parts) > 2:
                self.distance = float(parts[2])
            
            self.rules = {}
            for line in lines[1:]:
                if '->' in line:
                    key, value = line.split('->')
                    self.rules[key.strip()] = value.strip()
            
            return True
        except:
            return False
    
    def generate(self, iterations=3):
        """Генерация строки"""
        current = self.axiom
        for _ in range(iterations):
            next_str = ""
            for char in current:
                if char in self.rules:
                    next_str += self.rules[char]
                else:
                    next_str += char
            current = next_str
        return current


# Создаем файлы конфигурации при импорте
import os

def create_configs():
    os.makedirs("src/l_systems/fractals", exist_ok=True)
    
    configs = {
        "koch_curve.txt": "F 60 5\nF -> F+F--F+F",
        "sierpinski_triangle.txt": "F-G-G 120 4\nF -> F-G+F+G-F\nG -> GG", 
        "sierpinski_carpet.txt": "F 90 3\nF -> F+F-F-FF-F-F-fF"
    }
    
    for name, content in configs.items():
        path = f"src/l_systems/fractals/{name}"
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)

create_configs()