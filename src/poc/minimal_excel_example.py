from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference

# Create workbook and sheet
wb = Workbook()
ws = wb.active

# Add simple data (header + data rows)
data = [
    ["X", "Y"],
    [1, 10],
    [2, 20],
    [3, 30],
    [4, 40],
]
for row in data:
    ws.append(row)

# Create line chart
chart = LineChart()
chart.title = "Simple Line Chart"

# Set the data range (Y values only, exclude header)
data_ref = Reference(ws, min_col=2, min_row=1, max_row=5)

# Set the categories (X values)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)

# Add data to chart
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats)

# Add chart to the sheet
ws.add_chart(chart, "E5")

# Save workbook
wb.save("/home/pete/Documents/testdata/minimal_line_chart.xlsx")
# -*- coding: utf-8 -*-

