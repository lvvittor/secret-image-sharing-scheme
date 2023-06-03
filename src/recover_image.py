import random
from bmp_file import BMPFile
from polynomial import Polynomial
from z251 import Z251

class RecoverImage:
    def __init__(self, shadows: list[BMPFile]):
        self.shadows = shadows
        self.k = len(shadows)

    # Input k shadows, without loss of generality (S1, S2, ..., Sk)
    def recover(self):
        secret_image = []
        # Extract vi,j = (mi,j, di,j), i = 1,2,...,t, j = 1,2,...,k from S1, S2, ..., Sk
        for shadow in self.shadows:
            mij = []
            dij = []

            for i in range(0, self.k):
                mij = shadow.image_data[i]
                dij = shadow.image_data[i + 1]

            # For each group of vi,1, vi,2, ..., vi,k, i = 1,2,...,t, reconstruct fi(x) and gi(x)
            # from mi,1, mi,2, ..., mi,k and di,1, di,2, ..., di,k using Lagrange interpolation
            fi = Polynomial.interpolate(mij)
            gi = Polynomial.interpolate(dij)

            # Let ai,0, ai,1, bi,0 and bi,1 be the coefficients of x^0 and x^1 in fi(x) and gi(x) 
            a0 = fi.coefficients[0]
            a1 = fi.coefficients[1]
            b0 = gi.coefficients[0]
            b1 = gi.coefficients[1]

            # If there exists a common integer ri, which satisfies that riai,0 + bi,0 = 0 and riai,1 + bi,1 = 0
            # recover the 2k - 2 pixel block Bi = {ai,0, ai,1, ..., ai,k-1, bi,2, bi,3, ..., bi,k-1} 
            # then, the secret image I is I = B1 || B2 || ... || Bt
            # Else, there are fake shadows participating in the image reconstruction -> cheating is detected
            if self.is_cheating(a0, a1, b0, b1):
                print("Cheating detected!")
                return None
            
            # Recover the 2k - 2 pixel block Bi = {ai,0, ai,1, ..., ai,k-1, bi,2, bi,3, ..., bi,k-1}
            bi = fi.coefficients[:self.k] + gi.coefficients[2:self.k]

            # Append the recovered block to the secret image
            secret_image.append(bi)

        return secret_image
    
    def is_cheating(self, a0, a1, b0, b1):
        for r in range(1, 251):
            if r * a0 + b0 == Z251(0) and r * a1 + b1 == Z251(0):
                return False
        return True