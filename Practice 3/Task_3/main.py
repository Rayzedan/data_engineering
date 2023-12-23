import collections
import json
import os
import pandas as pd
from bs4 import BeautifulSoup

os.system("unzip zip_var_55.zip")
items = []
for filename in os.listdir():
	if filename.endswith(".xml"):
		with open(filename, encoding="utf-8") as file:
			text = ""
			for row in file.readlines():
				text += row

			soup = BeautifulSoup(text, 'xml')
			for it in soup.find_all("star"):
				item = {}
				for el in it.contents:
					if el.name == "radius":
						item[el.name] = int(el.get_text().strip())

					elif el.name is not None:
						item[el.name] = el.get_text().strip()
				items.append(item)

items = sorted(items, key=lambda x: x['radius'], reverse=True)
with open("result_all.json", "w", encoding="utf-8") as f:
	f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for constellation in items:
	if constellation['constellation'] != 'Рак':
		filtered_items.append(constellation)

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['radius'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

result2 = []

constellation = [item['constellation'] for item in items]
f1 = collections.Counter(constellation)
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
