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
from config import api_url

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
        table.add_row([ 4.00, 0])

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

        label2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label2.setStyleSheet("background-color: #27ae60; font-size:20px; color:#000;")

        label3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label3.setStyleSheet("background-color: #2980b9; font-size:20px; color:#000;")

        label7.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label7.setStyleSheet("background-color: #f39c12; font-size:20px; color:#000;")

        label8.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label8.setStyleSheet("background-color: #d35400; font-size:20px; color:#000;")

        label9.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label9.setStyleSheet("background-color: #c0392b; font-size:20px; color:#000;")

        #self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('BlankyMonit')  
        self.showFullScreen()  
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

        label1.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data1_label'], data['data1']))
        label2.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data2_label'], data['data2']))
        label3.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data3_label'], data['data3']))

        label7.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data4_label'], data['data4']))
        label8.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data5_label'], data['data5']))
        label9.setText("<span style='font-size:28pt;'>%s<br/></span><span style='font-size:80pt;'>%s</span>" % (data['data6_label'], data['data6']))

class WorkerThread(QtCore.QThread):
    updateData = QtCore.pyqtSignal(dict)

    def init(self):
        QtCore.QThread.init(self)

    def run(self):
        data_tb = {}
        while True:
            try: 
                req = requests.get(api_url)
                if req.status_code == 200:
                    resjson = json.loads(req.text)
                    if resjson.get('data'):
                        data_tb['chart1'] = [
                            [ 1.00, resjson['data']['chart1_list'][0]],
                            [ 2.00, resjson['data']['chart1_list'][1]],
                            [ 3.00, resjson['data']['chart1_list'][2]]
                        ]
                        data_tb['chart2'] = [
                            [ 1.00, resjson['data']['chart2_list'][0]],
                            [ 2.00, resjson['data']['chart2_list'][1]],
                            [ 3.00, resjson['data']['chart2_list'][2]]
                        ]
                        data_tb['chart3'] = [
                            [ 1.00, resjson['data']['chart3_list'][0]],
                            [ 2.00, resjson['data']['chart3_list'][1]],
                            [ 3.00, resjson['data']['chart3_list'][2]]
                        ]

                        data_tb['data1_label'] = resjson['data']['data1_label']
                        data_tb['data2_label'] = resjson['data']['data2_label']
                        data_tb['data3_label'] = resjson['data']['data3_label']
                        data_tb['data4_label'] = resjson['data']['data4_label']
                        data_tb['data5_label'] = resjson['data']['data5_label']
                        data_tb['data6_label'] = resjson['data']['data6_label']

                        data_tb['data1'] = resjson['data']['data1']
                        data_tb['data2'] = resjson['data']['data2']
                        data_tb['data3'] = resjson['data']['data3']
                        data_tb['data4'] = resjson['data']['data4']
                        data_tb['data5'] = resjson['data']['data5']
                        data_tb['data6'] = resjson['data']['data6']

                        self.updateData.emit(data_tb)
            except Exception as e:
                print(e)

            time.sleep(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainView()
    sys.exit(app.exec_())
