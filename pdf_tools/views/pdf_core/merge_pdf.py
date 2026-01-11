import os
import uuid

from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.merge import merge_pdfs


@csrf_exempt
def merge_pdf(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)

    files = request.FILES.getlist('files')

    if len(files) < 2:
        return JsonResponse({"error": "At least 2 PDF files required"}, status=400)

    # ensure media folder exists
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    output_filename = f"merged_{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    try:
        merge_pdfs(files, output_path)
    except Exception as e:
        print("MERGE ERROR 👉", e)   # 👈 VERY IMPORTANT
        return JsonResponse({"error": str(e)}, status=500)

    return FileResponse(
        open(output_path, 'rb'),
        as_attachment=True,
        filename='merged.pdf'
    )
