from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(input_pdf_path, output_pdf_path, angle=90, pages=None):
    """
    Rotate PDF pages

    angle: 90, 180, 270
    pages: list of page numbers (1-based), None = all pages
    """

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    if pages:
        pages = [p - 1 for p in pages if 0 < p <= total_pages]

    for i, page in enumerate(reader.pages):
        if pages is None or i in pages:
            page.rotate(angle)
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    return output_pdf_path
