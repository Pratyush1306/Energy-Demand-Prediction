# Energy-Demand-Prediction
A time-series analysis project for predicting energy demand using the ARIMA (AutoRegressive Integrated Moving Average) model. It includes automated data collection through web scraping, data preprocessing, and ARIMA modeling for accurate energy consumption forecasting. Ideal for exploring statistical methods in energy analytics. Visual dashboards are also available for real-time monitoring via localhost.


# Repository Overview
Scrape.py: Automates data scraping from Grid India, updating the CSV file with the latest data.

sample.csv: Stores the processed daily energy data.

main.py: Implements the ARIMA model for energy demand prediction using the updated CSV data.

# Setup Instructions
Prerequisites

Ensure the following dependencies are installed:

-Python (3.8 or higher)

-Jupyter Notebook

-Required libraries: pandas, numpy, requests, beautifulsoup4, statsmodels, matplotlib, dash

  Install dependencies using:
  
  pip install pandas numpy requests beautifulsoup4 statsmodels matplotlib dash

# Troubleshooting
CSV Path Error

-Ensure the file path specified in the notebooks matches your directory structure.

Scraping Errors

-Verify internet connectivity and that the Grid India website URL is correct and accessible. Update the scraping logic if the website's structure changes.

Library Issues

-Reinstall missing libraries using pip install <library_name>.

Dashboard Issues

-Ensure dashboard.py is running and that port 8061 is not occupied by another service. Check the browser and server logs for any errors.
