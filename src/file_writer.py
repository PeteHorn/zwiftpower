from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import os
import csv
import logging

class filewriter:
    def __init__(self, path: str):
        self.path = path
    
    def write(self, data):
        pass
    
class csv_writer(filewriter):  
    def write(self, data):
        header = [
        "date", "weight", "zftp", "zftp_wkg", "racing_score",
        "15s_w", "1m_w", "5m_w", "20m_w",
        "15s_wkg", "1m_wkg", "5m_wkg", "20m_wkg"
    ]


        file_exists = os.path.isfile(self.path)
        with open(self.path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        logging.info(f"📁 Data written to {self.path}")

class xlsx_writer(filewriter):
    def write(self, data):
        sheet_name = "Zwift Data"
        header = [
    "date", "weight", "zftp", "zftp_wkg", "racing_score",
    "15s_w", "1m_w", "5m_w", "20m_w",
    "15s_wkg", "1m_wkg", "5m_wkg", "20m_wkg"
]

        # Load or create workbook
        if os.path.exists(self.path):
            wb = load_workbook(self.path)
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                ws = wb.create_sheet(title=sheet_name)
                ws.append(header)
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = sheet_name
            ws.append(header)
        
        # Append row
        row = [data.get(col) for col in header]
        ws.append(row)
        
        # Optional: Auto-resize columns
        for i, col in enumerate(header, 1):
            col_letter = get_column_letter(i)
            max_length = max((len(str(cell.value)) if cell.value else 0) for cell in ws[col_letter])
            ws.column_dimensions[col_letter].width = max(10, min(max_length + 2, 30))
        
        wb.save(self.path)
        logging.info(f"📁 Data written to {self.path} (sheet: '{sheet_name}')")