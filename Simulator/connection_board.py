import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import serial
from serial.tools.list_ports import comports
import tkinter.messagebox

ser = None

def connect_board():
    popup = ctk.CTk()
    popup.title("The card's parameters")

    ports = [port.device for port in comports()]
    if not ports:
       tk.Label(popup, text="Aucun port COM disponible",font=("Arial",20),foreground="red").grid(row=0)
    else:
        com_port = tk.StringVar(popup)
        com_port.set(ports[0])  # set the default option
        tk.Label(popup, text="Available COM ports").grid(row=0)
        com_port_menu = ttk.OptionMenu(popup, com_port, *ports)
        com_port_menu.grid(row=0, column=1)

    baudrates = [300, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200]
    baudrate = tk.StringVar(popup)
    baudrate.set(baudrates[4])  # set the default option to 9600
    tk.Label(popup, text="Baudrate").grid(row=1)
    baudrate_menu = ttk.OptionMenu(popup, baudrate, *baudrates)
    baudrate_menu.grid(row=1, column=1)

    timeouts = [None, 1, 2, 3, 4, 5]
    timeout = tk.StringVar(popup)
    timeout.set(timeouts[1])  # set the default option
    tk.Label(popup, text="Timeout").grid(row=2)
    timeout_menu = ttk.OptionMenu(popup, timeout, *timeouts)
    timeout_menu.grid(row=2, column=1)

    parities = ['None', 'Even', 'Odd', 'Mark', 'Space']
    parity = tk.StringVar(popup)
    parity.set(parities[0])  # set the default option
    tk.Label(popup, text="Parity").grid(row=3)
    parity_menu = ttk.OptionMenu(popup, parity, *parities)
    parity_menu.grid(row=3, column=1)

    stopbits = [0,1]
    stopbit = tk.StringVar(popup)
    stopbit.set(stopbits[0])  # set the default option
    tk.Label(popup, text="Stopbits").grid(row=4)
    stopbits_menu = ttk.OptionMenu(popup, stopbit, *stopbits)
    stopbits_menu.grid(row=4, column=1)

    bytesizes = [8,16,32]
    bytesize = tk.StringVar(popup)
    bytesize.set(bytesizes[3])  # set the default option
    tk.Label(popup, text="Bytesize").grid(row=5)
    bytesize_menu = ttk.OptionMenu(popup, bytesize, *bytesizes)
    bytesize_menu.grid(row=5, column=1)

    def on_ok():
        global ser
        selected_baudrate = int(baudrate.get())
        selected_timeout = int(timeout.get())
        selected_parity = parity.get()
        selected_stopbits = int(stopbit.get())
        selected_bytesize = int(bytesize.get())

        # Map the values of chains to constants of serial for parity
        parity_mapping = {'None': serial.PARITY_NONE, 'Even': serial.PARITY_EVEN, 'Odd': serial.PARITY_ODD, 'Mark': serial.PARITY_MARK, 'Space': serial.PARITY_SPACE}
        selected_parity = parity_mapping.get(selected_parity, serial.PARITY_NONE)

        # Map the values of chains to constants of serial for stopbits
        stopbits_mapping = {0: serial.STOPBITS_ONE, 1: serial.STOPBITS_TWO}
        selected_stopbits = stopbits_mapping.get(selected_stopbits, serial.STOPBITS_ONE)
        ser = serial.Serial(port=com_port.get(),baudrate=selected_baudrate, timeout=selected_timeout, parity=selected_parity, stopbits=selected_stopbits, bytesize=selected_bytesize)
        popup.destroy()
    ttk.Button(popup, text="OK", command=on_ok).grid(row=6)

    popup.mainloop()
    
def disconnect_board():
    close_serial = tkinter.messagebox.askyesno("Fermer la connexion série", "Voulez-vous fermer la connexion série?")
    
    if close_serial:
        global ser
        ser.close()
        print("Connexion série fermée.")
    else:
        print("Connexion série non fermée.") 
