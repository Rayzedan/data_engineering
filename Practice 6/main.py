import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df_list = []

df1 = pd.DataFrame()
for chunk in pd.read_csv('data/[1]game_logs.csv', chunksize=1000,
				  dtype={"h_score": "Int64", "v_score": "Int64", "day_of_week": "string", "h_name": "string",
						 "length_outs": "Int64", "v_hits": "Int64", "v_doubles": "Int64", "v_triples": "Int64",
						 "v_homeruns": "Int64", "v_rbi": "Int64"}):
	df1 = pd.concat([df1, chunk])
df_list.append(df1)

df2 = pd.DataFrame()
for chunk in pd.read_csv('data/[3]flights.csv', chunksize=1000,
				  dtype={"FLIGHT_NUMBER": "Int64", "ORIGIN_AIRPORT": "string", "DAY_OF_WEEK": "string",
						 "DESTINATION_AIRPORT": "string", "DISTANCE": "Int64", "AIR_TIME": "Int64", "TAXI_OUT": "Int64",
						 "ARRIVAL_DELAY": "Int64", "AIRLINE": "string", "TAXI_IN": "Int64"}):
	df2 = pd.concat([df2, chunk])
df_list.append(df2)

df3 = pd.DataFrame()
for chunk in pd.read_csv('data/CIS_Automotive_Kaggle_Sample.csv', chunksize=1000,
				  dtype={"vf_MAKE": "string", "stockNum": "string", "vf_EngineCylinders": "Int64", "vf_EngineKW": float,
						 "vf_EngineModel": "string", "vf_EntertainmentSystem": "string",
						 "vf_ForwardCollisionWarning": "string", "vf_FuelInjectionType": "string",
						 "vf_FuelTypePrimary": "string", "vf_FuelTypeSecondary": "string"}):
	df3 = pd.concat([df3, chunk])
df_list.append(df3)

df4 = pd.DataFrame()
for chunk in pd.read_csv('data/dataset.csv', chunksize=1000,
				  dtype={"name": "string", "spkid": "Int64", "id": "string", "diameter": float, "albedo": float,
						 "diameter_sigma": float, "epoch": float, "epoch_cal": float, "om": float, "w": float}):
	df4 = pd.concat([df4, chunk])
df_list.append(df4)

df5 = pd.DataFrame()
for chunk in pd.read_csv('data/vacancies_2020.csv', chunksize=1000,
				  dtype={"id": "Int64", "key_skills": "string", "schelude_name": "string", "schelude_id": "string",
						 "expirience_id": "string", "expirience_name": "string", "salary_from": "Int64",
						 "salary_to": "Int64", "employer_name": "string", "employer_industries": "string"}):
	df5 = pd.concat([df5, chunk])
df_list.append(df5)

df6 = pd.DataFrame()
for chunk in pd.read_csv('data/la_crime_2010_to_2023.csv', chunksize=1000,
				  dtype={"AREA_NAME": "string", "Vict age": "Int64", "Vict sex": "string", "Premis Cd": "Float64",
						 "Status": "string", "Status Desc": "string", "Location": "string",
						 "LAT": "Float64", "LON": "Float64", "Cross Street": "string"}):
	df6 = pd.concat([df6, chunk])
df_list.append(df6)


def analyze_data(source_dataframe: pd.DataFrame):
	file_size = source_dataframe.memory_usage(deep=True).sum()
	memory_usage = source_dataframe.memory_usage(deep=True).sum()
	col_sizes = []
	for col in source_dataframe.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		col_sizes.append({'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	sorted_df = source_dataframe.loc[:, source_dataframe.dtypes != object]
	sorted_sizes = []
	for col in sorted_df.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		sorted_sizes.append(
			{'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


result_analyze = []
for df in df_list:
	result_analyze.append(analyze_data(df))

with open('statistics.json', 'a') as f:
	for index, data in enumerate(result_analyze):
		json.dump({f'file{index}': data['col_sizes']}, f)


def convert_data(df):
	converted_data = df.copy()
	for column in converted_data.columns:
		if converted_data[column].dtype == 'object':
			unique_values = converted_data[column].unique()
			if len(unique_values) < 50:
				converted_data[column] = converted_data[column].astype('category')
			if converted_data[column].dtype == 'int64':
				converted_data[column] = converted_data[column].astype(np.int32)
			elif converted_data[column].dtype == 'float64':
				converted_data[column] = converted_data[column].astype(np.float32)
	return converted_data


def analyze_optimized_data(df):
	return convert_data(df)


def compare_memory_usage(source_data, optimized_data):
	source_data_memory = source_data.memory_usage(deep=True).sum()
	optimized_data_memory = optimized_data.memory_usage(deep=True).sum()
	if source_data_memory > optimized_data_memory:
		print("success optimization diff between source data and optimized data - " + str(
			source_data_memory - optimized_data_memory))
	else:
		print("fail optimization diff between source data and optimized data - " + str(
			optimized_data_memory - source_data_memory))


for index, data in enumerate(df_list):
	optimized_data = analyze_optimized_data(data)
	compare_memory_usage(data, optimized_data)
	optimized_data.to_csv(f'file{index}')

sns.histplot(data=df1, x="v_score")
plt.show()

sns.histplot(data=df2, x="AIRLINE", y="ARRIVAL_DELAY")
plt.show()

sns.histplot(data=df3, x="vf_EngineModel", y="vf_FuelInjectionType")
plt.show()

sns.histplot(data=df4, x="spkid", y="diameter")
plt.show()

sns.boxplot(data=df5, x="employer_name", y="salary_from")
plt.show()

sns.boxplot(data=df6, x="Vict age", y="Vict sex")
plt.show()
