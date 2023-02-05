import sys, time, os
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph import ViewBox, ImageItem, ImageView
import matplotlib.image as mpimg

pg.setConfigOption('background', None)

from functools import partial
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
import cv2

# Import the compiled UI file
import Render3D_GUI as MainWindow
Ui_MainWindow = MainWindow.Ui_MainWindow


def my_excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)


sys.excepthook = my_excepthook

lastdir = ''

# def psi(i, j, k, offset=(50, 50, 100)):
#     x = i - offset[0]
#     y = j - offset[1]
#     z = k - offset[2]
#     th = np.arctan2(z, (x ** 2 + y ** 2) ** 0.5)
#     phi = np.arctan2(y, x)
#     r = (x ** 2 + y ** 2 + z ** 2) ** 0.5
#     a0 = 2
#     ps = (1. / 81.) * 1. / (6. * np.pi) ** 0.5 * (1. / a0) ** (3 / 2) * (r / a0) ** 2 * np.exp(-r / (3 * a0)) * (
#                 3 * np.cos(th) ** 2 - 1)

#     return ps

# data = np.fromfunction(psi, (100, 100, 200))
# positive = np.log(np.clip(data, 0, data.max()) ** 2)
# negative = np.log(np.clip(-data, 0, -data.min()) ** 2)

# d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
# d2[..., 0] = positive * (255. / positive.max())
# d2[..., 1] = negative * (255. / negative.max())
# d2[..., 2] = d2[..., 1]
# d2[..., 3] = d2[..., 0] * 0.3 + d2[..., 1] * 0.3
# d2[..., 3] = (d2[..., 3].astype(float) / 255.) ** 2 * 255

# d2[:, 0, 0] = [255, 0, 0, 100]
# d2[0, :, 0] = [0, 255, 0, 100]
# d2[0, 0, :] = [0, 0, 255, 100]


# Helper file for reading OCT image directory and flipping the axes.
def read_oct_data(filedir):
    filelist = [f for f in os.listdir(filedir) if os.path.isfile(os.path.join(filedir, f))]

    # Sort filelist by using the key that is the last integer
    filelist.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # remove the first frame since it is usually messed up
    filelist = filelist[1:]

    # todo: initialize empty array size and check if all the files have the same dimensions
    data_3d = []
    for f in filelist:
        data_3d.append(mpimg.imread(os.path.join(filedir, f)))

    data_3d = np.array(data_3d)
    # Swap from YZX (stitches of 'XZ' scans) to XYZ
    data_3d = np.moveaxis(data_3d, [0, 1, 2], [1, 2, 0])
    data_3d = np.flip(data_3d, axis=2)

    return data_3d

class Render3DApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        
        self.setupUi(self)
        
        # self.showFullScreen = True
        self.cross_section_enable = False
        
        # https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
        ###     Contrast control defual value (1.0-3.0)     ###
        self.alpha_xy = 1.0
        self.alpha_xz = 1.0
        self.alpha_yz = 1.0
        
        self.contrast_xy.textChanged.connect(self.on_contrast_change_xy)
        self.contrast_xz.textChanged.connect(self.on_contrast_change_xz)
        self.contrast_yz.textChanged.connect(self.on_contrast_change_yz)
        
        ###     Brightness control defual value (0-100)     ###
        self.beta_xy = 0
        self.beta_xz = 0
        self.beta_yz = 0
        
        self.slider_brightness_xy.valueChanged.connect(self.on_brightness_change_xy)
        self.slider_brightness_xz.valueChanged.connect(self.on_brightness_change_xz)
        self.slider_brightness_yz.valueChanged.connect(self.on_brightness_change_yz)

        # configure PyQTgraph
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')

        ###     set mouseMoved XY       ###
        proxy_xy = pg.SignalProxy(self.vb_xy.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMovedXY)
        self.vb_xy.scene().sigMouseMoved.connect(self.mouseMovedXY)
        
        ###     set mouseMoved XZ       ###
        proxy_xz = pg.SignalProxy(self.vb_xz.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMovedXZ)
        self.vb_xz.scene().sigMouseMoved.connect(self.mouseMovedXZ)
        
        ###     set mouseMoved YZ       ###
        proxy_yz = pg.SignalProxy(self.vb_yz.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMovedYZ)
        self.vb_yz.scene().sigMouseMoved.connect(self.mouseMovedYZ)
        
        ###     3D Display  ###
        self.glview = gl.GLViewWidget()
        self.glview.opts['center'] = pg.Vector(0, 0, 0)
        self.glview.opts['distance'] = 1000
        self.glview.setWindowTitle('pyqtgraph example: GLVolumeItem')

        ###     ตาราง 2D   ###
        self.gl_grid = gl.GLGridItem()
        self.gl_grid.setSize(x=10, y=10)
        self.gl_grid.scale(50, 50, 1)
        self.glview.addItem(self.gl_grid)

        ###     Render Object   ###
        self.glitem = gl.GLVolumeItem(np.zeros((100, 100, 200, 4)))
        self.glview.addItem(self.glitem)
        
        ###     Add Widget to grid_2d, grid_3d   ###
        self.grid_2d.addWidget(self.glw_2d, 0, 0)
        self.grid_3d.addWidget(self.glview, 0, 0)
        
        self.data_3d = []
        self.data_4d = []

        self.btn_load.clicked.connect(self.load_data)
        self.btn_save.clicked.connect(self.save_screenshot)
        # self.btn_new.clicked.connect(startApp)

        self.slider_x.valueChanged.connect(self.set_x)
        self.slider_y.valueChanged.connect(self.set_y)
        self.slider_z.valueChanged.connect(self.set_z)
        
        self.slider_x.setEnabled(False)
        self.slider_y.setEnabled(False)
        self.slider_z.setEnabled(False)

        self.spinBox_x.valueChanged.connect(self.update_range_x)
        self.spinBox_y.valueChanged.connect(self.update_range_y)
        self.spinBox_z.valueChanged.connect(self.update_range_z)

        self.combobox.currentTextChanged.connect(self.current_color_changed)
        
    def save_screenshot(self):
        if not self.isFullScreen(): self.showFullScreen()
        QtCore.QTimer.singleShot(1000, self.screenshot)
        
    def screenshot(self):
        self.preview_screen = QtWidgets.QApplication.primaryScreen().grabWindow(0)
        self.preview_screen.save("src/screenshot.png", "png")
        self.showNormal()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.cross_section_enable = not self.cross_section_enable
        
    def mouseMovedXY(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_xy.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_xy.mapSceneToView(pos)
            self.vLine_xy.setPos(mousePoint.x())
            self.hLine_xy.setPos(mousePoint.y())
            
    def mouseMovedXZ(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_xz.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_xz.mapSceneToView(pos)
            self.vLine_xz.setPos(mousePoint.x())
            self.hLine_xz.setPos(mousePoint.y())
            
    def mouseMovedYZ(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_yz.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_yz.mapSceneToView(pos)
            self.vLine_yz.setPos(mousePoint.x())
            self.hLine_yz.setPos(mousePoint.y())
            
    def current_color_changed(self, s):
        self.qtimg_xy.setColorMap(s)
        self.qtimg_xz.setColorMap(s)
        self.qtimg_yz.setColorMap(s)
        
    def load_3d(self, is_show_3d):
        if is_show_3d and len(self.data_3d):
            self.data_4d = np.zeros((self.data_3d.shape[0], self.data_3d.shape[1], self.data_3d.shape[2], 4))

            # todo: This works, but add manual options
            self.data_4d[..., 0] = self.data_3d[...]
            self.data_4d[..., 1] = 0
            self.data_4d[..., 2] = 0
            self.data_4d[..., 3] = self.data_3d[...] / 5.0

            # v = gl.GLVolumeItem(self.data_4d)
            self.glitem.resetTransform()
            self.glitem.setData(self.data_4d)
            self.glitem.translate(-self.data_4d.shape[0] / 2, -self.data_4d.shape[1] / 2,
                                  -0 * self.data_4d.shape[2] / 2)

    def load_data(self):
        global lastdir
        lastdir = '/Users/70007742/Documents/dev/Code/3d-project/acne'
        if not lastdir:
            dialog = QtWidgets.QFileDialog(directory=os.path.expanduser(os.path.join('~','/Users/70007742/Documents/dev/Code/3d-project/acne')))
        else:
            dialog = QtWidgets.QFileDialog(directory=lastdir)
        dialog.setAcceptMode(1)
        targetdir = dialog.getExistingDirectory(self, "Select Directory")
        
        if targetdir != '':
            lastdir = os.path.dirname(targetdir)

            self.data_3d = read_oct_data(targetdir)

            self.load_3d(self.chkbx_3d.isChecked())
            
            self.cross_section_enable = True
            self.vb_xy.setMouseEnabled(x=True, y=True)
            self.vb_xz.setMouseEnabled(x=True, y=True)
            self.vb_yz.setMouseEnabled(x=True, y=True)

            self.slider_x.setMinimum(0)
            self.slider_x.setMaximum(self.data_3d.shape[0]-self.spinBox_x.value())
            self.slider_y.setMinimum(0)
            self.slider_y.setMaximum(self.data_3d.shape[1]-self.spinBox_y.value())
            self.slider_z.setMinimum(0)
            self.slider_z.setMaximum(self.data_3d.shape[2]-self.spinBox_z.value())

            self.slider_x.setEnabled(True)
            self.slider_y.setEnabled(True)
            self.slider_z.setEnabled(True)

            self.slider_x.setValue(int(self.data_3d.shape[0]/2))
            self.slider_y.setValue(int(self.data_3d.shape[1]/2))
            self.slider_z.setValue(int(self.data_3d.shape[2]/2))

            # self.label_dir.setText(targetdir)
            
    def update_range_x(self, avg):
        self.slider_x.setMinimum(0)
        self.slider_x.setMaximum(self.data_3d.shape[0] - avg)
        self.set_x(self.slider_x.value())

    def update_range_y(self, avg):
        self.slider_y.setMinimum(0)
        self.slider_y.setMaximum(self.data_3d.shape[1] - avg)
        self.set_y(self.slider_y.value())

    def update_range_z(self, avg):
        self.slider_z.setMinimum(0)
        self.slider_z.setMaximum(self.data_3d.shape[2] - avg)
        self.set_z(self.slider_z.value())

    def set_x(self, x):
        # self.label_slider_x.setText(str(x))
        navg = self.spinBox_x.value()
        self.img_xy = np.squeeze(np.nanmean(self.data_3d[int(x):int(x)+navg, :, :], 0))
        w, h = self.img_xy.shape
        self.vb_xy.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        self.qtimg_xy.setImage(self.img_xy)
        
    def set_y(self, y):
        # self.label_slider_y.setText(str(y))
        navg = self.spinBox_y.value()
        self.img_xz = np.squeeze(np.nanmean(self.data_3d[:, int(y):int(y)+navg, :], 1))
        w, h = self.img_xz.shape
        self.vb_xz.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        self.qtimg_xz.setImage(self.img_xz)

    def set_z(self, z):
        # self.label_slider_z.setText(str(z))
        navg = self.spinBox_z.value()
        self.img_yz = np.squeeze(np.nanmean(self.data_3d[:, :, int(z):int(z)+navg], 2))
        w, h = self.img_yz.shape
        self.vb_yz.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        self.qtimg_yz.setImage(self.img_yz)
        
    def on_contrast_change_xy(self, v):
        self.alpha_xy = float(v)
        adjusted = cv2.convertScaleAbs(self.img_xy, alpha=self.alpha_xy, beta=self.beta_xy)
        self.qtimg_xy.setImage(adjusted)
    
    def on_contrast_change_xz(self, v):
        self.alpha_xz = float(v)
        adjusted = cv2.convertScaleAbs(self.img_xz, alpha=self.alpha_xz, beta=self.beta_xz)
        self.qtimg_xz.setImage(adjusted)
    
    def on_contrast_change_yz(self, v):
        self.alpha_yz = float(v)
        adjusted = cv2.convertScaleAbs(self.img_yz, alpha=self.alpha_yz, beta=self.beta_yz)
        self.qtimg_yz.setImage(adjusted)
        
    def on_brightness_change_xy(self, v):
        self.beta_xy = v
        adjusted = cv2.convertScaleAbs(self.img_xy, alpha=self.alpha_xy, beta=self.beta_xy)
        self.qtimg_xy.setImage(adjusted)
        
    def on_brightness_change_xz(self, v):
        self.beta_xz = v
        adjusted = cv2.convertScaleAbs(self.img_xz, alpha=self.alpha_xz, beta=self.beta_xz)
        self.qtimg_xz.setImage(adjusted)
    
    def on_brightness_change_yz(self, v):
        self.beta_yz = v
        adjusted = cv2.convertScaleAbs(self.img_yz, alpha=self.alpha_yz, beta=self.beta_yz)
        self.qtimg_yz.setImage(adjusted)


def startApp():
    global windows
    windows.append(Render3DApp())
    windows[-1].setWindowTitle('3D OCT Rendering #%d' % len(windows))
    windows[-1].show()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windows = []
    startApp()
    sys.exit(app.instance().exec())
