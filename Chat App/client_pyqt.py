import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QFont

class ChatClient(QWidget):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.client_socket = None
        self.username = None
        self.chatroom = None

    def init_ui(self):
        self.setWindowTitle("Chat Application")
        self.resize(800, 600)  # Increase window size
        self.setStyleSheet("""
            background-color: #ECE5DD;
            color: #000;
            font-size: 14px;
        """)  # Set window background color to WhatsApp light grey

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            padding: 10px;
        """)  # Set username input background color to white
        self.layout.addWidget(self.username_input)

        self.chatroom_label = QLabel("Chatroom")
        self.layout.addWidget(self.chatroom_label)
        self.chatroom_input = QLineEdit()
        self.chatroom_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            padding: 10px;
        """)  # Set chatroom input background color to white
        self.layout.addWidget(self.chatroom_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #25D366, stop:1 #128C7E);
            color: white;
            padding: 10px;
            font-weight: bold;
        """)  # Set connect button gradient background color
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            padding: 10px;
        """)  # Set text area background color to white
        self.layout.addWidget(self.text_area)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message...")
        self.message_input.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            padding: 10px;
        """)  # Set message input background color to white
        self.message_input.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #25D366, stop:1 #128C7E);
            color: white;
            padding: 10px;
            font-weight: bold;
        """)  # Set send button gradient background color
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.file_button = QPushButton("Send Media")
        self.file_button.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #075E54, stop:1 #128C7E);
            color: white;
            padding: 10px;
            font-weight: bold;
        """)  # Set send media button gradient background color
        self.file_button.clicked.connect(self.send_file)
        self.layout.addWidget(self.file_button)

        self.clear_button = QPushButton("Clear History")
        self.clear_button.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF0000, stop:1 #8B0000);
            color: white;
            padding: 10px;
            font-weight: bold;
        """)  # Set clear history button gradient background color
        self.clear_button.clicked.connect(self.clear_history)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)
        self.message_received.connect(self.display_message)

    def connect_to_server(self):
        self.username = self.username_input.text()
        self.chatroom = self.chatroom_input.text()

        if not self.username or not self.chatroom:
            QMessageBox.warning(self, "Input Error", "Please enter both username and chatroom.")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("127.0.0.1", 12345))

            self.client_socket.send(self.username.encode('utf-8'))
            self.client_socket.recv(1024)  # Acknowledgement from server
            self.client_socket.send(self.chatroom.encode('utf-8'))
            self.client_socket.recv(1024)  # Acknowledgement from server

            self.connect_button.setDisabled(True)
            self.username_input.setDisabled(True)
            self.chatroom_input.setDisabled(True)
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.message_received.emit(message)
            except ConnectionResetError:
                break

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_input.clear()
            self.display_message(f'{self.username}: {message}')

    def send_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Select File")[0]
        if file_path:
            # For now, just display a message about the file
            self.display_message(f'File selected: {file_path}')

    def clear_history(self):
        self.text_area.clear()

    def display_message(self, message):
        # Check if the message contains a username
        if ":" in message:
            # Split the message into username and text
            username, text = message.split(":", 1)

            # Determine if the message is from the sender or receiver
            is_sender = username.strip() == self.username

            # Set colors and font weight based on sender or receiver
            if is_sender:
                color = "#DCF8C6"  # Color for sender (light green)
            else:
                color = "#ECE5DD"  # Color for receiver (light grey)

            # Add HTML tags to apply color and font weight
            formatted_message = f"<div style='background-color:{color}; padding:5px; margin:5px; border-radius:5px;'><b>{username}:</b> {text}</div>"

            # Append the formatted message to the text area
            self.text_area.append(formatted_message)
            self.text_area.moveCursor(QTextCursor.End)
        else:
            # If the message format is unexpected, simply display it
            self.text_area.append(message)
            self.text_area.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    font = QFont("Arial", 12)  # Increase font size
    app.setFont(font)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
