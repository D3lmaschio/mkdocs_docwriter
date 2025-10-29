# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QToolButton, QTreeView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(748, 597)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(10, 10, 721, 431))
        font = QFont()
        font.setFamilies([u"Inter 28pt"])
        font.setPointSize(9)
        self.treeView.setFont(font)
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(390, 510, 20, 20))
        self.toolButton.setFont(font)
        # Adiciona o botão de atualizar a tree
        self.pushButton_refresh = QPushButton(self.centralwidget)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setGeometry(QRect(630, 510, 101, 31))  # canto inferior direito
        self.pushButton_refresh.setFont(font)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(430, 450, 101, 31))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(530, 450, 101, 31))
        self.pushButton_2.setFont(font)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(630, 450, 101, 31))
        self.pushButton_3.setFont(font)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 510, 401, 21))
        self.lineEdit.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 490, 101, 20))
        font1 = QFont()
        font1.setFamilies([u"Inter 28pt"])
        font1.setPointSize(10)
        font1.setWeight(QFont.Weight.Medium)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.label.setFont(font1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 440, 101, 20))
        self.label_2.setFont(font1)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(10, 460, 401, 21))
        self.lineEdit_2.setFont(font)
        # Botão de renomear
        self.pushButton_rename = QPushButton(self.centralwidget)
        self.pushButton_rename.setObjectName(u"pushButton_rename")
        self.pushButton_rename.setGeometry(QRect(530, 510, 101, 31))  # posição ao lado do refresh
        self.pushButton_rename.setFont(font)
        self.pushButton_create_index = QPushButton(self.centralwidget)
        self.pushButton_create_index.setObjectName(u"pushButton_create_index")
        self.pushButton_create_index.setGeometry(QRect(420, 510, 101, 31))  # posição ao lado de renomear
        self.pushButton_create_index.setFont(font)       
        MainWindow.setCentralWidget(self.centralwidget)
        self.treeView.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_refresh.raise_()
        self.pushButton_rename.raise_()
        self.pushButton_create_index.raise_()
        self.lineEdit.raise_()
        self.toolButton.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.lineEdit_2.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 748, 33))
        self.menuDocument_Tree = QMenu(self.menubar)
        self.menuDocument_Tree.setObjectName(u"menuDocument_Tree")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDocument_Tree.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MkDocs Editor", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.pushButton_rename.setText(QCoreApplication.translate("MainWindow", u"Renomear", None))
        self.pushButton_create_index.setText(QCoreApplication.translate("MainWindow", u"Criar index", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u" New document", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u" Path Tree", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"Folder.Application.Document", None))
        self.menuDocument_Tree.setTitle(QCoreApplication.translate("MainWindow", u"Document Tree", None))

