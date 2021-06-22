from typing import Tuple, Dict
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
    
    def get_obj(self, ratio) -> Dict[str, float]:
        (x1, y1, x2, y2) = self.get_coords()
        r_xg = min(x1, x2)
        r_xd = max(x1, x2)
        r_yh = min(y1, y2)
        r_yb = max(y1, y2)
        r_w = r_xd - r_xg
        r_h = r_yb - r_yh
        obj = {
            "x": int(r_xg * ratio),
            "y": int(r_yh * ratio),
            "width": int(r_w * ratio),
            "height": int(r_h * ratio),
        }
        return obj