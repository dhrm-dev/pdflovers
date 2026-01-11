from django.shortcuts import render

# Create your views here.
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils.merge import merge_pdfs
import os, uuid, zipfile
from django.http import HttpResponse
from .utils.pdf_to_jpg import pdf_to_jpg

@csrf_exempt
def merge_pdf(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)

    pdf_files = request.FILES.getlist('files')

    if not pdf_files:
        return JsonResponse({"error": "No PDF files uploaded"}, status=400)

    output_path = os.path.join(settings.MEDIA_ROOT, 'merged.pdf')

    merge_pdfs(pdf_files, output_path)

    return FileResponse(
        open(output_path, 'rb'),
        as_attachment=True,
        filename='merged.pdf'
    )


@csrf_exempt
def pdf_to_jpg(request):
    if request.method != "POST":
        return HttpResponse("POST method required", status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return HttpResponse("No file uploaded", status=400)

    work_id = str(uuid.uuid4())
    base = f"media/{work_id}"
    os.makedirs(base, exist_ok=True)

    pdf_path = os.path.join(base, pdf.name)
    with open(pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    images = pdf_to_jpg(pdf_path, base)

    zip_path = os.path.join(base, "images.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for img in images:
            zipf.write(img, os.path.basename(img))

    with open(zip_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=images.zip"
        return response
