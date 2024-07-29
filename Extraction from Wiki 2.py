import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the web page
url = "https://en.wikipedia.org/wiki/2021_Nepal_census"
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all tables with the specified class
tables = soup.find_all('table', class_='wikitable sortable')

# Check if tables were found
if not tables:
    print("No tables with the specified class found.")
    exit()

# Initialize a list to hold all DataFrames
all_rows = []
headers = []

# Step 4: Extract data from each table
for table in tables:
    # Extract table headers
    header_row = table.find('thead').find('tr') if table.find('thead') else table.find('tr')
    if header_row:
        headers = [th.text.strip() for th in header_row.find_all('th')]

    # Extract table rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:  # Avoid empty rows
            rows.append(cells)

    # Add rows to all_rows
    all_rows.extend(rows)

# Remove rows where 'SN' column has the value 'Total'
if headers and all_rows:
    df = pd.DataFrame(all_rows, columns=headers)
    if 'SN' in df.columns:
        df = df[df['SN'] != 'Total']

    # Step 5: Save all data to a single Excel sheet
    df.to_excel('Districts_Wise_Details_Single_Sheet.xlsx', index=False)
    print("All tables have been successfully extracted and saved to 'Districts_Wise_Details_Single_Sheet.xlsx'.")
else:
    print("No data found to write to Excel.")
