import csv

source_data = []
with open('text_4_var_55', encoding='utf-8') as file:
	reader = csv.reader(file)
	next(reader)
	data = list(reader)
	for row in data:
		del row[5]
		source_data.append(row)

total_salary = 0
count_salary = 0
for row in source_data:
	salary_str = row[4].replace('₽', '').replace('.', '')
	if salary_str.isdigit():
		salary = int(salary_str)
		total_salary += salary
		count_salary += 1
avg_salary = total_salary / count_salary if count_salary > 0 else 0

filtered_data = []
for row in source_data:
	salary_str = row[4].replace('₽', '').replace('.', '')
	if salary_str.isdigit() and int(salary_str) >= avg_salary and int(row[3]) > 8:
		filtered_data.append(row)
sorted_data = sorted(filtered_data, key=lambda x: x[0])

with open('result.csv', mode='w', encoding='utf-8', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['id', 'name', 'surname', 'age', 'salary'])
	for row in sorted_data:
		writer.writerow(row)
