import csv
import os

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crime_database']
collection = db['crimes']


def load_data(file_path):
	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)
		data = []
		for row in reader:
			data.append(row)
		collection.insert_many(data)


data_folder = 'datasets/'
data_files = os.listdir(data_folder)
for file in data_files:
	file_path = os.path.join(data_folder, file)
	if file.endswith(".csv"):
		load_data(file_path)


def fetch_data():
	result1 = list(collection.find({}, {'Crime Type': 1, 'Location': 1}).limit(5))
	result2 = list(collection.find({'Location': 'On or near The Drive'}, {'Crime Type': 1}).limit(5))
	result3 = list(collection.find({'Location': 'On or near Rushden Road'}, {'Crime Type': 1}).limit(5))
	result4 = list(collection.find({'Location': 'On or near High Street'}))
	result5 = list(collection.find({'Location': 'On or near Supermarket'}, {'Crime Type': 1}).limit(5))
	return result1, result2, result3, result4, result5


def aggregate_data():
	pipeline1 = [{'$group': {'_id': '$Crime Type', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 5}]
	result1 = list(collection.aggregate(pipeline1))

	pipeline2 = [{'$match': {'Location': 'On or near High Street'}},
		{'$group': {'_id': '$Crime Type', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 5}]
	result2 = list(collection.aggregate(pipeline2))

	pipeline3 = [
		{'$group': {'_id': '$Location', 'count': {'$sum': 1}}},
		{'$sort': {'count': -1}}
	]
	result3 = list(collection.aggregate(pipeline3))

	pipeline4 = [
		{'$match': {'Location': 'On or near High Elms'}},
		{'$group': {'_id': '$Crime Type', 'count': {'$sum': 1}}},
		{'$sort': {'count': -1}}
	]
	result4 = list(collection.aggregate(pipeline4))

	pipeline5 = [
		{'$group': {'_id': '$Location', 'count': {'$sum': 1}}},
		{'$sort': {'count': -1}}
	]
	result5 = list(collection.aggregate(pipeline5))

	return result1, result2, result3, result4, result5


def update_data():
	query1 = {'Crime Type': 'Burglary'}
	update1 = {'$set': {'Crime Type': 'Robbery'}}
	collection.update_many(query1, update1)

	query2 = {'LSOA name': 'Bedford 001A'}
	collection.delete_many(query2)

	query3 = {'Latitude': '52.238948'}
	collection.delete_many(query3)

	query4 = {'Longitude': '-0.438967'}
	collection.delete_many(query4)

	query5 = {'Reported by': 'Bedfordshire Police'}
	collection.delete_many(query5)


fetch_data_result = fetch_data()
aggregate_data_result = aggregate_data()

print("Задание 1: Выборка данных")
print("Результаты:")
for item in fetch_data_result:
	print(item)
print("Задание 2: Выборка данных с агрегацией")
print("Результаты:")
for item in aggregate_data_result:
	print(item)
print("Задание 3: Обновление/удаление данных")
update_data()
print("Данные успешно обновлены/удалены")
