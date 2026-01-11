import pikepdf

def repair_pdf(input_pdf_path, output_pdf_path):
    """
    Repairs corrupted/damaged PDF using QPDF engine
    """
    with pikepdf.open(input_pdf_path, allow_overwriting_input=True) as pdf:
        pdf.save(
            output_pdf_path,
            linearize=True,
            fix_metadata_version=True
        )

    return output_pdf_path
