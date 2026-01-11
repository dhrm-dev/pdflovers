import os
import uuid
import zipfile

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.pdf_to_jpg import convert_pdf_to_jpg


@csrf_exempt
def pdf_to_jpg(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    dpi = int(request.POST.get("dpi", 200))  # optional

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    pdf_path = os.path.join(base_dir, pdf.name)
    with open(pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        images = convert_pdf_to_jpg(pdf_path, base_dir, dpi)
    except Exception as e:
        print("PDF TO JPG ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    zip_path = os.path.join(base_dir, "images.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img in images:
            zipf.write(img, os.path.basename(img))

    response = HttpResponse(open(zip_path, "rb"), content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=pdf_to_jpg.zip"
    return response
