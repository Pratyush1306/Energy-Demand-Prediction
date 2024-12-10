import requests
from datetime import date, timedelta
import calendar
import pandas as pd
import xlrd
import os

today = date.today()
previous_date = today - timedelta(days=1)
formatted_date = previous_date.strftime("%d.%m.%y")
current_year = previous_date.year
current_month = previous_date.month
month_name = calendar.month_name[current_month]

url = f"https://report.grid-india.in/ReportData/Daily%20Report/PSP%20Report/{current_year}-{current_year+1}/{month_name}%20{current_year}/{formatted_date}_NLDC_PSP.xls"

response = requests.get(url)
if response.status_code == 200:
    excel_filename = f"{formatted_date}_NLDC_PSP.xls"
    with open(excel_filename, 'wb') as f:
        f.write(response.content)
    print(f"Excel file downloaded successfully for {formatted_date}")

    book = xlrd.open_workbook(excel_filename, on_demand=True)
    
    if 'MOP_E' in book.sheet_names():
        sheet = book.sheet_by_name('MOP_E')
        
        data = []
        for row_idx in range(5, 14):  
            cell_value = sheet.cell_value(row_idx, 7)  
            data.append(cell_value)
        
        columns = [
            "Date",
            "Demand Met during Evening Peak hrs(MW) (at 20:00 hrs; from RLDCs)",
            "Peak Shortage (MW)",
            "Energy Met (MU)",
            "Hydro Gen (MU)",
            "Wind Gen (MU)",
            "Solar Gen (MU)*",
            "Energy Shortage (MU)",
            "Maximum Demand Met During the Day (MW) (From NLDC SCADA)",
            "Time Of Maximum Demand Met"
        ]
        
        df = pd.DataFrame([[formatted_date] + data], columns=columns)

        csv_filename = "daily_data_grid_india1.csv"
        if os.path.exists(csv_filename):
            existing_df = pd.read_csv(csv_filename)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv(csv_filename, index=False)
        else:
            df.to_csv(csv_filename, index=False)
        
        print(f"Data appended and saved to {csv_filename} for {formatted_date}.")
    else:
        print(f"Sheet 'MOP_E' not found in the Excel file.")
else:
    print(f"Failed to download Excel file for {formatted_date}. Status code: {response.status_code}")

print(url)
