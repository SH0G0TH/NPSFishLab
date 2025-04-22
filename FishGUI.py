import sys
import paramiko
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

'''
This script handles connecting to your raspberry pi, creating a Gui allowing for a user to input commands for the fish,
and passing those commands onto the pi.

Author: Justin Rauh
Date: 04/22/2025
Version: 1.0
'''


# These parameters are for the SSH connection.
# Replace the values of HOST_NAME, USER_NAME, and PASSWORD

HOST_NAME = "guppy.local"
USER_NAME = "fish"
PASSWORD = "password"
PORT = 22


# This class defines the GUI window. It requires a client object to be run, as it also houses the code that controls
# what is sent to the pi.
class MainWindow(QMainWindow):
    def __init__(self, client):


        super().__init__()
        self.client = client # Sets the SSH client as a global variable
        self.setWindowTitle("Fish Controls")
        self.head = QPushButton("Head")
        self.head.pressed.connect(self.move_head)
        self.head.released.connect(self.head_tail_neutral)
        self.tail = QPushButton("Tail")
        self.tail.pressed.connect(self.move_tail)
        self.tail.released.connect(self.head_tail_neutral)
        self.mouth = QPushButton("Mouth")
        self.mouth.pressed.connect(self.open_mouth)
        self.mouth.released.connect(self.mouth_close)

        layout = QVBoxLayout()

        layout.addWidget(self.head)
        layout.addWidget(self.tail)
        layout.addWidget(self.mouth)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    def fish_command(self, command):
        stdin, stdout, stderr = client.exec_command("source Billy/bin/activate;"+command)
        print(stdout.read().decode())
        print(stderr.read().decode())
    def move_head(self):
        self.fish_command("python fishCommand.py 1 .9")
        print("Head!")

    def move_tail(self):
        self.fish_command("python fishCommand.py 1 -.9")
        print("Tail!")

    def open_mouth(self):
        self.fish_command("python fishCommand.py 2 1")
        print("Mouth Open!")

    def head_tail_neutral(self):
        self.fish_command("python fishCommand.py 1 0")
        print("Head/Tail Rest!")

    def mouth_close(self):
        self.fish_command("python fishCommand.py 2 0")
        print("Mouth Close!")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.move_head()
        elif event.key() == Qt.Key.Key_W:
            self.move_tail()
        elif event.key() == Qt.Key.Key_E:
            self.open_mouth()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.head_tail_neutral()
        elif event.key() == Qt.Key.Key_W:
            self.head_tail_neutral()
        elif event.key() == Qt.Key.Key_E:
            self.mouth_close()


app = QApplication(sys.argv)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, password=PASSWORD)

window = MainWindow(client)
window.show()

app.exec()