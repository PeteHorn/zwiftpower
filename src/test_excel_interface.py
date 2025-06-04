from excel_interface import xlsx_report

xlsx_report = xlsx_report()
xlsx_report.add_data("Date", ["2025-03-04", "2025-03-05", "2025-03-06", "2025-03-07", "2025-03-09"])
xlsx_report.add_data("Values1", [0, 2, 1, 4, 3])
xlsx_report.add_data("Values2", [5, 6, 9, 8, 5])
xlsx_report.add_chart("Values_1", [2])
xlsx_report.add_chart("Values_2", [3])
xlsx_report.add_chart("All", [2, 3])
xlsx_report.save_file("/home/pete/Documents/testdata/practise_line_chart.xlsx")