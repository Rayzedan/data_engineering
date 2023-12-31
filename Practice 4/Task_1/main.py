import json
import sqlite3

from utils import save_result


def update_table():
	with open("task_1_var_55_item.json", encoding='utf-8') as jsonFile:
		data = json.load(jsonFile)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				cursor.execute("""
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
				""")
				cursor.executemany("""
					INSERT INTO game_results (id, name, city, begin, system, tours_count, min_rating, time_on_game)
					VALUES(
						:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
					""", data)
		except Exception as e:
			print(e)
			pass


def sorted_data():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				results = cursor.execute("SELECT * FROM game_results ORDER BY min_rating LIMIT 65")
				save_result([dict(row) for row in results.fetchall()], "result_sorted_by_min_rating_request")
		except Exception as e:
			print(e)
			pass


def sorted_by_column_data():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				results = cursor.execute(
					'''
					SELECT
						SUM(time_on_game) as sum,
						MIN(time_on_game) as min,
						MAX(time_on_game) as max,
						AVG(time_on_game) as avg
						FROM game_results
				''')
				save_result([dict(row) for row in results.fetchall()], "result_sorted_by_column_request")
		except Exception as e:
			print(e)
			pass


def sorted_by_city():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				cursor.execute("SELECT city FROM game_results")
				results = cursor.fetchall()
		except Exception as e:
			print(e)
			pass
		city_counts = {}
		for city in results:
			if city[0] in city_counts:
				city_counts[city[0]] += 1
			else:
				city_counts[city[0]] = 1
		with open('result_sorted_by_city_request.json', 'w', encoding='utf-8') as f:
			json.dump(city_counts, f, ensure_ascii=False)


def sorted_by_predicate():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				results = cursor.execute("SELECT * FROM game_results WHERE min_rating > 100 ORDER BY time_on_game LIMIT 65")
				save_result([dict(row) for row in results.fetchall()], "result_sorted_by_predicate_request")
		except Exception as e:
			print(e)
			pass


if __name__ == '__main__':
	update_table()
	sorted_data()
	sorted_by_column_data()
	sorted_by_city()
	sorted_by_predicate()
