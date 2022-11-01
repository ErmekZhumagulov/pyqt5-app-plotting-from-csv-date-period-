from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("dateChoice.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

def onClick():
    print(form.calendarWidget.dateTime().toString('dd.mm.yyyy'))
    #print('clicked')
form.pushButton.clicked.connect(onClick)

app.exec()