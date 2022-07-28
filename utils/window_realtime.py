from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import cv2
import shutil
import tensorflow as tf
from PIL import Image
import numpy as np


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('images/logo.png'))
        self.setWindowTitle('果蔬识别系统')
        self.to_predict_name = "images/tim9.jpeg"
        self.model = tf.keras.models.load_model("../models/mobilenet_fv.h5")
        self.class_names = ['土豆', '圣女果', '大白菜', '大葱', '梨', '胡萝卜', '芒果', '苹果', '西红柿', '韭菜', '香蕉', '黄瓜']
        self.resize(900, 700)
        self.source = ''
        self.timer_camera = QTimer()
        self.video_capture = cv2.VideoCapture()
        self.CAM_NUM = 0
        # 初始化中止事件
        self.initUI()
        self.center()
        self.center()
        # 联系到展示的界面

    def initUI(self):
        img = cv2.imread(self.to_predict_name)
        img_to_predict = cv2.resize(img, (224, 224))
        cv2.imwrite('../images/target.png', img_to_predict)
        # target_image_name = "images/tmpx.jpg"
        # shutil.copy(self.to_predict_name, target_image_name)
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        font = QFont('楷体', 15)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        img_title = QLabel("样本")
        img_title.setFont(font)
        img_title.setAlignment(Qt.AlignCenter)
        self.img_label = QLabel()
        img_init = cv2.imread(self.to_predict_name)
        h, w, c = img_init.shape
        scale = 400 / h
        img_show = cv2.resize(img_init, (0, 0), fx=scale, fy=scale)
        cv2.imwrite("../images/show.png", img_show)
        self.img_label.setPixmap(QPixmap("images/show.png"))
        left_layout.addWidget(img_title)
        left_layout.addWidget(self.img_label, 1, Qt.AlignCenter)
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        self.btn_open = QPushButton(" 打开摄像头 ")
        self.btn_open.clicked.connect(self.display_video)
        self.btn_open.setFont(font)
        # self.btn_change = QPushButton(" 拍  照 ")
        # self.btn_change.clicked.connect(self.change_img)
        # self.btn_change.setFont(font)
        # btn_predict = QPushButton(" 开始识别 ")
        # btn_predict.setFont(font)
        # btn_predict.clicked.connect(self.predict_img)

        label_result = QLabel(' 果蔬名称 ')
        self.result = QLabel("等待识别")
        label_result.setFont(QFont('楷体', 16))
        self.result.setFont(QFont('楷体', 24))

        right_layout.addStretch()
        right_layout.addWidget(label_result, 0, Qt.AlignCenter)
        right_layout.addStretch()
        right_layout.addWidget(self.result, 0, Qt.AlignCenter)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_open)
        # right_layout.addWidget(self.btn_change)
        # right_layout.addWidget(btn_predict)
        right_layout.addStretch()
        right_widget.setLayout(right_layout)

        # 关于页面
        about_widget = QWidget()
        about_layout = QVBoxLayout()
        about_title = QLabel('欢迎使用智能线束识别系统')
        about_title.setFont(QFont('楷体', 18))
        about_title.setAlignment(Qt.AlignCenter)
        about_img = QLabel()
        about_img.setPixmap(QPixmap('images/bj.png'))
        about_img.setAlignment(Qt.AlignCenter)
        label_super = QLabel("作者：XXX\n指导老师：XXX")
        label_super.setFont(QFont('楷体', 12))
        label_super.setAlignment(Qt.AlignRight)
        about_layout.addWidget(about_title)
        about_layout.addStretch()
        about_layout.addWidget(about_img)
        about_layout.addStretch()
        about_layout.addWidget(label_super)
        about_widget.setLayout(about_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_widget.setLayout(main_layout)
        self.addTab(main_widget, '主页')
        self.addTab(about_widget, '关于')
        self.setTabIcon(0, QIcon('images/主页面.png'))
        self.setTabIcon(1, QIcon('images/关于.png'))
        self.timer_camera.timeout.connect(self.show_camera)
        # print("初始化结束")

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft, newTop)

    def display_video(self):
        # 首先把打开按钮关闭
        # self.btn_open.setEnabled(False)
        # self.btn_change.setEnabled(True)
        # todo 这里执行显示的逻辑
        if self.timer_camera.isActive() == False:
            flag = self.video_capture.open(self.CAM_NUM)
            print(flag)
            if flag == False:
                QMessageBox.warning(self, 'warning', "please check it")
            else:
                self.timer_camera.start(30)
                self.btn_open.setText(' 关闭摄像头 ')
        else:
            print("关闭摄像头")
            self.timer_camera.stop()
            self.video_capture.release()
            self.img_label.clear()
            self.img_label.setPixmap(QPixmap("images/show.png"))
            self.btn_open.setText(' 打开摄像头 ')

    def show_camera(self):
        # print("show camera")
        ret, frame = self.video_capture.read()
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        frame_scale = 400 / frame_height
        frame_resize = cv2.resize(frame, (int(frame_width * frame_scale), int(frame_height * frame_scale)))
        cv2.imwrite("../images/tmp.jpg", frame_resize)
        self.img_label.setPixmap(QPixmap("images/tmp.jpg"))

        img = Image.open("../images/tmp.jpg")
        img = img.resize((224, 224), Image.BILINEAR)
        img = np.asarray(img)
        outputs = self.model.predict(img.reshape(1, 224, 224, 3))
        result_index = int(np.argmax(outputs))
        result = self.class_names[result_index]
        # print(result)
        self.result.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainWindow()
    x.show()
    sys.exit(app.exec_())
