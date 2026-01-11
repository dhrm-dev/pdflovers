import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.jpg_to_pdf import convert_jpg_to_pdf


@csrf_exempt
def jpg_to_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    images = request.FILES.getlist("files")
    if not images:
        return JsonResponse({"error": "No images uploaded"}, status=400)

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    image_paths = []

    for img in images:
        img_path = os.path.join(base_dir, img.name)
        with open(img_path, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)
        image_paths.append(img_path)

    output_pdf = os.path.join(base_dir, "output.pdf")

    try:
        convert_jpg_to_pdf(image_paths, output_pdf)
    except Exception as e:
        print("JPG TO PDF ERROR 👉", e)
        return JsonResponse({"error": str(e)}, status=500)

    response = HttpResponse(open(output_pdf, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=images.pdf"
    return response
