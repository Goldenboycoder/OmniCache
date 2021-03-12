from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QLabel
import sys
from PyQt5.QtCore import QTimer
import threading
from p2p import Node
from blockchain import bcNode
from gui import Ui_JoinNetwork, Ui_homepage,Ui_splashscreen, Ui_settings

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'OmniCache')
        menu = QtWidgets.QMenu(parent)  # Create a Qt widget with tray icon parent

        open_app = menu.addAction("Open OmniCache")  # Adding Open OmniCache in tray menu
        open_app.triggered.connect(self.open_omnicache)

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())  # Adding Exit in tray menu

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.open_omnicache()

    # On click open OmniCache in Tray
    def open_omnicache(self):

        # Opening Application
        Homepage_UI.show()

OmniCacheApp = QApplication(sys.argv)   # Create Qt Application
OmniCacheApp.setWindowIcon(QtGui.QIcon('./Images/taskbar_icon.png'))

SplashscreenUI = Ui_splashscreen()      # Create an instance of Splashcreen UI
Join_Network_UI = Ui_JoinNetwork()      # Create an instance of Join Network UI
#Homepage_UI = Ui_homepage()             # Create an instance of Homepage UI
Settings_UI = Ui_settings()             # Create an instance of Settings UI
Homepage_UI=""
# Giving the system tray an icon and show()
tray_icon = SystemTrayIcon(QtGui.QIcon("./Images/currency_logo.png"), Join_Network_UI)
tray_icon.show()

# Enabling splash screen function to show
Ui_splashscreen.flashSplash(SplashscreenUI)

# Showing Join Network UI after 3s until splash screen is done
QTimer.singleShot(2000, lambda: Join_Network_UI.show())
def initNode():
    ip=Join_Network_UI.ipaddress_input.text()
    port=Join_Network_UI.port_input.text()
    bNode = bcNode("127.0.0.1")
    node=Node(ip,port,bNode)
    Homepage_UI = Ui_homepage(node)
    Homepage_UI.upload_btn.clicked.connect(lambda: Homepage_UI.upload_onclick())                                      # Triggering Upload File button in Homepage
    Homepage_UI.settings_btn.clicked.connect(lambda: Homepage_UI.settings_onclick(Settings_UI,Homepage_UI))           # Triggering Settings button and passing Settings UI & Homepage UI as param
    return Homepage_UI

# Onclick Listeners
Join_Network_UI.join_network_btn.clicked.connect(lambda: Join_Network_UI.join_network_btn_onclick(initNode()))   # Triggering Join Network button and passing Homepage UI as param


OmniCacheApp.exec_() # Executing app

