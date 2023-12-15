from PyQt5.QtWidgets import QMessageBox


def error(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Ошибка")
    msg.setInformativeText(text)
    msg.setWindowTitle("Ошибка")
    msg.exec_()
