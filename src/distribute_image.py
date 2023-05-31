import random

class DistributeImage:
    ALLOWED_K_VALUES = [3, 4, 5, 6, 7, 8]

    def __init__(self, secret_image, k, images):
        if k not in DistributeImage.ALLOWED_K_VALUES:
            raise ValueError(f"Invalid k value: {k}. Allowed values: {DistributeImage.ALLOWED_K_VALUES}")

        self.secret_image = secret_image
        self.k = k
        self.images = images

    @property
    def ri(self):
        """Random integer between 1 and 251"""
        return random.randint(1, 251)
    

    def distribute(self):
        # do something
        return self.image