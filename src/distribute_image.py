import random
from src.polynomial import Polynomial
from src.bmp_file import BMPFile
from src.z251 import Z251

class DistributeImage:
    ALLOWED_K_VALUES = [3, 4, 5, 6, 7, 8]

    def __init__(self, secret_image, k, participants):
        if k not in DistributeImage.ALLOWED_K_VALUES:
            raise ValueError(f"Invalid k value: {k}. Allowed values: {DistributeImage.ALLOWED_K_VALUES}")

        self.secret_image = BMPFile(secret_image)
        self.k = k
        self.participants = participants

    @property
    def ri(self):
        """Random integer between 1 and 251"""
        return random.randint(1, 251)
    
    
    
    def generate_shadows(self):

        block_size = 2 * self.k - 2
        if not self.secret_image.is_dibisible_by(block_size):
            raise ValueError(f"Image size must be divisible by {block_size}")
        
        shadows = []
        image_array = [byte for row in self.secret_image.image_data for byte in row]
        # The dealer divides the image intro t-non-overlapping 2k - 2 pixel blocks
        # For each block Bi (i in [1, t]) there are 2k - 2 secret pixels
        # a_{i,0}, a_{i,1}, ..., a_{i,k-1} and b_{i,0}, b_{i,1}, ..., b_{i,k-1} in Z251
        for i in range(0, self.secret_image.total_pixels, block_size):
            # The dealer generates a k-1 degree polynomial fi(x) = a_{i,0} + a_{i,1}x + ... + a_{i,k-1}x^k-1 in Z251[x]
            fi = Polynomial(coefficients=[Z251(image_array[i + j]) for j in range(self.k - 1)])

            # The dealer chooses a random integer ri and computes two pixels b_{i,0} and b_{i,1} which satisfy that:
            # ri*a_{i,0} + b_{i,0} = 0 (mod 251) and ri*a_{i,1} + b_{i,1} = 0 (mod 251)
            # and then generates another k-1 degree polynomial gi(x) = b_{i,0} + b_{i,1}x + ... + b_{i,k-1}x^k-1 in Z251[x]

            ri = self.ri

            # a0 and a1 cant be 0, otherwise they are computed as 1
            a0 = image_array[i] if image_array[i] != 0 else 1
            a1 = image_array[i + 1] if image_array[i + 1] != 0 else 1

            b0 = Z251(ri * a0 * -1)
            b1 = Z251(ri * a1 * -1)

            gi = Polynomial(coefficients=[Z251(image_array[i + self.k - 1 + j]) for j in range(self.k - 1)])

            gi.set_coefficient(0, b0)
            gi.set_coefficient(1, b1)

            # For each block Bi (i in [1, t]) the dealer computes sub-shadow
            # v_{i,j} = (m_{i,j}; d_{i,j}) with: m_{i,j} = fi(j) and d_{i,j} = gi(j) for j in [1, n] for each participant Pj
            # the shadow Sj for Pj is Sj = (v_{1,j}, v_{2,j}, ..., v_{t,j})

            # TODO: refactor this, to actually generate the shadows
            shadow_image = []
            for j in range(self.participants):
                mi = fi.evaluate(j + 1)
                di = gi.evaluate(j + 1)
                shadow_image.append(mi)
                shadow_image.append(di)
            
            shadows.append(shadow_image)
        return shadows

    # TODO: check if bits modification is being done correctly
    def lsb_hide(self, shadows, images):
        mask = self.lsb_mask(self.k) # determine whether LSB2 or LSB4 should be used 

        for i, shadow in enumerate(shadows):
            image = images[i]

            shadow_bytes = bytearray(shadow)
            image_bytes = bytearray(image)

            for j, byte in enumerate(shadow_bytes):
                # Modify the LSB4 bits of the corresponding byte in the image
                image_bytes[j] = (image_bytes[j] & mask[0]) | (byte & mask[1])  
            # Update the modified image
            images[i] = bytes(image_bytes)

    def lsb_mask(self, k):
        # If k is 3 or 4, the dealer hides the secret image in LSB4
        return (0xFC, 0x03) if k not in [3, 4] else (0xF0, 0x0F)


