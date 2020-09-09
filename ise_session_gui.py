import sys
import requests
import xmltodict
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic


#Link : Qt5 UI File
# - condition : The UI file should be located in the sam directory as the this file
form_class = uic.loadUiType("./ise_session.ui")[0]

# Class Define : UI Open
class ISE_Session():
    def __init__(self, ip, id, pwd):
        self.ip = ip
        self.id = id
        self.pwd = pwd

    def getActiveSession(self):
        url = "https://%s/admin/API/mnt/Session/ActiveList" % self.ip

        ret_state, ret_val = self.request_action("get", url, self.id, self.pwd)
        return ret_state, ret_val

    def deleteSessionByMAC(self, MAC):
        url = "https://%s/admin/API/mnt/Session/Delete/MACAddress/%s" % (self.ip, MAC)
        ret_state, ret_val = self.request_action("delete", url, self.id, self.pwd)

        return ret_state, ret_val

    def request_action(self, request_type, url, id, pwd, ):
        print("\t Request URL : %s %s" % (request_type, url))
        print("\t Request ID/PWD : [%s][%s]" % (id, pwd))

        session = requests.Session()
        session.auth = (id, pwd)
        if request_type == "get":
            response = session.get(url, verify=False)
        elif request_type == "delete":
            response = session.delete(url, verify=False)
        else:
            return 000, "unknow error"
        
        ret_val = None
        if response.status_code == 401:
            ret_val = "Auth failed"
        elif response.status_code != 200:
            ret_val = "Error code %s " % (response.status_code)
        else:
            ret_val = xmltodict.parse(response.text)
        return response.status_code, ret_val

        

class MyWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.lineEdit_IP.setText("10.200.150.212")
        self.lineEdit_ID.setText("admin")
        self.lineEdit_PWD.setText("Comtec123")

         # Linking functions to buttons
        self.pushButton.clicked.connect(self.button1Function)

    def button1Function(self):
        ISE_IP = self.lineEdit_IP.text()
        ISE_ID = self.lineEdit_ID.text()
        ISE_PWD = self.lineEdit_PWD.text()

        print("[MyWindow] button1Function() - [%s][%s][%s]" % (ISE_IP, ISE_ID, ISE_PWD))
        ise_session = ISE_Session(ISE_IP, ISE_ID, ISE_PWD)
        ret_state, ret_val = ise_session.getActiveSession()

        if ret_state != 200:
            QMessageBox.about(self, "에러", "%s" % (ret_val) )
        else:
            print("[MyWindow] button1Function() - %s" % (ret_state))
            
            session_count = 0
            session_list = []
            if ret_val is not None and "activeList" in ret_val:
                session_count = ret_val['activeList']['@noOfActiveSession']
                if session_count == "1":
                    ret = ret_val['activeList']['activeSession']
                    session = {}
                    session['user_name'] = ret['user_name'] if 'user_name' in ret else '!!!'
                    session['mac'] = ret['calling_station_id'] if 'calling_station_id' in ret else '!!!'
                    session['ip'] = ret['framed_ip_address'] if 'framed_ip_address' in ret else '!!!'
                    session['sw_ip'] = ret['nas_ip_address'] if 'nas_ip_address' in ret else '!!!'
                    session_list.append(session)
                    print("\t%s" % (session))
                else:
                    for ret in ret_val['activeList']['activeSession']:
                        session = {}
                        session['user_name'] = ret['user_name'] if 'user_name' in ret else '!!!'
                        session['mac'] = ret['calling_station_id'] if 'calling_station_id' in ret else '!!!'
                        session['ip'] = ret['framed_ip_address'] if 'framed_ip_address' in ret else '!!!'
                        session['sw_ip'] = ret['nas_ip_address'] if 'nas_ip_address' in ret else '!!!'
                        session_list.append(session)
                        print("\t%s" % (session))
            
            self.Set_Table(["user_name", "mac", "ip", "sw_ip"], session_list)

    def click_btn(self, btnClass, MAC):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Are you soure you want to delete session on MAC(%s)" % (MAC))
        msgBox.setWindowTitle("warring")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            ISE_IP = self.lineEdit_IP.text()
            ISE_ID = self.lineEdit_ID.text()
            ISE_PWD = self.lineEdit_PWD.text()
            ise_session = ISE_Session(ISE_IP, ISE_ID, ISE_PWD)
            ret_state, ret_val = ise_session.deleteSessionByMAC(MAC)
            if ret_state == 200:
                if ret_val is not None and "mnt-rest-result" in ret_val:
                    if "status" in ret_val["mnt-rest-result"]:
                        btnClass.setEnabled(False)
                        return
            QMessageBox.about(self, "Error[%s]" % ret_state, "%s" % (ret_val) )
                
        pass

    def Set_Table(self, head_list, data_list):
        self.tableWidget.setRowCount(len(data_list))
        self.tableWidget.setColumnCount(len(head_list)+1)
        self.tableWidget.setHorizontalHeaderLabels([" "]+head_list)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 130)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 130)
        self.tableWidget.setColumnWidth(4, 130)
        col_count = 0
        row_count = 0
        for table_data in data_list:
            col_count = 0
            btnDelete = QPushButton("Delete")
            btnDelete.MAC = table_data['mac']
            btnDelete.clicked.connect(partial(self.click_btn, btnDelete, table_data['mac']))
            #btnDelete.clicked.connect(self.click_btn)
            self.tableWidget.setCellWidget(row_count, col_count, btnDelete)
            col_count = 1
            for column_name in head_list:
                column_val = table_data[column_name] if column_name in table_data else '!!!'
                tableitem = QTableWidgetItem(column_val)
                tableitem.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_count, col_count, tableitem)
                col_count = col_count + 1
            row_count = row_count + 1


if __name__ == "__main__" :
    #QApplication : run the servic
    app = QApplication(sys.argv) 

    #created the instance to WindowClass
    myWindow = MyWindow() 

    #show UI
    myWindow.show()

    #Run Program
    app.exec_()