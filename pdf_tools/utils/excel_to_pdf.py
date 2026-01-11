import subprocess
import os

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def excel_to_pdf(excel_path, output_dir):
    command = [
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        excel_path
    ]

    subprocess.run(command, check=True)

    base = os.path.splitext(os.path.basename(excel_path))[0]
    return os.path.join(output_dir, base + ".pdf")
