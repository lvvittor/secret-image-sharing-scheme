import os
import random
import struct

class BMPFile:
    HEADER_BYTES = 54
    BITS_PER_BYTE = 8
    ROW_ALIGNMENT = 4

    def __init__(self, file_path=None, header=None, image_data=None):
        if file_path and not header and not image_data:
            self.file_path = file_path
            self.header = {}
            self.header_size = {}
            self.image_data = []
            self.set_header_size()
            self.read_header()
            self.read_image_data()
        elif header is not None and image_data is not None:
            self.header_size = {}
            self.set_header_size()
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
    def bytes_per_pixel(self):
        return self.header['bits_per_pixel'] // BMPFile.BITS_PER_BYTE
    
    @property
    def total_bytes(self):
        return self.total_bits // BMPFile.BITS_PER_BYTE
    
    @property
    def is_square(self):
        return self.header['width'] == self.header['height']
    
    @property
    def row_padding(self):
        """
        Calculate the padding for each row to ensure it is a multiple of ROW_ALIGNMENT bytes
        
        Returns:
            int -- Number of bytes to pad each row ((4 - (300 * 1) % 4) % 4 = 0)
        """
        return (BMPFile.ROW_ALIGNMENT - (self.header['width'] * self.bytes_per_pixel) % BMPFile.ROW_ALIGNMENT) % BMPFile.ROW_ALIGNMENT

    def is_dibisible_by(self, n: int):
        """Returns True if the total number of pixels is divisible by n, False otherwise
        
        
        Arguments:
            n {int} -- Number to check divisibility with. n = 2k - 2, where k is the number of blocks to be used in the scheme
            
        """
        return self.total_pixels % n == 0

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

    def set_header_size(self):
        self.header_size['signature'] = 2
        self.header_size['file_size'] = 4
        self.header_size['reserved1'] = 2
        self.header_size['reserved2'] = 2
        self.header_size['data_offset'] = 4
        self.header_size['header_size'] = 4
        self.header_size['width'] = 4
        self.header_size['height'] = 4
        self.header_size['planes'] = 2
        self.header_size['bits_per_pixel'] = 2
        self.header_size['compression'] = 4
        self.header_size['image_size'] = 4
        self.header_size['x_pixels_per_meter'] = 4
        self.header_size['y_pixels_per_meter'] = 4
        self.header_size['total_colors'] = 4
        self.header_size['important_colors'] = 4

    def read_image_data(self):
        with open(self.file_path, 'rb') as file:
            # Skip the first bytes corresponding to the header
            file.seek(self.header['data_offset'])

            # Iterate over each row of pixels
            for _ in range(self.header['height']):
                row_data = []

                # Iterate over each pixel in the row
                for _ in range(self.header['width']):
                    # Read the pixel data corresponding to the bits per pixel size
                    pixel_data = file.read(self.bytes_per_pixel)
                    row_data.append(pixel_data)

                # Skip the row padding, if present
                file.seek(self.row_padding, 1)

                # Add the row pixel data to the image data list
                self.image_data.append(row_data)

    def print_header_info(self):
        print("[Header Info]")
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

    def save(self, file_path):
        """Save the image data as a BMP file
        
        Arguments:
            file_path {str} -- File path to save the BMP file
        """
        flatten_array = []
        for row in self.image_data:
            for pixel in row:
                flatten_array.append(pixel)

        with open(file_path, 'w+b') as file:
            file.seek(0)
            for key, value in self.header.items():
                if key == 'signature':
                    file.write(value.encode('utf-8'))
                else:
                    file.write(value.to_bytes(self.header_size[key], 'little'))

            # this is in order to copy what other bmp files
            # had between the header and the data
            zero = 0
            count = 0
            for _ in range(BMPFile.HEADER_BYTES, self.header['data_offset']):
                file.write(zero.to_bytes(1, 'little'))
                count += 1
                if count == 4:
                    count = 0
                    zero += 1

            for column in range(self.header['height']):
                for row in range(self.header['width']):
                    file.write(flatten_array[column * self.header['width'] + row])

    def get_header_data(self):
        """Get the header data as bytes
        
        Returns:
            bytes -- Header data
        """
        header_data = [
            self.header['signature'].encode('utf-8'),
            struct.pack('<I', self.header['file_size']),
            struct.pack('<H', self.header['reserved1']),
            struct.pack('<H', self.header['reserved2']),
            struct.pack('<I', self.header['data_offset']),
            struct.pack('<I', self.header['header_size']),
            struct.pack('<I', self.header['width']),
            struct.pack('<I', self.header['height']),
            struct.pack('<H', self.header['planes']),
            struct.pack('<H', self.header['bits_per_pixel']),
            struct.pack('<I', self.header['compression']),
            struct.pack('<I', self.header['image_size']),
            struct.pack('<I', self.header['x_pixels_per_meter']),
            struct.pack('<I', self.header['y_pixels_per_meter']),
            struct.pack('<I', self.header['total_colors']),
            struct.pack('<I', self.header['important_colors']),
        ]

        return b''.join(header_data)