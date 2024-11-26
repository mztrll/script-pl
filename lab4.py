import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QTableView, QMessageBox,
    QDialog, QFormLayout, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex

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

class AddRecordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить запись")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QFormLayout(self)

        self.user_id_input = QSpinBox()
        self.title_input = QLineEdit()
        self.body_input = QTextEdit()

        self.layout.addRow("User ID:", self.user_id_input)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Body:", self.body_input)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_button)

    def add_record(self):
        user_id = self.user_id_input.value()
        title = self.title_input.text()
        body = self.body_input.toPlainText()

        if title and body:
            connection = sqlite3.connect('lab4.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)", (user_id, title, body))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена.")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Приложение с таблицей")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по заголовку...")
        self.search_field.textChanged.connect(self.update_search)

        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.load_data)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_record_dialog)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)

        self.table_view = QTableView()

        self.layout.addWidget(self.search_field)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.table_view)

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('lab4.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id, user_id, title, body FROM posts")
        data = cursor.fetchall()

        connection.close()

        self.model = DataModel(data)
        self.table_view.setModel(self.model)

    def update_search(self):
        query = self.search_field.text()
        self.model.filter_data(query)
        self.table_view.setModel(DataModel(self.model.get_filtered_data()))

    def open_add_record_dialog(self):
        dialog = AddRecordDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def delete_record(self):
        selected_indexes = self.table_view.selectedIndexes()

        if not selected_indexes:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        selected_row = selected_indexes[0].row()
        record_id = self.model.get_filtered_data()[selected_row][0]

        reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите удалить эту запись?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            connection = sqlite3.connect('lab4.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM posts WHERE id=?", (record_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "Успех", "Запись успешно удалена.")
            self.load_data()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())