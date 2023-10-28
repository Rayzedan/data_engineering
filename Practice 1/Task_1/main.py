import re

with open('text_1_var_55', 'r') as f:
    text = f.read()
words = re.findall(r'\w+', text.lower())
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

with open('result.txt', 'w') as f:
    for word, count in sorted_freq:
        f.write(f"{word}:{count}\n")
