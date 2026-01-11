import fitz  # PyMuPDF
from PIL import Image
import os

def sign_pdf(
    input_pdf_path,
    output_pdf_path,
    text=None,
    image_path=None,
    page_number=1,
    x=100,
    y=100,
    font_size=14
):
    """
    Adds a visual signature (text or image) to a PDF page.
    Coordinates are in points (72 points = 1 inch).
    page_number is 1-based.
    """

    doc = fitz.open(input_pdf_path)
    page_index = max(0, page_number - 1)

    if page_index >= doc.page_count:
        raise ValueError("Invalid page number")

    page = doc[page_index]

    # ---- TEXT SIGNATURE ----
    if text:
        page.insert_text(
            (x, y),
            text,
            fontsize=font_size,
            fontname="helv",
            color=(0, 0, 0)
        )

    # ---- IMAGE SIGNATURE ----
    if image_path:
        img = Image.open(image_path)
        width, height = img.size

        rect = fitz.Rect(
            x,
            y,
            x + width * 0.5,
            y + height * 0.5
        )
        page.insert_image(rect, filename=image_path)

    doc.save(output_pdf_path)
    doc.close()

    return output_pdf_path
