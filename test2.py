import sys
import os
import json

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QStackedLayout
from PyQt5 import QtWidgets


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz Application")

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        # LOG IN LAYOUT

        self.login_layout = QVBoxLayout()

        login_form_layout = QtWidgets.QFormLayout()

        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.username_edit.setFixedWidth(120)
        self.password_edit.setFixedWidth(120)
        login_form_layout.addRow(QtWidgets.QLabel(
            "Username"), self.username_edit)
        login_form_layout.addRow(QtWidgets.QLabel(
            "Password"), self.password_edit)

        self.login_btn = QPushButton("Log In")
        self.login_btn.setFixedWidth(120)
        self.login_btn.pressed.connect(self.login_cmd)
        login_form_layout.addWidget(self.login_btn)

        self.login_layout.addLayout(login_form_layout)
        login_form_layout.setFormAlignment(Qt.AlignCenter)

        self.login_widget = QWidget()
        self.login_widget.setLayout(self.login_layout)

        # Main Menu Layout

        self.main_menu_layout = QVBoxLayout()
        self.logout_btn = QPushButton("Log Out")
        self.logout_btn.setFixedWidth(120)
        self.logout_btn.pressed.connect(self.logout_cmd)
        self.main_menu_layout.addWidget(self.logout_btn)
        self.main_menu_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.main_menu_widget = QWidget()
        self.main_menu_widget.setLayout(self.main_menu_layout)

        # Stack Layout
        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.login_widget)
        self.stack_layout.addWidget(self.main_menu_widget)
        self.stack_layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.stack_layout)
        self.setCentralWidget(widget)

    def login_cmd(self):
        self.stack_layout.setCurrentIndex(1)

    def logout_cmd(self):
        self.stack_layout.setCurrentIndex(0)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec_()