#!/usr/bin/env python

import argparse
from pathlib import Path
from src.distribute_image import DistributeImage
from src.recover_image import RecoverImage
from src.bmp_file import BMPFile

def distribute_image(
    secret_image: str,
    k: int,
    directory: str,
):
    # Verify existence of the secret image
    secret_image_path = Path(secret_image)
    if not secret_image_path.is_file() or secret_image_path.suffix.lower() != ".bmp":
        print(
            "Error: The secret image does not exist or does not have a .bmp extension"
        )
        return

    # Verify existence of the directory and count images
    directory_path = Path(directory)
    if not directory_path.is_dir():
        print("Error: The directory does not exist")
        return

    images = list(directory_path.glob("*.bmp"))
    if len(images) < k:
        print(f"Error: At least {k} images are required in the directory")
        return

    # Perform distribution of the secret image
    print(
        f"Distributing the secret image '{secret_image}' into {len(images)} images with path: {images}"
    )

    # Add your logic here to distribute the secret image into the images in the directory
    distribute_image = DistributeImage(secret_image, k, participants=[BMPFile(image) for image in images])
    distribute_image.generate_shadows()


def recover_image(
    secret_image: str,
    k: int,
    directory: str,
):
    # Verify existence of the directory and count images
    directory_path = Path(directory)
    if not directory_path.is_dir():
        print("Error: The directory does not exist")
        return

    images = list(directory_path.glob("*.bmp"))
    if len(images) < k:
        print(f"Error: At least {k} images are required in the directory")
        return

    # Perform recovery of the secret image
    print(
        f"Recovering the secret image '{secret_image}' from {len(images)} images"
    )
    # Add your logic here to recover the secret image from the images in the directory
    bmp_images = [BMPFile(image) for image in images]
    recover_image = RecoverImage(shares=bmp_images, k=k, share_length=bmp_images[0].total_pixels)
    recover_image.recover()


def main():
    parser = argparse.ArgumentParser(description="Distribute or recover secret images.")
    parser.add_argument(
        "operation",
        choices=["d", "r"],
        help="Operation to perform ('d' for distribute, 'r' for recover)",
    )
    parser.add_argument("secret_image", help="Name of the secret image file (.bmp)")
    parser.add_argument(
        "k", type=int, help="Minimum number of shadows to recover the secret in a (k, n) scheme"
    )
    parser.add_argument(
        "directory", help="Directory containing the images (.bmp)"
    )
    args = parser.parse_args()

    match args.operation:
        case "d":
            distribute_image(args.secret_image, args.k, args.directory)
        case "r":
            recover_image(args.secret_image, args.k, args.directory)
        case _:
            print("Error: Invalid operation (must be 'd' or 'r')")


if __name__ == "__main__":
    main()
