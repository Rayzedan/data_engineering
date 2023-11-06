import json
import pickle


def load_data(path: str):
	results = {}
	with open(path, 'rb') as f:
		data = pickle.load(f)
	for item in data:
		results[item['name']] = item['price']
	increase_result('price_info_55.json', results)


def increase_result(path: str, data: dict):
	with open(path, 'rb') as f:
		source_data = json.load(f)
	for item in source_data:
		product_name = item['name']
		if item['method'] == 'sum':
			data[product_name] = data[item['name']] + item['param']
		if item['method'] == 'sub':
			data[product_name] = data[item['name']] / item['param']
		if item['method'] == 'percent-':
			number = data[item['name']]
			number -= (number * item['param'] / 100)
			data[product_name] = number
		if item['method'] == 'percent+':
			number = data[item['name']]
			number += (number * item['param'] / 100)
			data[product_name] = number
	save_to_pkl_file('result.pkl', data)


def save_to_pkl_file(path: str, data: dict):
	with open(path, 'wb') as f:
		pickle.dump(data, f)


if __name__ == '__main__':
	load_data('products_55.pkl')
