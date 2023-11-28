import sqlite3
import json
import msgpack


def create_db():
	with open("../Task_1/task_1_var_55_item.json") as jsonFile:
		data = json.load(jsonFile)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
				cursor.execute("PRAGMA foreign_keys = 1")
				cursor.execute('''
				CREATE TABLE IF NOT EXISTS game_results (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				city TEXT NOT NULL,
				begin TEXT NOT NULL,
				system TEXT NOT NULL,
				tours_count INTEGER NOT NULL,
				min_rating INTEGER NOT NULL,
				time_on_game INTEGER NOT NULL
				)
				''')
				cursor.execute('''
				CREATE TABLE IF NOT EXISTS city_awards (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				place INTEGER NOT NULL,
				price INTEGER NOT NULL
				)
				''')
				for item in data:
					insert_query = (f"INSERT INTO game_results (id, name, city, begin, system, tours_count, min_rating, "
									f"time_on_game) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
					values = (
						item['id'], item['name'], item['city'], item['begin'], item['system'], item['tours_count'],
						item['min_rating'], item['time_on_game'])
					cursor.execute(insert_query, values)
		except Exception as e:
			print(e)
			pass


def update_table():
	with open('task_2_var_55_subitem.msgpack', 'rb') as f:
		data = msgpack.unpack(f)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				for item in data:
					insert_query = f"INSERT INTO city_awards (name, place, price) VALUES (?, ?, ?)"
					values = (item['name'], item['place'], item['prise'])
					cursor.execute(insert_query, values)
		except Exception as e:
			print(e)
			pass


def join_tables():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				insert_query = f"SELECT	* FROM game_results JOIN city_awards ON game_results.name = city_awards.name"
				cursor.execute(insert_query)
				print(cursor.fetchall())
				insert_query = (f"SELECT MAX(time_on_game) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE place > 4")
				cursor.execute(insert_query)
				print(cursor.fetchall())
				insert_query = (f"SELECT MIN(time_on_game) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE price > 5000")
				cursor.execute(insert_query)
				print(cursor.fetchall())
				insert_query = (f"SELECT AVG(place) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE min_rating > 100")
				cursor.execute(insert_query)
				print(cursor.fetchall())
		except Exception as e:
			print(e)
			pass


if __name__ == '__main__':
	create_db()
	update_table()
	join_tables()
