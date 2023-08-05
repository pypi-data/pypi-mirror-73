import tkinter as tk
from tkinter import filedialog, Text
from twilio.rest import Client
import os
try:
    from run import *
except ModuleNotFoundError:
    try:
        from sms import *
    except ModuleNotFoundError:
        from main import *
# from back import *

root = tk.Tk()
root.title('twilioSMS')
rgbl = '#6B5A00'

client = Client(account_sid, auth_token)

def fsms(cell, message):
    client.messages.create(
        to=cell, from_=my_twilio, body=message)


def fspam(cell, message):
    i = 0
    while i < 5:
        fsms(cell, message)
        i += 1


canvas = tk.Canvas(root, height=200, width=300)
canvas.pack()

frame = tk.Frame(root, bg='#6B5A00')
frame.place(relheight=1, relwidth=1)

sid = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
sid.pack()
sid.insert(0, account_sid)

token = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
token.pack()
token.insert(0, auth_token)

message = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
message.pack()
message.insert(0, 'message')

cell = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
cell.pack()
cell.insert(0, my_cell)

Send = tk.Button(frame, text='Send', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=lambda: fsms(cell.get(), message.get()))
Send.pack()

Spam = tk.Button(frame, text='SPAM!', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=lambda: fspam(cell.get(), message.get()))
Spam.pack()

# Color = tk.Button(frame, text='Change Color', padx=10,
#                  pady=5, fg='#FFFFFF', bg='#6B5A00',
#                  command=lambda: fcolor())

Quit = tk.Button(frame, text='Quit', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=root.destroy)
Quit.pack()

root.mainloop()
