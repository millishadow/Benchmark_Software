# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 21:23:38 2023

@author: 64634
"""
import sys  
import pandas as pd  
import plotly.graph_objects as go  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QInputDialog  
from PyQt5.QtGui import QIcon  
from PyQt5.QtCore import Qt  
  
class MyApp(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
        self.data = pd.DataFrame()  # 初始化一个空的DataFrame用于存储数据  
        self.highlighted_data = None  # 用于存储高亮显示的数据 
  
    def initUI(self):  
        self.setWindowTitle('车型项目管理与分析系统')  # 设置窗口标题  
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小  
        self.setWindowIcon(QIcon('icon.png'))  # 设置窗口图标，需要准备一个icon.png文件  
        layout = QVBoxLayout()  # 创建一个垂直布局管理器  
        # 设置样式表，应用简洁扁平的UI风格  
        self.setStyleSheet("""  
            QWidget {  
                background-color: white;  
                border: none;  
                font: bold 14px;  
                color: black;  
            }  
            QPushButton {  
                border: 2px solid black;  
                border-radius: 5px;  
                padding: 10px;  
                margin: 5px;  
            }  
        """)  
  
        # 创建读取数据按钮，并连接点击事件到read_data函数  
        btn1 = QPushButton('读取数据', self)  
        btn1.clicked.connect(self.read_data)  
        layout.addWidget(btn1)  # 将按钮添加到布局中  
  
        # 创建绘制图表按钮，并连接点击事件到plot_data函数  
        btn2 = QPushButton('绘制图表', self)  
        btn2.clicked.connect(self.plot_data)  
        layout.addWidget(btn2)  # 将按钮添加到布局中  
  
        # 创建添加新数据按钮，并连接点击事件到add_entry函数  
        btn3 = QPushButton('添加新数据', self)  
        btn3.clicked.connect(self.add_entry)  
        layout.addWidget(btn3)  # 将按钮添加到布局中  
  
        # 创建保存更改按钮
        btn4 = QPushButton('保存更改', self)  
        btn4.clicked.connect(self.save_data)  # 这里连接到一个尚未定义的save_data函数，需要实现该函数或注释掉这行代码  
        layout.addWidget(btn4)  # 将按钮添加到布局中 
 
        # 创建显示统计数据的按钮
        btn5 = QPushButton('显示统计数据', self)  
        btn5.clicked.connect(self.show_statistics)  # 连接点击事件到show_statistics函数  
        layout.addWidget(btn5)  # 将按钮添加到布局中  
  
        self.setLayout(layout)  # 设置窗口的布局管理器为上面创建的布局对象  
        self.show()  # 显示窗口  
  
    def read_data(self):  
        # 弹出一个文件选择对话框，让用户选择CSV文件，并返回选择的文件路径和文件类型  
        fname, _ = QFileDialog.getOpenFileName(self, '选择CSV文件', '.', 'CSV Files (*.csv)')  
        if fname:  # 如果用户选择了文件  
            try:  
                self.data = pd.read_csv(fname)  # 读取CSV文件数据到DataFrame中  
                self.data.columns = ["车型项目名称", "前排座椅模态性能", "前排座椅重量"]  # 重命名DataFrame的列名  
                QMessageBox.information(self, '信息', '数据读取成功！')  # 弹出一个信息对话框提示用户数据读取成功  
            except pd.errors.EmptyDataError:  
                QMessageBox.critical(self, '错误', '文件为空或格式不正确！')  
            except Exception as e:  
                QMessageBox.critical(self, '错误', f'读取数据时出错：{e}')  
  
    def plot_data(self):  
        if self.data.empty:  # 如果DataFrame为空，即没有读取过数据  
            QMessageBox.warning(self, '警告', '请先读取数据！')  # 弹出一个警告对话框提示用户先读取数据  
            return  # 结束函数执行  
        # 使用Plotly创建一个图表对象，并添加散点图轨迹，x轴为前排座椅模态性能，y轴为前排座椅重量，点的大小和颜色根据车型项目名称确定  
        fig = go.Figure()  
        fig.add_trace(go.Scatter(x=self.data["前排座椅模态性能"], y=self.data["前排座椅重量"], mode='markers', marker_color=self.data["车型项目名称"]))  
        fig.update_layout(title='车型项目与性能及重量的关系', xaxis_title='前排座椅模态性能', yaxis_title='前排座椅重量')  # 更新图表的布局和标题等属性  
        fig.show()  # 显示图表  
        # 如果有高亮数据显示，则设置高亮  
        if self.highlighted_data:  
            fig.update_traces(marker_color=[(1 if (row.车型项目名称 == self.highlighted_data[0]) and (row.前排座椅模态性能 == self.highlighted_data[1]) and (row.前排座椅重量 == self.highlighted_data[2]) else 0) for row in self.data.itertuples()],  
                      selector=dict(type='scatter', mode='markers'))  
            self.plot_widget.setPlot(fig)  
        
       
    def add_entry(self):
        project_name, ok = QInputDialog.getText(self, '输入', '请输入车型项目名称:')  
        if ok and project_name:  
            performance, ok = QInputDialog.getDouble(self, '输入', '请输入前排座椅模态性能:')  
            if ok:  
                weight, ok = QInputDialog.getDouble(self, '输入', '请输入前排座椅重量:')  
                if ok:  
                    new_entry = {"车型项目名称": [project_name], "前排座椅模态性能": [performance], "前排座椅重量": [weight]}  
                    self.data = pd.concat([self.data, pd.DataFrame(new_entry)])  
                    self.highlighted_data = (project_name, performance, weight)  # 存储新添加的数据用于高亮显示  
                    self.plot_data()  


    def save_data(self):  
        # 这里只是一个简单的保存方法，您可能需要更复杂的保存逻辑（例如保存到数据库）  
        fname, _ = QFileDialog.getSaveFileName(self, '保存CSV文件', '.', 'CSV Files (*.csv)')  
        if fname:  
            self.data.to_csv(fname, index=False)  
            QMessageBox.information(self, '信息', '数据保存成功！')
            
    def show_statistics(self):  
        statistics = self.data.describe()  # 使用pandas的describe方法计算统计数据  
        statistics_window = QWidget()  
        statistics_layout = QVBoxLayout()  
        statistics_window.setWindowTitle('统计数据')  
  
        # 将统计数据添加到新的窗口中  
        statistics_text = QWidget()  
        statistics_text.setPlainText(str(statistics))  
        statistics_layout.addWidget(statistics_text)  
  
        btn_close = QPushButton('关闭', statistics_window)  
        btn_close.clicked.connect(statistics_window.close)  
        statistics_layout.addWidget(btn_close)  
  
        statistics_window.setLayout(statistics_layout)  
        statistics_window.show()


if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    window = MyApp()  
    sys.exit(app.exec_())