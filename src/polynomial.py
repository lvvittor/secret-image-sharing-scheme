from __future__ import annotations
from src.z251 import Z251
from typing import List, Tuple


class Polynomial:
    def __init__(self, coefficients: List[Z251]=None):
        if coefficients:
            self.coefficients = coefficients
            self.degree = len(self.coefficients) - 1
        else:
            raise ValueError("Invalid arguments")

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
    @staticmethod
    def interpolate(points: List[Tuple[Z251, Z251]]) -> "Polynomial":
        """
        Returns the polynomial that interpolates the given points
        
        Arguments:
            points {List[Tuple[Z251, Z251]]} -- List of points to interpolate [(x1, y1), (x2, y2), ..., (xn, yn)]

        Returns:
            Polynomial -- Polynomial that interpolates the given points
        """
        n = len(points)
        coefficients = []
        # print(f"POINTS: {[(p[0].value, p[1].value) for p in points]}")
        ca = 0 # coefficients analysed
        yp_cache: List[Z251] = [0 for _ in range(n)] # y' cache
        while ca < n:
            curr_coefficient = Z251(0)
            top = n - ca # Reduced Lagrange -> We ignore one extra point each iteration
            for i in range(top):
                # Calculate y' for the current point
                y = Z251(0)
                if ca == 0:
                    y = points[i][1]
                else: 
                    y = (yp_cache[i] - coefficients[ca - 1]) * Z251.INVERSE_TABLE[points[i][0].value] 
                
                yp_cache[i] = y

                # Calculate Li(0)
                li = Z251(1)
                for j in range(top):
                    if i != j:
                        li *= Z251(-1) * points[j][0] / (points[i][0] - points[j][0])

                curr_coefficient += y * li
  
            ca += 1
            coefficients.append(curr_coefficient)

        return Polynomial(coefficients)
    
    def set_coefficient(self, index: int, value: Z251):
        self.coefficients[index] = value

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.degree == other.degree and all(a == b for a, b in zip(self.coefficients, other.coefficients))
        return False




