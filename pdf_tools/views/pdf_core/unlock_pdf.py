import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.unlock_pdf import unlock_pdf


@csrf_exempt
def unlock_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    password = request.POST.get("password")

    if not pdf or not password:
        return JsonResponse(
            {"error": "PDF file and password required"},
            status=400
        )

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    output_pdf_path = os.path.join(base_dir, "unlocked.pdf")

    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        unlock_pdf(input_pdf_path, output_pdf_path, password)
    except ValueError:
        return JsonResponse(
            {"error": "Incorrect password"},
            status=401
        )
    except Exception as e:
        print("UNLOCK PDF ERROR 👉", e)
        return JsonResponse(
            {"error": "PDF unlock failed"},
            status=500
        )

    response = HttpResponse(
        open(output_pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=unlocked.pdf"
    return response
