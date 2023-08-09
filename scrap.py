import requests
from bs4 import BeautifulSoup
import csv

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_African_countries_by_population"

# Send an HTTP request and get the page content
response = requests.get(url)
html_content = response.content

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the table section by its ID
table_section = soup.find("span", {"id": "Table"})

# Find the table within the section
table = table_section.find_next("table")

# Extract table data into a list of rows and cells
table_data = []
for row in table.find_all("tr"):
    row_data = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
    table_data.append(row_data)

# Define the CSV filename
csv_filename = "african_countries_population.csv"

# Save the table data as a CSV file
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    for row_data in table_data:
        csv_writer.writerow(row_data)