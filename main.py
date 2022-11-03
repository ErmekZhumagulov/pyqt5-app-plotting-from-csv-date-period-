from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QAction, QFileDialog
# from PyQt5.QtCore.QObject import QAction
from PyQt5.QtCore import QDate, QDateTime
import csv
import matplotlib.pyplot as plt
import os.path
import numpy as np
from os import path
from datetime import date, timedelta

Form, Window = uic.loadUiType("plot.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()



# changable
scaleTemperature0to100 = np.arange(0, 105, step=5)

def displayTimePeriod():
    for i in range(0, 99):
        filePath = r'C:\Users\User\PycharmProjects\plotting\Data Logs\Первичная пастеризация' + str(i) + '.csv'
        fileExists = path.exists(filePath)
        if fileExists == True:
            with open('Первичная пастеризация' + str(i) + '.csv') as csvFile:
                csvReader = csv.reader(csvFile, delimiter=';')
                array = []
                arrayTime = []
                arrayValue = []
                for row in csvReader:
                    if row[0] == 'Sensors\AI-2.VALUE.10_PB1TT60':
                        array.append(row)
                for i in array:
                    if form.fromDate.selectedDate().toString('dd.MM.yyyy') in i[1]:
                        arrayTime.append(i[1])
                        arrayValue.append(i[2])

                floatedValueArray = []
                for tofloat in arrayValue:
                    floated = float(tofloat.replace(",", "."))
                    floatedValueArray.append(floated)

                plt.title('PB1TT60 | График за ' + form.fromDate.selectedDate().toString('dd.MM.yyyy'), fontsize=12)
                # plt.figure(figsize=(8, 6))
                plt.xlabel('Time', fontsize=10)
                plt.ylabel('Value', fontsize=10)
                plt.plot(arrayTime, floatedValueArray)
                plt.xticks(rotation=60)
                plt.yticks(scaleTemperature0to100)
                plt.grid(True)
                periodArray = []
                for i in range(0, 11 * 1440, 11 * 40):
                    periodArray.append(i)
                plt.xticks(periodArray)
                plt.show()
            break

def dateC():
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    start_date = form.fromDate.selectedDate().toPyDate()
    end_date = form.tilDate.selectedDate().toPyDate()
    for single_date in daterange(start_date, end_date):
        temp = single_date.strftime("%d.%m.%Y")
        print(temp)

def formPlot():
    dateC()
    displayTimePeriod()
form.formPlot.clicked.connect(formPlot)

def openFileManager():
    fileChosen = QFileDialog.getOpenFileName()
    with open(fileChosen[0]) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';')
        sensorsFullArray = []
        for row in csvReader:
            sensorsFullArray.append(row[0])
        sensorsFullArrayCut = list(set(sensorsFullArray))
        sensorsFullArrayCut.remove('VarName')
        if '$RT_COUNT$' in sensorsFullArrayCut:
            sensorsFullArrayCut.remove('$RT_COUNT$')
        else:
            pass
        print(sensorsFullArrayCut)
        form.dropDownListSensors.clear()
        form.dropDownListSensors.addItems(sensorsFullArrayCut)
form.openFile.triggered.connect(openFileManager)

app.exec()