import sys
from Client import Client
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread


class MainWindow(QWidget):
    """
    A class used to create a window
    here we have all of its elements
    like QStackedWidget to switch between
    sceens or instance of TopBar class

    Methods:

    setMainStyle(self)
        Loads the qss style, set window size,
        its opacity etc...

    layoutSetUp(self)
        Creates layout and add widgets to it

    switchSceen(self, userName, ipAddr)
        Changes the displayed widget in QStackedWidget
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.MainStack = QStackedWidget()

        self.setMainStyle()
        self.layoutSetUp()

    def setMainStyle(self):
        self.setMinimumSize(800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        self.setStyleSheet(open("MainStyle.qss", "r").read())

    def layoutSetUp(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(TopBar(self))
        stack1 = LoginWidget(self)
        self.MainStack.addWidget(stack1)
        layout.addWidget(self.MainStack)
        self.setLayout(layout)

    def switchSceen(self, userName, ipAddr):
        stack2 = ChatWidget(userName, ipAddr)
        self.MainStack.addWidget(stack2)
        self.MainStack.setCurrentWidget(stack2)


class LoginWidget(QWidget):
    """
    A class used to create login sceen

    Methods:
    loginSetUp(self)
        Creates a layout and add widgets to it

    """
    def __init__(self, parent):
        super(LoginWidget, self).__init__()
        self.setStyleSheet(open("LoginStyle.qss", "r").read())
        self.parent = parent
        self.loginSetUp()

    def loginSetUp(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(200, 100, 200, 100)

        inputName = QLineEdit()
        inputName.setPlaceholderText("Enter Your Name")
        inputIp = QLineEdit()
        inputIp.setPlaceholderText("Enter server ip address")

        btn = QPushButton("Connect!")
        btn.clicked.connect(self.switchSceen(inputName, inputIp))
        layout.addWidget(inputName)
        layout.addWidget(inputIp)
        layout.addWidget(btn)
        self.setLayout(layout)

    def switchSceen(self, inputName, inputIp):
        """
        Calls the parent method to change the scene

        Params:

        inputName : str
            User name

        inputIp : str
            Ip address of the server

        """
        def switch():
            self.parent.switchSceen(inputName.text(), inputIp.text())
        return switch


class ChatWidget(QWidget):
    """
    Main chat widget
    Displays a list of connected users
    Chat box, and user input box

    styleSetUp(self)
        Loads the qss style, set window size,
        its opacity etc...

    layoutSetUp(self)
        Creates layout and add widgets to it

    keyPressEvent(self, e)
        Sends a message to the server if the eneter key was pressed

    """

    def __init__(self, name, ip):
        super(ChatWidget, self).__init__()
        self.name = name
        self.usersNames = []
        self.handler = Client(name)
        self.handler.connect(ip, 7776)
        self.usersList = QTextEdit()
        self.chatText = QTextEdit()
        self.inputLine = QLineEdit()
        self.styleSetUp()
        self.layoutSetUp()
        thread1 = Thread(target=self.handler.myrecive, args=(self.chatText, self.usersNames,))
        thread1.start()

    def styleSetUp(self):
        self.setStyleSheet(open("ChatStyle.qss", "r").read())

    def layoutSetUp(self):
        layout = QHBoxLayout()
        sublayout = QVBoxLayout()
        sublayout.addWidget(self.chatText)
        sublayout.addWidget(self.inputLine)
        layout.addWidget(self.usersList, 20)
        layout.addLayout(sublayout, 80)
        self.chatText.setReadOnly(True)
        self.usersList.setReadOnly(True)
        self.setLayout(layout)

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.handler.mysend(bytes(self.inputLine.text(), "utf8"))
            self.inputLine.clear()
            self.usersList.clear()
            for e in self.usersNames:
                self.usersList.append(e)


class TopBar(QWidget):
    def __init__(self, parent):
        super(TopBar, self).__init__()
        self.parent = parent
        self.setStyleSheet(open("TopBarStyle.qss", "r").read())
        self.layoutSetUp();
        self.start = QPoint(0, 0)

    def layoutSetUp(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Chat App")
        title.setAlignment(Qt.AlignCenter)

        btn_close = QPushButton("x")
        btn_close.clicked.connect(self.btn_close_clicked)

        btn_min = QPushButton("-")
        btn_min.clicked.connect(self.btn_min_clicked)

        layout.addWidget(title)
        layout.addWidget(btn_min)
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())

    def mouseMoveEvent(self, event):
        shift = self.mapToGlobal(self.mapToGlobal(event.pos()) - self.start)
        self.parent.move(shift.x(), shift.y())
        self.start = event.globalPos()

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()


app = QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec_())

