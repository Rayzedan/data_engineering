import os
import json
import re

from bs4 import BeautifulSoup
from collections import Counter


os.system("unzip zip_var_55.zip")
data = []
for filename in os.listdir():
	if filename.endswith(".html"):
		with open(filename, "r") as f:
			html = f.read()
			soup = BeautifulSoup(html, 'html.parser')
			info = {}
			info['type'] = soup.find('div', {'class': 'chess-wrapper'}).find_all('span')[0].text
			info['tournament'] = soup.find('h1', {'class': 'title'}).text
			info['city'] = soup.find('p', {'class': 'address-p'}).text.split(':')[1].strip()
			info['start_date'] = soup.find('p', {'class': 'address-p'}).text.split(':')[2].strip()
			info['num_rounds'] = int(soup.find('span', {'class': 'count'}).text.split(':')[1])
			info['time_control'] = soup.find('span', {'class': 'year'}).text.split(':')[1].strip()
			info['min_rating'] = int(soup.find_all('span')[-1].text.split(':')[1])
			info['rating'] = float(soup.find_all('span')[-3].text.split(':')[1])
			info['views'] = int(
				soup.find_all("span", string=re.compile("Просмотры:"))[0].getText().split(':')[1].strip())
			data.append(info)

with open('statistics.json', 'w') as f:
	json.dump(data, f, ensure_ascii=False)

sorted_data = sorted(data, key=lambda x: x['rating'])
filtered_data = [d for d in data if d['type'] == 'Swiss']
ratings = [d['rating'] for d in data]
sum_rating = sum(ratings)
min_rating = min(ratings)
max_rating = max(ratings)
avg_rating = sum_rating / len(ratings)

tournaments = [d['tournament'] for d in data]
label_freq = dict(Counter(tournaments))

print('Отсортированные значения:\n', sorted_data)
print('Отфильтрованные значения:\n', filtered_data)
print('Сумма рейтингов:', sum_rating)
print('Минимальный рейтинг:', min_rating)
print('Максимальный рейтинг:', max_rating)
print('Средний рейтинг:', avg_rating)
print('Частота меток:', label_freq)

for filename in os.listdir():
	if filename.endswith(f'.html'):
		os.remove(filename)
