"""
Упрощенная демонстрация L-систем и Midpoint Displacement
"""

import turtle

# Добавьте этот импорт для сплайнов Безье
try:
    from src.Bezier import BezierSpline, ConsoleRenderer, SVGRenderer
except ImportError as e:
    print(f"⚠️  Модуль Bezier не загружен: {e}")

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

def draw_midpoint_1d():
    """1D Midpoint Displacement - горная линия"""
    from src.midpoint_displacement import MidpointDisplacement, draw_1d_mountain_safe
    
    print("Генерация 1D горной линии...")
    md = MidpointDisplacement(roughness=0.7, seed=42)
    points = md.generate_1d(6, 0, 0)
    
    print(f"Сгенерировано {len(points)} точек")
    y_values = [p[1] for p in points]
    print(f"Диапазон высот: {min(y_values):.2f} до {max(y_values):.2f}")
    
    draw_1d_mountain_safe(points, title="Midpoint Displacement - 1D Горная линия")

def draw_midpoint_2d():
    """2D Midpoint Displacement - горный массив"""
    from src.midpoint_displacement import MidpointDisplacement, draw_2d_mountain_simple
    
    print("Генерация 2D горного массива...")
    md = MidpointDisplacement(roughness=0.8, seed=42)
    grid = md.generate_2d(33, 5, 0, 1)
    print(f"Сгенерирована сетка {len(grid)}x{len(grid[0])}")
    
    draw_2d_mountain_simple(grid, title="Midpoint Displacement - 2D Горный массив")

def midpoint_interactive():
    """Интерактивная демонстрация Midpoint Displacement"""
    try:
        from examples.midpoint_examples import interactive_demo
        interactive_demo()
    except ImportError as e:
        print(f"Ошибка загрузки интерактивной демонстрации: {e}")
        print("Убедитесь, что файл examples/midpoint_examples.py существует")
    except Exception as e:
        print(f"Ошибка в интерактивной демонстрации: {e}")

def demo_bezier_splines():
    """Демонстрация кубических сплайнов Безье"""
    try:
        from src.Bezier import BezierSpline, ConsoleRenderer, SVGRenderer
        
        print("\n" + "="*50)
        print("   КУБИЧЕСКИЕ СПЛАЙНЫ БЕЗЬЕ")
        print("="*50)
        
        spline = BezierSpline()
        
        # Создаём начальный сплайн с двумя сегментами
        print("Создаём начальный сплайн...")
        spline.add_segment()
        spline.add_segment()
        
        # Основной цикл взаимодействия
        while True:
            print("\n" + ConsoleRenderer.render_ascii(spline))
            ConsoleRenderer.print_info(spline)
            
            print("\nДОСТУПНЫЕ ДЕЙСТВИЯ:")
            print("A. Добавить сегмент")
            print("B. Удалить последний сегмент") 
            print("C. Добавить контрольную точку")
            print("D. Удалить контрольную точку")
            print("E. Переместить контрольную точку")
            print("F. Сохранить в SVG файл")
            print("G. Вернуться в главное меню")
            
            action = input("\nВыберите действие (A-G): ").strip().upper()
            
            if action == "A":
                if spline.add_segment():
                    print(" Сегмент добавлен!")
                else:
                    print(" Ошибка добавления сегмента!")
            
            elif action == "B":
                if spline.remove_last_segment():
                    print(" Последний сегмент удалён!")
                else:
                    print(" Нечего удалять!")
            
            elif action == "C":
                try:
                    x = float(input("X координата новой точки: "))
                    y = float(input("Y координата новой точки: "))
                    spline.add_control_point(x, y)
                    print(" Точка добавлена!")
                except ValueError:
                    print(" Ошибка: введите числа!")
            
            elif action == "D":
                try:
                    index = int(input("Индекс точки для удаления: "))
                    if spline.remove_control_point(index):
                        print("✅ Точка удалена!")
                    else:
                        print(" Неверный индекс или нельзя удалить эту точку!")
                except ValueError:
                    print(" Ошибка: введите число!")
            
            elif action == "E":
                try:
                    index = int(input("Индекс точки: "))
                    x = float(input("Новая X координата: "))
                    y = float(input("Новая Y координата: "))
                    if spline.move_control_point(index, x, y):
                        print(" Точка перемещена!")
                    else:
                        print(" Неверный индекс!")
                except ValueError:
                    print(" Ошибка: введите числа!")
            
            elif action == "F":
                filename = input("Имя SVG файла (например: bezier.svg): ").strip()
                if not filename:
                    filename = "bezier_spline.svg"
                SVGRenderer.save_svg(spline, filename)
                print(f" Сплайн сохранён в {filename}")
            
            elif action == "G":
                print("Возвращаемся в главное меню...")
                break
            
            else:
                print(" Неверный выбор!")
                
    except ImportError as e:
        print(f" Ошибка загрузки модуля Bezier: {e}")
        print("Убедитесь, что файлы находятся в папке src/Bezier/")
    except Exception as e:
        print(f" Неожиданная ошибка: {e}")

def main():
    """Главное меню"""
    while True:
        print("\n" + "="*50)
        print("           🎨 FRACTALS PROJECT")
        print("="*50)
        print("1. Триадная кривая Коха")
        print("2. Треугольник Серпинского (заполненная версия)")
        print("3. Ковер Серпинского")
        print("4. Midpoint Displacement - 1D горная линия")
        print("5. Midpoint Displacement - 2D горный массив")
        print("6. Midpoint Displacement - интерактивная демонстрация")
        print("7.  Кубические сплайны Безье (интерактивно)")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите фрактал (0-7): ").strip()
        
        if choice == '1':
            print("Рисуем кривую Коха...")
            draw_koch_curve()
        elif choice == '2':
            print("Рисуем треугольник Серпинского (заполненная версия)...")
            draw_sierpinski_triangle_simple()
        elif choice == '3':
            print("Рисуем ковер Серпинского...")
            draw_sierpinski_carpet()
        elif choice == '4':
            print("Рисуем 1D горную линию...")
            draw_midpoint_1d()
        elif choice == '5':
            print("Рисуем 2D горный массив...")
            draw_midpoint_2d()
        elif choice == '6':
            print("Запускаем интерактивную демонстрацию...")
            midpoint_interactive()
        elif choice == '7':
            print("Запускаем интерактивные сплайны Безье...")
            demo_bezier_splines()
        elif choice == '0':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()