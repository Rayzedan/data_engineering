import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df1 = pd.read_csv('data/[1]game_logs.csv',
				  dtype={"h_score": "Int64", "v_score": "Int64", "day_of_week": "string", "h_name": "string",
						 "length_outs": "Int64", "v_hits": "Int64", "v_doubles": "Int64", "v_triples": "Int64",
						 "v_homeruns": "Int64", "v_rbi": "Int64"})
df2 = pd.read_csv('data/[3]flights.csv',
				  dtype={"FLIGHT_NUMBER": "Int64", "ORIGIN_AIRPORT": "string", "DAY_OF_WEEK": "string",
						 "DESTINATION_AIRPORT": "string", "DISTANCE": "Int64", "AIR_TIME": "Int64", "TAXI_OUT": "Int64",
						 "ARRIVAL_DELAY": "Int64", "AIRLINE": "string", "TAXI_IN": "Int64"})
df3 = pd.read_csv('data/CIS_Automotive_Kaggle_Sample.csv',
				  dtype={"vf_MAKE": "string", "stockNum": "string", "vf_EngineCylinders": "Int64", "vf_EngineKW": float,
						 "vf_EngineModel": "string", "vf_EntertainmentSystem": "string",
						 "vf_ForwardCollisionWarning": "string", "vf_FuelInjectionType": "string",
						 "vf_FuelTypePrimary": "string", "vf_FuelTypeSecondary": "string"})
df4 = pd.read_csv('data/dataset.csv',
				  dtype={"name": "string", "spkid": "Int64", "id": "string", "diameter": float, "albedo": float,
						 "diameter_sigma": float, "epoch": float, "epoch_cal": float, "om": float, "w": float})
df5 = pd.read_csv('data/vacancies_2020.csv',
				  dtype={"id": "Int64", "key_skills": "string", "schelude_name": "string", "schelude_id": "string",
						 "expirience_id": "string", "expirience_name": "string", "salary_from": "Int64",
						 "salary_to": "Int64", "employer_name": "string", "employer_industries": "string"})
df6 = pd.read_csv('data/la_crime_2010_to_2023.csv',
				  dtype={"AREA_NAME": "string", "Vict age": "Int64", "Vict sex": "string", "Premis Cd": "Float64",
						 "Status": "string", "Status Desc": "string", "Location": "string",
							 "LAT": "Float64", "LON": "Float64", "Cross Street": "string"})


def analyze_data(df):
	file_size = df.memory_usage(deep=True).sum()
	memory_usage = df.memory_usage(deep=True).sum()
	col_sizes = []
	for col in df.columns:
		col_size = df[col].memory_usage(deep=True)
		col_type = df[col].dtype
		col_sizes.append({'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	sorted_df = df.loc[:, df.dtypes != object]
	sorted_sizes = []
	for col in sorted_df.columns:
		col_size = df[col].memory_usage(deep=True)
		col_type = df[col].dtype
		sorted_sizes.append(
			{'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


analysis1 = analyze_data(df1)
analysis2 = analyze_data(df2)
analysis3 = analyze_data(df3)
analysis4 = analyze_data(df4)
analysis5 = analyze_data(df5)
analysis6 = analyze_data(df6)

with open('statistics.json', 'w') as f:
	json.dump({'file1': analysis1['col_sizes'], 'file2': analysis2['col_sizes'], 'file3': analysis3['col_sizes'],
			   'file4': analysis4['col_sizes'], 'file5': analysis5['col_sizes'], 'file6': analysis6['col_sizes']}, f)


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


optimized_df1 = analyze_optimized_data(df1)
optimized_df2 = analyze_optimized_data(df2)
optimized_df3 = analyze_optimized_data(df3)
optimized_df4 = analyze_optimized_data(df4)
optimized_df5 = analyze_optimized_data(df5)
optimized_df6 = analyze_optimized_data(df6)
compare_memory_usage(df1, optimized_df1)
compare_memory_usage(df2, optimized_df2)
compare_memory_usage(df3, optimized_df3)
compare_memory_usage(df4, optimized_df4)
compare_memory_usage(df5, optimized_df5)
compare_memory_usage(df6, optimized_df6)

chunksize = 1000
df = pd.concat([pd.read_csv('data/[1]game_logs.csv',
							dtype={"h_score": "Int64", "v_score": "Int64", "day_of_week": "string", "h_name": "string",
								   "length_outs": "Int64", "v_hits": "Int64", "v_doubles": "Int64",
								   "v_triples": "Int64", "v_homeruns": "Int64", "v_rbi": "Int64"}),
				pd.read_csv('data/[3]flights.csv',
							dtype={"FLIGHT_NUMBER": "Int64", "ORIGIN_AIRPORT": "string", "DAY_OF_WEEK": "string",
								   "DESTINATION_AIRPORT": "string", "DISTANCE": "Int64", "AIR_TIME": "Int64",
								   "TAXI_OUT": "Int64", "ARRIVAL_DELAY": "Int64", "AIRLINE": "string",
								   "TAXI_IN": "Int64"}),
				pd.read_csv('data/vacancies_2020.csv',
							dtype={"id": "Int64", "key_skills": "string",
								   "schelude_name": "string",
								   "schelude_id": "string",
								   "expirience_id": "string",
								   "expirience_name": "string",
								   "salary_from": "Int64",
								   "salary_to": "Int64",
								   "employer_name": "string",
								   "employer_industries": "string"}),
				pd.read_csv('data/dataset.csv',
							dtype={"name": "string", "spkid": "Int64", "id": "string", "diameter": float,
								   "albedo": float, "diameter_sigma": float, "epoch": float, "epoch_cal": float,
								   "om": float, "w": float}),
				pd.read_csv('data/CIS_Automotive_Kaggle_Sample.csv',
							dtype={"vf_MAKE": "string",
								   "stockNum": "string",
								   "vf_EngineCylinders": "Int64",
								   "vf_EngineKW": float,
								   "vf_EngineModel": "string",
								   "vf_EntertainmentSystem": "string",
								   "vf_ForwardCollisionWarning": "string",
								   "vf_FuelInjectionType": "string",
								   "vf_FuelTypePrimary": "string",
								   "vf_FuelTypeSecondary": "string"}),
				pd.read_csv('data/la_crime_2010_to_2023.csv',
				  			dtype={"AREA_NAME": "string", "Vict age": "Int64",
								   "Vict sex": "string", "Premis Cd": "Float64",
						 			"Status": "string", "Status Desc": "string", "Location": "string",
							 		"LAT": "Float64", "LON": "Float64", "Cross Street": "string"})])

optimized_df = convert_data(df)
optimized_df.to_csv('optimized_data.csv')

# График распределения значений в колонке "price"
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
