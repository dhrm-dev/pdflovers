import subprocess
import os

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def convert_word_to_pdf(word_path, output_dir):
    """
    Converts DOC/DOCX to PDF using LibreOffice headless mode
    Returns output PDF path
    """
    command = [
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        word_path
    ]

    subprocess.run(command, check=True)

    base = os.path.splitext(os.path.basename(word_path))[0]
    return os.path.join(output_dir, base + ".pdf")
