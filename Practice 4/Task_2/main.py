import sqlite3
import json
import msgpack
from utils import save_result

def create_db():
	with open("../Task_1/task_1_var_55_item.json") as jsonFile:
		data = json.load(jsonFile)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		connection.row_factory = sqlite3.Row

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
				prise INTEGER NOT NULL
				)
				''')
				cursor.executemany('''
					INSERT INTO game_results (id, name, city, begin, system, tours_count, min_rating, time_on_game)
					VALUES(
						:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
					''', data)
		except Exception as e:
			print(e)
			pass


def update_table():
	with open('task_2_var_55_subitem.msgpack', 'rb') as f:
		data = msgpack.unpack(f)

	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		connection.row_factory = sqlite3.Row
		try:
			with connection:
				cursor.executemany('''
					INSERT INTO city_awards (name, place, prise)
					VALUES(:name, :place, :prise)
				''', data)
		except Exception as e:
			print(e)
			pass


def join_tables():
	with sqlite3.connect('game_results.db') as connection:
		cursor = connection.cursor()
		connection.row_factory = sqlite3.Row
		try:
			with connection:
				insert_query = f"SELECT	* FROM game_results JOIN city_awards ON game_results.name = city_awards.name"
				cursor.execute(insert_query)
				save_result(cursor.fetchall(), "result_request_1")
				insert_query = (f"SELECT MAX(time_on_game) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE place > 4")
				cursor.execute(insert_query)
				save_result(cursor.fetchall(), "result_request_2")
				insert_query = (f"SELECT MIN(time_on_game) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE prise > 5000")
				cursor.execute(insert_query)
				save_result(cursor.fetchall(), "result_request_3")
				insert_query = (f"SELECT AVG(place) FROM game_results JOIN city_awards "
								f"ON game_results.name = city_awards.name WHERE min_rating > 100")
				cursor.execute(insert_query)
				save_result(cursor.fetchall(), "result_request_4")
		except Exception as e:
			print(e)
			pass


if __name__ == '__main__':
	create_db()
	update_table()
	join_tables()
