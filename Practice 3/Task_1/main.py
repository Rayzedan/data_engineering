import collections
import json
import os
import re
import zipfile
import pandas as pd
from bs4 import BeautifulSoup


with zipfile.ZipFile('zip_var_55.zip', 'r') as zip_ref:
	zip_ref.extractall()
items = []
for filename in os.listdir():
	if filename.endswith(".html"):
		with open(filename, "r") as f:
			html = f.read()
			soup = BeautifulSoup(html, 'html.parser')
			item = {}
			item['type'] = soup.find('div', {'class': 'chess-wrapper'}).find_all('span')[0].text.split(':')[1].strip()
			item['tournament'] = soup.find('h1', {'class': 'title'}).text.split(':')[1].strip()
			city = soup.find_all("p",attrs={"class": "address-p"})[0].get_text().replace("Город:", "")
			start_date = city.find("Начало")
			date = city[start_date:].replace("Начало:", "").strip()
			city = city[:start_date].strip()
			item["city"] = city
			item["start_date"] = date
			item['num_rounds'] = int(soup.find('span', {'class': 'count'}).text.split(':')[1])
			item['time_control'] = soup.find('span', {'class': 'year'}).text.split(':')[1].strip()
			item['min_rating'] = int(
				soup.find_all("span", string=re.compile("Минимальный рейтинг для участия:"))[0].getText().split(':')[1].strip())
			item['rating'] = float(
				soup.find_all("span", string=re.compile("Рейтинг:"))[0].getText().split(':')[
					1].strip())
			item['views'] = int(
				soup.find_all("span", string=re.compile("Просмотры:"))[0].getText().split(':')[1].strip())
			items.append(item)

items = sorted(items, key=lambda x: x['min_rating'], reverse=True)
with open("result_all.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))
filtered_items = []
for it in items:
	if it['min_rating'] < 2000:
		filtered_items.append(it)

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['min_rating'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

result2 = []

words = [item['city'] for item in items]
f1 = collections.Counter(words)
result2.append(f1)

with open("result_filter.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("result_math.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(result, ensure_ascii=False))

with open("result_frequency.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(result2, ensure_ascii=False))

for filename in os.listdir():
	if filename.endswith(f'.html'):
		os.remove(filename)
