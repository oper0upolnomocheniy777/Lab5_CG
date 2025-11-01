import turtle
import math
import random
from typing import Dict, List, Tuple

class LSystem:
    def __init__(self, filename: str = None):
        self.axiom = ""
        self.rules = {}
        self.angle = 0
        self.initial_angle = 0
        self.distance = 10
        self.randomness = 0.0
        
        if filename:
            self.load_from_file(filename)
    
    def load_from_file(self, filename: str):
        """Загрузка L-системы из файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if len(lines) < 2:
            raise ValueError("Неверный формат файла")
        
        # Первая строка: атом угол начальное_направление
        first_line = lines[0].split()
        self.axiom = first_line[0]
        self.angle = float(first_line[1])
        self.initial_angle = float(first_line[2]) if len(first_line) > 2 else 90
        
        # Остальные строки: правила
        self.rules = {}
        for line in lines[1:]:
            if '->' in line:
                key, value = line.split('->', 1)
                self.rules[key.strip()] = value.strip()
    
    def set_randomness(self, randomness: float):
        """Установка уровня случайности (0-1)"""
        self.randomness = randomness
    
    def generate_string(self, iterations: int) -> str:
        """Генерация строки L-системы"""
        current_string = self.axiom
        
        for _ in range(iterations):
            new_string = []
            for char in current_string:
                if char in self.rules and random.random() > self.randomness:
                    new_string.append(self.rules[char])
                else:
                    new_string.append(char)
            current_string = ''.join(new_string)
        
        return current_string
    
    def calculate_bounds(self, l_string: str) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Вычисление границ для масштабирования"""
        x, y = 0, 0
        angle = self.initial_angle
        min_x = max_x = min_y = max_y = 0
        stack = []
        
        for char in l_string:
            if char == 'F' or char == 'G':
                rad_angle = math.radians(angle)
                x += math.cos(rad_angle) * self.distance
                y += math.sin(rad_angle) * self.distance
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
            elif char == '+':
                angle += self.angle * (1 + random.uniform(-self.randomness, self.randomness))
            elif char == '-':
                angle -= self.angle * (1 + random.uniform(-self.randomness, self.randomness))
            elif char == '[':
                stack.append((x, y, angle))
            elif char == ']':
                x, y, angle = stack.pop()
        
        return (min_x, min_y), (max_x, max_y)
    
    def draw(self, l_string: str, screen_width: int = 800, screen_height: int = 600):
        """Отрисовка L-системы с масштабированием"""
        # Вычисляем границы
        (min_x, min_y), (max_x, max_y) = self.calculate_bounds(l_string)
        
        # Вычисляем масштаб
        width = max_x - min_x
        height = max_y - min_y
        
        if width == 0 or height == 0:
            scale = 1
        else:
            scale = min(screen_width * 0.8 / width, screen_height * 0.8 / height)
        
        # Настраиваем turtle
        screen = turtle.Screen()
        screen.setup(screen_width, screen_height)
        screen.title("L-System Fractal")
        
        t = turtle.Turtle()
        t.speed(0)
        t.penup()
        t.hideturtle()
        
        # Центрируем рисунок
        start_x = -width * scale / 2
        start_y = -height * scale / 2
        t.goto(start_x, start_y)
        t.pendown()
        
        # Отрисовываем
        angle = self.initial_angle
        stack = []
        
        for char in l_string:
            current_angle = angle * (1 + random.uniform(-self.randomness, self.randomness))
            
            if char == 'F' or char == 'G':
                rad_angle = math.radians(current_angle)
                t.setheading(current_angle)
                t.forward(self.distance * scale)
            elif char == '+':
                angle += self.angle
            elif char == '-':
                angle -= self.angle
            elif char == '[':
                stack.append((t.xcor(), t.ycor(), angle))
            elif char == ']':
                t.penup()
                x, y, angle = stack.pop()
                t.goto(x, y)
                t.pendown()
        
        screen.exitonclick()

def main():
    """Примеры использования"""
    # Создаем конфигурационные файлы для фракталов
    
    # Триадная кривая Коха
    koch_config = """F 60 0
F -> F+F--F+F"""
    
    with open('src/l_systems/fractals/koch_curve.txt', 'w') as f:
        f.write(koch_config)
    
    # Ковер Серпинского
    carpet_config = """F 90 0
F -> F+F-F-FF-F-F-fF
f -> fff"""
    
    with open('src/l_systems/fractals/sierpinski_carpet.txt', 'w') as f:
        f.write(carpet_config)
    
    # Треугольник Серпинского
    triangle_config = """F 60 0
F -> F-G+F+G-F
G -> GG"""
    
    with open('src/l_systems/fractals/sierpinski_triangle.txt', 'w') as f:
        f.write(triangle_config)
    
    # Демонстрация
    print("Демонстрация L-систем:")
    
    # Кривая Коха
    print("1. Триадная кривая Коха")
    koch = LSystem('src/l_systems/fractals/koch_curve.txt')
    koch_string = koch.generate_string(3)
    koch.draw(koch_string)
    
    # Ковер Серпинского
    print("2. Ковер Серпинского")
    carpet = LSystem('src/l_systems/fractals/sierpinski_carpet.txt')
    carpet_string = carpet.generate_string(2)
    carpet.draw(carpet_string)
    
    # Треугольник Серпинского
    print("3. Треугольник Серпинского")
    triangle = LSystem('src/l_systems/fractals/sierpinski_triangle.txt')
    triangle_string = triangle.generate_string(4)
    triangle.draw(triangle_string)

if __name__ == "__main__":
    main()