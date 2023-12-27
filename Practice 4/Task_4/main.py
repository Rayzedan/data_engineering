import sqlite3
import pickle
import json
from utils import save_result


def create_db():
	with open('task_4_var_55_product_data.pkl', 'rb') as f:
		data = pickle.load(f)

	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				cursor.execute('''CREATE TABLE IF NOT EXISTS computer_accessories(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				price INTEGER,
				quantity INTEGER,
				views INTEGER,
				fromCity TEXT,
				isAvailable TEXT,
				count INTEGER DEFAULT 0
				)
				''')
				cursor.executemany('''
					INSERT INTO computer_accessories (name, price, quantity, views, fromCity, isAvailable)
					VALUES(
						:name, :price, :quantity, :views, :fromCity, :isAvailable)
					''', data)
		except Exception as e:
			print(e)
			pass


def update_db():
	with open('task_4_var_55_update_data.json', 'r') as f:
		data = json.load(f)

	with (sqlite3.connect('computer_accessories.db') as connection):
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				for record in data:
					parameters = record['method'].split('_')
					value = record['param']
					if len(parameters) > 1:
						cursor.execute(
							'''
							SELECT ? FROM computer_accessories
							WHERE name = ?
							''', [parameters[0], record['name']])
						for query in cursor.fetchall():
							current_value = query[0]
							if parameters[1] == f'add':
								current_value = current_value + value
							elif parameters[1] == f'percent' and value > 0:
								current_value = current_value * value
							elif parameters[1] == f'abs':
								current_value = abs(value)
							elif parameters[1] == f'sub':
								current_value = current_value - value
							if current_value > 0:
								cursor.execute(
							'''
								UPDATE computer_accessories SET ? = ?, count = count + 1 WHERE NAME = ? AND ? = ?
								''', [parameters[0], str(current_value), record['name'], parameters[0],
									  str(query[0])])
					elif len(parameters) == 1:
						if parameters[0] == f'remove':
							cursor.execute('''
							DELETE FROM computer_accessories WHERE name = ?
							''', [record['name']])
						else:
							available = 'True' if value else 'False'
							cursor.execute('''
							UPDATE computer_accessories SET isAvailable = ?, count = count + 1 WHERE name = ?
							''', [available, record['name']])

		except Exception as e:
			print(e)
			pass


def most_updated_products():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				cursor.execute('''SELECT * FROM computer_accessories
				ORDER BY count DESC
				''')
				save_result([dict(row) for row in cursor.fetchall()], "result_request_order")
		except Exception as e:
			print(e)
			pass


def products_price():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				data = cursor.execute(
					'''
					SELECT
						SUM(price) as sum,
						MIN(price) as min,
						MAX(price) as max,
						AVG(price) as avg
						FROM computer_accessories
						ORDER BY name
				''')
				save_result([dict(row) for row in data.fetchall()], "result_request_price")
		except Exception as e:
			print(e)
			pass


def products_quantity():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				data = cursor.execute(
					'''
					SELECT
						SUM(quantity) as sum,
						MIN(quantity) as min,
						MAX(quantity) as max,
						AVG(quantity) as avg
						FROM computer_accessories
						ORDER BY name
				''')
				save_result([dict(row) for row in data.fetchall()], "result_request_quantity")
		except Exception as e:
			print(e)
			pass


def products_view():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				data = cursor.execute(
					'''
					SELECT
						SUM(views) as sum,
						MIN(views) as min,
						MAX(views) as max,
						AVG(views) as avg
						FROM computer_accessories
						ORDER BY name
				''')
				save_result([dict(row) for row in data.fetchall()], "result_request_views")
		except Exception as e:
			print(e)
			pass


if __name__ == '__main__':
	create_db()
	update_db()
	most_updated_products()
	products_price()
	products_quantity()
	products_view()
