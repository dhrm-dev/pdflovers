from PyPDF2 import PdfReader, PdfWriter

def unlock_pdf(input_pdf_path, output_pdf_path, password):
    """
    Removes password protection from a PDF
    Requires correct password (user or owner)
    """
    reader = PdfReader(input_pdf_path)

    if reader.is_encrypted:
        if not reader.decrypt(password):
            raise ValueError("Incorrect password")

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    return output_pdf_path
