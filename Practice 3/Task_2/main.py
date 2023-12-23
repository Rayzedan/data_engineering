import collections
import json
import os
import pandas as pd
from bs4 import BeautifulSoup


os.system("unzip zip_var_55.zip")
items = []
for filename in os.listdir():
	if filename.endswith(".html"):
		with open(filename, "r") as file:
			text = ""
			for row in file.readlines():
				text += row

			soup = BeautifulSoup(text, 'html.parser')
			products = soup.find_all("div", attrs={'class': 'product-item'})

			for product in products:
				item = dict()
				item['id'] = product.a['data-id']
				item['link'] = product.find_all('a')[1]['href']
				item['img_url'] = product.find_all("img")[0]['src']
				item['title'] = product.find_all("span")[0].get_text().strip()
				item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
				item['bonus'] = int(
					product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())

				props = product.ul.find_all("li")
				for prop in props:
					item[prop['type']] = prop.get_text().strip()

				items.append(item)

items = sorted(items, key=lambda x: x['price'], reverse=True)
with open("result_all.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))
filtered_items = []
for it in items:
	if it['price'] < 80000:
		filtered_items.append(it)

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['price'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

result2 = []

words = [item['title'] for item in items]
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
