import random
from src.bmp_file import BMPFile
from src.polynomial import Polynomial
from src.z251 import Z251
import numpy as np
from typing import List, Tuple

class RecoverImage:
    def __init__(self, shares: list[BMPFile], k, share_length):
        self.k = k
        self.shares_amount = len(shares)
        if self.shares_amount < self.k:
            raise ValueError(f"Invalid shares amount value: {self.shares_amount}. At least {self.k} shares are required")
        
        # pick k shadows randomly
        self.shares = random.sample(shares, self.k)

        self.block_size = 2 * self.k - 2
        self.secret_length = share_length
        self.blocks_amount = self.secret_length // self.block_size

        self.shadow_length = self.secret_length // (self.k - 1)

        print(f"TOTAL {self.shares_amount} SHARES")
        print(f"K: {self.k}")
        print(f"BLOCK SIZE: {self.block_size}")
        print(f"SECRET LENGTH: {self.secret_length}")
        print(f"BLOCKS AMOUNT: {self.blocks_amount}")
        print(f"SHADOW LENGTH: {self.shadow_length}")

    # Input k shadows, without loss of generality (S1, S2, ..., Sk)
    def recover(self):
        secret_data = []
        ids = []

        shadows = []
        mask = self.lsb_mask(self.k)

        print(f"MASK: {mask}")

        # Reconstruct the shadows
        for share in self.shares:
            image_array = [byte for row in share.image_data for byte in row]
            shadow = 0
            for i in range(0, self.shadow_length * 4):
                share_byte = int.from_bytes(image_array[i], byteorder='little')
                shadow_bits = share_byte & mask
                shadow = shadow << 2
                shadow = shadow | shadow_bits
            shadow_bytearray = shadow.to_bytes((shadow.bit_length() + 7) // 8, 'big')
            print(f"BYTEARRAY LENGTH: {len(shadow_bytearray)}")
            shadows.append(shadow_bytearray)
            ids.append(Z251(share.header['reserved1']))

        # Extract vi,j = (mi,j, di,j), i = 1, 2, ..., t, j = 1, 2, ..., k from S1, S2, ..., Sk
        # For each group of vi,1, vi,2, ..., vi,k, i = 1,2,...,t, reconstruct fi(x) and gi(x)
        # from mi,1, mi,2, ..., mi,k and di,1, di,2, ..., di,k using Lagrange interpolation+

        for block in range(0, self.blocks_amount, 2): # BLOCKS AMOUNT 11250 
            fi_points = []
            gi_points = []

            for i in range(0, self.k): # BYTEARRAY 5625
                # print(f"BLOCK: {block} - SHARE: {i}")
                mik: Tuple[Z251, Z251] = (ids[i], Z251(shadows[i][block]))
                dik: Tuple[Z251, Z251] = (ids[i], Z251(shadows[i][block + 1]))
                fi_points.append(mik)
                gi_points.append(dik)

            fi = Polynomial.interpolate(points=fi_points)
            gi = Polynomial.interpolate(points=gi_points)

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
            secret_data.extend(bi)
        
        # Copy the header from the first shadow
        print(f"SECRET DATA: {len(secret_data)}")
        secret_header = self.shares[0].header
        secret_matrix = np.reshape(secret_data, (secret_header['height'], secret_header['width']))
        secret_image = BMPFile(header=secret_header, image_data=secret_matrix)
        
        return secret_image
    
    def is_cheating(self, a0, a1, b0, b1):
        for r in range(0, 251):
            if r * a0 + b0 == Z251(0) and r * a1 + b1 == Z251(0):
                return False
        return True
    
    def lsb_mask(self, k):
        # If k is 3 or 4, get the 4 least significant bits, otherwise get the 2 least significant bits
        return 0b1111 if k < 5 else 0b11