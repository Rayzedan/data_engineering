import numpy as np
import json


def normalize_matrix(source_path: str, result_path: str) -> None:
	matrix = np.load('matrix_55.npy')
	sum_all = np.sum(matrix)
	avr_all = np.mean(matrix)
	sum_md = np.sum(np.diag(matrix))
	avr_md = np.mean(np.diag(matrix))
	sum_sd = np.sum(np.diag(np.fliplr(matrix)))
	avr_sd = np.mean(np.diag(np.fliplr(matrix)))
	max_val = np.max(matrix)
	min_val = np.min(matrix)
	norm_matrix = (matrix - np.mean(matrix)) / np.std(matrix)
	np.save(result_path, norm_matrix)
	result = {
		'sum': int(sum_all),
		'avr': float(avr_all),
		'sumMD': int(sum_md),
		'avrMD': float(avr_md),
		'sumSD': int(sum_sd),
		'avrSD': float(avr_sd),
		'max': int(max_val),
		'min': int(min_val)
	}
	save_to_json(result)


def save_to_json(json_data: dict, path: str = 'result.json') -> None:
	with open(path, 'w') as f:
		json.dump(json_data, f)


if __name__ == '__main__':
	normalize_matrix('matrix_55.npy', 'result_matrix.npy')
