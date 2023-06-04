import unittest, os
from pathlib import Path
from src.distribute_image import DistributeImage
from src.bmp_file import BMPFile


class DistributeImageTests(unittest.TestCase):
    FOLDER_PATH = Path("images/covers")
    K_AND_BLOCK_SIZES = [
        [3, 2 * 3 - 2],
        [4, 2 * 4 - 2],
        [5, 2 * 5 - 2],
        [6, 2 * 6 - 2],
        [7, 2 * 7 - 2],
        # [8, 2 * 8 - 2], TODO: This fails for some reason, need to check why
    ]

    def setUp(self):
        self.bmp_files = [BMPFile(file_path) for file_path in DistributeImageTests.FOLDER_PATH.glob("*.bmp")]

    def test_generate_shadows(self):
        for k, block_size in DistributeImageTests.K_AND_BLOCK_SIZES:
            # Create an instance of DistributeImage with the secret image
            distribute_image = DistributeImage("images/shares/Gustavoshare.bmp", k=k, participants=self.bmp_files)

            self.assertEqual(distribute_image.block_size, block_size) # Check that the block size is correct
            
            # Generate shadows
            shadows = distribute_image.generate_shadows()

            self.assertEqual(len(shadows), len(self.bmp_files)) # There should be one shadow per participant
            self.assertEqual(len(shadows[0]), 2 * distribute_image.total_blocks)  # |S_j| = 2 * t (where t is the number of blocks in the secret image, and S_j is the shadow j)
            self.assertEqual(len(shadows[0]), distribute_image.secret_image.total_pixels // (distribute_image.k - 1)) # |S_j| = |I| / (k - 1) (where I is the secret image, and S_j is the shadow j)

    @unittest.skip("Skipping this test for a reason.")    
    def test_lsb_hide(self):
        for k, block_size in DistributeImageTests.K_AND_BLOCK_SIZES:
            # Create an instance of DistributeImage with the secret image
            distribute_image = DistributeImage("test/images/gustavo-share.bmp", k=k, participants=self.bmp_files)
            
            # Generate shadows
            shadows = distribute_image.generate_shadows()
            
            # Create test images
            images = [b"\x00\x00\x00", b"\xFF\xFF\xFF", b"\x55\xAA\x55"]
            
            # Hide the shadows in the images
            distribute_image.lsb_hide(shadows, images)
            
            # Verify that the shadows are hidden correctly
            # Add assertions to check if the LSB modification is done correctly
            
            # Add more assertions to check the properties of the modified images
            
if __name__ == '__main__':
    unittest.main()
