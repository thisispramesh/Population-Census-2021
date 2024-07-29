import os
import tabula
import jpype
import pandas as pd

# Set JAVA_HOME explicitly in the script
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-22'  # Replace with your actual path
os.environ['PATH'] = os.environ['JAVA_HOME'] + r'\bin;' + os.environ['PATH']

source_file = "National Report_English.pdf"
dfs = tabula.read_pdf(source_file, pages='22')

# Check if dfs is a list and has elements
if dfs:
    df = dfs[0]  # Assuming the first table is the one you want to save

    # Save the DataFrame to an Excel file
    output_file = "extracted_data.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Data successfully extracted and saved to {output_file}")
else:
    print("No tables found on the specified page.")
