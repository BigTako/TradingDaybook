from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QTableWidgetItem,QCompleter
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QIcon
import sys
import datetime
from modules.database import *
from modules.names import *
import modules.utils as utils

Form, _ = uic.loadUiType("interfaces\interface.ui")
Table, _ = uic.loadUiType("interfaces\\table_panel.ui")
Input_panel, _ = uic.loadUiType("interfaces\input_panel.ui")

class TrasactionsTable(QDialog, Table):
    def __init__(self):
        super(TrasactionsTable, self).__init__()
        self.setupUi(self)
        self.deleteButton.clicked.connect(self.ask_deleting_row)
        self.clearButton.clicked.connect(self.ask_cleaning)
        self.tableWidget.cellChanged.connect(self.change_cell_data)

    def ask_cleaning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Clearing table")
        msg.setWindowIcon(QIcon("icons/message.png"))
        msg.setText("Are you sure you want to clear the table?\nData isn't renewable!")
        msg.setStyleSheet("color:white;background-color: rgb(30, 31, 49);")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.clean_table)
        msg.setFont(utils.bahnschrift_l_c_20)
        msg.exec_()

    def ask_deleting_row(self):
        msg = QMessageBox()
        msg.setWindowTitle("Deleting row")
        msg.setWindowIcon(QIcon("icons/message.png"))
        msg.setText("Are you sure you want to delete row?\nData isn't renewable!")
        msg.setStyleSheet("color:white;background-color: rgb(30, 31, 49);")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.delete_tables_row)
        msg.setFont(utils.bahnschrift_l_c_20)
        msg.exec_()

    def clean_table(self, i):
        try:
            if (i.text() == "&Yes"):
                db = db_connect()
                mycursor = db.cursor()
                self.tableWidget.clear()
                formula = f"DROP TABLE {table_name}"
                mycursor.execute(formula)
                db.commit()
                self.tableWidget.setHorizontalHeaderLabels(columns)
        except Exception:
            QMessageBox.critical(self, "Cleaning table", str(sys.exc_info()[1]))

    def refresh_data(self):
        try:
            db = db_connect()
            mycursor = db.cursor()
            for column in columns:
                k = 0
                formula = f"SELECT {column} FROM transactions"
                mycursor.execute(formula)
                results = mycursor.fetchall()
                for el in results:
                    for i in el:
                        self.tableWidget.setItem(k, columns.index(column), QTableWidgetItem(str(i)))
                        k += 1
        except Exception:
            QMessageBox.critical(self, "Updating table data", str(sys.exc_info()[1]))

    def change_cell_data(self):
        try:
            column_index = self.tableWidget.currentColumn()
            row_index = self.tableWidget.currentRow()
            if self.tableWidget.horizontalHeaderItem(
                    column_index) is not None and self.tableWidget.currentItem() is not None:
                column_name = self.tableWidget.horizontalHeaderItem(column_index).text()
                current_cell_content = self.tableWidget.currentItem().text()
                db = db_connect()
                mycursor = db.cursor()
                formula = f"""UPDATE transactions SET {column_name.replace('.',"").casefold()} = '{current_cell_content}' WHERE id = {row_index}"""
                mycursor.execute(formula)
                db.commit()
        except Exception:
            QMessageBox.critical(self, "Changing cell data", str(sys.exc_info()[1]))


    def delete_tables_row(self,i):
        try:
            if (i.text() == "&Yes"):
                row_index = self.tableWidget.currentRow()
                db = db_connect()
                mycursor = db.cursor()
                formula = f"""DELETE FROM {table_name} WHERE id = {row_index}"""
                mycursor.execute(formula)
                db.commit()
                self.recount_id(row_index)
                self.tableWidget.removeRow(row_index)
        except Exception:
            QMessageBox.critical(self, "[ERROR] DELETING ROW", str(sys.exc_info()[1]))

    def recount_id(self, cell_index):
        try:
            db = db_connect()
            mycursor = db.cursor()
            mycursor.execute(f"SELECT MAX(id) FROM {table_name}")
            max_id = mycursor.fetchall()[0][0]
            for i in range(cell_index, max_id):
                query = f"""UPDATE {table_name}
                                    SET id = {i}
                                    WHERE id = {i + 1}"""
                mycursor.execute(query)
            db.commit()
        except Exception:
            QMessageBox.critical(self, "[ERROR] RECOUNTING ID", f"{str(sys.exc_info()[1])}\nMaybe table is already clean.")

class InputPanel(QDialog, Input_panel):
    def __init__(self):
        super(InputPanel, self).__init__()
        self.setupUi(self)
        self.submitButton.clicked.connect(self.insert_data)
        self.screenButton.clicked.connect(self.get_screendhot)
        self.cleanButton.clicked.connect(self.clean)
        self.set_compliter(assetsNames, self.assetEdit)
        self.set_compliter(assetsNames, self.newsEdit)

    def set_compliter(self, names, edit):
        completer = QCompleter(names)
        edit.setCompleter(completer)

    def get_screendhot(self):
        '''Getting screenshot function'''
        try:
            dialog = QFileDialog.getOpenFileUrl(self, "Open File Url", QUrl())[0]
            url = str(dialog.toString())
            self.urlEdit.setText(url)
        except Exception:
            QMessageBox.critical(self, "Opening table", str(sys.exc_info()[1]))

    def clean(self):
        try:
            self.newsEdit.setText('')
            self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
            self.assetEdit.setText('')
            self.situationEdit.setText('')
            self.urlEdit.setText('')
            self.detailsEdit.setText('')
        except Exception:
            QMessageBox.critical(self, "Cleaning edits", str(sys.exc_info()[1]))

    def insert_data(self):
        """function for inserting input data to database"""
        try:
            # connection to database
            db = db_connect()
            news = self.newsEdit.text()
            d = self.dateTimeEdit.date()
            date = d.toString("yyyy.MM.dd")
            t = self.dateTimeEdit.time()
            time = t.toString()
            moneym = self.moneymBox.value()
            riskm = self.riskmBox.value()
            asset = self.assetEdit.text()
            result = self.resultBox.currentText()
            exptime = self.expBox.value()
            situation = self.situationEdit.text()
            url = self.urlEdit.text()
            details = self.detailsEdit.text()
            mycursor = db.cursor()
            mycursor.execute("SELECT MAX(id) FROM transactions")
            id = mycursor.fetchall()[0][0]
            if id is None:
                id = -1
            formula = f"INSERT INTO transactions(id, news,date,time,moneym,riskm,asset,exptime,result,situation,url,details) " \
                      f"VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
            mycursor.execute(formula,
                             (id + 1, news, date, time, moneym, riskm, asset, exptime, result, situation, url, details))
            db.commit()
        except Exception:
            QMessageBox.critical(self, "Inserting data", str(sys.exc_info()[1]))

class Ui(QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.insertButton.clicked.connect(self.open_panel)
        self.editButton.clicked.connect(self.view_table)
        self.statButton.clicked.connect(self.view_statistic)
        self.view_statistic()
        self.table = TrasactionsTable()
        self.panel = InputPanel()

    def open_panel(self):
        '''Opening input panel function'''
        try:
            self.panel.clean()
            self.panel.show()
        except Exception:
            QMessageBox.critical(self, "Opening table", str(sys.exc_info()[1]))


    def clearLayout(self, layout):
        ''' clears layout from widgets'''
        try:
            while layout.count() > 0:
                item = layout.takeAt(0)
                if not item:
                    continue
                w = item.widget()
                if w:
                    w.deleteLater()
        except Exception:
            QMessageBox.critical(self, "Clearing layout", str(sys.exc_info()[1]))

    def view_statistic(self):
        ''' function which views all the data on interface '''
        try:
            self.get_patterns_statistic('win')
            self.get_patterns_statistic('exp')
            self.get_asset('win')
            self.get_asset('exp')

            self.clearLayout(self.graphicsLayout)
            self.clearLayout(self.graphics2Layout)

            self.graphicsLayout.addWidget(self.get_time_statistic("win"))
            self.graphicsLayout.addWidget(self.get_time_statistic("exp"))
            self.graphics2Layout.addWidget(self.get_asset('win')[0])
            self.graphics2Layout.addWidget(self.get_asset('exp')[0])

            win = self.get_patterns_statistic('win')
            exp = self.get_patterns_statistic('exp')
            winCount = 0
            expCount = 0
            if (win + exp):
                winCount = win * 100 // (win + exp)
                expCount = 100 - winCount
            self.winEdit.setText(str(winCount) + '%')
            self.expEdit.setText(str(expCount) + '%')
        except Exception:
            QMessageBox.critical(self, "Viewing statistic", str(sys.exc_info()[1]))

    def get_patterns_statistic(self, kind):
        '''function for getting full transactions statistic. Kind argument(win/exp)
            variant -- kind of figure,pattern etc'''
        try:
            winCount = 0
            expCount = 0
            x = 0
            db = db_connect()
            mycursor = db.cursor()
            results = []
            if kind == 'win':
                mycursor.execute('''SELECT situation FROM transactions WHERE result = "WIN"''')
                results = mycursor.fetchall()
            elif kind == 'exp':
                mycursor.execute('''SELECT situation FROM transactions WHERE result = "EXP"''')
                results = mycursor.fetchall()

            for tup in results:
                for el in tup:
                    sits = el.split(',')
                    for sit in sits:
                        if sit in figures:
                            figures[sit] = sits.count(sit)
                        elif sit in patterns:
                            patterns[sit] = sits.count(sit)
                        elif sit in direction:
                            direction[sit] = sits.count(sit)
                        elif sit in indicator:
                            indicator[sit] = sits.count(sit)

            if kind == 'win':
                winCount = len(results)
            elif (kind == 'exp'):
                expCount = len(results)

            # choosing the best patterns
            if kind == "win":
                # best figure
                f = [(value, key) for key, value in figures.items()]
                bfigure = max(f)[1]
                self.bfigureEdit.setText(str(bfigure))
                # best pattern
                p = [(value, key) for key, value in patterns.items()]
                bpattern = max(p)[1]
                self.bpatternEdit.setText(str(bpattern))
                # best direction
                d = [(value, key) for key, value in direction.items()]
                bdir = max(d)[1]
                self.bdirEdit.setText(str(bdir))
                # best indicator state
                i = [(value, key) for key, value in indicator.items()]
                bindi = max(i)[1]
                self.bindiEdit.setText(str(bindi))
                # the best combination
                self.combiEdit.setText(bfigure + " " + bpattern + " " + bdir + " " + bindi)
                return winCount

            elif kind == "exp":
                # worst pattern
                p = [(value, key) for key, value in patterns.items()]
                wpattern = max(p)[1]
                self.wpatternEdit.setText(str(wpattern))
                # worst direction
                d = [(value, key) for key, value in direction.items()]
                wdir = max(d)[1]
                self.wdirEdit.setText(str(wdir))
                return expCount
        except Exception:
            QMessageBox.critical(self, "Pattern statistic", f"{str(sys.exc_info()[1])}")

    def get_time_statistic(self, kind):
        '''Function that get time by count of transactions with them(max count times is the last)
            Also makes ChartView(circle diagram) with times(exploded max)
            kind - is result of transactions (WIN/EXP)'''
        try:
            results = 0
            db = db_connect()
            mycursor = db.cursor()
            if kind == 'win':
                mycursor.execute('''SELECT time FROM transactions WHERE result = "WIN"''')
                results = mycursor.fetchall()
            elif kind == 'exp':
                mycursor.execute('''SELECT time FROM transactions WHERE result = "EXP"''')
                results = mycursor.fetchall()

            trading_periods = periods_dict.copy()
            for times in results:
                for delta in times:
                    t = datetime.datetime.strptime(delta, "%H:%M:%S")
                    delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
                    for time in periods_dict.keys():
                        h1 = int(time.split("-")[0])
                        h2 = int(time.split("-")[1])
                        if datetime.timedelta(hours=h1, minutes=00, seconds=00) <= \
                                delta <= datetime.timedelta(hours=h2, minutes=00, seconds=00):
                            trading_periods[time] += 1

            sorted_periods = {k: v for k, v in sorted(trading_periods.items(), key=lambda item: item[1]) if (v) != 0}
            # dictionary with sorted up elements(periods)
            series = QPieSeries()
            counter = 0

            color_counter = int(255 // (len(sorted_periods) + 1))
            for period, value in sorted_periods.items():
                slice = QPieSlice()
                slice.setValue(value)
                slice.setLabel(period)
                slice.setLabelColor(Qt.white)
                slice.setLabelPosition(0)  # label inside and staying straight
                slice.setLabelFont(utils.bahnschrift_l_c_20)
                if counter == len(sorted_periods) - 1:
                    slice.setExploded(True)
                if (kind == "win"):
                    slice.setColor(utils.QColor(0, 255, 0))
                elif (kind == "exp"):
                    slice.setColor(utils.QColor(255, 0, 0))
                slice.setLabelVisible(True)
                color_counter += int(255 // len(sorted_periods))
                series.append(slice)
                counter += 1

            series.setVisible(0)
            series.setHoleSize(0.4)
            series.setPieSize(0.6)
            chart = QChart()
            chartView = QChartView(chart)
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartView.setRenderHint(QPainter.Antialiasing)
            chart.setBackgroundBrush(utils.dark_blue)
            chart.setTitleBrush(Qt.white)
            chart.setTitleFont(utils.bahnschrift_l_c_25)
            chartView.setFixedSize(QSize(350, 300))
            return chartView
        except Exception:
            QMessageBox.critical(self, "Getting time", f"{str(sys.exc_info()[1])}")


    def get_asset(self, kind):
        '''Function that get sorts an assets by count of transactions with them(max count asset is the last)
            Also makes ChartView(circle diagram) with assets(exploded max)
            kind - is result of transactions (WIN/EXP)'''
        try:
            global Index
            x = []
            db = db_connect()
            mycursor = db.cursor()

            if kind == 'win':
                mycursor.execute('''SELECT asset FROM transactions WHERE result = "WIN"''')
            elif kind == 'exp':
                mycursor.execute('''SELECT asset FROM transactions WHERE result = "EXP"''')
            results = mycursor.fetchall()

            for i in results:
                for asset in i:
                    x.append(asset)
            assets = {}
            for i in assetsNames:
                assets[i] = x.count(i)
            # choosing the best asset
            assetList = {k: v for k, v in sorted(assets.items(), key=lambda item: item[1]) if (v) != 0}
            # dict of assets with counts
            series = QPieSeries()
            color_counter = int(255 // (len(assetsNames) + 1))
            counter = 1
            for asset, count in assetList.items():
                slice = QPieSlice()
                slice.setLabel(asset)
                slice.setValue(count)
                slice.setLabelColor(Qt.white)
                slice.setLabelPosition(0)  # label outside(1-inside straight, 2 - insight not straight)
                slice.setLabelFont(utils.bahnschrift_l_c_20) # set font
                if (kind == "win"):
                    slice.setColor(utils.QColor(0, 255, 0)) # green color
                elif (kind == "exp"):
                    slice.setColor(utils.QColor(255, 0, 0)) # red color
                slice.setLabelVisible(True)
                if counter == len(assetList):
                    slice.setExploded(True)
                series.append(slice)
                color_counter += int(255 // len(assetsNames))
                counter += 1

            series.setVisible(False) # set series labels unvisible
            series.setHoleSize(0.4) # 0..1 - PieSeries inside hole diameter
            series.setPieSize(0.6)
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations) # set Animation
            chart.setBackgroundBrush(utils.dark_blue) # Chart background color
            chart.setTitleBrush(Qt.white)
            chartView = QChartView(chart)
            chartView.setRenderHint(QPainter.Antialiasing)
            chart.setTitleFont(utils.bahnschrift_l_c_25)
            chartView.setFixedSize(QSize(350, 300)) # set Chart Window's size fixed
            return chartView, assetsNames
        except Exception:
            QMessageBox.critical(self, "Getting asset",
                                 f"{str(sys.exc_info()[1])}")
    def view_table(self):
        """Function of viewing window with table of transactions"""
        try:
            self.table.refresh_data() # refill a table
            self.table.show()
            self.view_statistic()
        except Exception:
            QMessageBox.critical(self, "Viewing table", str(sys.exc_info()[1]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())

