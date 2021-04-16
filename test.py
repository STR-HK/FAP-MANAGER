import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

class PageShotter(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, url, parent=None):
        super(PageShotter, self).__init__(parent)
        self.loadFinished.connect(self.save)
        self.url = url
        self.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.show()
        settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()
        for attr in (QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, 
                     QtWebEngineWidgets.QWebEngineSettings.ScreenCaptureEnabled,):
            settings.setAttribute(attr, True)

    def shot(self):
        if self.size().isNull():
            self.resize(640, 480)
        self.load(QtCore.QUrl.fromLocalFile(self.url))

    @QtCore.pyqtSlot(bool)
    def save(self, finished):
        if finished:
            size = self.contentsRect()
            print(u"width：%d，hight：%d" % (size.width(), size.height()))
            img = QtGui.QImage(size.width(), size.height(), QtGui.QImage.Format_ARGB32)
            painter = QtGui.QPainter(img)
            self.render(painter)
            painter.end()
            filename = 'page.png'
            if img.save(filename):
                filepath = os.path.join(os.path.dirname(__file__), filename)
                print(u"success：%s" % filepath)
            else:
                print(u"fail")
        else:
            print("Error")
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    shotter = PageShotter(r'C:\Output.html')
    shotter.shot()
    app.exec()