import json
import os
import msgpack
import numpy as np
import pandas as pd
from pandas import DataFrame


class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		return super(NumpyEncoder, self).default(obj)


def read_large_data(path: str) -> None:
	data = pd.read_csv(path, low_memory=False)
	data = data[["day_of_week", "v_name", "v_game_number", "h_name", "v_score", "h_score", "length_outs", "v_hits"]]
	filter_data(data)


def filter_data(data: DataFrame) -> None:
	numeric_fields = ["v_game_number", "v_score", "h_score", "length_outs", "v_hits"]
	numeric_stats = data[numeric_fields].agg(["min", "max", "mean", "sum", "std"]).to_dict()
	categorical_fields = ["day_of_week", "v_name", "h_name"]
	categorical_stats = {}
	for field in categorical_fields:
		categorical_stats[field] = dict(data[field].value_counts())
	stats = {"numeric": numeric_stats, "categorical": categorical_stats}
	with open("data.json", "w") as f:
		json.dump(stats, f, cls=NumpyEncoder)
	result = pd.read_json("data.json")
	save_result_to_files(result)


def save_result_to_files(data) -> None:
	data.to_csv("data.csv", index=False)
	with open('data.msgpack', 'wb') as f:
		packed = msgpack.packb(data.to_json())
		f.write(packed)
	data.to_pickle("data.pkl")
	if os.path.exists("data.csv") and os.path.exists("data.json") and os.path.exists("data.msgpack") and os.path.exists(
		"data.pkl"):
		print('csv file size:', round(os.path.getsize("data.csv") / 1024, 2), 'KB')
		print('json file size:', round(os.path.getsize("data.json") / 1024, 2), 'KB')
		print('msgpack file size:', round(os.path.getsize("data.msgpack") / 1024, 2), 'KB')
		print('pkl file size:', round(os.path.getsize("data.pkl") / 1024, 2), 'KB')


if __name__ == '__main__':
	read_large_data("game_logs.csv")
