"""
Алгоритм Midpoint Displacement для генерации горного массива
Улучшенная цветовая схема
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

def get_terrain_color_enhanced(normalized):
    """
    Улучшенная цветовая схема для рельефа с плавными переходами
    
    Args:
        normalized (float): нормализованная высота [0, 1]
        
    Returns:
        tuple: цвет RGB (r, g, b)
    """
    # Цвета для разных биомов
    DEEP_OCEAN = (0, 0, 139)        # Темно-синий
    SHALLOW_OCEAN = (30, 144, 255)  # Голубой
    BEACH = (238, 214, 175)         # Песочный
    PLAINS = (34, 139, 34)          # Зеленый
    FOREST = (0, 100, 0)            # Темно-зеленый
    HILLS = (139, 115, 85)          # Коричневый
    MOUNTAINS = (128, 128, 128)     # Серый
    SNOW = (255, 250, 250)          # Белый
    
    # Определяем биомы с плавными переходами
    if normalized < 0.1:
        # Глубокий океан
        return DEEP_OCEAN
        
    elif normalized < 0.2:
        # Переход: глубокий океан -> мелкий океан
        t = (normalized - 0.1) / 0.1
        return interpolate_color(DEEP_OCEAN, SHALLOW_OCEAN, t)
        
    elif normalized < 0.25:
        # Мелкий океан
        return SHALLOW_OCEAN
        
    elif normalized < 0.3:
        # Переход: мелкий океан -> пляж
        t = (normalized - 0.25) / 0.05
        return interpolate_color(SHALLOW_OCEAN, BEACH, t)
        
    elif normalized < 0.35:
        # Пляж
        return BEACH
        
    elif normalized < 0.45:
        # Переход: пляж -> равнины
        t = (normalized - 0.35) / 0.1
        return interpolate_color(BEACH, PLAINS, t)
        
    elif normalized < 0.55:
        # Равнины
        return PLAINS
        
    elif normalized < 0.65:
        # Переход: равнины -> лес
        t = (normalized - 0.55) / 0.1
        return interpolate_color(PLAINS, FOREST, t)
        
    elif normalized < 0.7:
        # Лес
        return FOREST
        
    elif normalized < 0.75:
        # Переход: лес -> холмы
        t = (normalized - 0.7) / 0.05
        return interpolate_color(FOREST, HILLS, t)
        
    elif normalized < 0.8:
        # Холмы
        return HILLS
        
    elif normalized < 0.85:
        # Переход: холмы -> горы
        t = (normalized - 0.8) / 0.05
        return interpolate_color(HILLS, MOUNTAINS, t)
        
    elif normalized < 0.9:
        # Горы
        return MOUNTAINS
        
    elif normalized < 0.95:
        # Переход: горы -> снег
        t = (normalized - 0.9) / 0.05
        return interpolate_color(MOUNTAINS, SNOW, t)
        
    else:
        # Снежные вершины
        return SNOW

def interpolate_color(color1, color2, t):
    """
    Линейная интерполяция между двумя цветами
    
    Args:
        color1 (tuple): первый цвет RGB
        color2 (tuple): второй цвет RGB
        t (float): коэффициент интерполяции [0, 1]
        
    Returns:
        tuple: интерполированный цвет RGB
    """
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

def get_terrain_color_simple(normalized):
    """
    Упрощенная цветовая схема (оригинальная)
    """
    if normalized < 0.3:
        # Вода
        return (0, 0, int(normalized * 200 + 55))
    elif normalized < 0.5:
        # Равнина
        return (34, int(normalized * 200 + 55), 34)
    elif normalized < 0.7:
        # Холмы
        return (139, int(normalized * 200), 19)
    else:
        # Горы
        gray = int(normalized * 200)
        return (gray, gray, gray)

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

def draw_2d_mountain_enhanced(grid, width=600, height=600, title="Midpoint Displacement - 2D", color_scheme="enhanced"):
    """
    Рисование 2D массива с улучшенной цветовой схемой
    
    Args:
        grid (list): 2D массив высот
        width (int): ширина окна
        height (int): высота окна  
        title (str): заголовок окна
        color_scheme (str): схема цветов ("enhanced" или "simple")
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
        
        print(f"Цветовая схема: {color_scheme}")
        print(f"Диапазон высот: {min_val:.3f} - {max_val:.3f}")
        
        for y in range(size):
            for x in range(size):
                # Нормализуем высоту
                normalized = (grid[y][x] - min_val) / (max_val - min_val + 0.001)
                
                # Выбираем цветовую схему
                if color_scheme == "enhanced":
                    color = get_terrain_color_enhanced(normalized)
                else:
                    color = get_terrain_color_simple(normalized)
                
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

# Убраны функции, вызывающие циклический импорт
# demonstrate_color_schemes() и demonstrate_1d_step_by_step() перемещены в examples