import fitz  # PyMuPDF
from PIL import Image


def edit_pdf(
    input_pdf_path,
    output_pdf_path,
    page_number=1,
    text=None,
    x=100,
    y=100,
    font_size=14,
    image_path=None
):
    """
    Basic PDF editing:
    - Add text
    - Add image
    """

    doc = fitz.open(input_pdf_path)
    page_index = max(0, page_number - 1)

    if page_index >= doc.page_count:
        raise ValueError("Invalid page number")

    page = doc[page_index]

    # ---- ADD TEXT ----
    if text:
        page.insert_text(
            (x, y),
            text,
            fontsize=font_size,
            fontname="helv",
            color=(0, 0, 0)
        )

    # ---- ADD IMAGE ----
    if image_path:
        img = Image.open(image_path)
        w, h = img.size

        rect = fitz.Rect(x, y, x + w * 0.5, y + h * 0.5)
        page.insert_image(rect, filename=image_path)

    doc.save(output_pdf_path)
    doc.close()

    return output_pdf_path
