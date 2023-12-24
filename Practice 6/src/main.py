import json
import numpy as np
import pandas as pd
from plots import *

df_list = []

df1 = pd.DataFrame()
df1_cols = ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
			"v_homeruns", "v_rbi"]

for chunk in pd.read_csv('../data/[1]game_logs.csv', chunksize=10000,
						 usecols=df1_cols, low_memory=False, index_col=False):
	df1 = pd.concat([df1, chunk], ignore_index=True)
df_list.append(df1)

df2 = pd.DataFrame()
df2_cols = ["FLIGHT_NUMBER", "ORIGIN_AIRPORT", "DAY_OF_WEEK", "DESTINATION_AIRPORT", "DISTANCE", "AIR_TIME",
			"TAXI_OUT", "ARRIVAL_DELAY",
			"AIRLINE", "TAXI_IN"]
for chunk in pd.read_csv('../data/[3]flights.csv', chunksize=10000,
						 usecols=df2_cols, low_memory=False, index_col=False):
	df2 = pd.concat([df2, chunk], ignore_index=True)
df_list.append(df2)

df3 = pd.DataFrame()
df3_cols = ["vf_Make", "stockNum", "vf_EngineCylinders", "vf_EngineKW", "vf_EngineModel", "vf_EntertainmentSystem",
			"vf_ForwardCollisionWarning", "vf_FuelInjectionType",
			"vf_FuelTypePrimary", "vf_FuelTypeSecondary"]
for chunk in pd.read_csv('../data/CIS_Automotive_Kaggle_Sample.csv', chunksize=10000,
						 usecols=df3_cols, low_memory=False, index_col=False):
	df3 = pd.concat([df3, chunk], ignore_index=True)
df_list.append(df3)

df4 = pd.DataFrame()
df4_cols = ["name", "spkid", "id", "diameter", "albedo", "diameter_sigma",
			"epoch", "epoch_cal",
			"om", "w"]
for chunk in pd.read_csv('../data/dataset.csv', chunksize=10000,
						 usecols=df4_cols, low_memory=False, index_col=False):
	df4 = pd.concat([df4, chunk], ignore_index=True)
df_list.append(df4)

df5 = pd.DataFrame()
df5_cols = ["id", "key_skills", "schedule_name", "experience_id", "experience_name", "salary_from",
			"salary_to", "employer_name",
			"employer_industries", "schedule_id"]
for chunk in pd.read_csv('../data/vacancies_2020.csv', chunksize=10000,
						 usecols=df5_cols, low_memory=False, index_col=False):
	df5 = pd.concat([df5, chunk], ignore_index=True)
df_list.append(df5)

df6 = pd.DataFrame()
df6_cols = ["AREA", "Vict Age", "Vict Sex", "Premis Cd", "Status", "Status Desc",
			"LOCATION", "LAT",
			"LON", "Cross Street"]
for chunk in pd.read_csv('../data/la_crime_2010_to_2023.csv', chunksize=10000,
						 usecols=df6_cols, low_memory=False, index_col=False):
	df6 = pd.concat([df6, chunk], ignore_index=True)
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

with open('results.json', 'a') as f:
	for index, data in enumerate(result_analyze):
		json.dump({f'df{index}_memory_usage': data['col_sizes']}, f)


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
		print("success optimization diff between src data and optimized data - " + str(
			source_data_memory - optimized_data_memory))
	else:
		print("fail optimization diff between src data and optimized data - " + str(
			optimized_data_memory - source_data_memory))


for index, data in enumerate(df_list):
	optimized_data = analyze_optimized_data(data)
	compare_memory_usage(data, optimized_data)
	optimized_data.to_csv(f'optimized_df_{index + 1}.csv')


plot_linear(df1, "v_score", "h_score", "df_1_plot_1")
plot_linear(df1, "v_hits", "v_doubles", "df_1_plot_2")
plot_linear(df1, "v_hits", "v_triples", "df_1_plot_3")
plot_step(df1, "v_homeruns", "v_hits", "df_1_plot_4")
plot_step(df1, "v_homeruns", "v_score", "df_1_plot_5")

plot_linear(df2, "DISTANCE", "AIR_TIME", "df_2_plot_1")
plot_linear(df2, "FLIGHT_NUMBER", "TAXI_IN", "df_2_plot_2")
plot_linear(df2, "FLIGHT_NUMBER", "ARRIVAL_DELAY", "df_2_plot_3")
plot_step(df2, "ORIGIN_AIRPORT", "TAXI_OUT", "df_2_plot_4")
plot_step(df2, "FLIGHT_NUMBER", "DAY_OF_WEEK", "df_2_plot_5")

plot_linear(df3, "stockNum", "vf_EngineCylinders", "df_3_plot_1")
plot_linear(df3, "vf_EngineCylinders", "vf_FuelTypePrimary", "df_3_plot_2")
plot_linear(df3, "vf_EngineKW", "vf_FuelTypeSecondary", "df_3_plot_3")
plot_step(df3, "vf_EngineCylinders", "vf_FuelTypeSecondary", "df_3_plot_4")
plot_step(df3, "stockNum", "vf_ForwardCollisionWarning", "df_3_plot_5")

plot_linear(df4, "id", "diameter", "df_4_plot_1")
plot_linear(df4, "id", "diameter_sigma", "df_4_plot_2")
plot_linear(df4, "spkid", "om", "df_4_plot_3")
plot_step(df4, "albedo", "diameter", "df_4_plot_4")
plot_step(df4, "diameter", "diameter_sigma", "df_4_plot_5")

plot_linear(df5, "id", "salary_to", "df_5_plot_1")
plot_linear(df5, "id", "salary_from", "df_5_plot_2")
plot_linear(df5, "schedule_id", "experience_id", "df_5_plot_3")
plot_step(df5, "experience_id", "salary_to", "df_5_plot_4")
plot_step(df5, "experience_id", "salary_from", "df_5_plot_5")

plot_linear(df6, "Vict Age", "Vict Sex", "df_6_plot_1")
plot_linear(df6, "Vict Age", "LON", "df_6_plot_2")
plot_linear(df6, "LAT", "LON", "df_6_plot_3")
plot_step(df6, "Vict Age", "Status", "df_6_plot_4")
plot_step(df6, "Premis Cd", "LAT", "df_6_plot_5")
