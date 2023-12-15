from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QWidget

from messages import error

Form, Window = uic.loadUiType("sapr.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

kernels = {}
kernels_nagr = {}
nodes = {}
opora = form.comboBox_7.currentText()
print(opora)

def add_row(table):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)

def remove_row(table):
    rowPosition = table.rowCount()
    table.removeRow(rowPosition - 1)

form.pushButton_3.clicked.connect(lambda: add_row(form.tableWidget_2))
form.pushButton_4.clicked.connect(lambda: remove_row(form.tableWidget_2))

form.pushButton_5.clicked.connect(lambda: add_row(form.tableWidget_3))
form.pushButton_6.clicked.connect(lambda: remove_row(form.tableWidget_3))

form.pushButton_7.clicked.connect(lambda: add_row(form.tableWidget_4))
form.pushButton_8.clicked.connect(lambda: remove_row(form.tableWidget_4))

def get_values_kernels(table):
    kernels.clear()
    nodes.clear()
    kernels_nagr.clear()
    form.tableWidget_3.clearContents()
    form.tableWidget_4.clearContents()
    res = []
    column = []
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            try:
                column.append(float(table.item(row, col).text()))
            except:
                error("Проверьте введенные данные")
                return

        res.append(column)
        column = []

    for i in range(len(res)):
        kernels[i+1] = {}
        kernels[i+1]["width"] = res[i][0]
        kernels[i+1]["square"] = res[i][1]
        kernels[i+1]["elastic"] = res[i][2]
        kernels[i+1]["tension"] = res[i][3]

    if len(kernels) > 0:
        form.groupBox_5.setEnabled(True)
        form.groupBox_6.setEnabled(True)

    print(kernels)

def get_values_nodes(table):
    nodes.clear()
    column = []
    res = []
    print(kernels)
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            try:
                column.append(float(table.item(row, col).text()))
            except:
                error("Проверьте введенные данные")
                return

        res.append(column)
        column = []

    if len(res) > len(kernels)+1:
        error("Количество узлов превышает максимальное значение")
        return

    for i in range(len(res)):
        if res[i][0] in [j+1 for j in range(len(kernels)+1)]:
            nodes[int(res[i][0])] = res[i][1]
        else:
            error("Несуществующий узел")
            return

    print(nodes)

def get_values_kernels_nagr(table):
    kernels_nagr.clear()
    column = []
    res = []

    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            try:
                column.append(float(table.item(row, col).text()))
            except:
                error("Проверьте введенные данные")
                return

        res.append(column)
        column = []

    if len(res) > len(kernels):
        error("Количество нагрузок превышает максимальное значение")
        return

    for i in range(len(res)):
        if res[i][0] in [j+1 for j in range(len(kernels))]:
            kernels_nagr[int(res[i][0])] = res[i][1]
        else:
            error("Несуществующий стержень")
            return

    print(kernels_nagr)

form.pushButton_14.clicked.connect(lambda: get_values_kernels(form.tableWidget_2))
form.pushButton_15.clicked.connect(lambda: get_values_nodes(form.tableWidget_3))
form.pushButton_16.clicked.connect(lambda: get_values_kernels_nagr(form.tableWidget_4))


class Paint(QWidget):
    def __init__(self):
        super(Paint, self).__init__()

    def initUI(self):
        self.text = "Конструкция"
        self.setGeometry(100,100,800,800)
        self.setWindowTitle('Конструкция')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        if opora == "Слева":
            qp.drawLine(10,250,10,450)

            y1, y2 = 250, 240
            for i in range(26):
                qp.drawLine(10, y1, 0, y2)
                y1+=8
                y2+=8

        skip_x = 13
        skip_y = 300
        for kernel in kernels.items():
            qp.drawRect(skip_x, skip_y, kernel[1]["width"]*25, kernel[1]["square"]*25)
            # skip_y+=1
            skip_x += kernel[1]["width"]*25



        qp.end()

graph = Paint()

def paint(graph):
    graph.initUI()
    graph.paintEvent(graph)

form.pushButton.clicked.connect(lambda: paint(graph))

app.exec_()
