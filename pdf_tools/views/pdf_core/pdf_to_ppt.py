import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.pdf_to_ppt import convert_pdf_to_ppt


@csrf_exempt
def pdf_to_ppt(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    dpi = int(request.POST.get("dpi", 200))

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_path = os.path.join(base_dir, pdf.name)
    output_path = os.path.join(base_dir, "output.pptx")

    with open(input_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        convert_pdf_to_ppt(input_path, output_path, dpi)
    except Exception as e:
        print("PDF TO PPT ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(
        open(output_path, "rb"),
        content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    response["Content-Disposition"] = "attachment; filename=pdf.pptx"
    return response
