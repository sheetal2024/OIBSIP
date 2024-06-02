# Chat Application

This is a comprehensive chat application built using Python and PyQt5, designed to real-time communication between users. The application supports chatrooms, allowing users to join rooms and interact with others in those rooms. Additionally, it provides features such as sending files, maintaining chat history, and incorporating emojis in messages.

## Project Structure

```
Chat App/
│
├── client_pyqt.py         
├── server.py              
├── database.py            
├── multimedia.py          
├── emoji.py               
├── authentication.py      
├── requirements.txt       
├── README.md              
```

## Requirements

- Python 3.x
- PyQt5
- emoji
- plyer
- cryptography
- Pillow

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## How to Run

### Server

1. Navigate to the project directory.
2. Run the server application:

```bash
python server.py
```

The server will start.

### Client

1. Navigate to the project directory.
2. Run the client application:

```bash
python client_pyqt.py
```

3. In the client window, enter your username and chatroom, then click "Connect".

4. You can now send messages by typing in the input field and pressing "Enter" or clicking the "Send" button.

5. Use the "Send Media" button to send files, and the "Clear History" button to clear the chat history.

### Note

Make sure the server is running before starting the client application to ensure proper connection.