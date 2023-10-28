import re

with open('text_2_var_55', 'r') as f:
    lines = f.readlines()
averages = []
for line in lines:
    nums = re.findall(r'\d+', line)
    avg = sum(int(num) for num in nums) / len(nums)
    averages.append(avg)

with open('result.txt', 'w') as f:
    for avg in averages:
        f.write(f"{avg}\n")
