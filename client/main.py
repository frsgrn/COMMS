import socket
import json
import threading
from gui import *

gui = GUI()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    client.connect(('localhost', 8888))

    readIncomingThread = threading.Thread(target=read_incoming)
    readIncomingThread.start()

    gui.pack()
    gui.inputField.bind('<Return>', send_message)
    gui.root.mainloop()



def send_message(e):
    try:
        client.send(json.dumps({"route": "test", "body": {"text": gui.inputField.get()}}).encode())
        gui.inputField.delete(0, END)
    except:
        print("Failed to send...")

def read_incoming():
    while True:
        data, addr = client.recvfrom(1024)
        print(data.decode())
        j = json.loads(data.decode())
        gui.chatWindow.insert(END, j["sender"]["name"] + "> " + j["content"] + "\n")

if __name__ == "__main__":
    main()