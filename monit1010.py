import sys
import time
import json
import requests
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication)
from PyQt5.QtGui import QFont, QColor
from PyQt5 import QtCore
from PyQtCharts.qcharts import (PieChart, ScatterChart, LineChart, AreaChart,
                    DataTable, DialogViewer, Viewer)

label1 = None
label2 = None
label3 = None
label7 = None
label8 = None
label9 = None
chart1 = None
chart2 = None
chart3 = None
chart4 = None
grid = None

class MainView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.workerthread = WorkerThread()
        self.workerthread.updateData.connect(self.updateData)
        self.workerthread.start()
    
    def init_chartAnalityc(self, bgcolor, data=[[ 1.00, 120], [ 2.00, 270], [ 3.00,  50]]):
        table = DataTable()
        table.add_column('Time')
        table.add_column('Unique')
        table.add_row(data[0])
        table.add_row(data[1])
        table.add_row(data[2])

        chart = LineChart(table)
        chart.set_horizontal_axis_column(0)
        chart.haxis_title = 'Time'
        chart.haxis_vmin = 1.0
        chart.haxis_vmax = 3.0
        chart.haxis_step = 1
        chart_viewer = Viewer()
        chart_viewer.set_graph(chart)
        p = chart_viewer.palette()
        p.setColor(chart_viewer.backgroundRole(), QColor(bgcolor))
        chart_viewer.setAutoFillBackground(True);
        chart_viewer.setPalette(p)
        return {'chart': chart_viewer, 'table': table}

    def initUI(self):
        global label1, label2, label3, label7, label8, label9
        global chart1, chart2, chart3, chart4, grid

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor('#bdc3c7'))
        self.setAutoFillBackground(True);
        self.setPalette(p)

        label1 = QLabel('label1')
        label2 = QLabel('label2')
        label3 = QLabel('label3')
        label7 = QLabel('label7')
        label8 = QLabel('label8')
        label9 = QLabel('label9')

        grid = QGridLayout()
        grid.setSpacing(5)

        chart1 = self.init_chartAnalityc('#00aba9')
        chart2 = self.init_chartAnalityc('#f1c40f')
        chart3 = self.init_chartAnalityc('#e67e22')

        grid.addWidget(label1,0,0)
        grid.addWidget(label2,0,1)
        grid.addWidget(label3,0,2)
        grid.addWidget(chart1['chart'],1,0) 
        grid.addWidget(chart2['chart'],1,1) 
        grid.addWidget(chart3['chart'],1,2) 
        grid.addWidget(label7,2,0) 
        grid.addWidget(label8,2,1) 
        grid.addWidget(label9,2,2)         
        self.setLayout(grid) 

        label1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label1.setStyleSheet("background-color: #16a085; font-size:20px; color:#000;")
        label1.setText("<span style='font-size:28pt;'>AutoDownload<br/> Online:<br/></span><span style='font-size:80pt;'>800</span>")

        label2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label2.setStyleSheet("background-color: #27ae60; font-size:20px; color:#000;")
        label2.setText("<span style='font-size:28pt;'>Link4share<br/> Online:<br/></span><span style='font-size:80pt;'>600</span>")

        label3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label3.setStyleSheet("background-color: #2980b9; font-size:20px; color:#000;")
        label3.setText("<span style='font-size:28pt;'>Apkpoke<br/> Online:<br/></span><span style='font-size:80pt;'>500</span>")

        label7.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label7.setStyleSheet("background-color: #f39c12; font-size:20px; color:#000;")
        label7.setText("<span style='font-size:28pt;'>Api 4shared:<br/></span><span style='font-size:80pt;'>Error!</span>")

        label8.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label8.setStyleSheet("background-color: #d35400; font-size:20px; color:#000;")
        label8.setText("<span style='font-size:28pt;'>Server Status:<br/></span><span style='font-size:80pt;'>OK!</span>")

        label9.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label9.setStyleSheet("background-color: #c0392b; font-size:20px; color:#000;")
        label9.setText("<span style='font-size:28pt;'>Transaksi Laundry<br/>(Today):<br/></span><span style='font-size:80pt;'>0</span>")

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Monit1010')    
        self.show()

    def updateData(self, data):
        global chart1, chart2, chart3, chart4, grid
        grid.removeWidget(chart1['chart'])
        chart1['chart'].close()
        chart1 = self.init_chartAnalityc('#00aba9', data['chart1'])
        grid.addWidget(chart1['chart'],1,0) 

        grid.removeWidget(chart2['chart'])
        chart2['chart'].close()
        chart2 = self.init_chartAnalityc('#f1c40f', data['chart2'])
        grid.addWidget(chart2['chart'],1,1) 

        grid.removeWidget(chart3['chart'])
        chart3['chart'].close()
        chart3 = self.init_chartAnalityc('#e67e22', data['chart3'])
        grid.addWidget(chart3['chart'],1,2) 

        label1.setText("<span style='font-size:28pt;'>AutoDownload<br/> Online:<br/></span><span style='font-size:80pt;'>%s</span>" % data['autodownload_online'])
        label2.setText("<span style='font-size:28pt;'>Link4share<br/> Online:<br/></span><span style='font-size:80pt;'>%s</span>" % data['link4share_online'])
        label3.setText("<span style='font-size:28pt;'>Apkpoke<br/> Online:<br/></span><span style='font-size:80pt;'>%s</span>" % data['apkpoke_online'])

        label7.setText("<span style='font-size:28pt;'>Api 4shared:<br/></span><span style='font-size:80pt;'>%s</span>" % data['api4shared_status'])
        label8.setText("<span style='font-size:28pt;'>Server Status:<br/></span><span style='font-size:80pt;'>%s</span>" % data['server_status'])
        label9.setText("<span style='font-size:28pt;'>Transaksi Laundry<br/>(Today):<br/></span><span style='font-size:80pt;'>%s</span>" % data['laundry_today'])

class WorkerThread(QtCore.QThread):
    updateData = QtCore.pyqtSignal(dict)

    def init(self):
        QtCore.QThread.init(self)

    def run(self):
        data_tb = {}
        while True:
            try: 
                req = requests.get('http://188.166.184.127:1000/data_status')
                if req.status_code == 200:
                    resjson = json.loads(req.text)
                    if resjson.get('data'):
                        data_tb['chart1'] = [
                            [ 1.00, resjson['data']['autodownload_list'][0]],
                            [ 2.00, resjson['data']['autodownload_list'][1]],
                            [ 3.00, resjson['data']['autodownload_list'][2]]
                        ]
                        data_tb['chart2'] = [
                            [ 1.00, resjson['data']['link4share_list'][0]],
                            [ 2.00, resjson['data']['link4share_list'][1]],
                            [ 3.00, resjson['data']['link4share_list'][2]]
                        ]
                        data_tb['chart3'] = [
                            [ 1.00, resjson['data']['apkpoke_list'][0]],
                            [ 2.00, resjson['data']['apkpoke_list'][1]],
                            [ 3.00, resjson['data']['apkpoke_list'][2]]
                        ]
                        data_tb['autodownload_online'] = resjson['data']['autodownload_online']
                        data_tb['link4share_online'] = resjson['data']['link4share_online']
                        data_tb['apkpoke_online'] = resjson['data']['apkpoke_online']
                        data_tb['api4shared_status'] = resjson['data']['api4shared_status']
                        data_tb['server_status'] = resjson['data']['server_status']
                        data_tb['laundry_today'] = 0
                        self.updateData.emit(data_tb)
            except Exception as e:
                print(e)

            time.sleep(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainView()
    sys.exit(app.exec_())
