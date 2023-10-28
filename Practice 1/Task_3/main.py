import re
import math

with open('text_3_var_55', 'r') as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    nums = re.findall(r'\d+', line)
    new_nums = []
    for i, num in enumerate(nums):
        if num == 'NA':
            left_num = nums[i-1] if i > 0 and nums[i-1] != 'NA' else 0
            right_num = nums[i+1] if i < len(nums)-1 and nums[i+1] != 'NA' else 0
            avg = (int(left_num) + int(right_num)) / 2
            new_nums.append(str(avg))
        else:
            new_nums.append(num)
    new_line = ' '.join(new_nums) + '\n'
    new_lines.append(new_line)

with open('result.txt', 'w') as f:
    for line in new_lines:
        nums = re.findall(r'\d+', line)
        filtered_nums = [num for num in nums if math.sqrt(int(num)) >= 105]
        if len(filtered_nums) > 0:
            f.write(' '.join(filtered_nums) + '\n')
