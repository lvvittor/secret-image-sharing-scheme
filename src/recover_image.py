import random
from src.bmp_file import BMPFile
from src.polynomial import Polynomial
from src.z251 import Z251
import numpy as np
from typing import List, Tuple

class RecoverImage:
    def __init__(self, shadows: list[BMPFile], k, shadow_length):
        self.shadows = shadows
        self.shadows_amount = len(shadows)
        if self.shadows_amount < k:
            raise ValueError(f"Invalid k value: {k}. At least {k} shadows are required")
        self.block_size = 2 * k - 2
        self.secret_length = shadow_length
        self.blocks_amount = self.secret_length // self.block_size
        
        print("K")
        print(k)
        print("BLOCK SIZE")
        print(self.block_size)
        print("SHADOW LENGTH")
        print(shadow_length)
        print("SECRET LENGTH")
        print(self.secret_length)
        print("BLOCKS AMOUNT")
        print(self.blocks_amount)

    # Input k shadows, without loss of generality (S1, S2, ..., Sk)
    def recover(self):
        secret_data = []

        # Extract vi,j = (mi,j, di,j), i = 1,2,...,t, j = 1,2,...,k from S1, S2, ..., Sk
        mij = []
        dij = []
        ids = []
        for shadow in self.shadows:
            mi = []
            di = []
            for i in range(0, self.shadows_amount):
                mi.append(shadow.image_data[i])
                di.append(shadow.image_data[i + 1])
            mij.append(mi)
            dij.append(di)
            ids.append(shadow.header['reserved1'])
            
        # For each group of vi,1, vi,2, ..., vi,k, i = 1,2,...,t, reconstruct fi(x) and gi(x)
        # from mi,1, mi,2, ..., mi,k and di,1, di,2, ..., di,k using Lagrange interpolation+

        for block in range(0, self.blocks_amount):
            fi_points: List[Tuple[Z251, Z251]] = [(id, m[block]) for id, m in zip(ids, mij)]
            gi_points: List[Tuple[Z251, Z251]] = [(id, d[block]) for id, d in zip(ids, dij)]

            print("FI POINTS")
            print(fi_points)

            fi = Polynomial(points=fi_points)
            gi = Polynomial(points=gi_points)

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
            bi = fi.coefficients[:self.shadows_amount] + gi.coefficients[2:self.shadows_amount]

            # Append the recovered block to the secret image
            secret_data.extend(bi)

        # Copy the header from the first shadow
        secret_header = self.shadows[0].header
        secret_matrix = np.reshape(secret_data, (secret_header['height'], secret_header['width']))
        secret_image = BMPFile(header=secret_header, image_data=secret_matrix)
        
        return secret_image
    
    def is_cheating(self, a0, a1, b0, b1):
        for r in range(1, 251):
            if r * a0 + b0 == Z251(0) and r * a1 + b1 == Z251(0):
                return False
        return True