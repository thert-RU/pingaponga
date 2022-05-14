import json
a = {
    1 : ['Хитрый Гусь', 1000],
    2 : ['Шустрый Жмых', 850],
    3 : ['Низкий Гуль', 590],
    4 : ['Чиновник Антон', 360]
}


with open ("results_data.json", "w", encoding='utf-8') as file:
    json.dump(a, file)

