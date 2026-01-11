from PyPDF2 import PdfMerger

def merge_pdfs(uploaded_files, output_path):
    merger = PdfMerger()

    for pdf in uploaded_files:
        merger.append(pdf)

    with open(output_path, "wb") as f:
        merger.write(f)

    merger.close()
