import fitz  # PyMuPDF

def add_page_numbers(input_pdf, output_pdf, start_number=1):
    doc = fitz.open(input_pdf)
    total_pages = doc.page_count

    for i, page in enumerate(doc):
        page_number = start_number + i
        text = f"{page_number} / {total_pages}"

        rect = page.rect
        x = rect.width / 2
        y = rect.height - 20  # bottom margin

        page.insert_text(
            (x, y),
            text,
            fontsize=10,
            fontname="helv",
            align=fitz.TEXT_ALIGN_CENTER
        )

    doc.save(output_pdf)
    doc.close()
