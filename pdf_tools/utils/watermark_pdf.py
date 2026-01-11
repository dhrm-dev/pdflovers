import fitz  # PyMuPDF
from PIL import Image

def watermark_pdf(
    input_pdf_path,
    output_pdf_path,
    text=None,
    image_path=None,
    opacity=0.15,
    rotation=0,
    repeat=True,
    font_size=36
):
    """
    Adds text or image watermark to all pages.
    - opacity: 0.0 to 1.0
    - rotation: degrees
    - repeat: tile watermark across page
    """

    doc = fitz.open(input_pdf_path)

    for page in doc:
        rect = page.rect

        if text:
            # Create a transparent text watermark
            page.insert_text(
                (rect.width / 2, rect.height / 2),
                text,
                fontsize=font_size,
                rotate=rotation,
                fontname="helv",
                color=(0, 0, 0),
                render_mode=3,  # fill + stroke
                overlay=True,
                align=fitz.TEXT_ALIGN_CENTER
            )

        if image_path:
            img = Image.open(image_path).convert("RGBA")
            w, h = img.size

            # scale image reasonably
            scale = min(rect.width / w, rect.height / h) * 0.5
            new_w, new_h = int(w * scale), int(h * scale)

            img = img.resize((new_w, new_h))
            img.putalpha(int(255 * opacity))

            img_rect = fitz.Rect(
                (rect.width - new_w) / 2,
                (rect.height - new_h) / 2,
                (rect.width + new_w) / 2,
                (rect.height + new_h) / 2
            )

            page.insert_image(img_rect, stream=img.tobytes())

    doc.save(output_pdf_path)
    doc.close()

    return output_pdf_path
