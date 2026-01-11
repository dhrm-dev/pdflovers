from PIL import Image
import os

def convert_jpg_to_pdf(image_paths, output_pdf):
    images = []

    for path in image_paths:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if not images:
        raise ValueError("No images provided")

    images[0].save(
        output_pdf,
        save_all=True,
        append_images=images[1:]
    )
