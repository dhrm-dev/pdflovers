import os
import uuid
import zipfile

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.split_pdf import (
    split_pdf_by_ranges,
    split_pdf_every_n_pages
)


@csrf_exempt
def split_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    ranges = request.POST.get("ranges")   # e.g. "1-3|4-6" or "1,3,5"
    every = request.POST.get("every")     # e.g. 2

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    try:
        if ranges:
            range_list = ranges.split("|")
            output_files = split_pdf_by_ranges(
                input_pdf_path, base_dir, range_list
            )
        elif every:
            output_files = split_pdf_every_n_pages(
                input_pdf_path, base_dir, int(every)
            )
        else:
            return JsonResponse(
                {"error": "Provide ranges or every parameter"},
                status=400
            )
    except Exception as e:
        print("SPLIT PDF ERROR 👉", e)
        return JsonResponse({"error": "PDF split failed"}, status=500)

    # ZIP all split PDFs
    zip_path = os.path.join(base_dir, "split_pdfs.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in output_files:
            zipf.write(file, os.path.basename(file))

    response = HttpResponse(
        open(zip_path, "rb"),
        content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=split_pdfs.zip"
    return response
