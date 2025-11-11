import os
from typing import List, Tuple
from .spline import BezierSpline

class ConsoleRenderer:
    """Класс для консольной визуализации сплайнов"""
    
    @staticmethod
    def render_ascii(spline: BezierSpline, width: int = 60, height: int = 20) -> str:
        """
        Отрисовывает сплайн в виде ASCII арта
        
        Args:
            spline: Объект сплайна
            width: Ширина поля
            height: Высота поля
            
        Returns:
            Строка с ASCII визуализацией
        """
        # Создаём холст
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Функции масштабирования координат
        def scale_x(x): 
            return max(0, min(width - 1, int(x * (width - 1))))
        
        def scale_y(y): 
            return max(0, min(height - 1, int((1 - y) * (height - 1))))
        
        # Рисуем кривые Безье
        curves = spline.get_all_curves()
        for curve in curves:
            for x, y in curve:
                sx, sy = scale_x(x), scale_y(y)
                canvas[sy][sx] = '·'
        
        # Рисуем контрольные точки
        control_points = spline.get_control_points()
        for i, (x, y) in enumerate(control_points):
            sx, sy = scale_x(x), scale_y(y)
            if 0 <= sx < width and 0 <= sy < height:
                # Используем буквы для точек (A, B, C, ...)
                point_char = chr(65 + (i % 26))  # A, B, C, ...
                canvas[sy][sx] = point_char
        
        # Рисуем контрольный многоугольник
        for i in range(len(control_points) - 1):
            x1, y1 = control_points[i]
            x2, y2 = control_points[i + 1]
            
            # Простая линейная интерполяция для отрисовки линии
            steps = max(abs(scale_x(x2) - scale_x(x1)), abs(scale_y(y2) - scale_y(y1)))
            if steps > 0:
                for j in range(steps + 1):
                    t = j / steps
                    x = x1 + t * (x2 - x1)
                    y = y1 + t * (y2 - y1)
                    sx, sy = scale_x(x), scale_y(y)
                    if 0 <= sx < width and 0 <= sy < height and canvas[sy][sx] == ' ':
                        canvas[sy][sx] = '.'
        
        # Собираем результат
        result = []
        result.append("+" + "-" * width + "+")
        for row in canvas:
            result.append("|" + "".join(row) + "|")
        result.append("+" + "-" * width + "+")
        
        return "\n".join(result)
    
    @staticmethod
    def print_info(spline: BezierSpline) -> None:
        """Выводит информацию о сплайне"""
        points = spline.get_control_points()
        segments = spline.get_segments_count()
        
        print(f"\n=== ИНФОРМАЦИЯ О СПЛАЙНЕ ===")
        print(f"Количество сегментов: {segments}")
        print(f"Количество контрольных точек: {len(points)}")
        
        for i, (x, y) in enumerate(points):
            point_type = "Начало" if i % 3 == 0 else "Контрольная"
            if i == len(points) - 1:
                point_type = "Конец"
            print(f"  {chr(65 + (i % 26))} ({point_type}): ({x:.3f}, {y:.3f})")


class SVGRenderer:
    """Класс для сохранения сплайнов в SVG формате"""
    
    @staticmethod
    def save_svg(spline: BezierSpline, filename: str, width: int = 400, height: int = 400) -> None:
        """
        Сохраняет сплайн в SVG файл
        
        Args:
            spline: Объект сплайна
            filename: Имя файла для сохранения
            width: Ширина SVG
            height: Высота SVG
        """
        svg_lines = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            '  <rect width="100%" height="100%" fill="white"/>',
            '  <g stroke="black" fill="none">'
        ]
        
        # Функции масштабирования
        def scale_x(x): return x * (width - 40) + 20
        def scale_y(y): return (1 - y) * (height - 40) + 20
        
        # Рисуем кривые Безье
        curves = spline.get_all_curves()
        for i, curve in enumerate(curves):
            if curve:
                path_data = f"M {scale_x(curve[0][0])} {scale_y(curve[0][1])}"
                for point in curve[1:]:
                    path_data += f" L {scale_x(point[0])} {scale_y(point[1])}"
                
                svg_lines.append(f'    <path d="{path_data}" stroke="blue" stroke-width="3"/>')
        
        # Рисуем контрольный многоугольник
        control_points = spline.get_control_points()
        if control_points:
            poly_points = " ".join(f"{scale_x(x)},{scale_y(y)}" for x, y in control_points)
            svg_lines.append(f'    <polyline points="{poly_points}" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>')
        
        # Рисуем контрольные точки
        for i, (x, y) in enumerate(control_points):
            sx, sy = scale_x(x), scale_y(y)
            color = "red" if i % 3 == 0 or i == len(control_points) - 1 else "green"
            svg_lines.append(f'    <circle cx="{sx}" cy="{sy}" r="5" fill="{color}"/>')
            svg_lines.append(f'    <text x="{sx+8}" y="{sy+5}" font-size="12">{chr(65 + (i % 26))}</text>')
        
        svg_lines.extend(['  </g>', '</svg>'])
        
        # Сохраняем файл
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(svg_lines))
        
        print(f"Сплайн сохранён в файл: {filename}")