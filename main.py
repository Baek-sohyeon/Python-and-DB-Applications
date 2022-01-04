import sys, csv, json, datetime
import xml.etree.ElementTree as ET

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pymysql
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTableWidget, QComboBox, QTableWidgetItem, \
    QAbstractItemView, QApplication, QGroupBox, QRadioButton, QMessageBox, QGridLayout


class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user ='guest', password ='bemyguest', db ='kleague', charset ='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # dictionary based cursor
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

    def updateExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user ='guest', password ='bemyguest', db ='kleague', charset ='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의

    def __init__(self):
        self.util = DB_Utils()

    def selectAllPlayer(self):
        sql = "SELECT player.*, team.TEAM_NAME FROM player LEFT JOIN team ON player.TEAM_ID = team.TEAM_ID"
        params = ()
        tuples = self.util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerTeam(self):
        sql = "SELECT DISTINCT TEAM_NAME FROM player LEFT JOIN team ON player.TEAM_ID = team.TEAM_ID WHERE TEAM_NAME IS NOT NULL"
        params = ()
        tuples = self.util.queryExecutor(db="kleague", sql=sql, params=params)
        return list(map(lambda x: x['TEAM_NAME'], tuples))

    def selectPlayerPosition(self):
        sql = "SELECT DISTINCT POSITION FROM player WHERE POSITION IS NOT NULL"
        params = ()
        tuples = self.util.queryExecutor(db="kleague", sql=sql, params=params)
        return list(map(lambda x: x['POSITION'], tuples))

    def selectPlayerNation(self):
        sql = "SELECT DISTINCT NATION FROM player WHERE NATION IS NOT NULL"
        params = ()
        tuples = self.util.queryExecutor(db="kleague", sql=sql, params=params)
        return list(map(lambda x: x['NATION'], tuples))



class DB_Updates:
    # 모든 갱신문은 여기에 각각 하나의 메소드로 정의

    def __init__(self):
        self.util = DB_Utils()

    def insertPlayer(self, player_id, player_name, team_id, position):
        sql = "INSERT INTO player (player_id, player_name, team_id, position) VALUES (%s, %s, %s, %s)"
        params = (player_id, player_name, team_id, position)
        self.util.updateExecutor(db="kleague", sql=sql, params=params)


class MainWindow(QWidget):
    ALL = "ALL"

    def __init__(self):
        super().__init__()
        self.query = DB_Queries()
        self.update = DB_Updates()
        self.setupUI()
        self.players = list()


    def makeCombobox(self, items):
        cb = QComboBox(self)
        cb.addItems([self.ALL] + items)
        return cb

    def setupUI(self):
        # 윈도우 설정

        self.setWindowTitle("Report 1 : 선수 테이블 검색")
        self.setGeometry(0, 0, 1100, 620)
        layout = QGridLayout()

        self.label1 = QLabel("선수 검색 ", self)
        self.label2 = QLabel("팀명 : ", self)
        self.label2.resize(1,1)

        self.label3 = QLabel("포지션 : ", self)
        self.label4 = QLabel("출신국 : ", self)
        self.label5 = QLabel("키 : ", self)
        self.label6 = QLabel("몸무게 : ", self)
        self.label7 = QLabel("파일 출력", self)


        self.teamCombo = self.makeCombobox(items=self.query.selectPlayerTeam())
        self.positionCombo = self.makeCombobox(items=self.query.selectPlayerPosition())
        self.nationCombo = self.makeCombobox(items=self.query.selectPlayerNation())

        self.teamCombo .setStyleSheet("background-color: orange");
        self.positionCombo.setStyleSheet("background-color: orange");
        self.nationCombo.setStyleSheet("background-color: orange");

        for Combo in self.teamCombo, self.positionCombo, self.nationCombo:
            Combo.setMinimumWidth(150)


        self.inputHeight = QLineEdit(self)
        self.inputHeight.setStyleSheet("background-color : honeydew")


        self.heightGroup = QGroupBox(parent=self, flat=True)
        self.heightGt = QRadioButton("이상", self.heightGroup, checked=True)
        self.heightLt = QRadioButton("이하", self.heightGroup)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.heightGt)
        hbox1.addWidget(self.heightLt)
        self.heightGroup.setLayout(hbox1)


        self.inputWeight = QLineEdit(self)
        self.inputWeight.setStyleSheet("background-color : honeydew")

        self.weightGroup = QGroupBox(parent=self, flat=True)
        self.weightGt = QRadioButton("이상", checked=True)
        self.weightLt = QRadioButton("이하", self.weightGroup)

        for input in self.inputWeight, self.inputHeight:
            input.setMinimumWidth(100)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.weightGt)
        hbox2.addWidget(self.weightLt)
        self.weightGroup.setLayout(hbox2)

        self.resetBtn = QPushButton("초기화", self)
        self.resetBtn.clicked.connect(self.resetBtnClicked)
        self.resetBtn.setStyleSheet("background-color: lightgrey");

        self.searchBtn = QPushButton("검색", self)
        self.searchBtn.clicked.connect(self.searchBtnClicked)
        self.searchBtn.setStyleSheet("background-color: lightgrey");

        self.tableWidget = QTableWidget(self)
        self.keyList = list(self.query.selectAllPlayer()[0].keys())
        self.tableWidget.setColumnCount(len(self.keyList))
        self.tableWidget.setHorizontalHeaderLabels(self.keyList)

        self.fileGroup = QGroupBox(parent=self, flat=True)
        self.fileCSV = QRadioButton("CSV", checked=True)
        self.fileJSON = QRadioButton("JSON")
        self.fileXML = QRadioButton("XML")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.fileCSV)
        hbox3.addWidget(self.fileJSON)
        hbox3.addWidget(self.fileXML)
        hbox3.addStretch()
        self.fileGroup.setLayout(hbox3)

        self.exportBtn = QPushButton("저장", self)
        self.exportBtn.clicked.connect(self.exportBtnClicked)
        self.exportBtn.setStyleSheet("background-color: lightgray");

        self.Group1 = QGroupBox(parent=self, flat=True)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.label2)
        hbox4.addWidget(self.teamCombo)
        hbox4.addWidget(self.label3)
        hbox4.addWidget(self.positionCombo)
        hbox4.addWidget(self.label4)
        hbox4.addWidget(self.nationCombo)
        hbox4.addStretch()
        hbox4.setAlignment(Qt.AlignCenter)
        self.Group1.setLayout(hbox4)

        self.Group2 = QGroupBox(parent=self, flat=True)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.label5)
        hbox5.addWidget(self.inputHeight)
        hbox5.addWidget(self.heightGroup)
        hbox5.addWidget(self.label6)
        hbox5.addWidget(self.inputWeight)
        hbox5.addWidget(self.weightGroup)
        hbox5.addStretch()

        self.Group2.setLayout(hbox5)

        self.Group3 = QGroupBox(parent=self, flat=True)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.resetBtn)
        vbox1.addWidget(self.searchBtn)
        vbox1.setStretch(2, 1)
        self.Group3.setLayout(vbox1)

        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.Group1, 1, 0)
        layout.addWidget(self.Group2, 2, 0)
        layout.addWidget(self.Group3, 1, 1, 2, 1)

        layout.addWidget(self.tableWidget, 3, 0, 1, 2)
        layout.addWidget(self.label7, 4, 0)
        layout.addWidget(self.fileGroup, 5, 0, 1, 1)
        layout.addWidget(self.exportBtn, 5, 1)

        self.setLayout(layout)


    def resetBtnClicked(self):
        self.teamCombo.setCurrentIndex(0)
        self.positionCombo.setCurrentIndex(0)
        self.nationCombo.setCurrentIndex(0)
        self.inputHeight.setText("")
        self.heightGt.setChecked(True)
        self.inputWeight.setText("")
        self.weightGt.setChecked(True)

    def filterPlayer(self, player):
        team = self.teamCombo.currentText()
        position = self.positionCombo.currentText()
        nation = self.nationCombo.currentText()
        height = self.inputHeight.text()
        height_gt = self.heightGt.isChecked()
        weight = self.inputWeight.text()
        weight_gt = self.weightGt.isChecked()

        if team != self.ALL and player['TEAM_NAME'] != team:
            return False

        if position != self.ALL and player['POSITION'] != position:
            return False

        if nation != self.ALL and player['NATION'] != nation:
            return False

        if height != "":
            height1 = int(height)

            try:
                heightDB = int(player['HEIGHT'])
            except TypeError:
                heightDB = 0
            if heightDB == 0:
                return False
            if height_gt:
                if heightDB < height1:
                    return False
            else:
                if heightDB > height1:
                    return False



        if weight != "":
            weight1 = int(weight)
            try:
                weightDB = int(player['WEIGHT'])
            except TypeError:
                weightDB = 0

            if weightDB == 0:
                return False
            if weight_gt:
                if weightDB < weight1:
                    return False
            else:
                if weightDB > weight1:
                    return False

        return True

    def searchBtnClicked(self):

        height = self.inputHeight.text()
        weight = self.inputWeight.text()

        try:
            int(height)
            heightInt = True

        except ValueError:
            heightInt = False
            if height=="":
                heightInt = True
            else:
                message = QMessageBox(self)
                message.setWindowTitle("Type Error")
                message.setText("정수값으로 다시 입력해주세요.")
                message.show()
                return

        try:
            int(weight)
            weightInt = True
        except ValueError:
            weightInt = False
            if weight=="":
                weightInt = True
            else:
                message = QMessageBox(self)
                message.setWindowTitle("Type Error")
                message.setText("정수값으로 다시 입력해주세요.")
                message.show()
                return

        players = list()

        for player in self.query.selectAllPlayer():
            if self.filterPlayer(player):
                players.append(player)

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(players))
        if len(players) > 0:
            for player in players:
                rowIDX = players.index(player)
                player = players[rowIDX]

                for k, v in player.items():
                    columnIDX = self.keyList.index(k)

                    if v is None:
                        if k == "POSITION":
                            v = "미정"
                        elif k == "NATION":
                            v = "대한민국"
                        else:
                            continue
                    if isinstance(v, datetime.date):
                        item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                    else:
                        item = QTableWidgetItem(str(v))
                    self.tableWidget.setItem(rowIDX, columnIDX, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.players = players


    def exportBtnClicked(self):
        players = list(map(dict, self.players))
        if len(players) == 0:
            message = QMessageBox(self)
            message.setWindowTitle("저장 실패")
            message.setText("저장할 데이터가 없습니다.")
            message.show()
            return

        if self.fileCSV.isChecked():
            with open("fileCSV.csv", "w", encoding="utf-8") as f:
                wr = csv.writer(f)
                columnNames = list(players[0].keys())
                wr.writerow(columnNames)
                for player in players:
                    valueList = list()
                    for key in self.keyList:
                        if player[key] is None:
                            valueList.append("")
                        elif isinstance(player[key], datetime.date):
                            valueList.append(player[key].strftime('%Y-%m-%d'))
                        else:
                            valueList.append(str(player[key]))
                    wr.writerow(valueList)


        elif self.fileJSON.isChecked():
            with open("fileJSON.json", "w", encoding="utf-8") as f:
                for player in players:
                    if player['BIRTH_DATE'] is None:
                        player['BIRTH_DATE'] = ''
                    else:
                        player['BIRTH_DATE'] = player['BIRTH_DATE'].strftime('%Y-%m-%d')
                json.dump(players, f)

        elif self.fileXML.isChecked():
            rootElement = ET.Element('TABLE')
            for player in players:
                rowElement = ET.Element('ROW')
                rootElement.append(rowElement)
                valueList = list()
                for key in self.keyList:
                    if player[key] is None:
                        valueList.append("")
                    elif isinstance(player[key], datetime.date):
                        valueList.append(player[key].strftime('%Y-%m-%d'))
                    else:
                        valueList.append(str(player[key]))

                for i in range(len(self.keyList)):
                    rowElement.attrib[self.keyList[i]] = valueList[i]
            ET.ElementTree(rootElement).write('fileXML.xml', encoding='utf-8', xml_declaration=True)

        message = QMessageBox(self)
        message.setWindowTitle("저장 성공")
        message.setText("저장이 성공적으로 완료되었습니다.")
        message.show()




def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


main()
