# ---------- ENSEA's Python LCM3 Simulator ---------- #
#
# Engineers :
#
# APPOURCHAUX Léo, BITTAUD CANOEN Lael, GABORIEAU Cyprien, JIN Clementine
# LATRECHE Loubna, OULAD ALI Rym, XIANG Justine, YE Yumeng
#
# Professors :
#
# Mr. Kessal, Mr. Laroche, Mr. Monchal
#
# --------------------------------------------------- #



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog






# ---------- Variables ---------- #

file_path = None  # Stores whether the file is saved somewhere

registers = []    # Registers' array

''' Some global variables are defined in functions:

    asm_zone:       Text center zone defined in asm_zone_init().
    reg_frame:      Register frame defined in registers_init().
    memory_tree:    Memory arraydefined in memory_array_init().
    pip_frame:      Pipeline frame defined in pipeline_init().
    file_path:      Redefined as global in save(), import(), and save_as().
'''






# ---------- Interface functions (for Lael and Cyprien) ---------- #


def reg_edit(Rx: int, value: int, color: str):
    '''Edits the registers' values and colors.\n
        Inputs:\n
        Rx: Index of the register (between 0 and 15).\n
        value: New value to put into the register.\n
        color: Name of the color in which the register will be displayed.'''

    if (Rx>=0) & (Rx<16):
        hex_value = "0x"+format(value, '08x')  # Changes from int to string hex display (0x08......)
        reg_value = tk.StringVar()             # Changes from string hex to tk.StringVar
        reg_value.set(hex_value)
        reg_label = ttk.Label(reg_frame, text=f"R{Rx}:", foreground=color)          # Register name and its color
        reg_field = ttk.Label(reg_frame, textvariable=reg_value, foreground=color)  # Register value and its color
        reg_label.grid(row=Rx, column=0, sticky="w", padx=5, pady=2)                # Register's name Config and size
        reg_field.grid(row=Rx, column=1, sticky="w", padx=5, pady=2)                # Register's value Config and size
        registers[Rx] = reg_value  # Changes the value


def mem_edit(line: int, value: int, instruction: str, color: str):
    '''Edits the memory values, corresponding instructions, and colors.\n
        Inputs:\n
        line: Number of the line to modify.\n
        value: Hex value to insert in the second column.\n
        instr: Text to insert in the third column.\n
        color: Name of the color in which the line will be displayed.'''

    hex_value = "0x"+format(value, '08x')           # Changes from int to string hex display (0x08......)
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


def pip_edit_column(pip_column_text, c: int, color_array):
    '''Creates or modifies an existing column in the pipeline array. \n
        Inputs:
        pip_column_text: Text data that will fill the column.\n
        c: Number of the column to create/modify /!\ FDE is 0, MAX is 16.\n
        color_aray: Array of 3 colors corresponding to the Fetch, Decode and execute lines in the column.'''

    if (c>0) & (c<17):
        column_frame = ttk.LabelFrame(pip_frame)
        column_frame.grid(row=0, column=c, sticky="w")  # Creation of the column

        for i, text in enumerate(pip_column_text):
            column_label = ttk.Label(column_frame, text=text, width=5, foreground=color_array[i])  # Column text and color
            column_label.grid(padx=10, pady=5, sticky="w")                                         # Column shape and place config


# /!\ This function might not be necessary as asm_code should be accessible everywhere. It improves visibility though.
def asm_get_code():
    '''Gets the asm code in the asm zone.\n
        Output: asm_code: Content of the asm zone.'''

    asm_code = asm_zone.get("1.0", tk.END)  # Copy of the asm_zone content into asm_code
    return(asm_code)






# ---------- Main function ---------- #


def main():
    '''Main function. Runs the program.'''

    window = main_window_init()

    # Examples of use
    reg_edit(6, 2526451350, "brown")
    mem_edit(9, 2526451350, "MOV R1, R2", "brown")
    pip_edit_column(["MOV", "LDR", "STR"], 6, ["red", "blue", "green"])

    # Call to Lael and Cyp's code

    window.mainloop()






# ---------- Interface Initialization functions ---------- #


def main_window_init():
    '''This function initializes the main window and calls all the other initialisation functions.\n
        Output: window: The window on which everything is happening.'''

        # Creation of the main window
    window = tk.Tk()
    window.title("ENSEA's Python LCM3 ASM Simulator") 
    window.geometry("980x720")      # Initial size of the window
    main_frame = ttk.Frame(window)  # Main frame
    main_frame.pack(expand=True, fill="both")

    # Creation of the other frames
    toolbar = toolbar_init(main_frame)    # Top toolbar
    memory_array_init(main_frame)         # Memory array frame on the left of the assembly zone
    asm_zone_init(main_frame)  # Assembly code area in the middle
    registers_init(main_frame)            # Register list frame on the right of the assembly zone
    pipeline_init(window)                 # Pipeline array frame at the bottom

    # Creation of the toolbar buttons
    btn_file_menu_init(toolbar)
    btn_run_init(toolbar)
    btn_step_init(toolbar)
    btn_reset_init(toolbar)
    btn_connect_init(toolbar)
    btn_dowload_init(toolbar)
    btn_settings_menu_init(toolbar)
    btn_help_menu_init(toolbar)

    return(window)


def toolbar_init(main_frame):
    '''Creates the top toolbar frame.\n
        Input: main_frame: Frame in which the toolbar will be generated.\n
        Output: toolbar_frame: Frame in which we will generate the buttons.'''

    toolbar_frame = ttk.Frame(main_frame)                  # Frame for the top toolbar
    toolbar_frame.pack(side="top", fill="x")
    left_empty_space = ttk.Label(toolbar_frame, width=10)  # Indentation to the left
    left_empty_space.pack(side="left")
    toolbar = ttk.Frame(toolbar_frame)
    toolbar.pack(side="left")
    return(toolbar_frame)


def memory_array_init(main_frame):
    '''Creates the left memory frame and fills it with an array.'''

    # Frame for the memory section
    memory_frame = ttk.LabelFrame(main_frame, text="Memory")
    memory_frame.pack(side="left", fill="y")

    # Creation of the Tree (array)
    global memory_tree
    memory_tree = ttk.Treeview(memory_frame, columns=("Address", "Value", "Instruction"), show='headings')
    memory_tree.heading("Address", text="Address")  # Title/heading text
    memory_tree.heading("Value", text="Value")
    memory_tree.heading("Instruction", text="Instruction")
    memory_tree.column("Address", width=70)         # Column widths
    memory_tree.column("Value", width=70)
    memory_tree.column("Instruction", width=180)

    # Initialization of the memory
    for i in range(2048):
        address = "0x"+format(i*2+134217728, '08x')  # Creates the iterable adress 2 by 2 with a 0x0800000 offset
        value = "0x"+format(0, '08x') 
        instruction = ""

        tags = ()  # Tags are used to add a background color inside the array to improve visibility
        if i % 2 == 0:
            tags = ("row1")
        else:
            tags = ("row2")
        memory_tree.insert("", tk.END, values=(address, value, instruction), tags=tags)
    memory_tree.tag_configure("row1", background="gainsboro", foreground="black")   # One color on even numbered lines
    memory_tree.tag_configure("row2", background="whitesmoke", foreground="black")  # Other one on odd numbered lines

    memory_tree.pack(fill="both", expand=True)

    mem_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=memory_tree.yview)  # Creation of a vertical scrollbar
    mem_scrollbar.pack(side="left", fill="y")
    memory_tree.config(yscrollcommand=mem_scrollbar.set)


def asm_zone_init(main_frame):
    '''Creates the asm text frame.\n
        Input: main_frame: Frame in which the asm window will be created.\n
        Output: asm_zone: Zone in which we can write ASM code.'''

    global asm_zone
    asm_zone = tk.Text(main_frame, width=40, height=20)
    asm_zone.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    asm_scrollbar = ttk.Scrollbar(asm_zone, orient="vertical", command=asm_zone.yview)  # Creation of a vertical scrollbar
    asm_scrollbar.pack(side="right", fill="y")
    asm_zone.config(yscrollcommand=asm_scrollbar.set)  # Configuration of the text widget to work with the scrollbar


def registers_init(main_frame):
    '''Initializes the registers' value and window.'''

    global reg_frame
    reg_frame = ttk.LabelFrame(main_frame, text="Registers")
    reg_frame.pack(side="right", fill="y")

    # Creation of the register widgets
    for i in range(16):
        reg_value = tk.StringVar()
        reg_value = tk.StringVar()
        registers.append(reg_value)
        reg_edit(i, 0, "black")


def pipeline_init(window):
    '''Creates the pipeline frame.\n
        Input: window: Frame into which the pipeline will be generated.'''
    
    # Pipeline frame at the bottom
    global pip_frame
    pip_frame = ttk.LabelFrame(window, text="Pipeline")
    pip_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=5)

    # Fetch Decode Execute
    pip_fde_frame = ttk.LabelFrame(pip_frame)
    pip_fde_frame.grid(row=0, column=0, sticky="w")  # Creation of the column
    pip_fde_lines = ["Fetch", "Decode", "Execute"]   # Text array to copy in the column
    for i, header in enumerate(pip_fde_lines):
        header_label = ttk.Label(pip_fde_frame, text=header, width=8)    # Column text
        header_label.grid(row=i, column=0, padx=12, pady=5, sticky="w")  # Column shape and place config

    # Initialisation of the other cells (15 of them)
    pip_column_text = [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""],
        ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]

    for i, col_labels in enumerate(pip_column_text):
        pip_edit_column(col_labels, i+1, ["black", "black", "black"])


def btn_file_menu_init(toolbar):
    '''Creates and initializes the file menu.\n
        Input: toolbar: Frame in which to place the button.'''

    file_menu = ttk.Menubutton(toolbar, text="File", direction="below")  # File menu button
    file_menu.pack(side="left")

    file_menu.menu = tk.Menu(file_menu, tearoff=0)  # File menu "menu"
    file_menu["menu"] = file_menu.menu

    file_menu.menu.add_command(label="New File", command=new_file)
    file_menu.menu.add_command(label="Import", command=import_code)
    file_menu.menu.add_separator()
    file_menu.menu.add_command(label="Save", command=save)
    file_menu.menu.add_command(label="Save As", command=save_as)
    file_menu.pack()


def btn_run_init(toolbar):
    '''Creates the run button which allows to simulate the code on the computer in one shot.\n
        Input: toolbar: Frame in which to place the button.'''

    button_run = ttk.Button(toolbar, text="Run", command=run)
    button_run.pack(side="left", padx=5)


def btn_step_init(toolbar):
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.\n
        Input: toolbar: Frame in which to place the button.'''

    button_step = ttk.Button(toolbar, text="Run Step by Step", command=run_step_by_step)
    button_step.pack(side="left", padx=5)


def btn_reset_init(toolbar):
    '''Creates the reset button which resets the registers, the memory, and the pipeline.\n
        Input: toolbar: Frame in which to place the button.'''

    button_reset = ttk.Button(toolbar, text="Reset", command=reset)
    button_reset.pack(side="left", padx=5)


def btn_connect_init(toolbar):
    '''Creates the connect button which automatically connects the simulator to a connected board, if there's one.\n
        Input: toolbar: Frame in which to place the button.'''

    button_connect = ttk.Button(toolbar, text="Connect Board", command=connect_board)
    button_connect.pack(side="left", padx=5)


def btn_dowload_init(toolbar):
    '''Creates the download button which downloads the code in the text window into the board, and executes it.\n
        Input: toolbar: Frame in which to place the button.'''

    button_download = ttk.Button(toolbar, text="Download Code", command=download_code)
    button_download.pack(side="left", padx=5)
    button_download.state(['disabled'])
    # To remove as soon as the simulator is connected to a board with the following command:
    #button_download.state(['!disabled'])


def btn_settings_menu_init(toolbar):
    '''Creates and initializes the settings menu.\n
        Input: toolbar: Frame in which to place the button.'''

    button_settings = ttk.Button(toolbar, text="Settings", command=settings)
    button_settings.pack(side="left", padx=5)


def btn_help_menu_init(toolbar):
    '''Creates and initializes the help menu.\n
        Input: toolbar: Frame in which to place the button.'''

    help_menu = ttk.Menubutton(toolbar, text="Help", direction="below")  # Help menu button
    help_menu.pack(side="left")

    help_menu.menu = tk.Menu(help_menu, tearoff=0)  # Help menu "menu"
    help_menu["menu"] = help_menu.menu

    help_menu.menu.add_command(label="ASM Documentation", command=help_asm_docu)
    help_menu.menu.add_separator()
    help_menu.menu.add_command(label="LCM3 Conventions", command=help_lcm3_conv)
    help_menu.menu.add_separator()
    help_menu.menu.add_command(label="Documentation of this simulator", command=help_simulator_docu)






# ---------- Button Control functions ---------- #


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
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
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

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
            file.write(saved_code)


# (To be implemented)
def run():
    '''Simulates on the computer the execution of the code, in one shot.'''

    reset()

    # ...


# (To be implemented)
def run_step_by_step():
    '''Simulates on the computer the execution of the code, step by step.'''

    reset()

    # ...


# (To be implemented)
def reset():
    '''Resets the registers, the memory, and the pipeline.'''

    for i in range(16):
        reg_edit(i, 0, "black")
    for i in range(255):
        mem_edit(i, 0, "", "black")
    for i in range(15):
        pip_edit_column(["", "", "",], i+1, ["black", "black", "black"])


# (To be implemented)
def connect_board():
    '''Connects the simulator with a board plugged on the computer.'''

    pass


# (To be implemented)
def download_code():
    '''Downloads the binary conversion of the asm code onto a connected board.'''

    pass


# (To be implemented)
def settings():
    '''Menu with user settings.'''

    pass


def help_asm_docu():
    '''Opens an online documentation of the ASM assembly code.'''

    open_link("https://example.com/asm_documentation")


def help_lcm3_conv():
    '''Onpens an online documentation of the LCM3 instructions.'''
    
    open_link("https://example.com/lcm3_conventions")


def help_simulator_docu():
    '''Onpens an online documentation of the simulator.'''

    pass


def open_link(url: str):
    '''Opens the provided url.\n
        Input: url: The online adress to open.'''
    
    import webbrowser
    webbrowser.open_new(url)






# ---------- Code ---------- #


main()


# Create a style object
#style = ttk.Style()
#style.configure("Color.TLabel", foreground="white", background="black")


