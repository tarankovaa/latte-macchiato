import sqlite3
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from addEditCoffeeForm import Ui_MainWindow as Ui_Form
from main_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('data/coffee.sqlite')
        self.cursor = self.connection.cursor()
        self.load_table()
        self.tableWidget.cellDoubleClicked.connect(self.show_form)

    def load_table(self):
        items = self.cursor.execute('SELECT * FROM Information').fetchall()
        for i, row in enumerate(items):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def show_form(self, row, column):
        self.form = Form()
        self.form.show()
        self.id = self.tableWidget.item(row, 0).text()
        items = self.cursor.execute("""SELECT * FROM Information
            WHERE id = ?""", (self.id, )).fetchone()
        self.form.id_edit.setText(str(items[0]))
        self.form.sort_edit.setText(items[1])
        self.form.roast_edit.setText(items[2])
        self.form.type_edit.setText(items[3])
        self.form.taste_edit.setText(items[4])
        self.form.price_edit.setText(str(items[5]))
        self.form.volume_edit.setText(str(items[6]))
        self.form.save_btn_1.clicked.connect(self.save)
        self.form.save_btn_2.clicked.connect(self.save)

    def save(self):
        if self.sender() == self.form.save_btn_1:
            items = (self.form.id_edit.text(), self.form.sort_edit.text(), self.form.roast_edit.text(),
                     self.form.type_edit.text(), self.form.taste_edit.text(), self.form.price_edit.text(),
                     self.form.volume_edit.text())
            try:
                self.cursor.execute("""UPDATE Information
            SET id = ?, sort = ?, roast = ?, type = ?, taste = ?, price = ?, volume = ?
            WHERE id = ?""", items + (self.id, ))
                self.connection.commit()
                self.load_table()
                self.form.close()
            except sqlite3.IntegrityError:
                self.form.statusBar().showMessage('Неверно заполнена форма')
        elif self.sender() == self.form.save_btn_2:
            items = (self.form.id_add.text(), self.form.sort_add.text(), self.form.roast_add.text(),
                     self.form.type_add.text(), self.form.taste_add.text(), self.form.price_add.text(),
                     self.form.volume_add.text())
            try:
                self.cursor.execute(f'INSERT INTO Information VALUES{items}')
                self.connection.commit()
                self.load_table()
                self.form.close()
            except sqlite3.IntegrityError:
                self.form.statusBar().showMessage('Неверно заполнена форма')

    def closeEvent(self, event):
        self.con.close()


class Form(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(400, 310)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
