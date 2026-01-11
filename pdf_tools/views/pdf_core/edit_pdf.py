import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.edit_pdf import edit_pdf


@csrf_exempt
def edit_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    text = request.POST.get("text")
    image = request.FILES.get("image")

    page = int(request.POST.get("page", 1))
    x = int(request.POST.get("x", 100))
    y = int(request.POST.get("y", 100))
    font_size = int(request.POST.get("font_size", 14))

    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    if not text and not image:
        return JsonResponse(
            {"error": "Text or image required for editing"},
            status=400
        )

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    output_pdf_path = os.path.join(base_dir, "edited.pdf")

    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    image_path = None
    if image:
        image_path = os.path.join(base_dir, image.name)
        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

    try:
        edit_pdf(
            input_pdf_path,
            output_pdf_path,
            page_number=page,
            text=text,
            x=x,
            y=y,
            font_size=font_size,
            image_path=image_path
        )
    except Exception as e:
        print("EDIT PDF ERROR 👉", e)
        return JsonResponse({"error": "PDF edit failed"}, status=500)

    response = HttpResponse(
        open(output_pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=edited.pdf"
    return response
