import pdfplumber
import pandas as pd
from openpyxl import load_workbook

def convert_pdf_to_excel(pdf_path, output_excel):
    writer = pd.ExcelWriter(output_excel, engine="openpyxl")

    with pdfplumber.open(pdf_path) as pdf:
        sheet_index = 1

        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                if not table or len(table) < 2:
                    continue

                # First row as header
                df = pd.DataFrame(table[1:], columns=table[0])

                sheet_name = f"Table_{sheet_index}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                sheet_index += 1

    writer.close()

    # Formatting (column width auto-adjust)
    wb = load_workbook(output_excel)
    for ws in wb.worksheets:
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(output_excel)
