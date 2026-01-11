import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.organize_pdf import organize_pdf


@csrf_exempt
def organize_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    order = request.POST.get("order")  # e.g. "3,1,2"

    if not pdf or not order:
        return JsonResponse({"error": "PDF file and page order required"}, status=400)

    try:
        page_order = [int(x) for x in order.split(",")]
    except ValueError:
        return JsonResponse({"error": "Invalid page order format"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_path = os.path.join(base_dir, pdf.name)
    output_path = os.path.join(base_dir, "organized.pdf")

    with open(input_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        organize_pdf(input_path, output_path, page_order)
    except Exception as e:
        print("ORGANIZE PDF ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(open(output_path, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=organized.pdf"
    return response
