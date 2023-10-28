import requests

url = 'https://api.chucknorris.io/jokes/random'

response = requests.get(url)
data = response.json()

html = f'<h1>Url {data["url"]}</h1>'
html += f'<p>Значение: {data["value"]} К</p>'
html += f'<p>Время создания: {data["updated_at"]}%</p>'

print(html)
