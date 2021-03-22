from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QLabel
import sys
from PyQt5.QtCore import QTimer
import threading
from p2p_C import Node
from blockchain_C import bcNode
import subprocess

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

        # Created an instance of Join Network UI and Homepage UI
        self.Homepage_UI = None
        

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
        self.Homepage_UI.show()

OmniCacheApp = QApplication(sys.argv)   # Create Qt Application
OmniCacheApp.setWindowIcon(QtGui.QIcon('./Images/taskbar_icon.png'))

SplashscreenUI = Ui_splashscreen()      # Create an instance of Splash screen UI
Join_Network_UI = Ui_JoinNetwork()      # Create an instance of Join Network UI
Homepage_UI = None          
Settings_UI = Ui_settings()             # Create an instance of Settings UI

# Giving the system tray an icon and show()
tray_icon = SystemTrayIcon(QtGui.QIcon("./Images/currency_logo.png"), Homepage_UI)

# Enabling splash screen function to show
Ui_splashscreen.flashSplash(SplashscreenUI)

# Showing Join Network UI after 3s until splash screen is done
QTimer.singleShot(2000, lambda: Join_Network_UI.show())

# Onclick Listeners
Join_Network_UI.join_network_btn.clicked.connect(lambda: Join_Network_UI.join_network_btn_onclick(initNode()))   # Triggering Join network button
Join_Network_UI.ipaddress_input.returnPressed.connect(lambda: Join_Network_UI.join_network_btn_onclick(initNode()))    # Triggering Join network button (Enter pressed)

# Initiliazing node on Join network click
def initNode():

    global Homepage_UI

    ip=Join_Network_UI.ipaddress_input.text()
    port="4444"
    bNode = bcNode("127.0.0.1")
    node= Node(ip,port,bNode)
    Homepage_UI = Ui_homepage(node)
    tray_icon.show()
    HomepageListeners()
    return Homepage_UI


def HomepageListeners():

    global Homepage_UI

    Homepage_UI.upload_btn.clicked.connect(lambda: Homepage_UI.upload_onclick())                             # Triggering Upload File button in Homepage
    Homepage_UI.settings_btn.clicked.connect(lambda: Homepage_UI.settings_onclick(Settings_UI,Homepage_UI))  # Triggering Settings button and passing Settings UI & Homepage UI as param
    Homepage_UI.search_input.textChanged.connect(lambda: Homepage_UI.on_searchTextChanged(Homepage_UI.search_input.text()))  # On text changed in search input
    tray_icon.Homepage_UI = Homepage_UI

OmniCacheApp.exec_() # Executing app