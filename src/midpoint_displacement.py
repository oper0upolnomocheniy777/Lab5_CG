"""
Алгоритм Midpoint Displacement для генерации горного массива
"""

import random
import turtle
import math

class MidpointDisplacement:
    """Класс для генерации ломаной линии методом Midpoint Displacement"""
    
    def __init__(self, roughness=0.7, seed=None):
        """
        Инициализация генератора
        
        Args:
            roughness (float): параметр шероховатости (0-1)
            seed (int): seed для генератора случайных чисел
        """
        self.roughness = roughness
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def generate_1d(self, iterations, start_height=0, end_height=0):
        """
        Генерация одномерной ломаной линии
        
        Args:
            iterations (int): количество итераций
            start_height (float): начальная высота
            end_height (float): конечная высота
            
        Returns:
            list: список точек (x, y)
        """
        points = [(0, start_height), (1, end_height)]
        
        for iter_num in range(iterations):
            new_points = []
            segment_count = len(points) - 1
            
            for i in range(segment_count):
                # Берем текущие точки
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Добавляем левую точку
                new_points.append((x1, y1))
                
                # Вычисляем среднюю точку
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Добавляем случайное смещение
                displacement = random.uniform(-1, 1) * self.roughness
                scale = 1.0 / (2 ** (iter_num * 0.5))  # Уменьшаем смещение с каждой итерацией
                mid_y += displacement * scale
                
                # Добавляем среднюю точку
                new_points.append((mid_x, mid_y))
            
            # Добавляем последнюю точку
            new_points.append(points[-1])
            points = new_points
        
        return points
    
    def generate_2d(self, size, iterations, min_height=0, max_height=1):
        """
        Генерация двумерного массива высот
        
        Args:
            size (int): размер сетки (должен быть степенью двойки + 1)
            iterations (int): количество итераций
            min_height (float): минимальная высота
            max_height (float): максимальная высота
            
        Returns:
            list: 2D массив высот
        """
        # Инициализация массива
        grid = [[0.0 for _ in range(size)] for _ in range(size)]
        
        # Устанавливаем угловые значения
        grid[0][0] = random.uniform(min_height, max_height)
        grid[0][size-1] = random.uniform(min_height, max_height)
        grid[size-1][0] = random.uniform(min_height, max_height)
        grid[size-1][size-1] = random.uniform(min_height, max_height)
        
        step = size - 1
        scale = 1.0
        
        while step > 1:
            # Diamond step
            for y in range(0, size - 1, step):
                for x in range(0, size - 1, step):
                    avg = (grid[y][x] + grid[y][x + step] + 
                          grid[y + step][x] + grid[y + step][x + step]) / 4
                    displacement = random.uniform(-1, 1) * scale * self.roughness
                    grid[y + step // 2][x + step // 2] = avg + displacement
            
            # Square step
            for y in range(0, size, step // 2):
                for x in range((y + step // 2) % step, size, step):
                    total = 0
                    count = 0
                    
                    # Собираем соседние точки
                    if y - step // 2 >= 0:
                        total += grid[y - step // 2][x]
                        count += 1
                    if y + step // 2 < size:
                        total += grid[y + step // 2][x]
                        count += 1
                    if x - step // 2 >= 0:
                        total += grid[y][x - step // 2]
                        count += 1
                    if x + step // 2 < size:
                        total += grid[y][x + step // 2]
                        count += 1
                    
                    if count > 0:
                        displacement = random.uniform(-1, 1) * scale * self.roughness
                        grid[y][x] = total / count + displacement
            
            step //= 2
            scale *= 0.5
        
        return grid

def create_turtle_screen(width=800, height=400, title="Turtle Graphics"):
    """Создает и настраивает экран turtle"""
    screen = turtle.Screen()
    screen.setup(width, height)
    screen.title(title)
    screen.bgcolor("white")
    return screen

def draw_1d_mountain_safe(points, width=800, height=400, title="Midpoint Displacement - 1D"):
    """
    Безопасное рисование одномерной горной линии
    """
    screen = None
    try:
        # Создаем новый экран
        screen = turtle.Screen()
        screen.setup(width, height)
        screen.title(title)
        screen.bgcolor("white")
        
        # Создаем черепашку
        t = turtle.Turtle()
        t.speed(0)
        t.penup()
        
        # Масштабируем точки для отображения
        x_values = [p[0] for p in points]
        y_values = [p[1] for p in points]
        
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        x_scale = (width - 100) / (x_max - x_min) if x_max > x_min else 1
        y_scale = (height - 100) / (y_max - y_min + 0.001)
        
        # Начальная позиция
        start_x = -width//2 + 50
        start_y = (points[0][1] - y_min) * y_scale - height//4
        t.goto(start_x, start_y)
        t.pendown()
        t.pensize(2)
        t.color("brown")
        
        # Рисуем линию
        for x, y in points[1:]:
            screen_x = -width//2 + 50 + (x - x_min) * x_scale
            screen_y = (y - y_min) * y_scale - height//4
            t.goto(screen_x, screen_y)
        
        t.hideturtle()
        
        # Ждем клика для закрытия
        print("Нажмите на окно для закрытия...")
        screen.exitonclick()
        
    except Exception as e:
        print(f"Ошибка при рисовании: {e}")
        if screen:
            try:
                screen.bye()
            except:
                pass
    finally:
        # Всегда пытаемся очистить
        try:
            turtle.clearscreen()
        except:
            pass

def draw_2d_mountain_simple(grid, width=500, height=500, title="Midpoint Displacement - 2D"):
    """
    Упрощенное рисование 2D массива
    """
    screen = None
    try:
        screen = turtle.Screen()
        screen.setup(width, height)
        screen.title(title)
        screen.bgcolor("black")
        screen.colormode(255)
        
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        screen.tracer(0, 0)  # Отключаем анимацию
        
        size = len(grid)
        cell_size = min(width, height) / size
        
        # Находим минимальную и максимальную высоту
        min_val = min(min(row) for row in grid)
        max_val = max(max(row) for row in grid)
        
        for y in range(size):
            for x in range(size):
                # Нормализуем высоту для цвета
                normalized = (grid[y][x] - min_val) / (max_val - min_val + 0.001)
                
                # Выбираем цвет
                if normalized < 0.3:
                    color = (0, 0, int(normalized * 200 + 55))  # Вода
                elif normalized < 0.5:
                    color = (34, int(normalized * 200 + 55), 34)  # Равнина
                elif normalized < 0.7:
                    color = (139, int(normalized * 200), 19)  # Холмы
                else:
                    color = (int(normalized * 200), int(normalized * 200), int(normalized * 200))  # Горы
                
                # Рисуем пиксель
                t.penup()
                t.goto(x * cell_size - width//2, y * cell_size - height//2)
                t.pendown()
                t.fillcolor(color)
                t.pencolor(color)
                t.begin_fill()
                for _ in range(4):
                    t.forward(cell_size)
                    t.left(90)
                t.end_fill()
        
        screen.update()
        print("Нажмите на окно для закрытия...")
        screen.exitonclick()
        
    except Exception as e:
        print(f"Ошибка при рисовании 2D: {e}")
        if screen:
            try:
                screen.bye()
            except:
                pass
    finally:
        try:
            turtle.clearscreen()
        except:
            pass

def demonstrate_1d_step_by_step():
    """Пошаговая демонстрация 1D алгоритма"""
    md = MidpointDisplacement(roughness=0.7, seed=42)
    
    print("🎯 ДЕМОНСТРАЦИЯ 1D MIDPOINT DISPLACEMENT")
    print("=" * 50)
    
    for iteration in range(6):
        points = md.generate_1d(iteration, 0, 0)
        print(f"\nИтерация {iteration}: {len(points)} точек")
        
        # Простая текстовая информация
        y_values = [p[1] for p in points]
        print(f"Высоты: от {min(y_values):.2f} до {max(y_values):.2f}")
        
        if len(points) <= 10:
            print("Точки:", " → ".join([f"{y:+.2f}" for x, y in points]))
        
        # Рисуем график
        draw_1d_mountain_safe(points, title=f"1D Midpoint - Итерация {iteration}")

if __name__ == "__main__":
    demonstrate_1d_step_by_step()