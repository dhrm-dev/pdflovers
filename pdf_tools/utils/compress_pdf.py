import fitz  # PyMuPDF
import os

def compress_pdf(input_path, output_path):
    """
    Lossless PDF compression using PyMuPDF
    """
    doc = fitz.open(input_path)

    for page in doc:
        page.clean_contents()   # remove unused objects

    doc.save(
        output_path,
        garbage=4,      # remove unused objects
        deflate=True,   # compress streams
        clean=True
    )

    doc.close()
