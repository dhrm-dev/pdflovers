from django.urls import path

from .views.pdf_core.merge_pdf import merge_pdf
from .views.pdf_core.split_pdf import split_pdf
from .views.pdf_core.compress_pdf import compress_pdf
from .views.pdf_core.pdf_to_jpg import pdf_to_jpg
from .views.pdf_core.jpg_to_pdf import jpg_to_pdf
from .views.pdf_core.pdf_to_word import pdf_to_word
from .views.pdf_core.word_to_pdf import word_to_pdf
from .views.pdf_core.excel_to_pdf import excel_to_pdf
from .views.pdf_core.pdf_to_excel import pdf_to_excel
from .views.pdf_core.html_to_pdf import html_to_pdf
from .views.pdf_core.pdf_to_ppt import pdf_to_ppt
from .views.pdf_core.ppt_to_pdf import ppt_to_pdf
from .views.pdf_core.edit_pdf import edit_pdf
from .views.pdf_core.sign_pdf import sign_pdf
from .views.pdf_core.watermark_pdf import watermark_pdf
from .views.pdf_core.rotate_pdf import rotate_pdf
from .views.pdf_core.unlock_pdf import unlock_pdf
from .views.pdf_core.protect_pdf import protect_pdf
from .views.pdf_core.organize_pdf import organize_pdf
from .views.pdf_core.repair_pdf import repair_pdf
from .views.pdf_core.crop_pdf import crop_pdf
from .views.pdf_core.page_number import page_number

urlpatterns = [
    path('pdf/merge/', merge_pdf),
    path('pdf/split/', split_pdf),
    path('pdf/compress/', compress_pdf),
    path('pdf/pdf-to-jpg/', pdf_to_jpg),
    path('pdf/jpg-to-pdf/', jpg_to_pdf),
    path('pdf/pdf-to-word/', pdf_to_word),
    path('pdf/word-to-pdf/', word_to_pdf),
    path('pdf/excel-to-pdf/', excel_to_pdf),
    path('pdf/pdf-to-excel/', pdf_to_excel),
    path('pdf/html-to-pdf/', html_to_pdf),
    path('pdf/pdf-to-ppt/', pdf_to_ppt),
    path('pdf/ppt-to-pdf/', ppt_to_pdf),
    path('pdf/edit/', edit_pdf),
    path('pdf/sign/', sign_pdf),
    path('pdf/watermark/', watermark_pdf),
    path('pdf/rotate/', rotate_pdf),
    path('pdf/unlock/', unlock_pdf),
    path('pdf/protect/', protect_pdf),
    path('pdf/organize/', organize_pdf),
    path('pdf/repair/', repair_pdf),
    path('pdf/crop/', crop_pdf),
    path('pdf/page-number/', page_number),
]
