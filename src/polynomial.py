from __future__ import annotations
from src.z251 import Z251
from typing import List, Tuple


class Polynomial:
    def __init__(self, coefficients: List[Z251]):
        self.coefficients = coefficients
        self.degree = len(self.coefficients) - 1

    def __str__(self):
        return " + ".join(
            [
                f"{coefficient}*x^{self.degree - index}"
                for index, coefficient in enumerate(self.coefficients)
            ]
        )
    
    def evaluate(self, x: Z251) -> Z251:
        result = Z251(0)
        for index, coefficient in enumerate(self.coefficients):
            result += coefficient * (x ** (self.degree - index))
        return result
    
    # TODO: Check if this is correct!
    def interpolate(self, points: List[Tuple[Z251, Z251]]) -> Polynomial:
        """
        Returns the polynomial that interpolates the given points
        
        Arguments:
            points {List[Tuple[Z251, Z251]]} -- List of points to interpolate [(x1, y1), (x2, y2), ..., (xn, yn)]

        Returns:
            Polynomial -- Polynomial that interpolates the given points
        """
        n = len(points)
        coefficients = []
        for current_point_index in range(n):
            current_coefficient = Z251(0)
            for i in range(n):
                if i != current_point_index:
                    li = Z251(1) / (points[current_point_index][0] - points[i][0])
                    current_coefficient += points[i][1] * li
            coefficients.append(current_coefficient)
        return Polynomial(coefficients)
    
    def set_coefficient(self, index: int, value: Z251):
        self.coefficients[index] = value

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.degree == other.degree and all(a == b for a, b in zip(self.coefficients, other.coefficients))
        return False




