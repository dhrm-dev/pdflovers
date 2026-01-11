import fitz  # PyMuPDF

def organize_pdf(input_pdf, output_pdf, page_order):
    """
    page_order: list of page numbers (1-based)
    example: [3, 1, 2]
    """
    src = fitz.open(input_pdf)
    new_doc = fitz.open()

    for page_num in page_order:
        # PyMuPDF uses 0-based index
        new_doc.insert_pdf(src, from_page=page_num - 1, to_page=page_num - 1)

    new_doc.save(output_pdf)
    src.close()
    new_doc.close()
