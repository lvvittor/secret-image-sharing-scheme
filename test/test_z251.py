import unittest
from src.z251 import Z251

class Z251TestCase(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(Z251(0) + Z251(0), Z251(0))  
        self.assertEqual(Z251(251) + Z251(0), Z251(251))  
        self.assertEqual(Z251(0) + Z251(251), Z251(251))  
        self.assertEqual(Z251(251) + Z251(251), Z251(251))  

    def test_subtraction(self):
        self.assertEqual(Z251(0) - Z251(0), Z251(0))  
        self.assertEqual(Z251(251) - Z251(0), Z251(251))  
        self.assertEqual(Z251(0) - Z251(251), Z251(0))  
        self.assertEqual(Z251(251) - Z251(251), Z251(0))  

    def test_multiplication(self):
        self.assertEqual(Z251(0) * Z251(0), Z251(0))  
        self.assertEqual(Z251(251) * Z251(0), Z251(0))  
        self.assertEqual(Z251(0) * Z251(251), Z251(0))  
        self.assertEqual(Z251(251) * Z251(251), Z251(251))  

    def test_power(self):
        self.assertEqual(Z251(0) ** 0, Z251(1))
        self.assertEqual(Z251(0) ** 1, Z251(0))
        self.assertEqual(Z251(251) ** 2, Z251(0))
        self.assertEqual(Z251(0) ** 3, Z251(251))
        self.assertEqual(Z251(251) ** 4, Z251(0))

    def test_division(self):
        # Division by zero
        with self.assertRaises(ValueError):
            result = Z251(0) / Z251(0)  

        with self.assertRaises(ValueError):
            result = Z251(251) / Z251(0)  
        
        with self.assertRaises(ValueError):
            result = Z251(0) / Z251(251)  

        with self.assertRaises(ValueError):
            result = Z251(251) / Z251(251)  

        # Division by non-zero
        self.assertEqual(Z251(251) / Z251(1), Z251(0))
        self.assertEqual(Z251(2) / Z251(1), Z251(2))
        self.assertEqual(Z251(300) / Z251(2), Z251(150))
        self.assertEqual(Z251(252) / Z251(252), Z251(1))


    def test_equality(self):
        self.assertEqual(Z251(0) == Z251(0), True)  
        self.assertEqual(Z251(251) == Z251(0), True)  
        self.assertEqual(Z251(0) == Z251(251), True)  
        self.assertEqual(Z251(251) == Z251(251), True) 
        self.assertEqual(Z251(0) == Z251(1), False)
        self.assertEqual(Z251(252) == Z251(1), True)

if __name__ == '__main__':
    unittest.main()