"""
Примеры использования алгоритма Midpoint Displacement
"""

from src.midpoint_displacement import MidpointDisplacement, draw_1d_mountain_safe, draw_2d_mountain_simple

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

def interactive_demo():
    """Интерактивная демонстрация с пользовательскими параметрами"""
    print("\n" + "="*50)
    print("   ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ MIDPOINT DISPLACEMENT")
    print("="*50)
    
    while True:
        print("\nВыберите тип демонстрации:")
        print("1. 1D горная линия (пошагово)")
        print("2. 1D горная линия (финальный результат)")
        print("3. 2D горный массив")
        print("0. Назад в главное меню")
        
        choice = input("Ваш выбор (0-3): ").strip()
        
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
                draw_2d_mountain_simple(grid, title=f"2D - Шероховатость: {roughness}")
                
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == '0':
            print("Возврат в главное меню...")
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите 0-3")

if __name__ == "__main__":
    interactive_demo()