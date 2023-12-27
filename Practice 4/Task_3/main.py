import sqlite3
import pickle
from utils import save_result


def create_db():
	with open('task_3_var_55_part_1.text', 'r') as f:
		lines = f.readlines()

	data = []
	record = {}
	for line in lines:
		if line.strip() == '=====':
			data.append(record)
			record = {}
		else:
			key, value = line.strip().split('::')
			if key == 'explicit':
				value = True if value == 'True' else False
			elif key in ['duration_ms', 'year']:
				value = int(value)
			elif key in ['tempo', 'instrumentalness', 'loudness']:
				value = float(value)
			record[key] = value

	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				cursor.execute("""CREATE TABLE IF NOT EXISTS music(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				artist TEXT,
				song TEXT,
				duration_ms INTEGER,
				year INTEGER,
				tempo REAL,
				genre TEXT,
				instrumentalness REAL,
				explicit BOOLEAN,
				loudness REAL
				)
				""")
				cursor.executemany("""
					INSERT INTO music (artist, song, duration_ms, year, tempo, genre, instrumentalness, explicit, loudness)
					VALUES(
						:artist, :song, :duration_ms, :year, :tempo, :genre, :instrumentalness, :explicit, :loudness)
					""", data)
		except Exception as e:
			print(e)
			pass


def update_table():
	with open('task_3_var_55_part_2.pkl', 'rb') as f:
		data = pickle.load(f)

	for item in data:
		item.pop("acousticness")
		item.pop("popularity")
		item.pop("energy")
		for row in item:
			if row in ['duration_ms', 'year']:
				item[row] = int(item[row])
			elif row in ['tempo']:
				item[row] = float(item[row])

	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				cursor.executemany("""
					INSERT INTO music (artist, song, duration_ms, year, tempo, genre)
					VALUES(
						:artist, :song, :duration_ms, :year, :tempo, :genre)
					""", data)
		except Exception as e:
			print(e)
			pass


def sorted_data():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT * FROM music ORDER BY tempo LIMIT 65"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_sorted_by_tempo_request")
		except Exception as e:
			print(e)
			pass


def sorted_by_column_data():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				results = cursor.execute(
					'''
					SELECT
						SUM(duration_ms) as sum,
						MIN(duration_ms) as min,
						MAX(duration_ms) as max,
						AVG(duration_ms) as avg
						FROM music
				''')
				save_result([dict(row) for row in results.fetchall()], "result_sorted_by_column_request")
		except Exception as e:
			print(e)
			pass


def sorted_by_genre():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT genre FROM music"
				cursor.execute(select_query)
				results = cursor.fetchall()
		except BaseException as e:
			print(e)
			pass
		genre_counts = {}
		for genre in results:
			if genre[0] in genre_counts:
				genre_counts[genre[0]] += 1
			else:
				genre_counts[genre[0]] = 1
		save_result(genre_counts, "result_sorted_by_genre_request")


def sorted_by_predicate():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT * FROM music WHERE tempo > 100.0 ORDER BY duration_ms LIMIT 70"
				cursor.execute(select_query)
		except Exception as e:
			print(e)
			pass
		save_result([dict(row) for row in cursor.fetchall()], "result_sorted_by_tempo_and_duration_request")


if __name__ == '__main__':
	create_db()
	update_table()
	sorted_data()
	sorted_by_column_data()
	sorted_by_genre()
	sorted_by_predicate()
