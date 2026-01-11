import fitz  # PyMuPDF
import os

def convert_pdf_to_jpg(pdf_path, output_dir, dpi=200):
    """
    Converts each PDF page to high-quality JPG
    Returns list of image paths
    """
    doc = fitz.open(pdf_path)
    image_paths = []

    zoom = dpi / 72  # DPI control
    mat = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_name = f"page_{i + 1}.jpg"
        img_path = os.path.join(output_dir, img_name)
        pix.save(img_path)
        image_paths.append(img_path)

    doc.close()
    return image_paths
