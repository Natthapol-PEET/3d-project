# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Render3D_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from pyqt_loading_progressbar.loadingProgressBar import LoadingProgressBar
from PyQt5.Qt import QPainter
import pyqtgraph as pg

class Ui_MainWindow(object):
    def __init__(self) -> None:
        self.setStyleSheet("background-color: black;")
        
        ###    get size Main window  ###
        size = QtWidgets.QApplication.primaryScreen().size()
        self.height = size.height() - 150
        self.width = size.width()
        
        ###    Left MenuBar  ###
        self.leftPaneHeight = size.height
        self.leftPaneWidth = 250
        self.leftPanePositionX = 0
        self.leftPanePositionY = 0
        
        ###    Right Layout width, height  ###
        self.rightPaneHeight = int(self.height / 4)
        self.rightPaneWidth = self.leftPaneWidth
        
        self.bodyContentHeight = self.height
        self.bodyContentWidth = self.width - self.leftPaneWidth - self.rightPaneWidth
        
        ###    Right Layout posX, posY  ###
        self.rightPanePositionX = self.bodyContentWidth + self.leftPaneWidth
        self.rightPanePositionY = 500
        
        self.grid2dHeight = 0
        self.grid2dWidth = 0
        
        self.grid3dHeight = int(self.bodyContentHeight / 2)
        self.grid3dWidth = int(self.bodyContentWidth / 2)
        self.grid3dpositionX = self.grid3dWidth + self.leftPaneWidth
        self.grid3dpositionY = self.height - self.grid3dHeight
        
        self.LEFT_X = -10
        self.RIGHT_X = 0
        self.data = []
        
    def setupUi(self, MainWindow):
        ###    set size Main window  ###
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)#(w, h)
        
        ###    create centralwidget  ###
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ###    set size 2D images showing window  ###
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(self.leftPaneWidth, 0, self.bodyContentWidth, self.bodyContentHeight))#(x, y, w, h)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        ###    set all 2D images showing window margin  ###
        self.grid_2d = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_2d.setContentsMargins(0, 0, 0, 0)#(left, top, right, bottom)
        self.grid_2d.setObjectName("grid_2d")
        
        ###     Create 2D Display   ###
        self.glw_2d = pg.GraphicsLayoutWidget()
        
        ###     cross hair in ViewBox XY   ###
        self.vLine_xy = pg.InfiniteLine(angle=90, movable=False)
        self.hLine_xy = pg.InfiniteLine(angle=0, movable=False)
        
        ###     Create ViewBox, ImageItem, PlotItem XY   ###
        self.vb_xy = pg.ViewBox(enableMouse=False)
        self.qtimg_xy = pg.ImageItem()
        self.vb_xy.addItem(self.qtimg_xy)
        self.vb_xy.setContentsMargins(0.01, 0.01, 0.01, 0.01)
        self.vb_xy.addItem(self.vLine_xy)
        self.vb_xy.addItem(self.hLine_xy)
        self.plt_xy = pg.PlotItem(viewBox=self.vb_xy)
        self.plt_xy.showGrid(x=True, y=True, alpha=0.2)
        self.plt_xy.setTitle('XY Slice')
        
        ###    Show graph XY Slice  ###
        self.glw_2d.addItem(self.plt_xy, 0, 0)
        
        ###     cross hair in ViewBox XZ   ###
        self.vLine_xz = pg.InfiniteLine(angle=90, movable=False)
        self.hLine_xz = pg.InfiniteLine(angle=0, movable=False)
        
        ###     Create ViewBox, ImageItem, PlotItem XZ   ###
        self.vb_xz = pg.ViewBox(enableMouse=False)
        self.qtimg_xz = pg.ImageItem()
        self.vb_xz.setLimits(xMin=0, xMax=1000, yMin=0, yMax=500)
        self.vb_xz.addItem(self.qtimg_xz)
        self.vb_xz.setContentsMargins(0.01, 0.01, 0.01, 0.01)
        self.vb_xz.addItem(self.vLine_xz)
        self.vb_xz.addItem(self.hLine_xz)
        self.plt_xz = pg.PlotItem(viewBox=self.vb_xz)
        self.plt_xz.showGrid(x=True, y=True, alpha=0.2)
        self.plt_xz.setTitle('XZ Slice')
        
        ###    Show graph XZ Slice  ###
        self.glw_2d.addItem(self.plt_xz, 0, 1)
        
        ###     cross hair in ViewBox YZ   ###
        self.vLine_yz = pg.InfiniteLine(angle=90, movable=False)
        self.hLine_yz = pg.InfiniteLine(angle=0, movable=False)
        
        ###     Create ViewBox, ImageItem, PlotItem YZ   ###
        self.vb_yz = pg.ViewBox(enableMouse=False)
        self.qtimg_yz = pg.ImageItem()
        self.vb_yz.setLimits(xMin=0, xMax=500, yMin=0, yMax=500)
        self.vb_yz.addItem(self.qtimg_yz)
        self.vb_yz.setContentsMargins(0.01, 0.01, 0.01, 0.01)
        self.vb_yz.addItem(self.vLine_yz)
        self.vb_yz.addItem(self.hLine_yz)
        self.plt_yz = pg.PlotItem(viewBox=self.vb_yz)
        self.plt_yz.showGrid(x=True, y=True, alpha=0.2)
        self.plt_yz.setTitle('YZ Slice')
        
        ###    Show graph YZ Slice  ###
        self.glw_2d.addItem(self.plt_yz, 1, 0)

        ###    set size 3D images showing window  ###
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(self.grid3dpositionX, self.grid3dpositionY, self.grid3dWidth, self.grid3dHeight))#(aleft, atop, awidth, aheight)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        
        ###    create grid_3d oblect  ###
        self.grid_3d = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.grid_3d.setContentsMargins(0, 0, 0, 0)#(left, top, right, bottom)
        self.grid_3d.setObjectName("grid_3d")
        
        ###     Create Layout btn_load, check_box   ###
        self.btn_box_widget = QtWidgets.QWidget(self.centralwidget)
        self.btn_box_widget.setGeometry(60, 100, 150, 100)#(x, y, w, h)
        self.btn_box_layout = QtWidgets.QVBoxLayout()
        self.btn_box_widget.setLayout(self.btn_box_layout)
        self.render_3d_layout = QtWidgets.QHBoxLayout()
        
        ###    Create Load Dataset button  ###
        self.btn_load = QtWidgets.QPushButton("Open File")
        self.btn_load.setStyleSheet("background-color: blue; width: 100px; height: 50px")
        self.btn_box_layout.addWidget(self.btn_load)
        
        ###     Create Check Box and Label  ###
        label_3d = QtWidgets.QLabel()
        label_3d.setText('Render 3D ')
        self.render_3d_layout.addWidget(label_3d)
        
        self.chkbx_3d = QtWidgets.QCheckBox(self.centralwidget)
        self.chkbx_3d.setChecked(False)
        self.render_3d_layout.addWidget(self.chkbx_3d)
        self.btn_box_layout.addLayout(self.render_3d_layout)
        
        ###    Create Save button  ###
        self.btn_save = QtWidgets.QPushButton("Save", self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(80, 800, 100, 50))#(x, y, w, h)
        self.btn_save.setStyleSheet("background-color: blue")
        
        ###    unkown fuction  ###
        # self.label_dir = QtWidgets.QLabel(self.centralwidget)
        # self.label_dir.setGeometry(QtCore.QRect(1260, 1100, 121, 31))#(int x, int y, int w, int h)
        # self.label_dir.setText("")
        # self.label_dir.setObjectName("label_dir")
        
        ###    set New window button  ###
        # self.btn_new = QtWidgets.QPushButton(self.centralwidget)
        # self.btn_new.setGeometry(QtCore.QRect(1510, 850, 200, 50))#(int x, int y, int w, int h)
        # self.btn_new.setObjectName("btn_new")
        
        ###     Create Layout right of screen    ###
        self.sub_lay_v1 = QtWidgets.QVBoxLayout()
        self.sub_lay_v2 = QtWidgets.QVBoxLayout()
        self.sub_lay_v3 = QtWidgets.QVBoxLayout()
        self.main_layout_right = QtWidgets.QHBoxLayout()
        h_right_widget = QtWidgets.QWidget(self.centralwidget)
        h_right_widget.setLayout(self.main_layout_right)
        h_right_widget.setGeometry(self.rightPanePositionX, self.rightPanePositionY, self.rightPaneWidth, self.rightPaneHeight)
        
        ###    set YZ slice button  ###
        self.slider_x = QtWidgets.QSlider()
        self.slider_x.setGeometry(QtCore.QRect(1360, 100, 100, 400))#(x, y, w, h)
        self.slider_x.setOrientation(QtCore.Qt.Vertical)
        self.slider_x.setObjectName("slider_x")
        self.sub_lay_v1.addWidget(self.slider_x)
        
        ###    Create YZ value box  ###
        self.spinBox_x = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_x.setGeometry(QtCore.QRect(1360, 510, 100, 40))#(x, y, w, h)
        self.spinBox_x.setMinimum(1)
        self.spinBox_x.setMaximum(99)
        self.spinBox_x.setObjectName("spinBox_x")
        self.sub_lay_v1.addWidget(self.spinBox_x)
        
        ###    set XZ slice button  ###
        self.slider_y = QtWidgets.QSlider()
        self.slider_y.setGeometry(QtCore.QRect(1560, 100, 100, 400))#(x, y, w, h)
        self.slider_y.setOrientation(QtCore.Qt.Vertical)
        self.slider_y.setObjectName("slider_y")
        self.sub_lay_v2.addWidget(self.slider_y)
        
        ###    Create XZ value box  ###
        self.spinBox_y = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_y.setGeometry(QtCore.QRect(1560, 510, 100, 40))#(x, y, w, h)
        self.spinBox_y.setMinimum(1)
        self.spinBox_y.setObjectName("spinBox_y")
        self.sub_lay_v2.addWidget(self.spinBox_y)
        
        ###    set XY slice button  ###
        self.slider_z = QtWidgets.QSlider()
        self.slider_z.setGeometry(QtCore.QRect(1760, 100, 100, 400))#(x, y, w, h)
        self.slider_z.setOrientation(QtCore.Qt.Vertical)
        self.slider_z.setObjectName("slider_z")
        self.sub_lay_v3.addWidget(self.slider_z)
        
        ###    set XY value box  ###
        self.spinBox_z = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_z.setGeometry(QtCore.QRect(1760, 510, 100, 40))#(x, y, w, h)
        self.spinBox_z.setMinimum(1)
        self.spinBox_z.setObjectName("spinBox_z")
        self.sub_lay_v3.addWidget(self.spinBox_z)
        
        self.main_layout_right.addLayout(self.sub_lay_v1)
        self.main_layout_right.addLayout(self.sub_lay_v2)
        self.main_layout_right.addLayout(self.sub_lay_v3)
        
        ###    set YZ symbol  ###
        # self.label_x = QtWidgets.QLabel(self.centralwidget)
        # self.label_x.setGeometry(QtCore.QRect(1400, 520, 100, 100))#(int x, int y, int w, int h)
        # self.label_x.setObjectName("label_x")
        
        ###     set XZ symbol  ###
        # self.label_y = QtWidgets.QLabel(self.centralwidget)
        # self.label_y.setGeometry(QtCore.QRect(1600, 520, 100, 100))#(int x, int y, int w, int h)
        # self.label_y.setObjectName("label_y")
        
        ###     set XY symbol  ###
        # self.label_z = QtWidgets.QLabel(self.centralwidget)
        # self.label_z.setGeometry(QtCore.QRect(1800, 520, 100, 100))#(int x, int y, int w, int h)
        # self.label_z.setObjectName("label_z")
        
        ###     show interface fuction  ###
        # self.label_slider_z = QtWidgets.QLabel(self.centralwidget)
        # self.label_slider_z.setGeometry(QtCore.QRect(1000, 10, 50, 20))#(int x, int y, int w, int h)
        # self.label_slider_z.setText("")
        # self.label_slider_z.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_slider_z.setObjectName("label_slider_z")
        
        # self.label_slider_x = QtWidgets.QLabel(self.centralwidget)
        # self.label_slider_x.setGeometry(QtCore.QRect(1000, 10, 50, 20))#(int x, int y, int w, int h)
        # self.label_slider_x.setText("")
        # self.label_slider_x.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_slider_x.setObjectName("label_slider_x")
        
        # self.label_slider_y = QtWidgets.QLabel(self.centralwidget)
        # self.label_slider_y.setGeometry(QtCore.QRect(1000, 10, 50, 20))#(int x, int y, int w, int h)
        # self.label_slider_y.setText("")
        # self.label_slider_y.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_slider_y.setObjectName("label_slider_y")
        
        ###     Menu left pane  ###
        # self.leftPane = QtWidgets.QVBoxLayout(self.centralwidget)
        # self.leftPane.setContentsMargins(0, 0, 0, 0)#(left, top, right, bottom)
        
        ###     Menu right pane  ###
        # self.rightPane = QtWidgets.QHBoxLayout(self.centralwidget)
        # self.rightPane.setContentsMargins(0, 0, 0, 0)#(left, top, right, bottom)
        
        ###     Dropdown, Label Group       ###
        widget_left_1 = QtWidgets.QWidget(self.centralwidget)
        layout_v_left = QtWidgets.QVBoxLayout()
        label_mode = QtWidgets.QLabel()
        label_mode.setText('MODE')
        
        self.combobox = QtWidgets.QComboBox(self.centralwidget)
        self.combobox.setStyleSheet("background-color: green")
        self.combobox.setFixedHeight(40)
        self.combobox.setFixedWidth(100)
        self.combobox.addItems(pg.colormap.listMaps())
        self.combobox.setCurrentIndex(pg.colormap.listMaps().index('CET-L2'))
        
        layout_v_left.addWidget(label_mode)
        layout_v_left.addWidget(self.combobox)
        layout_v_left.setAlignment(label_mode, QtCore.Qt.AlignCenter)
        layout_v_left.setAlignment(self.combobox, QtCore.Qt.AlignCenter)
        widget_left_1.setLayout(layout_v_left)
        widget_left_1.setGeometry(0, 300, self.leftPaneWidth, 100)#(ax, ay, aw, ah)
        
        ###     Create Contrast Widgets     ###
        label_contrast_title = QtWidgets.QLabel()
        label_contrast_title.setText('Contrast Control')
        
        label_contrast_xy = QtWidgets.QLabel()
        label_contrast_xz = QtWidgets.QLabel()
        label_contrast_yz = QtWidgets.QLabel()
        label_contrast_xy.setText('XY')
        label_contrast_xz.setText('XZ')
        label_contrast_yz.setText('YZ')
        
        self.contrast_xy = QtWidgets.QLineEdit()
        self.contrast_xz = QtWidgets.QLineEdit()
        self.contrast_yz = QtWidgets.QLineEdit()
        
        self.contrast_xy.setValidator(QtGui.QDoubleValidator(0.0, 3.3, 2))
        self.contrast_xz.setValidator(QtGui.QDoubleValidator(0.0, 3.3, 2))
        self.contrast_yz.setValidator(QtGui.QDoubleValidator(0.0, 3.3, 2))
        
        self.contrast_xy.setText('1.5')
        self.contrast_xz.setText('1.5')
        self.contrast_yz.setText('1.5')
        
        contrast_h_1 = QtWidgets.QHBoxLayout()
        contrast_h_2 = QtWidgets.QHBoxLayout()
        contrast_h_3 = QtWidgets.QHBoxLayout()
        contrast_v_main = QtWidgets.QVBoxLayout()
        
        contrast_h_1.addWidget(label_contrast_xy)
        contrast_h_1.addWidget(self.contrast_xy)
        
        contrast_h_2.addWidget(label_contrast_xz)
        contrast_h_2.addWidget(self.contrast_xz)
        
        contrast_h_3.addWidget(label_contrast_yz)
        contrast_h_3.addWidget(self.contrast_yz)
        
        contrast_v_main.addWidget(label_contrast_title)
        contrast_v_main.setAlignment(label_contrast_title, QtCore.Qt.AlignCenter)
        contrast_v_main.addLayout(contrast_h_1)
        contrast_v_main.addLayout(contrast_h_2)
        contrast_v_main.addLayout(contrast_h_3)
        
        contrast_widget = QtWidgets.QWidget(self.centralwidget)
        contrast_widget.setLayout(contrast_v_main)
        contrast_widget.setGeometry(self.width - 240, 50, 200, 150)#(ax, ay, aw, ah)
        
        ###     Create Widget Brightness       ###
        label_brightness_title = QtWidgets.QLabel()
        label_brightness_title.setText('Brightness control')
        
        label_brightness_xy = QtWidgets.QLabel()
        label_brightness_xz = QtWidgets.QLabel()
        label_brightness_yz = QtWidgets.QLabel()
        
        label_brightness_xy.setText('XY')
        label_brightness_xz.setText('XZ')
        label_brightness_yz.setText('YZ')
        
        self.slider_brightness_xy = QtWidgets.QSlider()
        self.slider_brightness_xz = QtWidgets.QSlider()
        self.slider_brightness_yz = QtWidgets.QSlider()
        
        self.slider_brightness_xy.setMinimum(0)
        self.slider_brightness_xy.setMaximum(100)
        
        self.slider_brightness_xz.setMinimum(0)
        self.slider_brightness_xz.setMaximum(100)
        
        self.slider_brightness_yz.setMinimum(0)
        self.slider_brightness_yz.setMaximum(100)
        
        self.slider_brightness_xy.setOrientation(QtCore.Qt.Horizontal)
        self.slider_brightness_xz.setOrientation(QtCore.Qt.Horizontal)
        self.slider_brightness_yz.setOrientation(QtCore.Qt.Horizontal)
        
        brightness_h_1 = QtWidgets.QHBoxLayout()
        brightness_h_2 = QtWidgets.QHBoxLayout()
        brightness_h_3 = QtWidgets.QHBoxLayout()
        
        brightness_h_1.addWidget(label_brightness_xy)
        brightness_h_1.addWidget(self.slider_brightness_xy)
        
        brightness_h_2.addWidget(label_brightness_xz)
        brightness_h_2.addWidget(self.slider_brightness_xz)
        
        brightness_h_3.addWidget(label_brightness_yz)
        brightness_h_3.addWidget(self.slider_brightness_yz)
        
        brightness_v_layout = QtWidgets.QVBoxLayout()
        brightness_v_layout.addWidget(label_brightness_title)
        brightness_v_layout.setAlignment(label_brightness_title, QtCore.Qt.AlignCenter)
        
        brightness_v_layout.addLayout(brightness_h_1)
        brightness_v_layout.addLayout(brightness_h_2)
        brightness_v_layout.addLayout(brightness_h_3)

        brightness_widget = QtWidgets.QWidget(self.centralwidget)
        brightness_widget.setLayout(brightness_v_layout)
        brightness_widget.setGeometry(self.width - 240, 240, 200, 130)#(ax, ay, aw, ah)
        
        ###     Add Widget to MainWindows   ###
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.btn_load.setText(_translate("MainWindow", "Open File"))
        # self.btn_save.setText(_translate("MainWindow", "Save"))
        # self.btn_new.setText(_translate("MainWindow", "New Window"))
        # self.label_x.setText(_translate("MainWindow", "YZ"))
        # self.label_y.setText(_translate("MainWindow", "XZ"))
        # self.label_z.setText(_translate("MainWindow", "XY"))
        # self.chkbx_3d.setText(_translate("MainWindow", "3D Render"))
