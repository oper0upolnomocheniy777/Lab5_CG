"""
Примеры использования алгоритма Midpoint Displacement
Улучшенная цветовая схема
"""

from src.midpoint_displacement import (
    MidpointDisplacement, 
    draw_1d_mountain_safe, 
    draw_2d_mountain_enhanced,
    get_terrain_color_enhanced,
    get_terrain_color_simple
)

def demonstrate_1d_step_by_step():
    """Пошаговая демонстрация 1D алгоритма"""
    md = MidpointDisplacement(roughness=0.7, seed=42)
    
    print("\n🎯 ПОШАГОВАЯ ДЕМОНСТРАЦИЯ 1D MIDPOINT DISPLACEMENT")
    print("=" * 60)
    
    for iteration in range(6):
        points = md.generate_1d(iteration, 0, 0)
        
        print(f"\n📈 Итерация {iteration}:")
        print(f"   • Количество точек: {len(points)}")
        
        y_values = [p[1] for p in points]
        print(f"   • Диапазон высот: {min(y_values):.2f} до {max(y_values):.2f}")
        
        if len(points) <= 10:
            print(f"   • Высоты точек: {' → '.join([f'{y:+.2f}' for x, y in points])}")
        
        input("   Нажмите Enter для отображения графика...")
        draw_1d_mountain_safe(points, title=f"1D Midpoint - Итерация {iteration}")

def demonstrate_2d_comparison():
    """Сравнение разных параметров для 2D"""
    print("\n🏔️ СРАВНЕНИЕ 2D ЛАНДШАФТОВ С РАЗНЫМИ ПАРАМЕТРАМИ")
    print("=" * 60)
    
    configurations = [
        (33, 0.3, "Низкая шероховатость", "Плавные холмы"),
        (33, 0.7, "Средняя шероховатость", "Реалистичные горы"),
        (33, 0.9, "Высокая шероховатость", "Скалистый рельеф")
    ]
    
    for size, roughness, title, description in configurations:
        print(f"\n{title}: {description}")
        print(f"Шероховатость: {roughness}")
        
        md = MidpointDisplacement(roughness=roughness, seed=42)
        grid = md.generate_2d(size, 5, 0, 1)
        
        input("Нажмите Enter для отображения...")
        draw_2d_mountain_enhanced(grid, title=title, color_scheme="enhanced")

def demonstrate_color_schemes():
    """Демонстрация разных цветовых схем"""
    md = MidpointDisplacement(roughness=0.7, seed=42)
    
    print("\n🎨 ДЕМОНСТРАЦИЯ ЦВЕТОВЫХ СХЕМ")
    print("=" * 50)
    
    # Генерируем небольшой ландшафт для демонстрации
    grid = md.generate_2d(33, 5, 0, 1)
    
    print("\n1. Упрощенная цветовая схема")
    input("Нажмите Enter для продолжения...")
    draw_2d_mountain_enhanced(grid, title="Упрощенная схема", color_scheme="simple")
    
    print("\n2. Улучшенная цветовая схема")
    input("Нажмите Enter для продолжения...")
    draw_2d_mountain_enhanced(grid, title="Улучшенная схема", color_scheme="enhanced")

def show_color_legend():
    """Показать легенду цветов"""
    print("\n🎨 ЛЕГЕНДА ЦВЕТОВ УЛУЧШЕННОЙ СХЕМЫ")
    print("=" * 40)
    print("0.0 - 0.1   : 🌊 Глубокий океан (темно-синий)")
    print("0.1 - 0.2   : 🌊 Мелкий океан (голубой)")
    print("0.2 - 0.25  : 🏖️  Пляж (песочный)")
    print("0.25 - 0.35 : 🌾 Равнины (зеленый)")
    print("0.35 - 0.55 : 🌳 Лес (темно-зеленый)")
    print("0.55 - 0.7  : 🏞️  Холмы (коричневый)")
    print("0.7 - 0.85  : 🏔️  Горы (серый)")
    print("0.85 - 1.0  : ❄️  Снежные вершины (белый)")
    print()

def interactive_demo():
    """Интерактивная демонстрация с улучшенной цветовой схемой"""
    print("\n" + "="*50)
    print("   ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ MIDPOINT DISPLACEMENT")
    print("="*50)
    
    while True:
        print("\nВыберите тип демонстрации:")
        print("1. 1D горная линия (пошагово)")
        print("2. 1D горная линия (финальный результат)")
        print("3. 2D горный массив (упрощенная схема)")
        print("4. 2D горный массив (улучшенная схема)")
        print("5. Сравнение цветовых схем")
        print("6. Сравнение параметров шероховатости")
        print("7. Показать легенду цветов")
        print("0. Назад в главное меню")
        
        choice = input("Ваш выбор (0-7): ").strip()
        
        if choice == '1':
            demonstrate_1d_step_by_step()
            
        elif choice == '2':
            try:
                roughness = float(input("Введите шероховатость (0.1-1.0) [0.7]: ") or "0.7")
                iterations = int(input("Введите количество итераций (1-8) [6]: ") or "6")
                
                md = MidpointDisplacement(roughness=roughness)
                points = md.generate_1d(iterations, 0, 0)
                
                print(f"Сгенерировано {len(points)} точек")
                draw_1d_mountain_safe(points, title=f"1D - Шероховатость: {roughness}")
                
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == '3':
            try:
                roughness = float(input("Введите шероховатость (0.1-1.0) [0.7]: ") or "0.7")
                
                md = MidpointDisplacement(roughness=roughness, seed=42)
                grid = md.generate_2d(33, 5, 0, 1)
                draw_2d_mountain_enhanced(grid, title=f"2D - Упрощенная схема", color_scheme="simple")
                
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == '4':
            try:
                roughness = float(input("Введите шероховатость (0.1-1.0) [0.7]: ") or "0.7")
                
                md = MidpointDisplacement(roughness=roughness, seed=42)
                grid = md.generate_2d(33, 5, 0, 1)
                draw_2d_mountain_enhanced(grid, title=f"2D - Улучшенная схема", color_scheme="enhanced")
                
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == '5':
            demonstrate_color_schemes()
            
        elif choice == '6':
            demonstrate_2d_comparison()
            
        elif choice == '7':
            show_color_legend()
            input("Нажмите Enter для продолжения...")
                
        elif choice == '0':
            print("Возврат в главное меню...")
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите 0-7")

if __name__ == "__main__":
    interactive_demo()