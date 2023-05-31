class BMPFile:
    HEADER_BYTES = 54
    BITS_PER_BYTE = 8
    ROW_ALIGNMENT = 4

    def __init__(self, file_path):
        self.file_path = file_path
        self.header = {}
        self.image_data = []

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
            file.seek(BMPFile.HEADER_BYTES)

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

