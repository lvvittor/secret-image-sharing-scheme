import unittest, os
from pathlib import Path
from src.distribute_image import DistributeImage


class DistributeImageTests(unittest.TestCase):
    folder_path = Path("images/shares")

    def setUp(self):
        """Get the list of BMP files in the test/images folder"""
        self.bmp_files = [file for file in os.listdir(DistributeImageTests.folder_path) if file.endswith(".bmp")]


    def test_generate_shadows(self):
        
        # Create an instance of DistributeImage with the secret image
        distribute_image = DistributeImage("images/shares/Gustavoshare.bmp", k=4, images=3)
        
        # Generate shadows
        shadows = distribute_image.generate_shadows()
        print(f"Shadows: {shadows}")
        print("-----------------------------\n")
        
        # Verify that the shadows are generated correctly
        self.assertEqual(len(shadows), 2)  # Assuming the secret image can be divided into 2 blocks of size 2k-2
        self.assertEqual(len(shadows[0]), 6)  # Assuming 3 images/participants
        
        # Add more assertions to check the properties of the generated shadows
    @unittest.skip("Skipping this test for a reason.")    
    def test_lsb_hide(self):
        
        # Create an instance of DistributeImage with the secret image
        distribute_image = DistributeImage("test/images/gustavo-share.bmp", k=4, n=3)
        
        # Generate shadows
        shadows = distribute_image.generate_shadows()
        
        # Create test images
        images = [b"\x00\x00\x00", b"\xFF\xFF\xFF", b"\x55\xAA\x55"]
        
        # Hide the shadows in the images
        distribute_image.lsb_hide(shadows, images)
        
        # Verify that the shadows are hidden correctly
        # Add assertions to check if the LSB modification is done correctly
        
        # Add more assertions to check the properties of the modified images
        
# Run the tests
if __name__ == '__main__':
    unittest.main()
