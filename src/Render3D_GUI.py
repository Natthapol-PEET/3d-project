# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Render3D_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(object):
    def __init__(self) -> None:
        self.setStyleSheet("background-color: black; ; color: white;")
        
        ###    get size Main window  ###
        size = QtWidgets.QApplication.primaryScreen().size()
        # self.height = size.height() - 150
        self.height = size.height() - 100
        self.width = size.width()
        
        ###    Left MenuBar  ###
        self.leftPaneHeight = size.height
        self.padding_all = 30
        self.leftPanePositionX = 0
        self.leftPanePositionY = 0
        
        ###    Right Layout width, height  ###
        self.right_panel_height = int(self.height / 4)
        self.padding_right = 300
        
        self.body_content_height = self.height - self.padding_all - self.padding_all
        self.body_content_width = self.width - self.padding_all - self.padding_right
        
        ###    Right Layout posX, posY  ###
        self.rightPanePositionX = self.body_content_width + self.padding_all
        self.rightPanePositionY = 500
        
        self.grid2dHeight = 0
        self.grid2dWidth = 0
        
        self.grid3dHeight = int(self.body_content_height / 2)
        self.grid3dWidth = int(self.body_content_width / 2)
        self.grid3dpositionX = self.grid3dWidth + self.padding_all
        self.grid3dpositionY = self.height - self.grid3dHeight
        
        self.LEFT_X = -10
        self.RIGHT_X = 0
        self.data = []
        
        self.color_map_obj = {
            'plasma': 'plasma',
            'inferno': 'inferno',
            'binary': 'CET-C5',
            'gray': 'CET-L2',
            'hot red': 'CET-L3',
            'green': 'CET-L5',
            'pink': 'CET-L17',
            'jet': 'CET-R4',
            'blue': 'CET-CBL2',
        }
        
        self.color_map_current = list(self.color_map_obj.keys())[0]
        
    def setupUi(self, MainWindow):
        ###    set size Main window  ###
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)#(w, h)
        
        ###    create centralwidget  ###
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ###    set size 2D images showing window  ###
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(self.padding_all, self.padding_all, self.body_content_width, self.body_content_height))#(x, y, w, h)
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
        self.plt_xy.setTitle('YZ Slice')
        
        ###    Show graph XY Slice  ###
        self.glw_2d.addItem(self.plt_xy, 0, 1)
        
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
        self.glw_2d.addItem(self.plt_xz, 1, 0)
        
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
        self.plt_yz.setTitle('XY Slice')
        
        ###    Show graph YZ Slice  ###
        self.glw_2d.addItem(self.plt_yz, 0, 0)

        ###    set size 3D images showing window  ###
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(self.grid3dpositionX, self.grid3dpositionY, self.grid3dWidth, self.grid3dHeight))#(aleft, atop, awidth, aheight)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        
        ###    create grid_3d oblect  ###
        self.grid_3d = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.grid_3d.setContentsMargins(20, 0, 0, 20)#(left, top, right, bottom)
        self.grid_3d.setObjectName("grid_3d")
        
        ###     Create Layout btn_load, check_box   ###
        self.btn_box_widget = QtWidgets.QWidget(self.centralwidget)
        self.btn_box_widget.setGeometry(self.width - 230, 100, 150, 100)#(x, y, w, h)
        self.btn_box_layout = QtWidgets.QVBoxLayout()
        self.btn_box_widget.setLayout(self.btn_box_layout)
        self.render_3d_layout = QtWidgets.QHBoxLayout()
        
        ###    Create Load Dataset button  ###
        self.btn_load = QtWidgets.QPushButton("Open File")
        self.btn_load.setStyleSheet("background-color: blue; width: 100px; height: 50px; color: white;")
        self.btn_box_layout.addWidget(self.btn_load)
        
        ###     Create Check Box and Label  ###
        label_3d = QtWidgets.QLabel()
        label_3d.setText('Render 3D ')
        self.render_3d_layout.addWidget(label_3d)
        
        self.chkbx_3d = QtWidgets.QCheckBox(self.centralwidget)
        self.chkbx_3d.setChecked(False)
        self.render_3d_layout.addWidget(self.chkbx_3d)
        self.btn_box_layout.addLayout(self.render_3d_layout)
        
        ###     Dropdown, Label Group       ###
        widget_left_1 = QtWidgets.QWidget(self.centralwidget)
        layout_v_left = QtWidgets.QVBoxLayout()
        label_mode = QtWidgets.QLabel()
        label_mode.setText('MODE')
        
        self.combobox = QtWidgets.QComboBox(self.centralwidget)
        self.combobox.setEnabled(False)
        self.combobox.setStyleSheet("background-color: green; color: white;")
        self.combobox.setFixedHeight(40)
        self.combobox.setFixedWidth(100)
        self.combobox.addItems(list(self.color_map_obj.keys()))
        
        layout_v_left.addWidget(label_mode)
        layout_v_left.addWidget(self.combobox)
        layout_v_left.setAlignment(label_mode, QtCore.Qt.AlignCenter)
        layout_v_left.setAlignment(self.combobox, QtCore.Qt.AlignCenter)
        widget_left_1.setLayout(layout_v_left)
        widget_left_1.setGeometry(self.width - 230, 230, 150, 100)#(ax, ay, aw, ah)
        
        ###     Create Contrast Widgets     ###
        label_contrast_title = QtWidgets.QLabel()
        label_contrast_title.setText('Contrast Control')
        
        self.label_contrast_val = QtWidgets.QLabel()
        
        self.contrast_val = QtWidgets.QSlider()
        self.contrast_val.setEnabled(False)
        
        self.contrast_val.setMinimum(10)
        self.contrast_val.setMaximum(30)
        
        self.contrast_val.setOrientation(QtCore.Qt.Horizontal)
        
        contrast_h_1 = QtWidgets.QHBoxLayout()
        contrast_h_1.addWidget(self.label_contrast_val)
        contrast_h_1.addWidget(self.contrast_val)
        
        contrast_v_main = QtWidgets.QVBoxLayout()
        contrast_v_main.addWidget(label_contrast_title)
        contrast_v_main.setAlignment(label_contrast_title, QtCore.Qt.AlignCenter)
        contrast_v_main.addLayout(contrast_h_1)
        
        contrast_widget = QtWidgets.QWidget(self.centralwidget)
        contrast_widget.setLayout(contrast_v_main)
        contrast_widget.setGeometry(self.width - 240, 360, 200, 100)#(ax, ay, aw, ah)
        
        ###     Create Widget Brightness       ###
        label_brightness_title = QtWidgets.QLabel()
        label_brightness_title.setText('Brightness control')
        
        self.label_brightness_val = QtWidgets.QLabel()
        
        self.slider_brightness_val = QtWidgets.QSlider()
        self.slider_brightness_val.setEnabled(False)
        
        self.slider_brightness_val.setMinimum(0)
        self.slider_brightness_val.setMaximum(100)
        
        self.slider_brightness_val.setOrientation(QtCore.Qt.Horizontal)
        
        brightness_h_1 = QtWidgets.QHBoxLayout()
        brightness_h_1.addWidget(self.label_brightness_val)
        brightness_h_1.addWidget(self.slider_brightness_val)
        
        brightness_v_layout = QtWidgets.QVBoxLayout()
        brightness_v_layout.addWidget(label_brightness_title)
        brightness_v_layout.setAlignment(label_brightness_title, QtCore.Qt.AlignCenter)
        brightness_v_layout.addLayout(brightness_h_1)

        brightness_widget = QtWidgets.QWidget(self.centralwidget)
        brightness_widget.setLayout(brightness_v_layout)
        brightness_widget.setGeometry(self.width - 240, 440, 200, 100)#(ax, ay, aw, ah)
        
        ###     Create Widget navg       ###
        label_navg_title = QtWidgets.QLabel()
        label_navg_title.setText('NAVG control')
        
        self.label_navg_val = QtWidgets.QLabel()
        
        self.slider_navg_val = QtWidgets.QSlider()
        self.slider_navg_val.setEnabled(False)
        
        self.slider_navg_val.setMinimum(1)
        self.slider_navg_val.setMaximum(99)
        
        self.slider_navg_val.setOrientation(QtCore.Qt.Horizontal)
        
        navg_h_1 = QtWidgets.QHBoxLayout()
        navg_h_1.addWidget(self.label_navg_val)
        navg_h_1.addWidget(self.slider_navg_val)
        
        navg_v_layout = QtWidgets.QVBoxLayout()
        navg_v_layout.addWidget(label_navg_title)
        navg_v_layout.setAlignment(label_navg_title, QtCore.Qt.AlignCenter)
        navg_v_layout.addLayout(navg_h_1)

        navg_widget = QtWidgets.QWidget(self.centralwidget)
        navg_widget.setLayout(navg_v_layout)
        navg_widget.setGeometry(self.width - 240, 520, 200, 100)#(ax, ay, aw, ah)
        
        ###    Create Save button  ###
        self.btn_save = QtWidgets.QPushButton("Save", self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(self.width - 200, 800, 100, 50))#(x, y, w, h)
        self.btn_save.setStyleSheet("background-color: blue; color: white;")
        self.btn_save.setEnabled(False)
        
        ###     Dropdown, Label Group       ###
        widget_left_1 = QtWidgets.QWidget(self.centralwidget)
        layout_main_left = QtWidgets.QVBoxLayout()
        
        list_rotate = ['0', '90', '180', '270']
        
        layout_v_xy_left = QtWidgets.QHBoxLayout()
        label_xy = QtWidgets.QLabel()
        label_xy.setText('Rotate XY : ')
        
        self.combobox_rotate_xy = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_rotate_xy.setEnabled(False)
        self.combobox_rotate_xy.setStyleSheet("background-color: green; color: white;")
        self.combobox_rotate_xy.setFixedHeight(40)
        self.combobox_rotate_xy.setFixedWidth(100)
        self.combobox_rotate_xy.addItems(list_rotate)
        
        layout_v_xy_left.addWidget(label_xy)
        layout_v_xy_left.addWidget(self.combobox_rotate_xy)
        layout_v_xy_left.setAlignment(self.combobox_rotate_xy, QtCore.Qt.AlignmentFlag.AlignRight)
        layout_main_left.addLayout(layout_v_xy_left)
        
        layout_v_xz_left = QtWidgets.QHBoxLayout()
        label_xz = QtWidgets.QLabel()
        label_xz.setText('Rotate XZ : ')
        
        self.combobox_rotate_xz = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_rotate_xz.setEnabled(False)
        self.combobox_rotate_xz.setStyleSheet("background-color: green; color: white;")
        self.combobox_rotate_xz.setFixedHeight(40)
        self.combobox_rotate_xz.setFixedWidth(100)
        self.combobox_rotate_xz.addItems(list_rotate)
        
        layout_v_xz_left.addWidget(label_xz)
        layout_v_xz_left.addWidget(self.combobox_rotate_xz)
        layout_v_xz_left.setAlignment(self.combobox_rotate_xz, QtCore.Qt.AlignmentFlag.AlignRight)
        layout_main_left.addLayout(layout_v_xz_left)
        
        layout_v_yz_left = QtWidgets.QHBoxLayout()
        label_yz = QtWidgets.QLabel()
        label_yz.setText('Rotate YZ : ')
        
        self.combobox_rotate_yz = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_rotate_yz.setEnabled(False)
        self.combobox_rotate_yz.setStyleSheet("background-color: green; color: white;")
        self.combobox_rotate_yz.setFixedHeight(40)
        self.combobox_rotate_yz.setFixedWidth(100)
        self.combobox_rotate_yz.addItems(list_rotate)
        
        layout_v_yz_left.addWidget(label_yz)
        layout_v_yz_left.addWidget(self.combobox_rotate_yz)
        layout_v_yz_left.setAlignment(self.combobox_rotate_yz, QtCore.Qt.AlignmentFlag.AlignRight)
        layout_main_left.addLayout(layout_v_yz_left)
        
        widget_left_1.setLayout(layout_main_left)
        widget_left_1.setGeometry(self.width - 250, 615, 210, 150)#(ax, ay, aw, ah)

        ###     Add Widget to MainWindows   ###
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
