import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl

class PyBridge(QObject):
    @Slot(str)
    def loadPage(self, page_key):
        print(f"➡ Python recebeu pedido para mostrar a seção: {page_key}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste SPA PySide6")
        self.resize(800, 600)

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # WebChannel
        self.channel = QWebChannel()
        self.bridge = PyBridge()
        self.channel.registerObject("pyBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        # Carrega o HTML
        base = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base, "index.html")
        self.web_view.load(QUrl.fromLocalFile(html_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
