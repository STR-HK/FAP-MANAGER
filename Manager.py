import sys
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QTextStream, QFile, QUrl
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QToolBar,
        QVBoxLayout, QWidget, QMessageBox, QStackedWidget, QStatusBar, QDesktopWidget,
        QMainWindow, QMenuBar, QAction, QMenu, QListWidget, QListWidgetItem, QInputDialog,
        QFileDialog, QTableWidgetItem, QHeaderView, QShortcut, QListWidget, QStyle)

from PyQt5.QtGui import (QIcon, QColor, QPainter, QFontDatabase, QFont,
        QPixmap, QCursor, QKeySequence)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5 import QtCore
import os
import json

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(320, 180)
        self.setWindowTitle('Thumbnail Grabber')
        self.setWindowIcon(QIcon('./Icons/image.svg'))

        self.videoName = QLabel('Title of the Video')

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()

        # self.abrir()
        openButton = QPushButton("Open Video")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(btnSize)
        openButton.setFont(QFont("Noto Sans", 8))
        openButton.setIcon(QIcon.fromTheme("document-open", QIcon("D:/_Qt/img/open.png")))
        openButton.clicked.connect(self.abrir)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.videoName)
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

        self.show()

    def abrir(self):
        # fileName = self.data[self.valulist[int(self.valu)]]
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.imgHide = 0

        if os.path.exists('data.ini') == False:
            print('Not Exist')
            f = open("data.ini", "x")
            f.write("{}")
            f.close()

        # try:
            
        # except:
        #     print('exist')

        self.data = open('data.ini','r')
        self.data = json.loads(self.data.read())

        self.setWindowTitle('Function Apply Packager')
        self.setWindowIcon(QIcon('./Icons/manage_search.svg'))
        self.resize(540, 570)

        self.geometryInfo = self.frameGeometry()
        self.centerpoint = QDesktopWidget().availableGeometry().center()
        self.geometryInfo.moveCenter(self.centerpoint)
        self.move(self.geometryInfo.topLeft())

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.menubar.setStyleSheet("""
            QMenu { background: white; padding: 5; margin-left: 1; font-size: 13px; }
            QMenuBar { background: white; }
            QMenuBar::item:selected { background: #FFC0BD; }
            QMenu::item:selected { background: #FFC0BD; color: black; }
        """)

        # tasks menu
        self.tasks = self.menubar.addMenu('&Tasks')
        self.saveAction = QAction(QIcon('./Icons/save.svg'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.tasks.addAction(self.saveAction)
        self.tasks.addSeparator()
        self.addItemAction = QAction(QIcon('./Icons/add.svg'), 'Add Item...', self)
        self.addItemAction.setShortcut('Ctrl+P')
        self.addItemAction.triggered.connect(self.addItem)
        self.tasks.addAction(self.addItemAction)
        self.addItemFromFolderAction = QAction(QIcon('./Icons/playlist_add.svg'), 'Add all Items in Folder...', self)
        self.tasks.addAction(self.addItemFromFolderAction)
        self.addFolderAction = QAction(QIcon('./Icons/create_new_folder.svg'), 'Add Folder and With Inner Items...', self)
        self.tasks.addAction(self.addFolderAction)
        self.tasks.addSeparator()
        self.exitAction = QAction(QIcon('./Icons/exit_to_app.svg'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+W')
        self.exitAction.triggered.connect(app.quit)
        self.tasks.addAction(self.exitAction)

        # 툴바 시작
        self.toolIcon = QAction(QIcon('./Icons/construction.svg'), 'Tool', self)
        self.toolIcon.setEnabled(False)

        self.toolbar = QToolBar('example')
        self.toolbar.addAction(self.toolIcon)
        self.toolbar.addAction(self.addItemAction)
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        # 툴바 끝
        
        self.tools = self.menubar.addMenu('&Tools')
        self.hideIconAction = QAction(QIcon('./Icons/hide_image.svg'), 'Hide List Images', self)
        self.hideIconAction.setShortcut('Ctrl+H')
        self.hideIconAction.triggered.connect(self.hideIcon)
        self.showIconAction = QAction(QIcon('./Icons/image.svg'), 'Show List Images', self)
        self.showIconAction.setShortcut('Ctrl+H')
        self.showIconAction.triggered.connect(self.hideIcon)
        self.tools.addAction(self.hideIconAction)

        self.options = self.menubar.addMenu('&Options')
        self.openPreferencesAction = QAction(QIcon('./Icons/settings.svg'), 'Preferences', self)
        self.options.addAction(self.openPreferencesAction)

        self.help = self.menubar.addMenu('&Help')
        self.aboutAction = QAction(QIcon('./Icons/info.svg'), 'Information', self)
        self.help.addAction(self.aboutAction)

        self.statusbar = self.statusBar()
        self.statusbutton = QPushButton('Footer QPushButton That Works')
        self.statusbar.addWidget(self.statusbutton)
        self.setStatusBar(self.statusbar)

        # List
        #Create widget
        self.MyIconSize = QSize(80, 55)

        self.layoutlist = QListWidget(self)
        self.layoutlist.setIconSize(self.MyIconSize)
        self.layoutlist.setStyleSheet("""
            QListWidget { show-decoration-selected: 0; padding: 0; margin: 0; outline: 0; margin: 0; }
            QListWidget::item:hover { background: #ffebeb; color: black; }
            QListWidget::item:selected { background: #FFC0BD; color: black; }
            QListWidget::item { border-bottom: 1px solid lightgray; }"
        """)

        self.loader()

    def hideIcon(self):
        if (self.imgHide == 0):
            self.layoutlist.setIconSize(QSize(0, 0))
            self.imgHide = 1
            self.tools.insertAction(self.hideIconAction, self.showIconAction)
            self.tools.removeAction(self.hideIconAction)
        else:
            self.layoutlist.setIconSize(self.MyIconSize)
            self.imgHide = 0
            self.tools.insertAction(self.showIconAction, self.hideIconAction)
            self.tools.removeAction(self.showIconAction)
    
    def loader(self):
        listItems = []
        for x in range(self.layoutlist.count()):
            listItems.append(self.layoutlist.item(x))
        try:
            for item in listItems:
                self.layoutlist.takeItem(self.layoutlist.row(item))
        except:
            print('first')

        counter = 0
        for name, img in self.data.items():
            lidel = QWidget()
            lidelVertical = QVBoxLayout()
            lidelTitle = QHBoxLayout()
            lidelTitle.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            lidelComment = QHBoxLayout()
            lidelComment.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

            widget = QWidget()
            widgetVertical = QVBoxLayout()
            widgetLine1 = QHBoxLayout()
            widgetLine1.setAlignment(Qt.AlignRight | Qt.AlignTop)
            widgetLine2 = QHBoxLayout()
            widgetLine2.setAlignment(Qt.AlignRight | Qt.AlignBottom)

            # widgetButton1 = QPushButton()
            # widgetButton1.setIcon(QIcon('./Icons/exit_to_app.svg'))
            # widgetButton1.setStyleSheet("background-color: transparent")
            # widgetLine2.addWidget(widgetButton1)

            # widgetButton2 = QPushButton()
            # widgetButton2.setIcon(QIcon('./Icons/construction.svg'))
            # widgetButton2.setStyleSheet("background-color: transparent")
            # widgetLine2.addWidget(widgetButton2)

            editButton = QPushButton()
            editButton.setIcon(QIcon('./Icons/edit.svg'))
            editButton.setStyleSheet("background-color: transparent")
            widgetLine1.addWidget(editButton)

            captureThumbnailButton = QPushButton()
            captureThumbnailButton.setStyleSheet("""
                QPushButton { background-color: transparent; }
            """)
            captureThumbnailButton.setIcon(QIcon('./Icons/insert_photo.svg'))
            captureThumbnailButton.clicked.connect(lambda state, c=str(counter): self.thumbNail(c))
            widgetLine1.addWidget(captureThumbnailButton)

            deleteButton = QPushButton()
            deleteButton.setStyleSheet("""
                QPushButton { background-color: transparent; }
            """)
            deleteButton.clicked.connect(lambda state, c=str(counter): self.deleteItem(c))
            deleteButton.setIcon(QIcon('./Icons/delete.svg'))
            widgetLine1.addWidget(deleteButton)

            widgetVertical.addLayout(widgetLine1)
            widgetVertical.addLayout(widgetLine2)
            widget.setLayout(widgetVertical)

            lidelVertical.addLayout(lidelTitle)
            lidelVertical.addLayout(lidelComment)
            lidel.setLayout(lidelVertical)

            widgetNlidel = QWidget()
            widgetNlidelBox = QHBoxLayout()
            widgetNlidelBox.setAlignment(Qt.AlignRight)
            widgetNlidelBox.addWidget(widget)
            widgetNlidelBox.addWidget(lidel)
            widgetNlidel.setLayout(widgetNlidelBox)

            if (img[1] == 'None'):
                img = './Icons/description.svg'
            else:
                img = img[1]

            item = QListWidgetItem(QIcon(img), name)
            self.layoutlist.addItem(item)
            self.layoutlist.setItemWidget(item, widget)

            counter += 1

        self.setCentralWidget(self.layoutlist)
    
        self.show()

    def deleteItem(self, value):
        if self.askDialog(QMessageBox.Warning,'./Icons/delete.svg', 'Item Remover', 'Are You Sure to Remove this Item?') == False:
            return
        keylist = []
        valulist = []
        for key in self.data.keys():
            keylist.append(key)
        for valu in self.data.items():
            valulist.append(valu)
        del self.data[keylist[int(value)]]
        self.saveData()
        self.loader()

    def addItem(self):
        self.load = QFileDialog()
        self.load.setWindowIcon(QIcon('./Icons/movie.svg'))
        self.load.setFileMode(QFileDialog.AnyFile)
        self.loadfilename = self.load.getOpenFileName(
            caption='Open Video file', filter="Video files (*.mp4 *.mkv)")

        if self.loadfilename:
            if self.loadfilename[0] == '':
                return
            else:
                # print(self.loadfilename[0])
                self.addName = self.loadfilename[0].split('/')[-1]
                # print(self.addName)
                self.data[self.addName] = [self.loadfilename[0], "None"]

                self.saveData()

                self.loader()

    def saveData(self):
        f = open("data.ini", "w")
        f.write(json.dumps(self.data))
        f.close()
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            app.quit()
    
    def askDialog(self, type, icon, title, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(type)
        msgBox.setWindowTitle(title)
        msgBox.setWindowIcon(QIcon(icon))
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            return True
        elif returnValue == QMessageBox.Cancel:
            return False

    def thumbNail(self, value):
        valulist = []
        for valu in self.data.items():
            valulist.append(valu)
        global glist ; valulist
        
        self.w = VideoPlayer()
        self.w.show()
    


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    # fontDB = QFontDatabase()
    # fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'fonts/NanumSquareOTF_acB.otf')))
    # app.setFont(QFont('NanumSquareOTF_ac Bold', 11))

    window = MainWindow()

    # palatte = window.palette()
    # palatte.setColor(window.backgroundRole(), QColor(255, 105, 97))
    # window.setPalette(palatte)

    window.show()
    sys.exit(app.exec())