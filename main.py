from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QAction, QFileDialog
# from PyQt5.QtCore.QObject import QAction
from PyQt5.QtCore import QDate, QDateTime
import csv
import matplotlib.pyplot as plt
import os.path
import numpy as np
from os import path
from datetime import date, timedelta, datetime

Form, Window = uic.loadUiType("plot.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()



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

                scaleTemperature0to100 = np.arange(0, 105, step=0.5)

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

# def dateC():
#     def daterange(start_date, end_date):
#         for n in range(int((end_date - start_date).days)):
#             yield start_date + timedelta(n)
#     start_date = form.fromDate.selectedDate().toPyDate()
#     end_date = form.tilDate.selectedDate().toPyDate()
#     for single_date in daterange(start_date, end_date):
#         temp = single_date.strftime("%d.%m.%Y")
#         print(single_date)

# def formPlot():
#     dateC()
#     displayTimePeriod()
# form.formPlot.clicked.connect(formPlot)

def openFileManager():
    fileChosen = QFileDialog.getOpenFileName()
    with open(fileChosen[0]) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';')
        array = []
        sensorsFullArray = []
        dateArray = []
        for row in csvReader:
            array.append(row)
        for row in array:
            sensorsFullArray.append(row[0])
            dateArray.append(row[1])

        # 30.10.2022 14:53 to 30.10.2022
        dateArrayCut = []
        for i in dateArray:
            cut = ' '.join(i.split(' ')[:1])
            dateArrayCut.append(cut)
        dateArrayCutCut = list(set(dateArrayCut))
        dateArrayCutCut.remove('TimeString')
        if '500001' in dateArrayCutCut:
            dateArrayCutCut.remove('500001')
        else:
            pass

        # string to date
        dateArrayCutCutStrToDate = []
        dateArrayCutCutStr = []
        for i in dateArrayCutCut:
            dateArrayCutCutStr.append(i)
            datetime_object = datetime.strptime(i, '%d.%m.%Y').date()
            dateArrayCutCutStrToDate.append(datetime_object)

        # set date from csv to qCalendar
        form.fromDate.setSelectedDate(min(dateArrayCutCutStrToDate))
        form.tilDate.setSelectedDate(max(dateArrayCutCutStrToDate))

        sensorsFullArrayCut = list(set(sensorsFullArray))
        sensorsFullArrayCut.remove('VarName')
        if '$RT_COUNT$' in sensorsFullArrayCut:
            sensorsFullArrayCut.remove('$RT_COUNT$')
        else:
            pass
        form.dropDownListSensors.clear()
        form.dropDownListSensors.addItems(sensorsFullArrayCut)



        def formPlot():
            sensorArray = []
            arrayTime = []
            arrayValue = []
            for row in array:
                if row[0] == form.dropDownListSensors.currentText():
                    sensorArray.append(row)
            # for i in sensorArray:
            #     if form.fromDate.selectedDate().toString('dd.MM.yyyy') in i[1]:
            #         arrayTime.append(i[1])
            #         arrayValue.append(i[2])

            # print(dateArrayCutCut)
            # for i in sensorArray:
            #     for i in dateArrayCutCut:
            #         arrayTime.append(i)
            #         arrayValue.append(i[2])
            # print(arrayTime)

            def daterange(selectedFromDate, selectedTilDate):
                for n in range(int((selectedTilDate - selectedFromDate).days)):
                    yield selectedFromDate + timedelta(n)
            selectedFromDate = form.fromDate.selectedDate().toPyDate()
            selectedTilDate = form.tilDate.selectedDate().toPyDate()

            #floatedValueArray = []
            for single_date in daterange(selectedFromDate, selectedTilDate):
                temp = single_date.strftime("%d.%m.%Y")

                for i in sensorArray:
                    if temp in i[1]:
                        arrayTime.append(i[1])
                        arrayValue.append(i[2])

                floatedValueArray = []
                for tofloat in arrayValue:
                    floated = float(tofloat.replace(",", "."))
                    floatedValueArray.append(floated)

            # scaleMaxValue = max(floatedValueArray)
            # print(scaleMaxValue)
            # scale = np.arange(0, scaleMaxValue, step = scaleMaxValue/10)
            scaleTemperature0to100 = np.arange(0, 105, step=5)

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

        form.formPlot.clicked.connect(formPlot)

form.openFile.triggered.connect(openFileManager)

app.exec()