import json
import msgpack


def load_data(path: str):
	results = {}
	with open(path, 'r') as f:
		data = json.load(f)
	for item in data:
		product_name = item['name']
		prices = [item['price']]
		result = {
			'average_price': sum(prices) / len(prices),
			'max_price': max(prices),
			'min_price': min(prices)
		}
		results[product_name] = result
	save_data_to_files(results)


def save_data_to_files(data: dict):
	with open('results.json', 'w') as f:
		json.dump(data, f)

	with open('results.msgpack', 'wb') as f:
		packed = msgpack.packb(data)
		f.write(packed)


if __name__ == '__main__':
	load_data('products_55.json')
