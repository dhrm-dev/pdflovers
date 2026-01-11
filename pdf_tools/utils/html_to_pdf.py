import subprocess
import os

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def convert_html_to_pdf(html_path, output_dir):
    command = [
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        html_path
    ]

    subprocess.run(command, check=True)

    base = os.path.splitext(os.path.basename(html_path))[0]
    return os.path.join(output_dir, base + ".pdf")
