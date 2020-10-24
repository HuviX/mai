from dataclasses import dataclass

"""
От создателей "Вы там в Тинькоффе программируете?"
"""


@dataclass
class Point:
    x: int
    y: int
    
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)