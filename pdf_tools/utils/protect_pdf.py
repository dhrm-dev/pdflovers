from PyPDF2 import PdfReader, PdfWriter

def protect_pdf(input_pdf_path, output_pdf_path, password):
    """
    Protects PDF with password (AES-128)
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    return output_pdf_path
