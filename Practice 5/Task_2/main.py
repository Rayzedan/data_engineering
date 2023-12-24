from utils import save_result
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
	collection.insert_many(objects)

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': None,
						'min': {'$min': '$salary'},
						'avg': {'$avg': '$salary'},
						'max': {'$max': '$salary'}
					}
			}
		])
	save_result(list(result), "result_aggregate_1")

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': '$profession',
						'count': {'$sum': 1}
					}
			}
		])
	save_result(list(result), "result_aggregate_2")

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': '$city',
						'min_salary': {'$min': '$salary'},
						'avg': {'$avg': '$salary'},
						'min': {'$max': '$salary'}
					}
			}
		])
	save_result(list(result), "result_aggregate_3")

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': '$job',
						'min': {'$min': '$salary'},
						'avg': {'$avg': '$salary'},
						'max': {'$max': '$salary'}
					}
			}
		])
	save_result(list(result), "result_aggregate_4")

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': '$city',
						'min': {'$min': '$age'},
						'avg': {'$avg': '$age'},
						'max': {'$max': '$age'}
					}
			}
		]
	)
	save_result(list(result), "result_aggregate_5")

	result = collection.aggregate(
		[
			{
				'$group':
					{
						'_id': '$job',
						'min': {'$min': '$age'},
						'avg': {'$avg': '$age'},
						'max_age': {'$max': '$age'}
					}
			}
		])
	save_result(list(result), "result_aggregate_6")

	result = collection.find().sort([('age', pymongo.ASCENDING), ('salary', pymongo.DESCENDING)]).limit(1)
	save_result(list(result), "result_aggregate_6")

	result = collection.find().sort([('age', pymongo.DESCENDING), ('salary', pymongo.ASCENDING	)]).limit(1)
	save_result(list(result), "result_aggregate_7")

	result = collection.aggregate(
		[
			{
				'$match':
					{
						'salary': {'$gt': 50000}
					}
			},
			{
				'$group':
					{
						'_id': '$city',
						'min': {'$min': '$age'},
						'avg': {'$avg': '$age'},
						'max': {'$max': '$age'}
					}
			},
			{
				'$sort':
					{'name': pymongo.ASCENDING}
			}
		])
	save_result(list(result), "result_aggregate_8")

	result = collection.aggregate(
		[
			{
				'$match':
					{
						'$or':
							[
								{
									'age':
										{
											'$gt': 18, '$lt': 25
										}
								},
								{
									'age':
										{
											'$gt': 50, '$lt': 65
										}
								}
							]
					}
			},
			{
				'$group':
					{
						'_id': {'city': '$city', 'job': '$job'},
						'min': {'$min': '$salary'},
						'avg': {'$avg': '$salary'},
						'max': {'$max': '$salary'}
					}
			}
		]
	)
	save_result(list(result), "result_aggregate_9")

	result = collection.aggregate(
		[
			{
				'$match':
					{
						'city': 'Баку'
					}
			},
			{
				'$group':
					{
						'_id': '$job',
						'total_salary': {'$sum': '$salary'}
					}
			},
			{
				'$sort':
					{'total_salary': pymongo.DESCENDING}
			}
		]
	)
	save_result(list(result), "result_aggregate_10")


if __name__ == '__main__':
	create_and_update_db()
