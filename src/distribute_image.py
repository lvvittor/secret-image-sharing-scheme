from __future__ import annotations
import random
from src.polynomial import Polynomial
from src.bmp_file import BMPFile
from src.z251 import Z251
from src.utils import flatten_array

class DistributeImage:
    ALLOWED_K_VALUES = [3, 4, 5, 6, 7, 8]

    def __init__(self, secret_image: str, k: int, participants: list[BMPFile]):
        if k not in DistributeImage.ALLOWED_K_VALUES:
            raise ValueError(f"Invalid k value: {k}. Allowed values: {DistributeImage.ALLOWED_K_VALUES}")

        self.secret_image = BMPFile(file_path=secret_image)
        self.k = k
        self.participants = participants
        self.block_size = 2 * self.k - 2

        if not self.secret_image.is_dibisible_by(self.block_size):
            raise ValueError(f"Image size must be divisible by {self.block_size}")


    @property
    def ri(self):
        return random.randint(1, 251)
    
    @property
    def total_blocks(self):
        return self.secret_image.total_pixels // self.block_size
    
    def generate_shadows(self):
        shadows = []
        v_ij = {}

        # v_ij should be a dictionary with the following structure:
        # v_ij = {1: [f_1(j), g_1(j)], 2: [f_2(j), g_2(j)], ..., t: [f_t(j), g_t(j)]}
        for i in range(self.total_blocks):
            v_ij.update({i+1: []})

        image_array = [byte for row in self.secret_image.image_data for byte in row]
        # The dealer divides the image intro t-non-overlapping 2k - 2 pixel blocks
        # For each block Bi (i in [1, t]) there are 2k - 2 secret pixels
        # a_{i,0}, a_{i,1}, ..., a_{i,k-1} and b_{i,0}, b_{i,1}, ..., b_{i,k-1} in Z251
        for i in range(0, self.secret_image.total_pixels, self.block_size):
            # The dealer generates a k-1 degree polynomial fi(x) = a_{i,0} + a_{i,1}x + ... + a_{i,k-1}x^k-1 in Z251[x]
            fi = Polynomial(coefficients=[Z251(image_array[i + j]) for j in range(self.k - 1)])

            # The dealer chooses a random integer r_i and computes two pixels b_{i,0} and b_{i,1} which satisfy that:
            # r_i*a_{i,0} + b_{i,0} = 0 (mod 251) and r_i*a_{i,1} + b_{i,1} = 0 (mod 251)
            # and then generates another k-1 degree polynomial g_i(x) = b_{i,0} + b_{i,1}x + ... + b_{i,k-1}x^k-1 in Z251[x]

            ri = self.ri

            # a_0 and a_1 cant be 0, otherwise they are computed as 1
            a0 = image_array[i] if image_array[i] != 0 else 1
            a1 = image_array[i + 1] if image_array[i + 1] != 0 else 1

            b0 = Z251(ri * a0 * -1)
            b1 = Z251(ri * a1 * -1)

            gi = Polynomial(coefficients=[Z251(image_array[i + self.k - 1 + j]) for j in range(self.k - 1)])

            gi.set_coefficient(0, b0)
            gi.set_coefficient(1, b1)

            dict_idx = i // self.block_size + 1
            v_ij[dict_idx].append(fi)
            v_ij[dict_idx].append(gi)

        # For each block B_i (i in [1, t]) the dealer computes sub-shadow
        # v_{i,j} = (m_{i,j}; d_{i,j}) with: m_{i,j} = fi(j) and d_{i,j} = g_i(j) for j in [1, n] for each participant P_j
        # the shadow S_j for P_j is S_j = (v_{1,j}, v_{2,j}, ..., v_{t,j})
        for i in range(len(self.participants)):
            pratial_shadows = []
            for j in range(self.total_blocks):
                m_ij = v_ij[j+1][0].evaluate(i+1)
                d_ij = v_ij[j+1][1].evaluate(i+1)
                pratial_shadows.append(m_ij)
                pratial_shadows.append(d_ij)
            shadows.append(pratial_shadows)
        self.lsb_hide(shadows, self.participants)
        return shadows

    # TODO: check if bits modification is being done correctly
    def lsb_hide(self, shadows, images):
        mask = self.lsb_mask(self.k) # determine whether LSB2 or LSB4 should be used

        for i, shadow in enumerate(shadows):
            # Get the i-th BMPFile from images
            image = images[i]

            # Set header value to the number of shadow we are going to mix in this participants
            image.header['reserved1'] = i.to_bytes(1, byteorder='little')

            image_bytes = flatten_array(image.image_data)

            # TODO: check if this actually works -> fixed in bmp.file with line file.seek(self.header['data_offset'])
            # byte_number = 54
            # byte_position = byte_number % len(image_bytes)
            # initial_offset = image.header["data_offset"] # previously, this variable was set to: byte_position if byte_position >= 54 else 0

            for j, byte in enumerate(shadow):
                # Modify the LSB4 bits of the corresponding byte in the image.
                image_byte = int.from_bytes(image_bytes[j], byteorder='little', signed=False)

                image_bytes[j] = ((image_byte & mask[0]) | (byte.value & mask[1])).to_bytes(1, byteorder='little')

            # Update image to modified image
            images[i].image_data = image_bytes

    def lsb_mask(self, k):
        # If k is 3 or 4, the dealer hides the secret image in LSB4
        return (0xFC, 0x03) if k not in [3, 4] else (0xF0, 0x0F)

