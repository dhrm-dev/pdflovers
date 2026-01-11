import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pdf_tools.utils.sign_pdf import sign_pdf


@csrf_exempt
def sign_pdf(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    pdf = request.FILES.get("file")
    signature_image = request.FILES.get("signature")  # optional
    text = request.POST.get("text")  # optional

    page = int(request.POST.get("page", 1))
    x = int(request.POST.get("x", 100))
    y = int(request.POST.get("y", 100))
    font_size = int(request.POST.get("font_size", 14))

    if not pdf:
        return JsonResponse({"error": "No PDF uploaded"}, status=400)

    if not text and not signature_image:
        return JsonResponse(
            {"error": "Text or signature image required"},
            status=400
        )

    work_id = uuid.uuid4().hex
    base_dir = os.path.join(settings.MEDIA_ROOT, work_id)
    os.makedirs(base_dir, exist_ok=True)

    input_pdf_path = os.path.join(base_dir, pdf.name)
    output_pdf_path = os.path.join(base_dir, "signed.pdf")

    with open(input_pdf_path, "wb") as f:
        for chunk in pdf.chunks():
            f.write(chunk)

    image_path = None
    if signature_image:
        image_path = os.path.join(base_dir, signature_image.name)
        with open(image_path, "wb") as f:
            for chunk in signature_image.chunks():
                f.write(chunk)

    try:
        sign_pdf(
            input_pdf_path,
            output_pdf_path,
            text=text,
            image_path=image_path,
            page_number=page,
            x=x,
            y=y,
            font_size=font_size
        )
    except Exception as e:
        print("SIGN PDF ERROR 👉", e)
        return JsonResponse({"error": "PDF signing failed"}, status=500)

    response = HttpResponse(
        open(output_pdf_path, "rb"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = "attachment; filename=signed.pdf"
    return response
