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
				acousticness REAL,
				popularity INTEGER,
				song TEXT,
				duration_ms INTEGER,
				year INTEGER,
				tempo REAL,
				genre TEXT,
				instrumentalness REAL,
				explicit BOOLEAN,
				energy REAL,
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
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row

		try:
			with connection:
				for record in data:
					artist = record['artist']
					cursor = cursor.execute("SELECT * FROM music WHERE artist=?", (artist,))
					existing_record = cursor.fetchone()
					if existing_record:
						cursor.execute("""
							UPDATE music SET
							acousticness=?,
							popularity=?
							WHERE artist=?""", (
								record['acousticness'], record['popularity'], artist))
					else:
						# если записи нет в таблице, добавляем ее
						cursor.execute("""
							INSERT INTO music (artist, song, duration_ms, year, tempo, genre,
							acousticness, energy, popularity)
							VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness, :energy, :popularity)
							""", record)
		except Exception as e:
			print(e)
			pass


def sorted_data():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT * FROM music ORDER BY popularity LIMIT 65"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_request_1")
		except Exception as e:
			print(e)
			pass


def sorted_by_column_data():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT MAX(energy) FROM music"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_request_2")
				select_query = "SELECT MIN(energy) FROM music"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_request_3")
				select_query = "SELECT AVG(energy) FROM music"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_request_4")
				select_query = "SELECT SUM(energy) FROM music"
				cursor.execute(select_query)
				save_result([dict(row) for row in cursor.fetchall()], "result_request_5")
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
		save_result([dict(row) for row in cursor.fetchall()], "result_request_6")


def sorted_by_predicate():
	with sqlite3.connect('music_catalog.db') as connection:
		cursor = connection.cursor()
		cursor.row_factory = sqlite3.Row
		try:
			with connection:
				select_query = "SELECT * FROM music WHERE popularity > 0.1 ORDER BY energy LIMIT 70"
				cursor.execute(select_query)
		except Exception as e:
			print(e)
			pass
		save_result([dict(row) for row in cursor.fetchall()], "result_request_7")


if __name__ == '__main__':
	create_db()
	update_table()
	sorted_data()
	sorted_by_column_data()
	sorted_by_genre()
	sorted_by_predicate()
