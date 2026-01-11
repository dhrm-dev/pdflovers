import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.crop_pdf import crop_pdf


@csrf_exempt
def crop_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    # Default crop margins (points)
    left = int(request.POST.get("left", 20))
    right = int(request.POST.get("right", 20))
    top = int(request.POST.get("top", 20))
    bottom = int(request.POST.get("bottom", 20))

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_path = os.path.join(base_dir, pdf.name)
    output_path = os.path.join(base_dir, "cropped.pdf")

    with open(input_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        crop_pdf(input_path, output_path, left, right, top, bottom)
    except Exception as e:
        print("CROP PDF ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(
        open(output_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=cropped.pdf"
    return response
