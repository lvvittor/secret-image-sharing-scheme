import os
import unittest
from pathlib import Path
from src.bmp_file import BMPFile

class BMPFileTestCase(unittest.TestCase):
    folder_path = Path("images/shares")

    def setUp(self):
        """Get the list of BMP files"""
        self.bmp_files = [file for file in os.listdir(BMPFileTestCase.folder_path) if file.endswith(".bmp")]

    def test_header_info(self):
        for file_name in self.bmp_files:
            file_path = Path(BMPFileTestCase.folder_path) / file_name
            bmp = BMPFile(file_path)

            self.assertEqual(bmp.header['signature'], 'BM')
            self.assertEqual(bmp.header['file_size'], os.path.getsize(file_path))
            # self.assertEqual(bmp.header['reserved1'], 3)
            self.assertEqual(bmp.header['reserved2'], 0)
            self.assertEqual(bmp.header['data_offset'], 1078)
            self.assertEqual(bmp.header['header_size'], 40)
            self.assertEqual(bmp.header['width'], 300)
            self.assertEqual(bmp.header['height'], 300)
            self.assertEqual(bmp.header['planes'], 1)
            self.assertEqual(bmp.header['bits_per_pixel'], 8)
            self.assertEqual(bmp.header['compression'], 0)
            self.assertEqual(bmp.header['image_size'], 90000)
            # self.assertEqual(bmp.header['x_pixels_per_meter'], 3780)
            # self.assertEqual(bmp.header['y_pixels_per_meter'], 3780)
            # self.assertEqual(bmp.header['total_colors'], 0)
            self.assertEqual(bmp.header['important_colors'], 0)

    def test_image_data(self):
        for file_name in self.bmp_files:
            file_path = Path(BMPFileTestCase.folder_path) / file_name
            bmp = BMPFile(file_path)
            image_data = bmp.image_data

            # Check that the length of the image data matches the image size
            self.assertEqual(len(image_data), 300)
            self.assertEqual(len(image_data[0]), 300)

            # Check that the image data is a list of lists of bytes
            self.assertIsInstance(image_data, list) # Check that the image data is a list of rows
            self.assertIsInstance(image_data[0], list) # Check that the first row is a list of pixels
            self.assertIsInstance(image_data[0][0], bytes) # Check that the first pixel is a byte        

    def test_total_pixels(self):
        for file_name in self.bmp_files:
            file_path = Path(BMPFileTestCase.folder_path) / file_name
            bmp = BMPFile(file_path)
            total_pixels = bmp.total_pixels

            # Check that the total number of pixels is equal to width x height
            self.assertEqual(total_pixels, 300 * 300)    

    def test_total_bits(self):
        for file_name in self.bmp_files:
            file_path = Path(BMPFileTestCase.folder_path) / file_name
            bmp = BMPFile(file_path)
            total_bits = bmp.total_bits

            # Check that the total number of bits is equal to pixels x bits per pixel
            self.assertEqual(total_bits, 300 * 300 * bmp.header['bits_per_pixel'])

    def test_is_divisible_by(self):
        for file_name in self.bmp_files:
            file_path = Path(BMPFileTestCase.folder_path) / file_name
            bmp = BMPFile(file_path)

            # Check that the image size is divisible by 2k - 2
            self.assertTrue(bmp.is_dibisible_by(2 * 3 - 2))
            self.assertTrue(bmp.is_dibisible_by(2 * 4 - 2))
            self.assertTrue(bmp.is_dibisible_by(2 * 5 - 2))
            self.assertTrue(bmp.is_dibisible_by(2 * 6 - 2))
            self.assertTrue(bmp.is_dibisible_by(2 * 7 - 2))

if __name__ == '__main__':
    unittest.main()
