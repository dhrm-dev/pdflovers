import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.rotate_pdf import rotate_pdf


@csrf_exempt
def rotate_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    angle = int(request.POST.get("angle", 90))
    pages = request.POST.get("pages")  # example: "1,3,5"

    if angle not in [90, 180, 270]:
        return JsonResponse(
            {"error": "Angle must be 90, 180, or 270"},
            status=400
        )

    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    page_list = None
    if pages:
        try:
            page_list = [int(p.strip()) for p in pages.split(",")]
        except ValueError:
            return JsonResponse(
                {"error": "Invalid pages format"},
                status=400
            )

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    output_pdf_path = os.path.join(base_dir, "rotated.pdf")

    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        rotate_pdf(input_pdf_path, output_pdf_path, angle, page_list)
    except Exception as e:
        print("ROTATE PDF ERROR 👉", e)
        return JsonResponse(
            {"error": "PDF rotation failed"},
            status=500
        )

    response = HttpResponse(
        open(output_pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=rotated.pdf"
    return response
