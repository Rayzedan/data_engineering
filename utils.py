import json


def save_result(data, name):
	with open(f"{name}.json", "w", encoding="utf-8") as f:
		f.write(json.dumps(data, ensure_ascii=False))
