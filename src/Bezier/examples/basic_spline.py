#!/usr/bin/env python3
"""
Пример использования кубических сплайнов Безье
"""

import os
import sys

# Добавляем путь к src для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.Bezier import BezierSpline, ConsoleRenderer, SVGRenderer

def demo_basic_spline():
    """Демонстрация базового функционала сплайнов"""
    print("ДЕМОНСТРАЦИЯ КУБИЧЕСКИХ СПЛАЙНОВ БЕЗЬЕ")
    print("=" * 50)
    
    # Создаём сплайн
    spline = BezierSpline()
    
    # Добавляем начальные точки
    print("Добавляем начальный сегмент...")
    spline.add_segment()  # Добавляет 4 точки
    
    # Показываем результат
    print(ConsoleRenderer.render_ascii(spline))
    ConsoleRenderer.print_info(spline)
    
    # Добавляем ещё один сегмент
    print("\nДобавляем второй сегмент...")
    spline.add_segment()
    
    print(ConsoleRenderer.render_ascii(spline))
    ConsoleRenderer.print_info(spline)
    
    # Сохраняем в SVG
    SVGRenderer.save_svg(spline, "bezier_demo.svg")
    
    print("\nДемонстрация завершена!")

if __name__ == "__main__":
    demo_basic_spline()