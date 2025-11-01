"""
Упрощенная демонстрация L-систем - ТРЕУГОЛЬНИК СЕРПИНСКОГО РАБОТАЕТ
"""

import turtle

def draw_koch_curve():
    """Кривая Коха - упрощенная версия"""
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Кривая Коха - Click to close")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, 100)
    t.pendown()
    t.pensize(2)
    
    # Рисуем кривую Коха вручную
    def koch_curve(length, level):
        if level == 0:
            t.forward(length)
        else:
            koch_curve(length/3, level-1)
            t.left(60)
            koch_curve(length/3, level-1)
            t.right(120)
            koch_curve(length/3, level-1)
            t.left(60)
            koch_curve(length/3, level-1)
    
    # Рисуем 3 стороны снежинки
    for _ in range(3):
        koch_curve(300, 3)
        t.right(120)
    
    t.hideturtle()
    screen.exitonclick()

def draw_sierpinski_triangle():
    """Треугольник Серпинского - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Треугольник Серпинского - Click to close")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -150)
    t.pendown()
    t.pensize(1)
    
    def sierpinski(length, level):
        if level == 0:
            # Рисуем маленький треугольник
            for i in range(3):
                t.forward(length)
                t.left(120)
        else:
            # Рекурсивно рисуем 3 меньших треугольника
            sierpinski(length/2, level-1)
            t.forward(length/2)
            sierpinski(length/2, level-1)
            t.backward(length/2)
            t.left(60)
            t.forward(length/2)
            t.right(60)
            sierpinski(length/2, level-1)
            t.left(60)
            t.backward(length/2)
            t.right(60)
    
    sierpinski(400, 4)
    t.hideturtle()
    screen.exitonclick()

def draw_sierpinski_carpet():
    """Ковер Серпинского - упрощенная версия"""
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Ковер Серпинского - Click to close")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-120, 120)
    t.pendown()
    t.pensize(1)
    
    def draw_square(size):
        for _ in range(4):
            t.forward(size)
            t.right(90)
    
    def sierpinski_carpet(x, y, size, level):
        if level == 0:
            t.penup()
            t.goto(x, y)
            t.pendown()
            draw_square(size)
        else:
            new_size = size / 3
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:
                        continue  # Пропускаем центральный квадрат
                    new_x = x + i * new_size
                    new_y = y - j * new_size
                    sierpinski_carpet(new_x, new_y, new_size, level-1)
    
    sierpinski_carpet(-120, 120, 240, 3)
    t.hideturtle()
    screen.exitonclick()

def draw_sierpinski_triangle_simple():
    """Треугольник Серпинского - САМАЯ ПРОСТАЯ РАБОТАЮЩАЯ ВЕРСИЯ"""
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Треугольник Серпинского - Click to close")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -150)
    t.pendown()
    t.pensize(1)
    
    def draw_triangle(size):
        """Рисует заполненный треугольник"""
        t.begin_fill()
        for _ in range(3):
            t.forward(size)
            t.left(120)
        t.end_fill()
    
    def sierpinski_simple(x, y, size, level):
        t.penup()
        t.goto(x, y)
        t.pendown()
        
        if level == 0:
            draw_triangle(size)
        else:
            # Рисуем 3 меньших треугольника
            sierpinski_simple(x, y, size/2, level-1)  # Левый нижний
            sierpinski_simple(x + size/2, y, size/2, level-1)  # Правый нижний
            sierpinski_simple(x + size/4, y + size * 0.433, size/2, level-1)  # Верхний
    
    # Рисуем контур большого треугольника
    t.penup()
    t.goto(-200, -150)
    t.pendown()
    for _ in range(3):
        t.forward(400)
        t.left(120)
    
    # Рисуем фрактал
    t.fillcolor("black")
    sierpinski_simple(-200, -150, 400, 4)
    
    t.hideturtle()
    screen.exitonclick()

def draw_sierpinski_triangle_line():
    """Треугольник Серпинского - версия только с линиями"""
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Треугольник Серпинского - Click to close")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -150)
    t.pendown()
    t.pensize(1)
    
    def sierpinski_line(length, level):
        if level == 0:
            # Рисуем треугольник
            for i in range(3):
                t.forward(length)
                t.left(120)
        else:
            # Рисуем 3 меньших треугольника
            sierpinski_line(length/2, level-1)
            t.forward(length/2)
            sierpinski_line(length/2, level-1)
            t.backward(length/2)
            t.left(60)
            t.forward(length/2)
            t.right(60)
            sierpinski_line(length/2, level-1)
            t.left(60)
            t.backward(length/2)
            t.right(60)
    
    sierpinski_line(400, 4)
    t.hideturtle()
    screen.exitonclick()

def main():
    """Главное меню"""
    while True:
        print("\n" + "="*50)
        print("           🎨 FRACTALS PROJECT")
        print("="*50)
        print("1. Триадная кривая Коха")
        print("2. Треугольник Серпинского (заполненная версия)")
        print("3. Ковер Серпинского")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите фрактал (0-3): ").strip()
        
        if choice == '1':
            print("Рисуем кривую Коха...")
            draw_koch_curve()
        elif choice == '2':
            print("Рисуем треугольник Серпинского (заполненная версия)...")
            draw_sierpinski_triangle_simple()
        elif choice == '3':
            print("Рисуем ковер Серпинского...")
            draw_sierpinski_carpet()
        elif choice == '0':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()