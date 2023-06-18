import os
import random

class BMPFile:
    HEADER_BYTES = 54
    BITS_PER_BYTE = 8
    ROW_ALIGNMENT = 4

    def __init__(self, file_path=None, header=None, image_data=None):
        if file_path and not header and not image_data:
            self.file_path = file_path
            self.header = {}
            self.image_data = []
            self.read_header()
            self.read_image_data()
        elif header and image_data and not file_path:
            self.header = header
            self.image_data = image_data
        else:
            raise ValueError("Invalid arguments")

    @property
    def total_pixels(self):
        return self.header['width'] * self.header['height']
    
    @property
    def total_bits(self):
        return self.total_pixels * self.header['bits_per_pixel']
    
    @property
    def total_bytes(self):
        return self.total_bits // BMPFile.BITS_PER_BYTE
    
    @property
    def is_square(self):
        return self.header['width'] == self.header['height']
    
    
    def is_dibisible_by(self, n: int):
        """Returns True if the total number of pixels is divisible by n, False otherwise
        
        
        Arguments:
            n {int} -- Number to check divisibility with. n = 2k - 2, where k is the number of blocks to be used in the scheme
            
        """
        return self.total_pixels % n == 0

    # TODO: this function will create a
    def create_image(self, noisy_image):
        """
        Arguments:
        noisy_image {int} -- Number of participant image

        """
        pass

    def read_header(self):
        with open(self.file_path, 'rb') as file:
            # Read the first 54 bytes corresponding to the header
            header_data = file.read(BMPFile.HEADER_BYTES)

            # Get the header data
            self.header['signature'] = header_data[:2].decode('utf-8')
            self.header['file_size'] = int.from_bytes(header_data[2:6], 'little')
            self.header['reserved1'] = int.from_bytes(header_data[6:8], 'little')
            self.header['reserved2'] = int.from_bytes(header_data[8:10], 'little')
            self.header['data_offset'] = int.from_bytes(header_data[10:14], 'little')
            self.header['header_size'] = int.from_bytes(header_data[14:18], 'little')
            self.header['width'] = int.from_bytes(header_data[18:22], 'little')
            self.header['height'] = int.from_bytes(header_data[22:26], 'little')
            self.header['planes'] = int.from_bytes(header_data[26:28], 'little')
            self.header['bits_per_pixel'] = int.from_bytes(header_data[28:30], 'little')
            self.header['compression'] = int.from_bytes(header_data[30:34], 'little')
            self.header['image_size'] = int.from_bytes(header_data[34:38], 'little')
            self.header['x_pixels_per_meter'] = int.from_bytes(header_data[38:42], 'little')
            self.header['y_pixels_per_meter'] = int.from_bytes(header_data[42:46], 'little')
            self.header['total_colors'] = int.from_bytes(header_data[46:50], 'little')
            self.header['important_colors'] = int.from_bytes(header_data[50:54], 'little')


    def read_image_data(self):
        with open(self.file_path, 'rb') as file:
            # Skip the first 54 bytes corresponding to the header
            file.seek(self.header['data_offset'])

            # Calculate the padding for each row to ensure it is a multiple of ROW_ALIGNMENT bytes
            bits_per_pixel = self.header['bits_per_pixel']
            bytes_per_pixel = bits_per_pixel // BMPFile.BITS_PER_BYTE
            row_padding = (BMPFile.ROW_ALIGNMENT - (self.header['width'] * bytes_per_pixel) % BMPFile.ROW_ALIGNMENT) % BMPFile.ROW_ALIGNMENT

            # Iterate over each row of pixels
            for _ in range(self.header['height']):
                row_data = []

                # Iterate over each pixel in the row
                for _ in range(self.header['width']):
                    # Read the pixel data corresponding to the bits per pixel size
                    pixel_data = file.read(bytes_per_pixel)
                    row_data.append(pixel_data)

                # Skip the row padding, if present
                file.seek(row_padding, 1)

                # Add the row pixel data to the image data list
                self.image_data.append(row_data)

    def print_header_info(self):
        print("Header Info:")
        print("Signature:", self.header['signature'])
        print("File Size:", self.header['file_size'])
        print("Reserved 1:", self.header['reserved1'])
        print("Reserved 2:", self.header['reserved2'])
        print("Data Offset:", self.header['data_offset'])
        print("Header Size:", self.header['header_size'])
        print("Width:", self.header['width'])
        print("Height:", self.header['height'])
        print("Planes:", self.header['planes'])
        print("Bits per Pixel:", self.header['bits_per_pixel'])
        print("Compression:", self.header['compression'])
        print("Image Size:", self.header['image_size'])
        print("X Pixels per Meter:", self.header['x_pixels_per_meter'])
        print("Y Pixels per Meter:", self.header['y_pixels_per_meter'])
        print("Total Colors:", self.header['total_colors'])
        print("Important Colors:", self.header['important_colors'])

    def print_image_data(self):
        print("Image Data:")
        for row in self.image_data:
            for pixel_data in row:
                print(pixel_data)
            print()

    def lsb_hide(self, secret_data, n_bits):
        """Hide the secret data in the least significant bits of the image data
        
        Arguments:
            secret_data {bytes} -- Secret data to hide in the image data
            n_bits {int} -- Number of least significant bits to use for hiding the secret data

        Raises:
            ValueError: If the secret data is too large to be hidden in the image data
        """
        max_secret_size = (self.total_pixels * n_bits) // BMPFile.BITS_PER_BYTE

        if len(secret_data) > max_secret_size:
            raise ValueError(f"Secret data is too large to be hidden in the image data. Maximum size: {max_secret_size} bytes")
        
        bits_to_keep = self.header['bits_per_pixel'] - n_bits

        # Create a binary string representation of the secret data
        # Example: 
        # If secret_data is b'AB', the resulting secret_bin would be '0100000101000010'
        secret_bin = ''.join(format(byte, '08b') for byte in secret_data)

        secret_index = 0

        # Iterate over each row of pixels
        for row_index, row in enumerate(self.image_data):
            # Iterate over each pixel in the row
            for pixel_index, pixel_data in enumerate(row):
                # Get the pixel data as an integer
                pixel_value = int.from_bytes(pixel_data, 'little')

                # Calculate the number of bits to shift the secret data to the right
                shift_bits = bits_to_keep * (pixel_index % (self.header['bits_per_pixel'] // n_bits))

                # Extract the bits from the secret data
                secret_bits = secret_bin[secret_index:secret_index + n_bits]

                # Shift the secret bits to the left
                secret_value = int(secret_bits, 2) << shift_bits

                # Clear the bits to be replaced in the pixel data
                pixel_value &= ~(2 ** bits_to_keep - 1) << shift_bits

                # Set the bits from the secret data in the pixel data
                pixel_value |= secret_value

                # Set the modified pixel data
                self.image_data[row_index][pixel_index] = pixel_value.to_bytes(self.header['bits_per_pixel'] // BMPFile.BITS_PER_BYTE, 'little')

                secret_index += n_bits

    def lsb_recover(self, n_bits):
        """Recover the secret data from the least significant bits of the image data
        
        Arguments:
            n_bits {int} -- Number of least significant bits used for hiding the secret data
        
        Returns:
            bytes -- Recovered secret data
        """
        # Calculate the number of bits to keep
        bits_to_keep = self.header['bits_per_pixel'] - n_bits

        secret_data = bytearray()
        secret_bin = ""

        # Iterate over each row of pixels
        for _, row in enumerate(self.image_data):
            # Iterate over each pixel in the row
            for pixel_index, pixel_data in enumerate(row):
                # Get the pixel data as an integer
                pixel_value = int.from_bytes(pixel_data, 'little')

                # Calculate the number of bits to shift the secret data to the right
                shift_bits = bits_to_keep * (pixel_index % (self.header['bits_per_pixel'] // n_bits))

                # Extract the secret bits from the pixel data
                secret_bits = (pixel_value >> shift_bits) & ((2 ** n_bits) - 1)

                # Add the extracted secret bits to the secret binary string
                secret_bin += format(secret_bits, f'0{n_bits}b')

                # While the secret binary string has enough bits, extract a byte and add it to the secret data
                while len(secret_bin) >= 8:
                    secret_byte = int(secret_bin[:8], 2)
                    secret_data.append(secret_byte)
                    secret_bin = secret_bin[8:]

        return bytes(secret_data)
