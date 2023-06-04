import unittest
from src.z251 import Z251
from src.polynomial import Polynomial


class PolynomialTest(unittest.TestCase):
    def test_str(self):
        coefficients = [Z251(2), Z251(-3), Z251(1)]
        polynomial = Polynomial(coefficients)
        expected_str = "2*x^2 + 248*x^1 + 1*x^0"
        self.assertEqual(str(polynomial), expected_str)

    def test_evaluate(self):
        coefficients = [Z251(2), Z251(-3), Z251(1)]
        polynomial = Polynomial(coefficients)
        self.assertEqual(polynomial.evaluate(x=Z251(2)), Z251(1)) # TODO: Check why this is comparing memory addresses. the result is correct, but the test fails

    def test_interpolate(self):
        polynomial = Polynomial([])
        interpolated_polynomial = polynomial.interpolate(points=[(Z251(0), Z251(1)), (Z251(1), Z251(2)), (Z251(2), Z251(3))])
        expected_coefficients = [Z251(1), Z251(1), Z251(1)]
        self.assertEqual(interpolated_polynomial, Polynomial(expected_coefficients)) # TODO: Check why this is comparing memory addresses. the result is correct, but the test fails
        self.assertEqual(interpolated_polynomial.degree, 2)


    def test_set_coefficient(self):
        coefficients = [Z251(2), Z251(-3), Z251(1)]
        polynomial = Polynomial(coefficients)
        index = 1
        value = Z251(5)
        polynomial.set_coefficient(index, value)
        expected_coefficients = [Z251(2), Z251(5), Z251(1)]
        self.assertEqual(polynomial.coefficients, expected_coefficients)


if __name__ == "__main__":
    unittest.main()
