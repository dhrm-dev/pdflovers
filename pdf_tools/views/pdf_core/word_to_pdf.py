import os
import uuid
import subprocess

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.word_to_pdf import convert_word_to_pdf


@csrf_exempt
def word_to_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    word = request.FILES.get("file")
    if not word:
        return JsonResponse({"error": "No Word file uploaded"}, status=400)

    # Allow .doc and .docx
    if not word.name.lower().endswith((".doc", ".docx")):
        return JsonResponse({"error": "Only .doc or .docx allowed"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    word_path = os.path.join(base_dir, word.name)
    with open(word_path, "wb") as f:
        for chunk in word.chunks():
            f.write(chunk)

    try:
        pdf_path = convert_word_to_pdf(word_path, base_dir)
    except subprocess.CalledProcessError as e:
        print("WORD TO PDF ERROR 👉", e)
        return JsonResponse({"error": "Conversion failed"}, status=500)

    response = HttpResponse(
        open(pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=word.pdf"
    return response
