from typing import Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def get_coords(self) -> Tuple[float, float]:
        return self.x, self.y

@dataclass
class Rect:
    id: int
    begin: Point
    end: Point

    @classmethod
    def begin_with(cls, id, x, y):
        return cls(id, Point(x, y), Point(x, y))
    
    def update_end_with(self, x: float, y: float) -> None:
        self.end = Point(x, y)
    
    def get_coords(self) -> Tuple[float, float, float, float]:
        return self.begin.x, self.begin.y, self.end.x, self.end.y
