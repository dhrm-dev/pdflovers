import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.page_number import add_page_numbers


@csrf_exempt
def page_number(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    start = int(request.POST.get("start", 1))

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_path = os.path.join(base_dir, pdf.name)
    output_path = os.path.join(base_dir, "page_numbered.pdf")

    with open(input_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        add_page_numbers(input_path, output_path, start)
    except Exception as e:
        print("PAGE NUMBER ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(open(output_path, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=page_numbered.pdf"
    return response
