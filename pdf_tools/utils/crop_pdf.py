import fitz  # PyMuPDF

def crop_pdf(input_path, output_path, left, right, top, bottom):
    """
    Crop PDF by margins (points)
    """
    doc = fitz.open(input_path)

    for page in doc:
        rect = page.rect
        new_rect = fitz.Rect(
            rect.x0 + left,
            rect.y0 + top,
            rect.x1 - right,
            rect.y1 - bottom
        )
        page.set_cropbox(new_rect)

    doc.save(output_path)
    doc.close()
