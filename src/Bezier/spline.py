import numpy as np
from typing import List, Tuple, Optional

class BezierSpline:
    """
    Класс для работы с составными кубическими сплайнами Безье
    """
    
    def __init__(self):
        self.control_points: List[Tuple[float, float]] = []
        self.segments: List[List[Tuple[float, float]]] = []
    
    def add_control_point(self, x: float, y: float) -> None:
        """
        Добавляет контрольную точку в сплайн
        
        Args:
            x: X-координата точки
            y: Y-координата точки
        """
        self.control_points.append((x, y))
        self._update_segments()
    
    def remove_control_point(self, index: int) -> bool:
        """
        Удаляет контрольную точку по индексу
        
        Args:
            index: Индекс точки для удаления
            
        Returns:
            True если удаление успешно, False если индекс неверный
        """
        if 0 <= index < len(self.control_points):
            # Не позволяем удалять точки, если это нарушит структуру сегментов
            if len(self.control_points) >= 4 and index % 3 == 0 and index != 0 and index != len(self.control_points) - 1:
                print("Нельзя удалить начальную точку сегмента (кроме первой и последней)")
                return False
            
            self.control_points.pop(index)
            self._update_segments()
            return True
        return False
    
    def move_control_point(self, index: int, new_x: float, new_y: float) -> bool:
        """
        Перемещает контрольную точку
        
        Args:
            index: Индекс точки
            new_x: Новая X-координата
            new_y: Новая Y-координата
            
        Returns:
            True если перемещение успешно
        """
        if 0 <= index < len(self.control_points):
            self.control_points[index] = (new_x, new_y)
            self._update_segments()
            return True
        return False
    
    def _update_segments(self) -> None:
        """Обновляет сегменты сплайна на основе контрольных точек"""
        self.segments = []
        # Каждый сегмент состоит из 4 точек: P0, P1, P2, P3
        for i in range(0, len(self.control_points) - 1, 3):
            if i + 3 < len(self.control_points):
                segment = self.control_points[i:i+4]
                self.segments.append(segment)
    
    def add_segment(self) -> bool:
        """
        Добавляет новый сегмент к сплайну
        
        Returns:
            True если сегмент добавлен успешно
        """
        if len(self.control_points) == 0:
            # Первый сегмент
            self.control_points.extend([(0.1, 0.1), (0.2, 0.3), (0.3, 0.2), (0.4, 0.4)])
        else:
            # Добавляем после последней точки
            last_x, last_y = self.control_points[-1]
            new_points = [
                (last_x + 0.1, last_y + 0.1),
                (last_x + 0.2, last_y + 0.0),
                (last_x + 0.3, last_y + 0.1)
            ]
            self.control_points.extend(new_points)
        
        self._update_segments()
        return True
    
    def remove_last_segment(self) -> bool:
        """
        Удаляет последний сегмент сплайна
        
        Returns:
            True если удаление успешно
        """
        if len(self.segments) > 0:
            # Удаляем последние 3 точки (P1, P2, P3 последнего сегмента)
            self.control_points = self.control_points[:-3]
            self._update_segments()
            return True
        return False
    
    def bezier_curve(self, points: List[Tuple[float, float]], num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Вычисляет точки кубической кривой Безье
        
        Args:
            points: 4 контрольные точки
            num_points: количество точек на кривой
            
        Returns:
            Список точек кривой
        """
        if len(points) != 4:
            return []
        
        curve = []
        P0, P1, P2, P3 = points
        
        for t in np.linspace(0, 1, num_points):
            # Формула кубической кривой Безье
            x = (1-t)**3 * P0[0] + 3*(1-t)**2*t * P1[0] + 3*(1-t)*t**2 * P2[0] + t**3 * P3[0]
            y = (1-t)**3 * P0[1] + 3*(1-t)**2*t * P1[1] + 3*(1-t)*t**2 * P2[1] + t**3 * P3[1]
            curve.append((x, y))
        
        return curve
    
    def get_all_curves(self) -> List[List[Tuple[float, float]]]:
        """Возвращает все кривые сплайна"""
        curves = []
        for segment in self.segments:
            curves.append(self.bezier_curve(segment))
        return curves
    
    def get_control_points(self) -> List[Tuple[float, float]]:
        """Возвращает копию списка контрольных точек"""
        return self.control_points.copy()
    
    def get_segments_count(self) -> int:
        """Возвращает количество сегментов"""
        return len(self.segments)
    
    def clear(self) -> None:
        """Очищает сплайн"""
        self.control_points.clear()
        self.segments.clear()