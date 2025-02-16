import requests


# "Тест"
# response = requests.get('http://localhost:5000')


# "Cоздание пользователя"
# response = requests.post('http://localhost:5000/api/v1/user',
#                             json={'username': 'test',
#                                   'password': 'test545656'}
#                          )
# "Получение пользователя"
# response = requests.get('http://localhost:5000/api/v1/user/1')

# "Обновление пользователя"
# response = requests.patch('http://localhost:5000/api/v1/user/1',
#                           json={'password': 'testtest'}
#                           )
# "Удаление пользователя"
# response = requests.delete('http://localhost:5000/api/v1/user/1')

# "Создание объявления"
# response = requests.post('http://localhost:5000/api/v1/advertisement',
#                             json={'owner_id': 2,
#                                   'title': 'Продам машину',
#                                   'description': 'в хорошем состоянии'}
#                          )

# "Получение объявления"
# response = requests.get('http://localhost:5000/api/v1/advertisement/1')

# "Получение всех объявлений"
# response = requests.get('http://localhost:5000/api/v1/advertisement')

# "Обновление объявления"
# response = requests.patch('http://localhost:5000/api/v1/advertisement/2',
#                           json={'title': 'Продам квартиру',
#                                 'description': 'Продам квартиру в хорошем состоянии'}
#                           )

# "Удаление объявления"
# response = requests.delete('http://localhost:5000/api/v1/advertisement/2')

# print(response.text)
# print(response.status_code)