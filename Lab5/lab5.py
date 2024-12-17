import json
import sys
import time
import sqlite3
import threading
import requests
import random
import datetime
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QWidget, QMainWindow,
    QLineEdit, QPushButton, QTableView, QLabel, QProgressBar
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtCore import QTimer


def create_database():
    conn = sqlite3.connect('lab5.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    ''')
    conn.commit()
    conn.close()


def delete_database():
    conn = sqlite3.connect('lab5.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS posts')
    conn.commit()
    conn.close()


def fetch_data():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    return response.json()


def save_data(posts):
    conn = sqlite3.connect('lab5.db')
    cursor = conn.cursor()
    for post in posts:
        cursor.execute('INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)',
                       (post['id'], post['userId'], post['title'], post['body']))
    conn.commit()
    conn.close()


def load_data():
    connection = sqlite3.connect('lab5.db')
    cursor = connection.cursor()

    cursor.execute("SELECT id, user_id, title, body FROM posts")
    data = cursor.fetchall()

    connection.close()

    return data


class DataModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ["ID", "User ID", "Title", "Body"]
                return headers[section]
        return None

    def filter_data(self, query):
        self.beginResetModel()
        self._filtered_data = [row for row in self._data if query.lower() in row[2].lower()]
        self.endResetModel()

    def get_filtered_data(self):
        return self._filtered_data if hasattr(self, '_filtered_data') else self._data


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        create_database()

    def initUI(self):

        self.setWindowTitle("Тестовое приложение")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по заголовку...")
        self.search_field.textChanged.connect(self.update_search)
        self.search_field.setVisible(False)

        self.load_button = QPushButton('Загрузить данные', self)
        self.load_button.clicked.connect(self.load_data)

        self.start_sync_button = QPushButton('Запустить синхронизацию', self)
        self.start_sync_button.clicked.connect(self.start_timer_check)
        self.start_sync_button.setVisible(False)

        self.stop_sync_button = QPushButton('Выключить синхронизацию', self)
        self.stop_sync_button.clicked.connect(self.stop_timer_check)
        self.stop_sync_button.setVisible(False)

        self.status_label = QLabel('', self)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        self.table_view = QTableView()

        self.layout.addWidget(self.search_field)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.start_sync_button)
        self.layout.addWidget(self.stop_sync_button)
        self.layout.addWidget(self.table_view)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
        self.show()

    def load_data(self):
        threading.Thread(target=self.threaded_load_data).start()

    def threaded_load_data(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText('Загрузка данных...')
        self.load_button.setEnabled(False)
        posts = fetch_data()
        with open('local_posts.json', 'w') as lpj:
            json.dump(posts, lpj)
            lpj.close()
        self.save_data(posts)
        data = load_data()
        self.model = DataModel(data)
        self.table_view.setModel(self.model)
        self.progress_bar.setVisible(False)
        self.load_button.setVisible(False)
        self.search_field.setVisible(True)
        self.start_sync_button.setVisible(True)

    def save_data(self, posts):
        time.sleep(1)
        save_data(posts)
        self.update_ui_after_save()

    def update_ui_after_save(self):
        for i in range(1, 101):
            time.sleep(random.randint(1, 10) / 1000)
            self.progress_bar.setValue(i)
        self.status_label.setText('Сохранение данных...')
        time.sleep(1)
        self.status_label.setText('Данные загружены и сохранены!')
        self.load_button.setEnabled(True)

    def update_search(self):
        threading.Thread(target=self.threaded_update_search).start()

    def threaded_update_search(self):
        query = self.search_field.text()
        self.model.filter_data(query)
        self.table_view.setModel(DataModel(self.model.get_filtered_data()))

    def start_timer_check(self):
        self.start_sync_button.setVisible(False)
        self.stop_sync_button.setVisible(True)
        self.sync()

    def sync(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(10000)  # Проверка каждые 10 секунд

    def check_for_updates(self):
        threading.Thread(target=self.threaded_update_data).start()

    def threaded_update_data(self):
        with open('posts.json') as pj:
            server_posts = json.load(pj)
            pj.close()
        with open('local_posts.json') as lpj:
            local_posts = json.load(lpj)
            lpj.close()
        check_time = datetime.datetime.now().strftime("%H:%M:%S")
        if server_posts != local_posts:
            delete_database()
            create_database()
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            with open('local_posts.json', 'w') as lpj:
                json.dump(server_posts, lpj)
                lpj.close()
            self.save_data(server_posts)
            data = load_data()
            self.model = DataModel(data)
            self.table_view.setModel(self.model)
            self.status_label.setText(f'Обновлено: {str(check_time)}. Обновления найдены')
            self.progress_bar.setVisible(False)
        else:
            self.status_label.setText(f'Обновлено: {str(check_time)}. Обновления не найдены')

    def stop_timer_check(self):
        self.start_sync_button.setVisible(True)
        self.stop_sync_button.setVisible(False)
        self.timer = QTimer()
        self.status_label.setText('Синхронизация выключена')


if __name__ == '__main__':
    delete_database()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
