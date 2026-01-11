import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.watermark_pdf import watermark_pdf


@csrf_exempt
def watermark_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    text = request.POST.get("text")              # optional
    image = request.FILES.get("image")           # optional
    opacity = float(request.POST.get("opacity", 0.15))
    rotation = int(request.POST.get("rotation", 0))
    font_size = int(request.POST.get("font_size", 36))

    if not pdf or (not text and not image):
        return JsonResponse(
            {"error": "PDF and watermark text or image required"},
            status=400
        )

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    output_pdf_path = os.path.join(base_dir, "watermarked.pdf")

    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    image_path = None
    if image:
        image_path = os.path.join(base_dir, image.name)
        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

    try:
        watermark_pdf(
            input_pdf_path,
            output_pdf_path,
            text=text,
            image_path=image_path,
            opacity=opacity,
            rotation=rotation,
            font_size=font_size
        )
    except Exception as e:
        print("WATERMARK PDF ERROR 👉", e)
        return JsonResponse({"error": "Watermarking failed"}, status=500)

    response = HttpResponse(
        open(output_pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=watermarked.pdf"
    return response
