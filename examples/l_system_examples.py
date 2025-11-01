from src.l_systems.l_system import LSystem

def demonstrate_fractals():
    """Демонстрация всех трех фракталов"""
    
    # Триадная кривая Коха
    koch = LSystem('src/l_systems/fractals/koch_curve.txt')
    koch.set_randomness(0.1)  # Добавляем немного случайности
    koch_string = koch.generate_string(4)
    print("Кривая Коха сгенерирована")
    koch.draw(koch_string)
    
    # Ковер Серпинского
    carpet = LSystem('src/l_systems/fractals/sierpinski_carpet.txt')
    carpet_string = carpet.generate_string(3)
    print("Ковер Серпинского сгенерирован")
    carpet.draw(carpet_string)
    
    # Треугольник Серпинского
    triangle = LSystem('src/l_systems/fractals/sierpinski_triangle.txt')
    triangle_string = triangle.generate_string(5)
    print("Треугольник Серпинского сгенерирован")
    triangle.draw(triangle_string)

if __name__ == "__main__":
    demonstrate_fractals()