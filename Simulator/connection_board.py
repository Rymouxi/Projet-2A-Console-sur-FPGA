import tkinter as tk
import customtkinter as ctk
import serial
from serial.tools.list_ports import comports

ser = None

def connect_board():
    popup = tk.Tk()
    popup.title("Paramètres de la carte")

    ports = [port.device for port in comports()]
    if not ports:
       tk.Label(popup, text="Aucun port COM disponible",font=("Arial",20),foreground="red").grid(row=0)
    else:
        tk.Label(popup, text="Port COM disponible").grid(row=0)
        com_port = tk.StringVar(popup)
        com_port.set(ports[0])  # set the default option
        tk.Label(popup, text="Com Port").grid(row=0)
        com_port_menu = tk.OptionMenu(popup, com_port, *ports)
        com_port_menu.grid(row=0, column=1)

    baudrates = [300, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200]
    baudrate = tk.IntVar(popup)
    baudrate.set(baudrates[4])  # set the default option to 9600
    tk.Label(popup, text="Baudrate").grid(row=1)
    baudrate_menu = tk.OptionMenu(popup, baudrate, *baudrates)
    baudrate_menu.grid(row=1, column=1)

    timeouts = [None, 1, 2, 3, 4, 5]
    timeout = tk.StringVar(popup)
    timeout.set(timeouts[1])  # set the default option
    tk.Label(popup, text="Timeout").grid(row=2)
    timeout_menu = tk.OptionMenu(popup, timeout, *timeouts)
    timeout_menu.grid(row=2, column=1)

    parities = ['None', 'Even', 'Odd', 'Mark', 'Space']
    parity = tk.StringVar(popup)
    parity.set(parities[0])  # set the default option
    tk.Label(popup, text="Parity").grid(row=3)
    parity_menu = tk.OptionMenu(popup, parity, *parities)
    parity_menu.grid(row=3, column=1)

    stopbits = [1, 1.5, 2]
    stopbit = tk.StringVar(popup)
    stopbit.set(stopbits[0])  # set the default option
    tk.Label(popup, text="Stopbits").grid(row=4)
    stopbits_menu = tk.OptionMenu(popup, stopbit, *stopbits)
    stopbits_menu.grid(row=4, column=1)

    bytesizes = [5, 6, 7, 8]
    bytesize = tk.StringVar(popup)
    bytesize.set(bytesizes[3])  # set the default option
    tk.Label(popup, text="Bytesize").grid(row=5)
    bytesize_menu = tk.OptionMenu(popup, bytesize, *bytesizes)
    bytesize_menu.grid(row=5, column=1)

    def on_ok():
        global ser
        baudrate = baudrate.get()
        timeout = timeout.get()
        parity = parity.get()
        stopbits = stopbits.get()
        bytesize = bytesize.get()

        ser = serial.Serial(port=com_port.get(), baudrate=baudrate, timeout=timeout, parity=parity, stopbits=stopbits, bytesize=bytesize)
        popup.destroy()

    tk.Button(popup, text="OK", command=on_ok).grid(row=6)

    popup.mainloop()

def disconnect_board():
    close_serial = input("Voulez-vous fermer la connexion série? (Oui/Non)").lower()

    if close_serial == "oui":
        global ser
        ser.close()
        print("Connexion série fermée.")
    else:
        print("Connexion série non fermée.")
