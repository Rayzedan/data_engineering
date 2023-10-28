import csv
from bs4 import BeautifulSoup

with open('text_5_var_55', 'r') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table')

headers = [header.text for header in table.find_all('th')]

rows = []
for row in table.find_all('tr'):
    rows.append([data.text for data in row.find_all('td')])

with open('result.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)
