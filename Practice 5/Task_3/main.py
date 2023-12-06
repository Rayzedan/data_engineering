import pymongo
import csv


def create_and_update_db():
	client = pymongo.MongoClient()
	db = client['task1_db']
	collection = db['workers']

	with open('task_3_item.csv') as file:
		reader = csv.DictReader(file)
		for row in reader:
			collection.insert_one(row)

	collection.delete_many({'$or': [{'salary': {'$lt': 25000}}, {'salary': {'$gt': 175000}}]})
	collection.update_many({}, {'$inc': {'age': 1}})
	collection.update_many({'profession': {'$in': ['Manager', 'Developer']}}, {'$mul': {'salary': 1.05}})
	collection.update_many({'city': 'New York'}, {'$mul': {'salary': 1.07}})
	collection.update_many({'$and': [{'city': 'San Francisco'}, {'profession': {'$in': ['Manager', 'Developer']}},
									 {'age': {'$gt': 30, '$lt': 50}}]}, {'$mul': {'salary': 1.1}})
	collection.delete_many({'age': {'$lt': 25}})


if __name__ == '__main__':
	create_and_update_db()
