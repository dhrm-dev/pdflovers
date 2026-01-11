import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
    


@csrf_exempt
def excel_to_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    excel = request.FILES.get("file")
    if not excel:
        return JsonResponse({"error": "No Excel file uploaded"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_path = os.path.join(base_dir, excel.name)
    output_path = os.path.join(base_dir, "output.pdf")

    with open(input_path, "wb") as f:
        for chunk in excel.chunks():
            f.write(chunk)

    try:
        excel_to_pdf(input_path, output_path)
    except Exception as e:
        print("EXCEL TO PDF ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(
        open(output_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=excel.pdf"
    return response
