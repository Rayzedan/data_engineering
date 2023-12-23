import collections
import json
import os
import pandas as pd
from bs4 import BeautifulSoup

os.system("unzip zip_var_55.zip")
items = []
for filename in os.listdir():
	if filename.endswith(".xml"):
		with open(filename, "r") as file:
			text = ""
			for row in file.readlines():
				text += row

			root = BeautifulSoup(text, 'xml')

			for clothing in root.find_all("clothing"):
				item = dict()
				for el in clothing.contents:
					if el.name is None:
						continue
					elif el.name == "price" or el.name == "reviews":
						item[el.name] = int(el.get_text().strip())
					elif el.name == "price" or el.name == "rating":
						item[el.name] = float(el.get_text().strip())
					elif el.name == "new":
						item[el.name] = el.get_text().strip() == "+"
					elif el.name == "exclusive" or el.name == "sorty":
						item[el.name] = el.get_text().strip() == "yes"
					else:
						item[el.name] = el.get_text().strip()

				items.append(item)

items = sorted(items, key=lambda x: x['rating'], reverse=True)

with open("result_all.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for color in items:
	if color['color'] != 'Оранжевый':
		filtered_items.append(color)

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['reviews'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

result2 = []

material = [item['material'] for item in items]
f1 = collections.Counter(material)
result2.append(f1)

with open("result_filtered.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("result_math.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(result, ensure_ascii=False))

with open("result_frequency.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(result2, ensure_ascii=False))

for filename in os.listdir():
	if filename.endswith(f'.xml'):
		os.remove(filename)
