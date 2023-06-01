import random
from polynomial import Polynomial
from bmp_file import BMPFile
from z251 import Z251

class DistributeImage:
    ALLOWED_K_VALUES = [3, 4, 5, 6, 7, 8]

    def __init__(self, secret_image, k, images):
        if k not in DistributeImage.ALLOWED_K_VALUES:
            raise ValueError(f"Invalid k value: {k}. Allowed values: {DistributeImage.ALLOWED_K_VALUES}")

        self.secret_image = BMPFile(secret_image)
        self.secret_image.read_header()
        self.secret_image.read_image_data()

        self.k = k
        self.images = images

    @property
    def ri(self):
        """Random integer between 1 and 251"""
        return random.randint(1, 251)
    

    def distribute(self):
        # do something
        return self.image
    
    def generate_shadows(self):

        block_size = 2 * self.k - 2
        if not self.secret_image.is_dibisible_by(block_size):
            raise ValueError(f"Image size must be divisible by {block_size}")
        
        shadows = []

        # The dealer divides the image intro t-non-overlapping 2k - 2 pixel blocks
        # For each block Bi, i e [1, t] there are 2k - 2 secret pixels
        # ai,0, ai,1, ..., ai,k-1 and bi,0, bi,1, ..., bi,k-1 e Z251
        for i in range(0, self.secret_image.total_pixels, block_size):
            # The dealer generates a k-1 degree polynomial fi(x) = ai,0 + ai,1x + ... + ai,k-1x^k-1 e Z251[x]
            coefficients = [Z251(self.secret_image.image_data[i + j]) for j in range(self.k - 1)]
            fi = Polynomial(coefficients)

            # The dealer chooses a random integer ri and computes two pixels bi,0 and bi,1 which satisfy that
            # ri*ai,0 + bi,0 = 0 (mod 251) and ri*ai,1 + bi,1 = 0 (mod 251)
            # and then generates another k-1 degree polynomial gi(x) = bi,0 + bi,1x + ... + bi,k-1x^k-1 e Z251[x]

            ri = self.ri
            # a0 and a1 cant be 0, otherwise they are computed as 1
            a0 = self.secret_image.image_data[i] if self.secret_image.image_data[i] != 0 else 1
            a1 = self.secret_image.image_data[i + 1] if self.secret_image.image_data[i + 1] != 0 else 1

            b0 = Z251(ri * a0 * -1)
            b1 = Z251(ri * a1 * -1)

            coefficients = [Z251(self.secret_image.image_data[i + j + self.k - 1]) for j in range(self.k - 1)]
            gi = Polynomial(coefficients)

            gi.set_coefficient(0, b0)
            gi.set_coefficient(1, b1)

            # For each block Bi, i e [1, t] the dealer computes sub-shadow
            # vi,j = {mi,j; di,j}, mi,j = fi(j) and di,j = gi(j) for j e [1, n] for each participant Pj
            # the shadow Sj for Pj is Sj = {v1,j, v2,j, ..., vt,j}

            # self.images is the amount of participants
            shadow_image = []
            for j in range(self.images):
                mi = fi.evaluate(j + 1)
                di = gi.evaluate(j + 1)
                shadow_image.append(mi)
                shadow_image.append(di)
            
            shadows.append(shadow_image)
