import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import threading
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox,
                             QLineEdit, QFileDialog, QDateEdit, QCheckBox)

from PyQt5.QtGui import QDoubleValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Тестовое приложение")
        self.setGeometry(400, 400, 1000, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.load_button = QPushButton("Загрузить данные из CSV")
        self.load_button.clicked.connect(self.load_data)

        self.stats_label = QLabel("")
        self.stats_label.setVisible(False)

        self.diagram_type_label = QLabel("Тип графика:")
        self.diagram_type_combo = QComboBox()
        self.diagram_type_combo.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])
        self.diagram_type_combo.currentIndexChanged.connect(self.update_graph)

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)

        self.category_combo_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["A", "B", "C", "D"])

        self.input_value1 = QLineEdit()
        self.input_value1.setPlaceholderText("Введите значение 1")
        self.input_value1.textEdited.connect(self.check_inputs)

        self.input_value2 = QLineEdit()
        self.input_value2.setPlaceholderText("Введите значение 2")
        self.input_value2.textEdited.connect(self.check_inputs)

        self.boolean_flag = QCheckBox("Логическое значение")

        self.update_button = QPushButton("Добавить")
        self.update_button.clicked.connect(self.update_graph)
        self.update_button.setEnabled(False)

        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.diagram_type_label)
        self.hbox_layout.addWidget(self.diagram_type_combo)
        self.hbox_layout.addWidget(self.date_edit)
        self.hbox_layout.addWidget(self.category_combo_label)
        self.hbox_layout.addWidget(self.category_combo)
        self.hbox_layout.addWidget(self.input_value1)
        self.hbox_layout.addWidget(self.input_value2)
        self.hbox_layout.addWidget(self.boolean_flag)
        self.hbox_layout.addWidget(self.update_button)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.main_layout.addWidget(self.load_button)
        self.main_layout.addWidget(self.stats_label)
        self.main_layout.addLayout(self.hbox_layout)
        self.main_layout.addWidget(self.canvas)

        self.show()

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")

        if file_path:
            self.data = pd.read_csv(file_path)
            self.stats_label.setVisible(True)
            self.display_statistics()
            self.update_graph()

    def display_statistics(self):
        if self.data is not None:
            stats = f"Количество записей: {len(self.data)}\n"
            stats += f"Количество столбцов: {len(self.data.columns)}\n"
            stats += f"Минимальные значения:\n{self.data.min()}\n"
            stats += f"Максимальные значения:\n{self.data.max()}\n"
            self.stats_label.setText(stats)

    def check_inputs(self):
        threading.Thread(target=self.threaded_check_inputs).start()

    def threaded_check_inputs(self):
        value1 = self.input_value1.text()
        value2 = self.input_value2.text()
        if self.data is not None and value1 != '' and value2 != '':
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    def update_graph(self):
        threading.Thread(target=self.threaded_update_graph).start()

    def threaded_update_graph(self):
        self.input_value1.clear()
        self.input_value2.clear()
        self.update_button.setEnabled(False)

        if self.data is not None:
            diagram_type = self.diagram_type_combo.currentText()
            date = str(self.date_edit.text())
            category = str(self.category_combo.currentText())
            value1 = self.input_value1.text()
            value2 = self.input_value2.text()
            boolean_flag = str(self.boolean_flag.isChecked())
            print(1)
            if value1 != '' and value2 != '':
                new_row = pd.DataFrame({"Date": [date], "Category": [category], "Value1": [value1],
                                        "Value2": [value2], "BooleanFlag": [boolean_flag]})
                self.data = pd.concat([self.data, new_row], ignore_index=True)

            self.figure.clear()
            ax = self.figure.add_subplot()

            if diagram_type == "Линейный график":
                ax.plot(self.data["Date"], self.data["Value1"], label='Value1', marker='X')
                ax.tick_params(axis='x', rotation=45)
                ax.set_title('Линейный график')
                ax.set_xlabel('Дата')
                ax.set_ylabel('Значение 1')

            elif diagram_type == "Гистограмма":
                ax.hist(self.data["Value2"])
                ax.tick_params(axis='x', rotation=45)
                ax.set_title('Гистограмма')
                ax.set_xlabel('Значение 2')
                ax.set_ylabel('Частота')

            elif diagram_type == "Круговая диаграмма":
                category_counts = self.data['Category'].value_counts()
                ax.pie(category_counts, labels=category_counts.index)
                ax.set_title('Круговая диаграмма по категориям')

            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
