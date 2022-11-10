import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import csv
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

Form, Window = uic.loadUiType("plot.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
errorWindow = QMessageBox()



def errors(text):
    errorWindow.setWindowTitle('Ошибка')
    errorWindow.setText(text)
    errorWindow.setIcon(QMessageBox.Warning)
    errorWindow.setStandardButtons(QMessageBox.Close)
    errorWindow.exec()

def openFileManager():
    try:
        fileChosen = QFileDialog.getOpenFileName()
        with open(fileChosen[0]) as csvFile:
            form.labelFile.setText('Файл: ' + '/'.join(fileChosen[0].split('/')[-1:]))
            try:
                csvReader = csv.reader(csvFile, delimiter=';')
                array = []
                sensorsFullArray = []
                dateArray = []
                for row in csvReader:
                    array.append(row)
                for row in array:
                    sensorsFullArray.append(row[0])
                    dateArray.append(row[1])

                dateArray.remove('TimeString')
                if '500001' in dateArray:
                    dateArray.remove('500001')
                else:
                    pass
                # 30.10.2022 14:53 to 30.10.2022
                dateArrayCut = []
                for i in dateArray:
                    cut = ' '.join(i.split(' ')[:1])
                    dateArrayCut.append(cut)
                dateArrayCutCut = list(set(dateArrayCut))
                form.labelPeriod.setText('Файл содержит данные с ' + dateArray[0] + ' по ' + dateArray[-1])

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
                    try:
                        sensorArray = []
                        arrayTime = []
                        arrayValue = []
                        for row in array:
                            if row[0] == form.dropDownListSensors.currentText():
                                sensorArray.append(row)

                        def daterange(selectedFromDate, selectedTilDate):
                            for n in range(int((selectedTilDate - selectedFromDate).days)):
                                yield selectedFromDate + timedelta(n)
                        selectedFromDate = form.fromDate.selectedDate().toPyDate()
                        dateConvert = form.tilDate.selectedDate().toPyDate()
                        selectedTilDate = dateConvert + timedelta(days = 1)

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

                        scaleMaxValue = max(floatedValueArray)
                        oneoften = scaleMaxValue/20
                        scale = np.arange(0, scaleMaxValue + oneoften, step = oneoften)

                        plt.title('PB1TT60 | График за ' + arrayTime[0] + ' - ' + arrayTime[-1], fontsize=12)
                        # plt.figure(figsize=(8, 6))
                        plt.xlabel('Time', fontsize=10)
                        plt.ylabel('Value', fontsize=10)
                        plt.plot(arrayTime, floatedValueArray)
                        plt.xticks(rotation=90)
                        plt.yticks(scale)
                        plt.grid(True)
                        periodArray = []
                        diff = len(arrayTime) / len(sensorsFullArrayCut)
                        diffRounded = round(diff) / 2
                        diffRoundedR = round(diffRounded)
                        for i in range(0, len(arrayTime), diffRoundedR):
                            periodArray.append(i)
                        plt.xticks(periodArray)
                        plt.show()

                    except UnboundLocalError:
                        errors('Неверно выбрана дата')
                    except ValueError:
                        errors('Неверно выбран промежуток времени')
                    except:
                        errors('Непредвиденная ошибка')

                form.formPlot.clicked.connect(formPlot)

            except IndexError:
                errors('Выбран неверный файл')
            except:
                errors('Непредвиденная ошибка')

    except FileNotFoundError:
        errors('Выберите файл')
    except UnicodeDecodeError:
        errors('Выберите файл с расширением .csv')
    except:
        errors('Непредвиденная ошибка')

form.openFile.triggered.connect(openFileManager)

app.exec()