import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QTabWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserExplorer(QMainWindow):
    def __init__(self):
        super(BrowserExplorer, self).__init__()
        self.setWindowTitle('ShellOS Browser')

        self.tab_widget = QTabWidget()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        back_btn = QPushButton('←')
        back_btn.clicked.connect(self.navigate_back)

        forward_btn = QPushButton('→')
        forward_btn.clicked.connect(self.navigate_forward)

        home_btn = QPushButton('🏠')
        home_btn.clicked.connect(self.navigate_home)

        navtb = QWidget()
        nav_layout = QHBoxLayout(navtb)
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(self.url_bar)

        main_layout = QVBoxLayout()
        main_layout.addWidget(navtb)
        main_layout.addWidget(self.tab_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

    def navigate_home(self):
        current_browser = self.tab_widget.currentWidget()
        current_browser.setUrl(QUrl('http://www.google.com'))

    def navigate_to_url(self):
        current_browser = self.tab_widget.currentWidget()
        url = self.url_bar.text()
        current_browser.setUrl(QUrl(url))

    def navigate_back(self):
        current_browser = self.tab_widget.currentWidget()
        current_browser.back()

    def navigate_forward(self):
        current_browser = self.tab_widget.currentWidget()
        current_browser.forward()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tab_widget.addTab(browser, label)

        self.tab_widget.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

    def update_urlbar(self, q, browser=None):
        if browser != self.tab_widget.currentWidget():
            return

        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserExplorer()
    window.show()
    sys.exit(app.exec_())