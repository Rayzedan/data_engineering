from pprint import pprint
import msgpack
import pymongo


def create_and_update_db():
	objects = []
	with open('task_2_item.msgpack', 'rb') as file:
		data = msgpack.unpack(file)

	for item in data:
		record = {}
		record['id'] = item['id']
		record['age'] = int(item['age'])
		record['city'] = item['city']
		record['job'] = item['job']
		record['salary'] = int(item['salary'])
		record['year'] = int(item['year'])
		objects.append(record)

	client = pymongo.MongoClient()
	db = client['task1_db']
	collection = db['workers']

	for record in objects:
		collection.insert_one(record)

	result = collection.aggregate([
		{'$group': {'_id': None, 'min_salary': {'$min': '$salary'}, 'avg_salary': {'$avg': '$salary'},
					'max_salary': {'$max': '$salary'}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$group': {'_id': '$profession', 'count': {'$sum': 1}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$group': {'_id': '$city', 'min_salary': {'$min': '$salary'}, 'avg_salary': {'$avg': '$salary'},
					'max_salary': {'$max': '$salary'}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$group': {'_id': '$job', 'min_salary': {'$min': '$salary'}, 'avg_salary': {'$avg': '$salary'},
					'max_salary': {'$max': '$salary'}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$group': {'_id': '$city', 'min_age': {'$min': '$age'}, 'avg_age': {'$avg': '$age'},
					'max_age': {'$max': '$age'}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$group': {'_id': '$job', 'min_age': {'$min': '$age'}, 'avg_age': {'$avg': '$age'},
					'max_age': {'$max': '$age'}}}
	])
	pprint(list(result))

	result = collection.find({'age': {'$eq': collection.find_one(sort=[('age', pymongo.ASCENDING)])['age']}}).sort(
		'salary', pymongo.DESCENDING).limit(1)
	pprint(list(result))

	result = collection.find({'age': {'$eq': collection.find_one(sort=[('age', pymongo.DESCENDING)])['age']}}).sort(
		'salary', pymongo.ASCENDING).limit(1)
	pprint(list(result))

	result = collection.aggregate([
		{'$match': {'salary': {'$gt': 50000}}},
		{'$group': {'_id': '$city', 'min_age': {'$min': '$age'}, 'avg_age': {'$avg': '$age'},
					'max_age': {'$max': '$age'}}},
		{'$sort': {'name': pymongo.ASCENDING}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$match': {'$or': [
			{'age': {'$gt': 18, '$lt': 25}},
			{'age': {'$gt': 50, '$lt': 65}}
		]}},
		{'$group': {'_id': {'city': '$city', 'job': '$job'}, 'min_salary': {'$min': '$salary'},
					'avg_salary': {'$avg': '$salary'}, 'max_salary': {'$max': '$salary'}}}
	])
	pprint(list(result))

	result = collection.aggregate([
		{'$match': {'city': 'Баку'}},
		{'$group': {'_id': '$job', 'total_salary': {'$sum': '$salary'}}},
		{'$sort': {'total_salary': pymongo.DESCENDING}}
	])
	pprint(list(result))


if __name__ == '__main__':
    create_and_update_db()
