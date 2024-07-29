import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the web page
url = "https://en.wikipedia.org/wiki/2021_Nepal_census"
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract the table by class
table = soup.find('table', class_='wikitable')  # Adjust the class name as needed

# Step 4: Extract table headers
headers = []
header_row = table.find('tr')  # Get the first row for headers if <th> elements are missing
for th in header_row.find_all('th'):
    headers.append(th.text.strip())

# If no headers are found, use the first row's cells as headers
if not headers:
    header_row = table.find_all('tr')[0]  # First row as header row
    headers = [td.text.strip() for td in header_row.find_all('td')]
    # If headers are still empty, you may have to manually specify or infer them

# Debug print statements
print("Headers found:", headers)

# Step 5: Extract table rows
rows = []
for tr in table.find_all('tr')[1:]:  # Skip the header row
    cells = []
    for td in tr.find_all('td'):
        cells.append(td.text.strip())
    if cells:  # Avoid empty rows
        rows.append(cells)

# Debug print statements
print("Rows found:", rows)

# Step 6: Create a DataFrame and save it as an Excel file
if headers and rows:
    df = pd.DataFrame(rows, columns=headers)
    df.to_excel('Nepal Population Summary.xlsx', index=False)
    print("Data has been successfully extracted and saved to 'Nepal Population Summary.xlsx'.")
else:
    print("No data found to write to Excel.")
