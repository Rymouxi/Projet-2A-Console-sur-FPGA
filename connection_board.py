import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale

def select_com_port():
    com_port = simpledialog.askstring("Sélection du Port COM", "Entrez le numéro du port COM (ex: COM1):")
    return com_port

def select_baudrate():
    baudrate = simpledialog.askinteger("Sélection du baudrate", "Entrez le baudrate (ex: 9600):")
    return baudrate


def select_timeout():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    timeout = simpledialog.askinteger("Sélection du timeout", "Entrez le timeout (ex: 1):")

    return timeout

def select_parity():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    parity = simpledialog.askstring("Sélection du parity", "Entrez le parity (ex: N):")

    return parity

def select_stopbits():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    stopbits = simpledialog.askinteger("Sélection du stopbits", "Entrez le stopbits (ex: 1):")

    return stopbits

def select_bytesize():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    bytesize = simpledialog.askinteger("Sélection du bytesize", "Entrez le bytesize (ex: 8):")

    return bytesize

