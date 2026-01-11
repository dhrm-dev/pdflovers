import os
import uuid
import subprocess

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.ppt_to_pdf import convert_ppt_to_pdf


@csrf_exempt
def ppt_to_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    ppt = request.FILES.get("file")
    if not ppt:
        return JsonResponse({"error": "No PPT file uploaded"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    ppt_path = os.path.join(base_dir, ppt.name)

    with open(ppt_path, "wb") as f:
        for chunk in ppt.chunks():
            f.write(chunk)

    try:
        pdf_path = convert_ppt_to_pdf(ppt_path, base_dir)
    except subprocess.CalledProcessError as e:
        print("PPT TO PDF ERROR 👉", e)
        return JsonResponse({"error": "Conversion failed"}, status=500)

    response = HttpResponse(
        open(pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=presentation.pdf"
    return response
