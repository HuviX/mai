from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)