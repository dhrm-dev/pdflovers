import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.html_to_pdf import convert_html_to_pdf



@csrf_exempt
def html_to_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    html_file = request.FILES.get("file")
    if not html_file:
        return JsonResponse({"error": "No HTML file uploaded"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    html_path = os.path.join(base_dir, html_file.name)
    output_pdf = os.path.join(base_dir, "output.pdf")

    with open(html_path, "wb") as f:
        for chunk in html_file.chunks():
            f.write(chunk)

    try:
        convert_html_to_pdf(html_path, output_pdf)
    except Exception as e:
        print("HTML TO PDF ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(open(output_pdf, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=html.pdf"
    return response
