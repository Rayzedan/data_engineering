import json
import sqlite3


def update_table():
	with open("task_1_var_55_item.json") as jsonFile:
		data = json.load(jsonFile)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()

		try:
			with connection:
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
				cursor.execute('BEGIN')
				for item in data:
					insert_query = (f"INSERT INTO game_results (id, name, city, begin, system, tours_count, min_rating, "
									f"time_on_game) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
					values = (
						item['id'], item['name'], item['city'], item['begin'], item['system'], item['tours_count'],
						item['min_rating'], item['time_on_game'])
					cursor.execute(insert_query, values)
		except:
			pass


def sorted_data():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				select_query = "SELECT * FROM game_results ORDER BY min_rating LIMIT 65"
				cursor.execute(select_query)
				results = cursor.fetchall()
		except:
			pass
		with open('sorted_data.json', 'w', encoding='utf-8') as f:
			json.dump(results, f, ensure_ascii=False)


def sorted_by_max_data():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				select_query = "SELECT MAX(time_on_game) FROM game_results"
				cursor.execute(select_query)
				results = cursor.fetchall()
		except:
			pass
		with open('sorted_by_max_data.json', 'w', encoding='utf-8') as f:
			json.dump(results, f, ensure_ascii=False)


def sorted_by_city():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				select_query = "SELECT city FROM game_results"
				cursor.execute(select_query)
				results = cursor.fetchall()
		except:
			pass
		city_counts = {}
		for city in results:
			if city[0] in city_counts:
				city_counts[city[0]] += 1
			else:
				city_counts[city[0]] = 1
		with open('sorted_by_city_data.json', 'w', encoding='utf-8') as f:
			json.dump(city_counts, f, ensure_ascii=False)


def sorted_by_predicate():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		try:
			with connection:
				select_query = "SELECT * FROM game_results WHERE min_rating > 100 ORDER BY time_on_game LIMIT 65"
				cursor.execute(select_query)
				results = cursor.fetchall()
		except:
			pass
		with open('sorted_by_predicate_data.json', 'w', encoding='utf-8') as f:
			json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
	update_table()
	sorted_data()
	sorted_by_max_data()
	sorted_by_city()
	sorted_by_predicate()
