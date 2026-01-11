from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf_by_ranges(input_pdf, output_dir, ranges):
    """
    ranges example:
    ["1-3", "4-6"] OR ["1,3,5"]
    Returns list of output pdf paths
    """
    reader = PdfReader(input_pdf)
    output_files = []

    for idx, r in enumerate(ranges, start=1):
        writer = PdfWriter()

        if "-" in r:
            start, end = r.split("-")
            pages = range(int(start) - 1, int(end))
        else:
            pages = [int(p) - 1 for p in r.split(",")]

        for p in pages:
            if 0 <= p < len(reader.pages):
                writer.add_page(reader.pages[p])

        output_path = os.path.join(output_dir, f"split_{idx}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        output_files.append(output_path)

    return output_files


def split_pdf_every_n_pages(input_pdf, output_dir, n):
    reader = PdfReader(input_pdf)
    output_files = []
    total_pages = len(reader.pages)

    for i in range(0, total_pages, n):
        writer = PdfWriter()
        for j in range(i, min(i + n, total_pages)):
            writer.add_page(reader.pages[j])

        output_path = os.path.join(output_dir, f"split_{i//n + 1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        output_files.append(output_path)

    return output_files
