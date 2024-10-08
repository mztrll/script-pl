import sqlite3
import requests


def create_db(name='lab3.db'):
    conn = sqlite3.connect(name)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS posts')

    cur.execute('''
    CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def get_posts(path='https://jsonplaceholder.typicode.com/posts'):
    r = requests.get(path)

    if r.status_code == 200:
        posts = r.json()
        return posts
    else:
        print('Подключение не удалось')
        exit()


def write_posts(posts, name='lab3.db'):
    conn = sqlite3.connect(name)
    cur = conn.cursor()

    try:
        for post in posts:
            cur.execute('INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)',
                        (int(post['id']), int(post['userId']), post['title'], post['body']))

        conn.commit()

    except Exception as e:
        print('write_posts')
        print(e)
    finally:
        conn.close()


def read_posts(name='lab3.db'):
    while True:
        try:
            user_id = int(input('Введите целое число: '))
            break
        except:
            print('Неверный ввод')
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM posts WHERE user_id = (?)', (str(user_id), ))
        posts = cur.fetchall()
        if posts:
            print('---------------------------------------------------------------')
            for post in posts:
                print('ID Поста:', post[0], end=' | ')
                print('ID Пользователя:', post[1])
                print('Заголовок:', post[2])
                print('Содержание:', post[3])
                print('---------------------------------------------------------------')
        else:
            print('У пользователя с таким ID не существует')
    except Exception as e:
        print('read_posts')
        print(e)
    finally:
        conn.close()


create_db()
write_posts(get_posts())
read_posts()
