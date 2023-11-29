import sqlite3
import pickle
import json


def create_db():
	with open('task_4_var_55_product_data.pkl', 'rb') as f:
		data = pickle.load(f)

	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()

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
				for record in data:
					cursor.execute('''INSERT INTO computer_accessories
					(name, price, quantity, views, fromCity, isAvailable)
					VALUES (?, ?, ?, ?, ?, ?)''', (
						record['name'], record['price'], record['quantity'], record['views'], record['fromCity'],
						record['isAvailable']))
		except Exception as e:
			print(e)
			pass


def update_db():
	with open('task_4_var_55_update_data.json', 'r') as f:
		data = json.load(f)

	with (sqlite3.connect('computer_accessories.db') as connection):
		cursor = connection.cursor()

		try:
			with connection:
				for record in data:
					parameters = record['method'].split('_')
					value = record['param']
					if len(parameters) > 1:
						select_query = f'''SELECT ''' + parameters[0] + f' FROM \"computer_accessories\"' + \
										f' WHERE name="' + record['name'] + f'"'
						cursor.execute(select_query)
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
								update_query = f'''UPDATE computer_accessories ''' + \
												f'SET ' + parameters[0] + f'=' + str(current_value) + \
												f', count = count + 1' + \
												f' WHERE name="' + record['name'] + f'" AND ' + parameters[0] + \
												f'=' + str(query[0])
								cursor.execute(update_query)
					elif len(parameters) == 1:
						if parameters[0] == f'remove':
							remove_query = f'''DELETE FROM computer_accessories ''' + \
											f' WHERE name="' + record['name'] + f'"'
							cursor.execute(remove_query)
						else:
							available = 'True' if value else 'False'
							update_query = f'''UPDATE computer_accessories ''' + f'SET isAvailable=' + available + \
											f', count = count + 1' + \
											' WHERE name="' + record['name'] + f'"'
							cursor.execute(update_query)

		except Exception as e:
			print(e)
			pass


def most_updated_products():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
				cursor.execute('''SELECT * FROM computer_accessories
				ORDER BY count DESC
				''')
				print(cursor.fetchall())
		except Exception as e:
			print(e)
			pass


def products_price():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
				cursor.execute('''SELECT SUM(price) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MIN(price) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MAX(price) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT AVG(price) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
		except Exception as e:
			print(e)
			pass


def products_quantity():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
				cursor.execute('''SELECT SUM(quantity) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MIN(quantity) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MAX(quantity) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT AVG(quantity) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
		except Exception as e:
			print(e)
			pass


def products_view():
	with sqlite3.connect('computer_accessories.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
				cursor.execute('''SELECT SUM(views) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MIN(views) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT MAX(views) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
				cursor.execute('''SELECT AVG(views) FROM computer_accessories
				ORDER BY name
				''')
				print(cursor.fetchall())
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
