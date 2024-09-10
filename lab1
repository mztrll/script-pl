import requests
import json

print('---------------------------------------------------------------')
print('------------------------GET - запрос---------------------------')
print('---------------------------------------------------------------')

r = requests.get('https://jsonplaceholder.typicode.com/posts')

if r.status_code == 200:
    posts = r.json()

    for post in posts:
        if post['userId'] % 2 == 0:
            print('ID Пользователя:', post['userId'], end= ' | ')
            print('ID Поста:', post['id'])
            print('Заголовок:', post['title'])
            print('Содержание:', post['body'])
            print('---------------------------------------------------------------')

    '''for post in posts:
        if post['userId'] % 2 == 0:
            print(post)'''
    print('')
else:
    print('Ошибка')

print('---------------------------------------------------------------')
print('-----------------------POST - запрос---------------------------')
print('---------------------------------------------------------------')

test_post = {'userId': 52, 'id': 101, 'title': 'Тестовый пост', 'body': 'Тело тестового поста'}

r = requests.post('https://jsonplaceholder.typicode.com/posts', test_post)

if r.status_code == 201:
    print('Успешно\nПост:', r.json())
    print('---------------------------------------------------------------\n')
else:
    print('Ошибка')

print('---------------------------------------------------------------')
print('------------------------PUT - запрос---------------------------')
print('---------------------------------------------------------------')

post_id = 52
post_update = {'title': 'Обновлённый пост'}
r = requests.put(f'https://jsonplaceholder.typicode.com/posts/{post_id}', json=post_update)

if r.status_code == 200:
    print('Успешно\nОбновлённый пост:', r.json())
    print('---------------------------------------------------------------\n')
else:
    print('Ошибка')
