import subprocess
import os

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def convert_ppt_to_pdf(ppt_path, output_dir):
    command = [
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        ppt_path
    ]

    subprocess.run(command, check=True)

    base = os.path.splitext(os.path.basename(ppt_path))[0]
    return os.path.join(output_dir, base + ".pdf")
