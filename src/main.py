import sys, os
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import matplotlib.image as mpimg

pg.setConfigOption('background', None)

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
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
    try: filelist.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    except: filelist.sort(key=lambda x: int(x.split('.')[0][-1]))

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
        self.lock_cross = True
        
        # https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
        ###     Contrast control defual value (1.0-3.0)     ###
        self.alpha = 1.0
        self.label_contrast_val.setText(str(self.alpha))
        self.contrast_val.setValue(int(self.alpha * 10))
        self.contrast_val.valueChanged.connect(self.on_contrast_change_val)
        
        ###     Brightness control defual value (0-100)     ###
        self.beta = 0
        self.label_brightness_val.setText(str(self.beta))
        self.slider_brightness_val.setValue(self.beta)
        self.slider_brightness_val.valueChanged.connect(self.on_brightness_change_val)

        ###     navg control defual value (0-100)     ###
        self.navg_val = 1
        self.label_navg_val.setText(str(self.navg_val))
        self.slider_navg_val.setValue(self.navg_val)
        self.slider_navg_val.valueChanged.connect(self.on_navg_change_val)

        ###     Rotate xy, xz, yz  (0, 90, 180, 270)   ###
        self.flag_rotate_xy = 0
        self.flag_rotate_xz = 0
        self.flag_rotate_yz = 0
        
        self.mouse_set_x = 0
        self.mouse_set_y = 0
        self.mouse_set_z = 0
        
        self.combobox_rotate_xy.currentTextChanged.connect(self.on_rotate_xy_change)
        self.combobox_rotate_xz.currentTextChanged.connect(self.on_rotate_xz_change)
        self.combobox_rotate_yz.currentTextChanged.connect(self.on_rotate_yz_change)

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

        self.combobox.currentTextChanged.connect(self.on_color_changed)
        
    def play_sound(self):
        self.player = QMediaPlayer()
        full_file_path = os.path.join(os.getcwd(), 'sound', 'shutter-sound.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        
        self.player.setMedia(content)
        self.player.play()
        
    def save_screenshot(self):
        initial_path = os.getcwd()
        
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
            "Save Image", initial_path, "Image Files(*.png)", options=options)
        
        if fileName == '': return
        save_path = fileName + '.png'
        
        self.play_sound()
        
        # save_path = os.path.join(os.getcwd(), 'src', 'screenshot.png')
        self.centralwidget.grab().save(save_path)
        
        img = cv2.imread(save_path)
        height, width, _ = img.shape
        
        cal_size = (width / self.width) * (self.body_content_width + self.padding_all)

        crop_img = img[0:height, 0:int(cal_size)]
        cv2.imwrite(save_path, crop_img)
        
        # winname = 'save screenshot'
        # cv2.namedWindow(winname)
        # cv2.moveWindow(winname, int((self.width-self.body_content_width)/2), 0)
        # cv2.imshow(winname, crop_img)
        # cv2.waitKey(3000)
        # cv2.destroyAllWindows()

        # if not self.isFullScreen(): self.showFullScreen()
        # QtCore.QTimer.singleShot(1000, self.screenshot)
        
    def screenshot(self):
        self.preview_screen = QtWidgets.QApplication.primaryScreen().grabWindow(0)
        self.preview_screen.save("src/screenshot.png", "png")
        self.showNormal()
        
    def keyPressEvent(self, event):
        if self.lock_cross: return
        if event.key() == QtCore.Qt.Key_Shift:
            self.cross_section_enable = not self.cross_section_enable
            
    def mousePressEvent(self, event):
        if self.lock_cross: return
        if event.button() == QtCore.Qt.LeftButton:
            self.cross_section_enable = not self.cross_section_enable

    def mouseMovedXY(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_xy.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_xy.mapSceneToView(pos)
            self.vLine_xy.setPos(mousePoint.x())
            self.hLine_xy.setPos(mousePoint.y())
            
            # self.vLine_yz.setPos(mousePoint.x())
            self.hLine_yz.setPos(mousePoint.y())
            
            self.hLine_xz.setPos(self.data_3d.shape[1] - mousePoint.x())
            # self.vLine_xz.setPos(mousePoint.x())
            
            self.mouse_set_z = self.data_3d.shape[2] - mousePoint.x()
            self.mouse_set_y = self.data_3d.shape[1] - mousePoint.y()
            
            self.set_z(self.mouse_set_z)
            self.set_y(self.mouse_set_y)
            
    def mouseMovedXZ(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_xz.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_xz.mapSceneToView(pos)
            self.vLine_xz.setPos(mousePoint.x())
            self.hLine_xz.setPos(mousePoint.y())
            
            self.vLine_xy.setPos(self.data_3d.shape[1] - mousePoint.y())
            # self.vLine_xy.setPos(mousePoint.x())
            
            # self.hLine_yz.setPos(mousePoint.y())
            self.vLine_yz.setPos(mousePoint.x())
            
            self.mouse_set_x = mousePoint.x()
            self.mouse_set_y = mousePoint.y()
            
            self.set_x(self.mouse_set_x)
            self.set_z(self.mouse_set_y)
            
    def mouseMovedYZ(self, evt):
        if not self.cross_section_enable: return
        pos = evt.toPoint()
        if self.vb_yz.sceneBoundingRect().contains(pos):
            mousePoint = self.vb_yz.mapSceneToView(pos)
            self.vLine_yz.setPos(mousePoint.x())
            self.hLine_yz.setPos(mousePoint.y())
            
            self.hLine_xy.setPos(mousePoint.y())
            self.vLine_xy.setPos(0)
            
            self.hLine_xz.setPos(0)
            self.vLine_xz.setPos(mousePoint.x())
            
            self.mouse_set_x = mousePoint.x()
            self.mouse_set_y = self.data_3d.shape[1] - mousePoint.y()
            
            self.set_x(self.mouse_set_x)
            self.set_y(self.mouse_set_y)
            
    def on_color_changed(self, s):
        self.color_map_current = s
        self.qtimg_xy.setColorMap((self.color_map_obj[self.color_map_current]))
        self.qtimg_xz.setColorMap((self.color_map_obj[self.color_map_current]))
        self.qtimg_yz.setColorMap((self.color_map_obj[self.color_map_current]))
        
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
        lastdir = os.path.join(os.getcwd(), 'dataset')
        if not lastdir:
            dialog = QtWidgets.QFileDialog(directory=os.path.expanduser(os.path.join('~', lastdir)))
        else:
            dialog = QtWidgets.QFileDialog(directory=lastdir)
        dialog.setAcceptMode(1)
        targetdir = dialog.getExistingDirectory(self, "Select Directory")
        
        if targetdir != '':
            lastdir = os.path.dirname(targetdir)

            self.data_3d = read_oct_data(targetdir)

            self.load_3d(self.chkbx_3d.isChecked())
            
            self.vb_xy.setMouseEnabled(x=True, y=True)
            self.vb_xz.setMouseEnabled(x=True, y=True)
            self.vb_yz.setMouseEnabled(x=True, y=True)
            
            self.set_x(0)
            self.set_y(0)
            self.set_z(0)

            self.slider_brightness_val.setEnabled(True)
            self.contrast_val.setEnabled(True)
            self.combobox.setEnabled(True)
            self.combobox_rotate_xy.setEnabled(True)
            self.combobox_rotate_xz.setEnabled(True)
            self.combobox_rotate_yz.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.slider_navg_val.setEnabled(True)
            self.lock_cross = False
            
    def update_range_x(self, avg):
        self.set_x(self.navg_val)

    def update_range_y(self, avg):
        self.set_y(self.navg_val)

    def update_range_z(self, avg):
        self.set_z(self.navg_val)
        
    def on_rotate_xy_change(self, v):
        self.flag_rotate_xy = int(v)
        self.set_x(self.mouse_set_x)
    
    def on_rotate_xz_change(self, v):
        self.flag_rotate_xz = int(v)
        self.set_y(self.mouse_set_y)
    
    def on_rotate_yz_change(self, v):
        self.flag_rotate_yz = int(v)
        self.set_z(self.mouse_set_z)

    def set_x(self, x):
        navg = self.navg_val
        self.img_xy = np.squeeze(np.nanmean(self.data_3d[int(x):int(x)+navg, :, :], 0))
        
        if self.flag_rotate_xy == 0:
            self.img_xy = cv2.rotate(self.img_xy, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif self.flag_rotate_xy == 90:
            pass
            # self.img_xy = cv2.rotate(self.img_xy, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif self.flag_rotate_xy == 180:
            self.img_xy = cv2.rotate(self.img_xy, cv2.ROTATE_90_CLOCKWISE)
        elif self.flag_rotate_xy == 270:
            self.img_xy = cv2.rotate(self.img_xy, cv2.ROTATE_180)

        w, h = self.img_xy.shape
        self.vb_xy.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        adjusted = cv2.convertScaleAbs(self.img_xy, alpha=self.alpha, beta=self.beta)
        self.qtimg_xy.setImage(adjusted)
        self.qtimg_xy.setColorMap(self.color_map_obj[self.color_map_current])
        
    def set_y(self, y):
        navg = self.navg_val
        self.img_xz = np.squeeze(np.nanmean(self.data_3d[:, int(y):int(y)+navg, :], 1))

        if self.flag_rotate_xz == 0:
            pass
        elif self.flag_rotate_xz == 90:
            self.img_xz = cv2.rotate(self.img_xz, cv2.ROTATE_90_CLOCKWISE)
        elif self.flag_rotate_xz == 180:
            self.img_xz = cv2.rotate(self.img_xz, cv2.ROTATE_180)
        elif self.flag_rotate_xz == 270:
            self.img_xz = cv2.rotate(self.img_xz, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
        w, h = self.img_xz.shape
        self.vb_xz.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        adjusted = cv2.convertScaleAbs(self.img_xz, alpha=self.alpha, beta=self.beta)
        self.qtimg_xz.setImage(adjusted)
        self.qtimg_xz.setColorMap(self.color_map_obj[self.color_map_current])

    def set_z(self, z):
        navg = self.navg_val
        self.img_yz = np.squeeze(np.nanmean(self.data_3d[:, :, int(z):int(z)+navg], 2))

        if self.flag_rotate_yz == 0:
            pass
        elif self.flag_rotate_yz == 90:
            self.img_yz = cv2.rotate(self.img_yz, cv2.ROTATE_90_CLOCKWISE)
        elif self.flag_rotate_yz == 180:
            self.img_yz = cv2.rotate(self.img_yz, cv2.ROTATE_180)
        elif self.flag_rotate_yz == 270:
            self.img_yz = cv2.rotate(self.img_yz, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
        w, h = self.img_yz.shape
        self.vb_yz.setLimits(xMin=0, xMax=w, yMin=0, yMax=h)
        adjusted = cv2.convertScaleAbs(self.img_yz, alpha=self.alpha, beta=self.beta)
        self.qtimg_yz.setImage(adjusted)
        self.qtimg_yz.setColorMap(self.color_map_obj[self.color_map_current])
        
    def on_contrast_change_val(self, v):
        self.alpha = self.verify_val(v)
        adjusted = cv2.convertScaleAbs(self.img_xy, alpha=self.alpha, beta=self.beta)
        self.qtimg_xy.setImage(adjusted)

        adjusted = cv2.convertScaleAbs(self.img_xz, alpha=self.alpha, beta=self.beta)
        self.qtimg_xz.setImage(adjusted)
    
        adjusted = cv2.convertScaleAbs(self.img_yz, alpha=self.alpha, beta=self.beta)
        self.qtimg_yz.setImage(adjusted)
        
        self.label_contrast_val.setText(str(self.alpha))
        
    def on_brightness_change_val(self, v):
        self.beta = v
        adjusted = cv2.convertScaleAbs(self.img_xy, alpha=self.alpha, beta=self.beta)
        self.qtimg_xy.setImage(adjusted)
        
        adjusted = cv2.convertScaleAbs(self.img_xz, alpha=self.alpha, beta=self.beta)
        self.qtimg_xz.setImage(adjusted)
    
        adjusted = cv2.convertScaleAbs(self.img_yz, alpha=self.alpha, beta=self.beta)
        self.qtimg_yz.setImage(adjusted)
        
        self.label_brightness_val.setText(str(v))
        
    def on_navg_change_val(self, v):
        self.navg_val = v
        self.update_range_x(v)
        self.update_range_y(v)
        self.update_range_z(v)
        self.label_navg_val.setText(str(v))
        
    def verify_val(self, v: str) -> float:
        return 0.0 if v == '' else v / 10.0


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
