# ---------- ENSEA's Python LCM3 Simulator ---------- #
#
# Engineers :
#
# APPOURCHAUX Léo, BITTAUD CANOEN Laël, GABORIEAU Cyprien, JIN Clémentine
# LATRECHE Loubna, OULAD ALI Rym, XIANG Justine, YE Yumeng
#
# Professors :
#
# Mr. Kessal, Mr. Laroche, Mr. Monchal
#
# --------------------------------------------------- #



import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random
import webbrowser

# Try to kill frames and re-init them on runsbs to lower the load
# Valeurs dans la mémoire c'est le code en hexa de l'intruction
# Rajouter un bouton compilation et calculer tous les 0 et les 1 ainsi que le schangements de valeurs des registres lors de l'appui sur le bouton.
# initialiser la taille de la mémoire en fonction du code

# Add the current directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the connect_board module
from connection_board import *




# ---------- Variables ---------- #

file_path = None  # Stores whether the file is saved somewhere

registers = []    # Registers' array

run_state = 0     # Turns to 1 when run_step_by_step is clicked, back to 0 when stop is clicked



''' Some global variables are defined in functions:

    asm_zone:       Text center zone defined in asm_zone_init().
    reg_frame:      Register frame defined in registers_init().
    memory_tree:    Memory arraydefined in memory_array_init().
    pip_frame:      Pipeline frame defined in pipeline_init().
    button_runsbs:  Step_by_step button defined in btn_runsbs_init().
    button_step:    Step button defined in btn_step_init().
    file_path:      Redefined as global in save(), import(), and save_as().
'''






# ---------- Interface Edition Functions (for Lael and Cyprien) ---------- #


def reg_edit(Rx: int, value: int, color: str):
    '''Edits the registers' values and colors.\n
        Inputs:\n
        Rx: Index of the register (between 0 and 15).\n
        value: New value to put into the register.\n
        color: Name of the color in which the register will be displayed.'''

    if 0 <= Rx < 8:
        hex_value = "0x"+format(value, '08x')  # Changes from int to string hex display (0x08......)
        reg_value = tk.StringVar()             # Changes from string hex to tk.StringVar
        reg_value.set(hex_value)
        reg_label = ttk.Label(reg_frame, text=f"R{Rx}:", foreground=color)          # Register name and its color
        reg_field = ttk.Label(reg_frame, textvariable=reg_value, foreground=color)  # Register value and its color
        reg_label.grid(row=Rx, column=0, sticky="w", padx=5, pady=2)                # Register's name Config and size
        reg_field.grid(row=Rx, column=1, sticky="w", padx=5, pady=2)                # Register's value Config and size
        registers[Rx] = reg_value  # Changes the value


def mem_edit(line: int, binary_value: str, instruction: str, color: str):
    '''Edits the memory values, corresponding instructions, and colors.\n
        Inputs:\n
        line: Number of the line to modify.\n
        value: Hex value to insert in the second column.\n
        instr: Text to insert in the third column.\n
        color: Name of the color in which the line will be displayed.'''

    value = int(binary_value, 2)
    hex_value = "0x"+format(value, '04x')           # Changes from int to string hex display (0x08......)
    item_id = memory_tree.get_children()[line - 1]  # Gets the item ID for the line
    memory_tree.item(item_id, values=(memory_tree.item(item_id, "values")[0], hex_value, memory_tree.item(item_id, "values")[2]))    # Updates the value
    memory_tree.item(item_id, values=(memory_tree.item(item_id, 'values')[0], memory_tree.item(item_id, 'values')[1], instruction))  # Updates the instruction

    if line % 2 == 1:  # Following part to ensure the background doesn't change color
        tags = "even"
    else:
        tags = "odd"
    memory_tree.item(item_id, tags=tags)
    memory_tree.tag_configure("even", background="gainsboro", foreground=color)  # One color on even numbered lines
    memory_tree.tag_configure("odd", background="whitesmoke", foreground=color)  # Other one on odd numbered lines


def pip_edit(pip_text):
    '''Iterates the pipeline and adds a new instruction column'''

    def pip_get_column(c: int):
        '''Retrieves the content of a specific column in the pipeline array.
            Input: c: Number of the column to retrieve /!\ FDE is 0, MAX is 16.
            Returns: A list of lists, where each inner list contains the content of the specified column (array of 3 strings).
        '''
        
        column_frame = pip_frame.grid_slaves(row=0, column=c)
        if column_frame:
            column_labels = column_frame[0].grid_slaves()
            column_labels.reverse()
            column_text = [[label.cget("text") for label in column_labels[i:i + 3]] for i in range(0, len(column_labels), 3)]         # Pastes the text
            column_color = [[label.cget("foreground") for label in column_labels[i:i + 3]] for i in range(0, len(column_labels), 3)]  # Puts the old color back
            return [column_text[0], column_color[0]]
        return None

    # Shift all the columns of the pipeline to the left.
    for i in range(18):
        text_color = pip_get_column(18-i)
        pip_modify_column(text_color[0], 19-i, text_color[1])

    text_color = pip_get_column(1)  # Gets the colors of each text in the first column

    # defines an array of colors we can pick into
    colors = ["black", "dimgray", "darkgray", "rosybrown", "lightcoral", "indianred", "brown", "maroon", "red", "tomato", "darksalmon", "coral", "sienna", "chocolate", "peru",
              "darkorange", "darkgoldenrod", "darkkhaki", "olive", "olivedrab", "yellowgreen", "darkolivegreen", "darkseagreen", "forestgreen", "limegreen", "seagreen", "turquoise",
              "lightseagreen", "teal", "deepskyblue", "skyblue", "lightskyblue", "steelblue", "dodgerblue", "slategray", "cornflowerblue", "royalblue", "navy", "mediumblue", "blue",
              "slateblue", "blueviolet", "darkorchid", "mediumorchid", "plum", "purple", "magenta", "orchid", "mediumvioletred", "deeppink", "hotpink", "crimson"]
    
    color = random.choice(colors)  # Choses a random color from 'colors'

    column_frame = ttk.LabelFrame(pip_frame)
    column_frame.grid(row=0, column=1, sticky="w")  # Creation of the column
    column_label = ttk.Label(column_frame, text=pip_text, width=5, foreground=color)  # Inserts the new element
    column_label.grid(padx=10, pady=8, sticky="w")
    column_label = ttk.Label(column_frame, text=text_color[0][0], width=5, foreground=text_color[1][0])  # Pastes the former first element in the 2nd line
    column_label.grid(padx=10, pady=8, sticky="w")
    column_label = ttk.Label(column_frame, text=text_color[0][1], width=5, foreground=text_color[1][1])  # Pastes the former second element in the 3rd line
    column_label.grid(padx=10, pady=8, sticky="w")


# /!\ This function might not be necessary as asm_code should be accessible everywhere. It improves visibility though.
def asm_get_code():
    '''Gets the asm code in the asm zone.\n
        Returns: Content of the asm zone.'''

    asm_code = asm_zone.get("1.0", tk.END)  # Copy of the asm_zone content into asm_code
    return(asm_code)






# ---------- Main Function ---------- #


def main():
    '''Main function. Runs the program.'''

    window = main_window_init()

    # Examples of use
    reg_edit(6, 2526451350, "red")
    mem_edit(10, "0100111010101", "MOV R1, R2", "red")
    pip_edit("MOV")
    pip_edit("LDR")
    pip_edit("STR")
    pip_edit("uretre")
    pip_edit("bruh")
    pip_edit("bryan")
    pip_edit("1")
    pip_edit("2")
    pip_edit("3")
    pip_edit("4")
    pip_edit("5")
    pip_edit("6")
    pip_edit("7")
    pip_edit("8")
    pip_edit("9")

    # Call to Lael and Cyp's code

    window.mainloop()






# ---------- Interface Initialization Functions ---------- #


def main_window_init():
    '''This function initializes the main window and calls all the other initialisation functions.\n
        Returns: The window on which everything is happening.'''

    # Creation of the main window
    window = ctk.CTk()
    window.title("ENSEA's Python LCM3 ASM Simulator") 
    window.geometry("980x720")      # Initial size of the window
    main_frame = ctk.CTkFrame(window)  # Main frame
    main_frame.pack(expand=True, fill="both")

    # Creation of the other frames
    toolbar = toolbar_init(main_frame)    # Top toolbar
    memory_array_init(main_frame)         # Memory array frame on the left of the assembly zone
    asm_zone_init(main_frame)  # Assembly code area in the middle
    registers_init(main_frame)            # Register list frame on the right of the assembly zone
    pipeline_init(window)                 # Pipeline array frame at the bottom

    # Creation of the toolbar buttons
    btn_file_menu_init(toolbar)
    btn_settings_menu_init(toolbar)
    btn_help_menu_init(toolbar)
    btn_dowload_init(toolbar)
    btn_connect_init(toolbar)
    btn_reset_init(toolbar)
    btn_step_init(toolbar)
    btn_runsbs_init(toolbar)
    btn_compile_init(toolbar)

    ctk.set_appearance_mode("Light")

    return(window)


def toolbar_init(main_frame):
    '''Creates the top toolbar frame.\n
        Input: main_frame: Frame in which the toolbar will be generated.\n
        Returns: Frame in which we will generate the buttons.'''

    toolbar_frame = ctk.CTkFrame(main_frame)                  # Frame for the top toolbar
    toolbar_frame.pack(side="top", fill="x")
    return(toolbar_frame)


def memory_array_init(main_frame):
    '''Creates the left memory frame and fills it with an array.'''

    # Frame for the memory section
    memory_frame = ttk.LabelFrame(main_frame, text="Memory")
    memory_frame.pack(side="left", fill="y", pady=10)

    # Creation of the Tree (array)
    global memory_tree
    memory_tree = ttk.Treeview(memory_frame, columns=("Address", "Value", "Instruction"), show='headings')
    memory_tree.heading("Address", text="Address")  # Title/heading text
    memory_tree.heading("Value", text="Value")
    memory_tree.heading("Instruction", text="Instruction")
    memory_tree.column("Address", width=70)         # Column widths
    memory_tree.column("Value", width=50)
    memory_tree.column("Instruction", width=180)

    # Initialization of the memory
    for i in range(2048):
        address = "0x"+format(i*2+134217728, '08x')  # Creates the iterable adress 2 by 2 with a 0x0800000 offset
        value = "0x"+format(0, '04x') 
        instruction = ""

        tags = ()  # Tags are used to add a background color inside the array to improve visibility
        if i % 2 == 0:
            tags = ("row1")
        else:
            tags = ("row2")
        memory_tree.insert("", tk.END, values=(address, value, instruction), tags=tags)
    memory_tree.tag_configure("row1", background="gainsboro", foreground="black")   # One color on even numbered lines
    memory_tree.tag_configure("row2", background="whitesmoke", foreground="black")  # Other one on odd numbered lines

    memory_tree.pack(fill="both", expand=True, pady=5)

    mem_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=memory_tree.yview)  # Creation of a vertical scrollbar
    mem_scrollbar.pack(side="left", fill="y", pady=10)
    memory_tree.config(yscrollcommand=mem_scrollbar.set)


def asm_zone_init(main_frame):
    '''Creates the asm text frame.\n
        Input: main_frame: Frame in which the asm window will be created.'''
    
    def on_key(event):
        if event.char.islower():
            # If the typed character is lowercase, replace it with uppercase
            asm_zone.insert(tk.INSERT, event.char.upper())
            return "break"  # Prevent the default action for lowercase characters
        else:
            return None  # Let the default action proceed for other keys

    global asm_zone
    asm_zone = tk.Text(main_frame, width=40, height=20)
    asm_zone.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    asm_scrollbar = ttk.Scrollbar(asm_zone, orient=tk.VERTICAL, command=asm_zone.yview)  # Creation of a vertical scrollbar
    asm_scrollbar.pack(side="right", fill="y")
    asm_zone.config(yscrollcommand=asm_scrollbar.set)  # Configuration of the text widget to work with the scrollbar

    asm_zone.bind("<Key>", on_key)


def registers_init(main_frame):
    '''Initializes the registers' value and window.'''

    global reg_frame
    reg_frame = ttk.LabelFrame(main_frame, text="Registers")
    reg_frame.pack(side="right", fill="y", pady=10)

    # Creation of the register widgets
    for i in range(8):
        reg_value = tk.StringVar()
        registers.append(reg_value)
        reg_edit(i, 0, "black")


def pipeline_init(window):
    '''Creates the pipeline frame.\n
        Input: window: Frame into which the pipeline will be generated.'''
    
    # Pipeline frame at the bottom
    global pip_frame
    pip_frame = ttk.LabelFrame(window, text="Pipeline")
    pip_frame.pack(side="bottom", fill="both", padx=10, pady=10)

    # Fetch Decode Execute
    pip_fde_frame = ttk.LabelFrame(pip_frame)
    pip_fde_frame.grid(row=0, column=0, sticky="w", padx=5)  # Creation of the column
    pip_fde_lines = ["Fetch", "Decode", "Execute"]   # Text array to copy in the column
    for i, header in enumerate(pip_fde_lines):
        header_label = ttk.Label(pip_fde_frame, text=header, width=8)    # Column text
        header_label.grid(row=i, column=0, padx=12, pady=8, sticky="w")  # Column shape and place config

    # Initialisation of the other cells (19 of them)
    pip_column_text = [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""],
        ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]

    for i, col_labels in enumerate(pip_column_text):
        pip_modify_column(col_labels, i+1, ["black", "black", "black"])


def pip_modify_column(pip_column_text, c: int, color_array):
    '''Creates or modifies an existing column in the pipeline array. \n
        Inputs:
        pip_column_text: Text data that will fill the column.\n
        c: Number of the column to create/modify /!\ FDE is 0, MAX is 16.\n
        color_aray: Array of 3 colors corresponding to the Fetch, Decode and execute lines in the column.'''

    if 0 <= c < 20:
        column_frame = ttk.LabelFrame(pip_frame)
        column_frame.grid(row=0, column=c, sticky="w")  # Creation of the column

        for i, text in enumerate(pip_column_text):
            column_label = ttk.Label(column_frame, text=text, width=5, foreground=color_array[i])  # Column text and color
            column_label.grid(padx=10, pady=8, sticky="w")                                         # Column shape and place config






# ---------- Button Functions ---------- #


def btn_file_menu_init(toolbar):
    '''Creates and initializes the file menu.\n
        Input: toolbar: Frame in which to place the button.'''

    file_menu = ttk.Menubutton(toolbar, text="File", direction="below")  # File menu button
    file_menu.pack(side="left")

    file_menu.menu = tk.Menu(file_menu, tearoff=0)  # File menu "menu"
    file_menu["menu"] = file_menu.menu

    def new_file():
        '''Creates a new blank code page. If code is present in the text window, asks if the user wants to save the current code.\n
            If yes: Calls the 'save_as' function.\n
            If not: The current code will be lost !'''
    
        global file_path

        # Checks if the asm_zone contains text
        if asm_zone.get("1.0", tk.END).strip():
            # Asks the user if they want to save the current content before creating a new file
            response = tk.messagebox.askyesno("Save Before Creating a New File?", "Do you want to save the current code before creating a blank page?")
            if response:
                save_as()
        if file_path:
            asm_zone.delete("1.0", tk.END)

    def import_code():
        '''Opens a dialog window to import a code. If code is present in the text window, asks if the user wants to save the current code.\n
            If yes: Calls the 'save_as' function.\n
            If not: The current code will be lost !'''

        global file_path
    
        # Checks if the asm_zone contains text
        if asm_zone.get("1.0", tk.END).strip():
            # Asks the user if they want to save the current content before importing
            response = tk.messagebox.askyesno("Save Before Import", "Do you want to save the current code before importing?")
            if response:
                save_as()

        # Open the file dialog to import code
        file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                imported_code = file.read()

                # Pastes imported code into the text area
                asm_zone.delete("1.0", tk.END)          # Clears the text area content
                asm_zone.insert(tk.END, imported_code)  # Pastes the code

    def save():
        '''Overwrites the current save file, or opens a dialog window to create a one.'''

        global file_path

        # If the file hasn't been saved yet, asks the user where to save it
        if file_path is None:
            save_as()
 
        # If the user selected a file location, saves the content of the text area to the file
        if file_path:
            with open(file_path, 'w') as file:
                saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
                file.write(saved_code)

    def save_as():
        '''Opens a dialog window to save the current code into a new file.\n
            It wont save it automatically like the 'save' function does.'''

        global file_path

        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
                file.write(saved_code)

    file_menu.menu.add_command(label="New File", command=new_file)
    file_menu.menu.add_command(label="Import", command=import_code)
    file_menu.menu.add_separator()
    file_menu.menu.add_command(label="Save", command=save)
    file_menu.menu.add_command(label="Save As", command=save_as)
    file_menu.pack()
    

def btn_settings_menu_init(toolbar):
    '''Creates and initializes the settings menu.\n
        Input: toolbar: Frame in which to place the button.'''

    settings_menu = ttk.Menubutton(toolbar, text="Settings", direction="below")
    settings_menu.pack(side="left")

    settings_menu.menu = tk.Menu(settings_menu, tearoff=0)  # File menu "menu"
    settings_menu["menu"] = settings_menu.menu

    def theme_toggle_dark():
        '''Toggles dark theme.'''

        asm_zone.config(background="dimgray", fg="white")
        ctk.set_appearance_mode("dark")

    def theme_toggle_light():
        '''Toggles light theme.'''

        asm_zone.config(background="white", fg="black")
        ctk.set_appearance_mode("light")

    settings_menu.menu.add_command(label="Dark mode", command=theme_toggle_dark)
    settings_menu.menu.add_command(label="Light mode", command=theme_toggle_light)
    settings_menu.pack()


def btn_help_menu_init(toolbar):
    '''Creates and initializes the help menu.\n
        Input: toolbar: Frame in which to place the button.'''

    help_menu = ttk.Menubutton(toolbar, text="Help", direction="below")  # Help menu button
    help_menu.pack(side="left")

    help_menu.menu = tk.Menu(help_menu, tearoff=0)  # Help menu "menu"
    help_menu["menu"] = help_menu.menu

    def help_lcm3_docu():
        '''Onpens an online documentation of the LCM3 instructions.'''

        webbrowser.open_new("https://www.irif.fr/~carton/Enseignement/Architecture/Cours/LC3/")

    help_menu.menu.add_command(label="This Simulator Documentation", command=help_simulator_docu)
    help_menu.menu.add_separator()
    help_menu.menu.add_command(label="LCM3 Documentation", command=help_lcm3_docu)


def btn_compile_init(toolbar):
    '''Compiles the code'''

    global button_compile
    button_compile = ctk.CTkButton(toolbar, text="Compile", command=compile, width=100, height=18, font = ("Arial", 10), fg_color="gray")
    button_compile.pack(side="right", padx=0)


def btn_runsbs_init(toolbar):
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.\n
        Input: toolbar: Frame in which to place the button.'''

    global button_runsbs
    button_runsbs = ctk.CTkButton(toolbar, text="Run Step by Step", command=run_step_by_step, width=100, height=18, font = ("Arial", 10), fg_color="forestgreen", state="!disabled")
    button_runsbs.pack(side="right", padx=20)


def btn_step_init(toolbar):
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.\n
        Input: toolbar: Frame in which to place the button.'''

    global button_step
    button_step = ctk.CTkButton(toolbar, text="Step ->", command=step_iter, width=100, height=18, font = ("Arial", 10), fg_color="gray")
    button_step.pack(side="right", padx=0)
    button_step.configure(state="disabled")


def btn_reset_init(toolbar):
    '''Creates the reset button which resets the registers, the memory, and the pipeline.\n
        Input: toolbar: Frame in which to place the button.'''

    button_reset = ctk.CTkButton(toolbar, text="Reset", command=reset, width=100, height=18, font = ("Arial", 10), fg_color="gray")
    button_reset.pack(side="right", padx=20)


def btn_connect_init(toolbar):
    '''Creates the connect button which automatically connects the simulator to a connected board, if there's one.\n
        Input: toolbar: Frame in which to place the button.'''

    button_connect = ctk.CTkButton(toolbar, text="Connect Board", command=connect_board, width=100, height=18, font = ("Arial", 10), fg_color="gray")
    button_connect.pack(side="right", padx=0)


def btn_dowload_init(toolbar):
    '''Creates the download button which downloads the code in the text window into the board, and executes it.\n
        Input: toolbar: Frame in which to place the button.'''

    button_download = ctk.CTkButton(toolbar, text="Download Code", command=download_code, width=100, height=18, font = ("Arial", 10), fg_color="gray")
    button_download.pack(side="right", padx=20)
    button_download.configure(state="disabled")
    # To remove as soon as the simulator is connected to a board !


def compile():
    '''Compiles the code'''

    # ...


def run_step_by_step():
    '''Simulates on the computer the execution of the code, step by step.'''

    reset()

    global run_state
    if run_state == 0:
        button_runsbs.configure(text="S T O P", fg_color="firebrick")
        run_state = 1
        button_step.configure(state="normal")
    else:
        button_runsbs.configure(text="Run Step by Step", fg_color="forestgreen")
        run_state = 0
        button_step.configure(state="disabled")


# (To be implemented)
def step_iter():
    '''Simulates on the computer the execution of the code, step by step.'''

    # ...


def reset():
    '''Resets the registers, the memory, and the pipeline.'''

    for i in range(8):
        reg_edit(i, 0, "black")
    for i in range(255):
        mem_edit(i, 0, "", "black")
    for i in range(19):
        pip_modify_column(["", "", "",], i+1, ["black", "black", "black"])


def connect_board():
    '''Connects the board.'''
    com_port = select_com_port()
    baudrate = select_baudrate()
    timeout = select_timeout()
    parity = select_parity()
    stopbits = select_stopbits()
    bytesize = select_bytesize()
    

    
    
    print(f"Paramètres de connexion :\n"
          f"Port COM : {com_port}\n"
          f"Baudrate : {baudrate}\n"
          f"Timeout : {timeout}\n"
          f"Parity : {parity}\n"
          f"Stopbits : {stopbits}\n"
          f"Bytesize : {bytesize}")


# Button "Connect Board"
connect_button = tk.Button(root, text="Connect Board", command=connect_board)
connect_button.pack()



# (To be implemented)
def download_code():
    '''Downloads the binary conversion of the asm code onto a connected board.'''


def help_simulator_docu():
    '''Onpens an online documentation of the simulator.'''

    documentation_text = ( "\n"+
    "------------------------ ENSEA's Python LCM3 Simulator ------------------------\n\n"
    "    Engineers :\n\n"
    "    APPOURCHAUX Léo, BITTAUD CANOEN Laël, GABORIEAU Cyprien, JIN Clémentine\n"
    "    LATRECHE Loubna, OULAD ALI Rym, XIANG Justine, YE Yumeng\n\n"
    "    Professors :\n\n"
    "    Mr. Kessal, Mr. Laroche, Mr. Monchal\n\n"
    "-------------------------------------------------------------------------------\n\n\n"
    "ENSEA's Python LCM3 Simulator Documentation\n\n"
    "1. Introduction\n"
    "   ENSEA's Python LCM3 Simulator is a tool that simulates the execution of programs "
    "written in LCM3 assembly language. This documentation will guide you through all the "
    "features and capabilities of the simulator.\n\n"
    "2. User Interface\n"
    "   2.1 Toolbar\n"
    "       The toolbar provides quick access to essential features.\n\n"
    "       New File: Creates a new LCM3 code file\n"
    "       Import: Imports LCM3 code from an external file\n"
    "       Save: Saves the current file\n"
    "       Save as: Saves the code to a new file or update the existing one\n"
    "       Run Step-by-Step: Starts a line-by-line execution\n"
    "       Step->: Executes the next line of code\n"
    "       Reset: Resets the simulator to its initial state\n"
    "       Setting: Customizes the simulator's appearance using theme options (light mode / dark mode)\n\n"
    "   2.2 Assembly code area\n"
    "       In this area, you can write your LCM3 assembly code. Each instruction must be on a separate line.\n\n"
    "   2.3 Memory\n"
    "       The memory display shows the current state of the simulator's memory, including addresses, "
    "values, and corresponding instructions.\n\n"
    "   2.4 Registers\n"
    "       The register panel displays the current values of the simulator's registers.\n\n"
    "   2.5 Pipeline\n"
    "       The pipeline section illustrates the currently executing instructions' steps (Fetch, Decode, Execute) and the history.\n\n"
    "3. Using the Simulator\n"
    "   3.1 Writing LCM3 Code\n"
    "       Each instruction must be on a separate line.\n\n"
    "   3.2 Running the Simulator\n"
    "       Step-by-step execution\n"
    "       1) Click Run Step by Step to execute the code one step at a time\n"
    "       2) Observe changes in memory, registers, and the pipeline at each step\n\n"
    "       Executing a step\n"
    "       1) Click Step-> to execute the next line of code\n"
    "       2) Monitor changes in memory, registers and the pipeline\n\n"
    "   3.3 Monitoring Execution\n"
    "       Checking memory Contents\n"
    "       Check the memory panel to view current values and instructions stored in memory\n\n"
    "       Observing register values\n"
    "       Check the register panel to observe values stored in each register during program execution\n\n"
    "4. Troubleshooting\n"
    "   4.1 Common Errors\n"
    "       1) Invalid Syntax: Check the syntax of your LCM3 instructions.\n"
    "       2) Undefined Labels: Ensure all labels are defined before use.\n"
    "       3) Incorrect Operator Types: Verify operator types for each instruction.\n\n"
    "   4.2 Debugging Tips\n"
    "       Check the debug window\n")

    popup = tk.Tk()
    popup.title("ENSEA's Python LCM3 Simulator - Documentation")
    popup.geometry("1200x800")

    # Frame to hold the text widget and scrollbar
    popup_frame = ttk.Frame(popup)
    popup_frame.pack(fill=tk.BOTH, expand=True)

    # Text widget for the documentation
    documentation_text_widget = tk.Text(popup_frame, wrap=tk.WORD, height=20, width=60)
    documentation_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for the Text widget
    scrollbar = ttk.Scrollbar(popup_frame, command=documentation_text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    documentation_text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the text
    documentation_text_widget.insert(tk.END, documentation_text)
    documentation_text_widget.configure(state='disabled')  # Make it un-editable






# ---------- Code ---------- #


main()


# Create a style object
#style = ttk.Style()
#style.configure("Color.TLabel", foreground="white", background="black")


