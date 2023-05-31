#!/usr/bin/env python

import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def distribute_image(
    secret_image: str = typer.Argumen(..., help="Name of the secret image file (.bmp)"),
    k: int = typer.Argument(
        ..., help="Minimum number of shadows to recover the secret in a (k, n) scheme"
    ),
    directory: str = typer.Argument(
        ..., help="Directory containing the images to distribute the secret into (.bmp)"
    ),
):
    # Verify existence of the secret image
    secret_image_path = Path(secret_image)
    if not secret_image_path.is_file() or secret_image_path.suffix.lower() != ".bmp":
        typer.echo(
            "Error: The secret image does not exist or does not have a .bmp extension"
        )
        return

    # Verify existence of the directory and count images
    directory_path = Path(directory)
    if not directory_path.is_dir():
        typer.echo("Error: The directory does not exist")
        return

    images = list(directory_path.glob("*.bmp"))
    if len(images) < k:
        typer.echo(f"Error: At least {k} images are required in the directory")
        return

    # Perform distribution of the secret image
    typer.echo(
        f"Distributing the secret image '{secret_image}' into {len(images)} images"
    )

    # Add your logic here to distribute the secret image into the images in the directory


@app.command()
def recover_image(
    secret_image: str = typer.Argument(
        ..., help="Name of the output secret image file (.bmp)"
    ),
    k: int = typer.Argument(
        ..., help="Minimum number of shadows to recover the secret in a (k, n) scheme"
    ),
    directory: str = typer.Argument(
        ..., help="Directory containing the images with the hidden secret (.bmp)"
    ),
):
    # Verify existence of the directory and count images
    directory_path = Path(directory)
    if not directory_path.is_dir():
        typer.echo("Error: The directory does not exist")
        return

    images = list(directory_path.glob("*.bmp"))
    if len(images) < k:
        typer.echo(f"Error: At least {k} images are required in the directory")
        return

    # Perform recovery of the secret image
    typer.echo(
        f"Recovering the secret image '{secret_image}' from {len(images)} images"
    )
    # Add your logic here to recover the secret image from the images in the directory


@app.command()
def main(
    operation: str = typer.Argument(
        ..., help="Operation to perform ('d' for distribute, 'r' for recover)"
    ),
    secret_image: str = typer.Argument(
        ..., help="Name of the secret image file (.bmp)"
    ),
    k: int = typer.Argument(
        ..., help="Minimum number of shadows to recover the secret in a (k, n) scheme"
    ),
    directory: str = typer.Argument(..., help="Directory containing the images (.bmp)"),
):
    match operation:
        case "d":
            distribute_image(secret_image, k, directory)
        case "r":
            recover_image(secret_image, k, directory)
        case _:
            typer.echo("Error: Invalid operation (must be 'd' or 'r')")


if __name__ == "__main__":
    app()
