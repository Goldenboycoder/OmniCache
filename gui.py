import sys
import threading
import datetime
from pathlib import Path
import time
import subprocess

from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QLabel, QFileDialog, QDesktopWidget
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QSplashScreen, QGraphicsColorizeEffect,QListWidgetItem
import ntpath

from p2p_C import Node
from blockchain_C import bcNode
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPoint, QTimer

#Splashscreen UI
class Ui_splashscreen(QDialog):
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
    #-----------------------------------------------------------------------
        super(Ui_splashscreen, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

    #-----------------------------------------------------------------------
    def flashSplash(self):
    #-----------------------------------------------------------------------
        self.splash = QSplashScreen(QPixmap('./Images/joinnetwork_logo.png'))

        #By default, SplashScreen will be in the center of the screen.
        self.splash.show()

        #Close SplashScreen after 2 seconds (2000 ms)
        QTimer.singleShot(2000, self.splash.close)

#Join Network UI
class Ui_JoinNetwork(QMainWindow):

    #Setup UI for the initial function
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
    #-----------------------------------------------------------------------
        super().__init__(parent)
        self.setupUi(self)

    #UI Design
    #-----------------------------------------------------------------------
    def setupUi(self, MainWindow):
    #-----------------------------------------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1128, 792)
        MainWindow.setStyleSheet("#centralwidget{background-image: url(./Images/joinnetwork_background.jpg)}\n"
                                 "QLineEdit{background-color: rgb(12,12,12);}"
                                 "QPushButton#join_network_btn{background-color: rgb(0, 168, 243);}\n"
                                 "QPushButton#join_network_btn:hover{background-color: rgb(30,144,255);}"
                                 )
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)
        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap("./Images/joinnetwork_logo.png"))
        self.logo_label.setObjectName("logo_label")
        self.verticalLayout_4.addWidget(self.logo_label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_1.setSpacing(6)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.ipaddress_label = QtWidgets.QLabel(self.centralwidget)
        self.ipaddress_label.setStyleSheet("font: 14pt \"Proxima Nova\";\n"
                                           "color: rgb(255, 255, 255);")
        self.ipaddress_label.setObjectName("ipaddress_label")
        self.horizontalLayout_1.addWidget(self.ipaddress_label, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.ipaddress_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ipaddress_input.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border: 0.5px solid grey;\n"
                                           "border-radius: 6px;\n"
                                           )
        self.ipaddress_input.setText("")
        self.ipaddress_input.setObjectName("ipaddress_input")

        #IP regex Validator
        IpAddressRegex = QtCore.QRegExp("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        IPvalidator = QtGui.QRegExpValidator(IpAddressRegex)
        self.ipaddress_input.setValidator(IPvalidator)

        self.horizontalLayout_1.addWidget(self.ipaddress_input, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.verticalLayout_4.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        spacerItem1 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout_25.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_25)
        self.join_network_btn = QtWidgets.QPushButton(self.centralwidget)
        self.join_network_btn.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                            "background-color: rgb(0, 168, 243);\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "border-radius: 6px;\n"
                                            "padding: 10px")
        self.join_network_btn.setObjectName("join_network_btn")
        self.verticalLayout_4.addWidget(self.join_network_btn, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem2 = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #On Click Join Network Button and passing UI in args
    #-----------------------------------------------------------------------
    def join_network_btn_onclick(self, ui):
    #-----------------------------------------------------------------------
        #To-do on clicking Join Network Button
        ui.showMaximized()
        self.hide()

    # Handling Close Window Button event
    #-----------------------------------------------------------------------
    def closeEvent(self, event):
    #-----------------------------------------------------------------------
        #Open dialog box asking to close the app
        close = QMessageBox.question(self,"Close application","Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No)

        #If yes is clicked
        if close == QMessageBox.Yes:
            event.accept()   #App closed

        #If no is clicked
        else:
            event.ignore()   #App not closed


    #Renaming Labels, LineEdits, Buttons
    #-----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
    #-----------------------------------------------------------------------
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ipaddress_label.setText(_translate("MainWindow", "IP Address:"))
        self.ipaddress_input.setPlaceholderText(_translate("MainWindow", "Enter IP..."))
        self.join_network_btn.setText(_translate("MainWindow", "Join Network"))

#Item widget for list in homepage
class Ui_file_item(QWidget):

    #-----------------------------------------------------------------------
    def __init__(self):
    #-----------------------------------------------------------------------
      QWidget.__init__(self)
      self.setupUi(self)

    #-----------------------------------------------------------------------
    def setupUi(self, file_item):
    #-----------------------------------------------------------------------
        file_item.setObjectName("file_item")
        file_item.resize(232, 48)
        self.horizontalLayout = QtWidgets.QHBoxLayout(file_item)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(file_item)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font: 14pt \"Proxima Nova\";\n"
                                "color: rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.download_btn = QtWidgets.QPushButton(file_item)
        self.download_btn.setStyleSheet("border: 0")
        self.download_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/download_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.download_btn.setIcon(icon)
        self.download_btn.setObjectName("download_btn")
        self.horizontalLayout.addWidget(self.download_btn, 0, QtCore.Qt.AlignLeft)
        self.pushButton = QtWidgets.QPushButton(file_item)
        self.pushButton.setStyleSheet("border:0")
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./Images/trash_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.retranslateUi(file_item)
        QtCore.QMetaObject.connectSlotsByName(file_item)

    #-----------------------------------------------------------------------
    def retranslateUi(self, file_item):
    #-----------------------------------------------------------------------
        _translate = QtCore.QCoreApplication.translate
        file_item.setWindowTitle(_translate("file_item", "Form"))
        self.label.setText(_translate("file_item", "Text Label"))


#Upload Task
class UploadTask(QtCore.QThread):

    #Task thread finished event
    finished = pyqtSignal(object)

    #-----------------------------------------------------------------------
    def __init__(self, node, filepath):
    #-----------------------------------------------------------------------
        QtCore.QThread.__init__(self)
        self.node = node
        self.filepath = filepath

    #When task thread starts
    #-----------------------------------------------------------------------
    def run(self):
    #-----------------------------------------------------------------------
        filename , _ = self.node.sendChunks(self.filepath)
        self.finished.emit(filename)

#Node ready task
""" class NodeReady(QtCore.QThread):

    #Task thread finished event
    finished = pyqtSignal(object)

    #-----------------------------------------------------------------------
    def __init__(self, node):
    #-----------------------------------------------------------------------
        QtCore.QThread.__init__(self)
        self.node = node

    #When task thread starts
    #-----------------------------------------------------------------------
    def run(self):
    #-----------------------------------------------------------------------
        while(not self.node.ready):

            time.sleep(1)
        
        
        self.finished.emit() """



#Homepage UI
class Ui_homepage(QMainWindow):

    #Setup UI for the initial function
    #-----------------------------------------------------------------------
    def __init__(self, node,parent=None):
    #-----------------------------------------------------------------------
        super(Ui_homepage, self).__init__(parent)
        self.setupUi(self)
        self.threads = []
        self.node = node

        #Thread for fetching files on startup
        """ nodeready = NodeReady(self.node)    #Creating a thread
        nodeready.finished.connect(self.fetchAllFiles)    #After thread is finished
        self.threads.append(nodeready)
        nodeready.start() """


    #UI Design
    #-----------------------------------------------------------------------
    def setupUi(self, MainWindow):
    #-----------------------------------------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1188, 886)
        MainWindow.setStyleSheet("#centralwidget{background-color: rgb(12, 12, 12);}\n"
                                 "QLineEdit{background-color: rgb(12,12,12);}"
                                 "QListWidget{background-color: rgb(12,12,12);}"
                                 "QPushButton#upload_btn{background-color: rgb(0, 168, 243);}\n"
                                 "QPushButton#upload_btn:hover{background-color: rgb(30,144,255);}"
                                 )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./Images/homepage_logo.png"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setStyleSheet("border: 0")
        self.settings_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Images/settings_icon.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.settings_btn.setIcon(icon)
        self.settings_btn.setIconSize(QtCore.QSize(25, 25))
        self.settings_btn.setObjectName("settings_btn")
        self.verticalLayout_2.addWidget(self.settings_btn, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.wallet_label = QtWidgets.QLabel(self.centralwidget)
        self.wallet_label.setStyleSheet("font: 14pt \"Proxima Nova\";\n"
                                            "color: rgb(255, 255, 255);")
        self.wallet_label.setObjectName("wallet_label")
        self.verticalLayout_2.addWidget(self.wallet_label, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.hosting_value_label = QtWidgets.QLabel(self.centralwidget)
        self.hosting_value_label.setStyleSheet("font: 14pt \"Proxima Nova\";\n"
                                                   "color: rgb(255, 255, 255);")
        self.hosting_value_label.setObjectName("hosting_value_label")
        self.verticalLayout_2.addWidget(self.hosting_value_label, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("background-color: rgb(0, 168, 243);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mystash_icon = QtWidgets.QLabel(self.centralwidget)
        self.mystash_icon.setStyleSheet("")
        self.mystash_icon.setText("")
        self.mystash_icon.setPixmap(
            QtGui.QPixmap("./Images/mystash.png"))
        self.mystash_icon.setObjectName("mystash_icon")
        self.horizontalLayout_2.addWidget(self.mystash_icon, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.mystash_label = QtWidgets.QLabel(self.centralwidget)
        self.mystash_label.setStyleSheet("font: 14pt \"Aquire\";\n"
                                             "color: rgb(255, 255, 255);")
        self.mystash_label.setObjectName("mystash_label")
        self.horizontalLayout_2.addWidget(self.mystash_label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.search_icon = QtWidgets.QLabel(self.centralwidget)
        self.search_icon.setText("")
        self.search_icon.setPixmap(QtGui.QPixmap("./Images/search_icon.png"))
        self.search_icon.setObjectName("search_icon")
        self.horizontalLayout_2.addWidget(self.search_icon, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 0.5px solid grey;\n"
                                        "border-radius: 6px;\n"
                                        "")
        self.search_input.setText("")
        self.search_input.setObjectName("search_input")
        self.horizontalLayout_2.addWidget(self.search_input, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.upload_btn = QtWidgets.QPushButton(self.centralwidget)
        self.upload_btn.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 6px;\n"
                                          "padding:3px;")
        self.upload_btn.setObjectName("upload_btn")
        self.horizontalLayout_2.addWidget(self.upload_btn, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.listWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{background:#000000;}")
        self.filedetails_label = QtWidgets.QLabel(self.centralwidget)
        self.filedetails_label.setStyleSheet("font: 14pt \"Proxima Nova\";\n"
                                             "color: rgb(255, 255, 255);")
        self.filedetails_label.setObjectName("filedetails_label")
        self.verticalLayout.addWidget(self.filedetails_label)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setMouseTracking(False)
        self.progress_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                          "color: rgb(255, 255, 255);")
        self.progress_label.setObjectName("progress_label")
        self.horizontalLayout_8.addWidget(self.progress_label)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setStyleSheet(
                                        "font: 10pt \"Proxima Nova\";\n"
                                        "color: rgb(255, 255, 255);"          
                                        )

        self.progress_bar.setProperty("value", 35)
        self.progress_bar.setOrientation(QtCore.Qt.Horizontal)
        self.progress_bar.setObjectName("progress_bar")
        self.horizontalLayout_8.addWidget(self.progress_bar)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fd_name_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_name_label.setMouseTracking(False)
        self.fd_name_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                             "color: rgb(255, 255, 255);")
        self.fd_name_label.setObjectName("fd_name_label")
        self.horizontalLayout_3.addWidget(self.fd_name_label)
        self.fd_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_speed_label.setMouseTracking(False)
        self.fd_speed_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                          "color: rgb(255, 255, 255);")
        self.fd_speed_label.setObjectName("fd_speed_label")
        self.horizontalLayout_3.addWidget(self.fd_speed_label)
        self.fd_eta_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_eta_label.setMouseTracking(False)
        self.fd_eta_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                            "color: rgb(255, 255, 255);")
        self.fd_eta_label.setObjectName("fd_eta_label")
        self.horizontalLayout_3.addWidget(self.fd_eta_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.fd_size_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_size_label.setMouseTracking(False)
        self.fd_size_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                         "color: rgb(255, 255, 255);")
        self.fd_size_label.setObjectName("fd_size_label")
        self.horizontalLayout_6.addWidget(self.fd_size_label)
        self.fd_downloaded_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_downloaded_label.setMouseTracking(False)
        self.fd_downloaded_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                               "color: rgb(255, 255, 255);")
        self.fd_downloaded_label.setObjectName("fd_downloaded_label")
        self.horizontalLayout_6.addWidget(self.fd_downloaded_label)
        self.fd_peers_label = QtWidgets.QLabel(self.centralwidget)
        self.fd_peers_label.setMouseTracking(False)
        self.fd_peers_label.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                          "color: rgb(255, 255, 255);")
        self.fd_peers_label.setObjectName("fd_peers_label")
        self.horizontalLayout_6.addWidget(self.fd_peers_label)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1188, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Search query for listview
    #-----------------------------------------------------------------------
    def on_searchTextChanged(self, search_query):
    #-----------------------------------------------------------------------
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            widget = self.listWidget.itemWidget(item)

            if search_query:
                item.setHidden(not self.filter(search_query, widget.label.text()))
            else:
                item.setHidden(True)

        if self.search_input.text() == "":
            for row in range(self.listWidget.count()):
                item = self.listWidget.item(row)
                item.setHidden(False)


    def filter(self, text, keywords):
        
        return text in keywords

    #On-Click Settings Button
    #-----------------------------------------------------------------------
    def settings_onclick(self,ui,ui1):
    #-----------------------------------------------------------------------
        ui.show()    #Showing Settings UI
        ui1.setWindowOpacity(0.9)    #Homepage UI on 0.9 opacity in the background


    #Fetching files and adding to list
    #-----------------------------------------------------------------------
    def fetchAllFiles(self):
    #-----------------------------------------------------------------------
        allFiles = self.node.fetchMyFiles()

        for item in allFiles:
            self.addItemtoList(item["fileName"])




    #On-Click Upload Button
    #-----------------------------------------------------------------------
    def upload_onclick(self):
    #-----------------------------------------------------------------------
        #To-do on clicking Upload Button
        
        filename = ""
        browseFile = QFileDialog()   # creating a File Dialog
        filename = browseFile.getOpenFileName(self,"Select File","",)   #Receiving a string from the file dialog

        #Extracting file name from filepath
        ntpath.basename("a/b/c")
        
        uploadtask = UploadTask(self.node, Path(filename[0]))    #Creating a thread
        uploadtask.finished.connect(self.addItemtoList)    #After thread is finished
        self.threads.append(uploadtask)
        uploadtask.start()

        """ if filename != "":
            thread = threading.Thread(target= self.node.sendChunks, args=[Path(filename[0]),])
            thread.start() """
        
    #-----------------------------------------------------------------------    
    def addItemtoList(self, filename):
    #-----------------------------------------------------------------------    
        #head, tail = ntpath.split(filename[0])
        # If filedialog open is clicked
        if filename != "":
            #Adding an item to the QListWidget
            myQCustomQWidget = Ui_file_item()
            myQCustomQWidget.label.setText(filename)
            myQListWidgetItem = QListWidgetItem(self.listWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem,myQCustomQWidget)

    #Handling Close Window Button event in Homepage
    #-----------------------------------------------------------------------
    def closeEvent(self, event):
    #-----------------------------------------------------------------------
        #Open dialog box asking to minimize tray or close app
        close = QMessageBox.question(self,"System Tray","Do you want the program to minimize to tray?", QMessageBox.Yes | QMessageBox.No)

        #If yes is clicked
        if close == QMessageBox.Yes:
            event.ignore()    #App not closed
            self.hide()    #UI hidden

        #If no is clicked
        else:
            event.accept() #App closed
            sys.exit()
    
    #If mouse is clicked on the Homepage UI window
    #-----------------------------------------------------------------------
    def enterEvent(self, event):
    #-----------------------------------------------------------------------
        self.setWindowOpacity(1)   # Return windows opacity to 1 after closing settings
        return super(Ui_homepage, self).enterEvent(event)


    #Renaming Labels, LineEdits, Buttons
    #-----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
    #-----------------------------------------------------------------------
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OmniCache"))
        self.wallet_label.setText(_translate("MainWindow", "120"))
        self.hosting_value_label.setText(_translate("MainWindow", "10 GB"))
        self.mystash_label.setText(_translate("MainWindow", "My Stash"))
        self.search_input.setPlaceholderText(_translate("MainWindow", "Search..."))
        self.upload_btn.setText(_translate("MainWindow", "Upload file"))
        self.filedetails_label.setText(_translate("MainWindow", "File Details:"))
        self.progress_label.setText(_translate("MainWindow", "Progress:"))
        self.progress_bar.setFormat(_translate("MainWindow", "%p%"))
        self.fd_name_label.setText(_translate("MainWindow", "Name:"))
        self.fd_speed_label.setText(_translate("MainWindow", "Download/Upload Speed:"))
        self.fd_eta_label.setText(_translate("MainWindow", "ETA:"))
        self.fd_size_label.setText(_translate("MainWindow", "Size:"))
        self.fd_downloaded_label.setText(_translate("MainWindow", "Downloaded:"))
        self.fd_peers_label.setText(_translate("MainWindow", "Number of Peers:"))




class Ui_settings(QMainWindow):

    #Setup UI for the initial function
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
    #-----------------------------------------------------------------------
        super(Ui_settings, self).__init__(parent)
        self.setupUi(self)
        
    #-----------------------------------------------------------------------
    def setupUi(self, MainWindow):
    #-----------------------------------------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(529, 544)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(35,35,35); border: 1px solid black;}"
                                 "QPushButton{background-color: rgb(0, 168, 243);}"
                                 "QPushButton::hover{background-color: rgb(30,144,255);}")

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)  #Set the window frameless and as a popup(clicking outside closes window)

        #Centering settings window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("border-radius:40px;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("font: 20pt \"Proxima Nova\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "margin-top: 20px;")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-radius: 6px;\n"
                                    "padding: 10px;\n"
                                    "width:150px;")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 6px;\n"
                                        "padding: 10px;\n"
                                        "margin-top:10px;\n"
                                        "width:150px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 6px;\n"
                                        "padding: 10px;\n"
                                        "margin-top:10px;\n"
                                        "width:150px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setStyleSheet("font: 10pt \"Proxima Nova\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 6px;\n"
                                        "padding: 10px;\n"
                                        "margin-top:10px;\n"
                                        "width:150px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #Renaming Labels, LineEdits, Buttons
    #-----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
    #-----------------------------------------------------------------------
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.label.setText(_translate("MainWindow", "Settings"))
        self.pushButton.setText(_translate("MainWindow", "Test 1"))
        self.pushButton_2.setText(_translate("MainWindow", "Test 2"))
        self.pushButton_3.setText(_translate("MainWindow", "Test 3"))
        self.pushButton_4.setText(_translate("MainWindow", "Test 4"))