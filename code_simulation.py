import tkinter as tk
from tkinter import ttk
from tkinter import filedialog




# ---------- Variables ---------- #

file_path = None

registers = []  # Registers' array

''' Some global variables are defined in functions:

asm_zone is defined in main_window_init() and is the text center zone.
reg_frame is defined in main_window_init() and is the register frame.
file_path is redefined as global in save(), import(), and save_as().

'''




# ---------- Active Functions ---------- #


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


# (To be implemented)
def run():
    pass


# (To be implemented)
def run_step_by_step():
    pass


# (To be implemented)
def reset():
    pass


# (To be implemented)
def connect_board():
    pass


# (To be implemented)
def download_code():
    pass


# (To be implemented)
def settings():
    pass


def open_link(url: str):
    '''Opens the provided url.\n
        Input: url: The online adress to open.'''
    
    import webbrowser
    webbrowser.open_new(url)


def open_asm_documentation():
    '''Opens an online documentation of the ASM assembly code.'''

    open_link("https://example.com/asm_documentation")


def open_lcm3_conventions():
    '''Onpens an online documentation of the LCM3 instructions.'''
    
    open_link("https://example.com/lcm3_conventions")


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


def save_as():
    '''Opens a dialog window to save the current code into a new file.\n
        It wont save it automatically like the 'save' function does.'''

    global file_path

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
            file.write(saved_code)




# ---------- Interface Initialization functions ---------- #


def main_window_init():
    '''Creates and initializes the window of the simulator.'''

    # Creation of the main window
    window = tk.Tk()
    window.title("ENSEA's Python LCM3 ASM Simulator")
    window.geometry("832x624")  # Initial size of the window

    # Main frame
    main_frame = ttk.Frame(window)
    main_frame.pack(expand=True, fill="both")

    # Top toolbar
    toolbar_frame = ttk.Frame(main_frame)                  # Frame for the top toolbar
    toolbar_frame.pack(side="top", fill="x")
    left_empty_space = ttk.Label(toolbar_frame, width=10)  # Indentation to the left
    left_empty_space.pack(side="left")
    toolbar = ttk.Frame(toolbar_frame)
    toolbar.pack(side="left")

    # Memory frame on the left of the assembly zone
    create_memory_array_display_frame(main_frame)

    # Assembly code area in the middle
    global asm_zone
    asm_zone = tk.Text(main_frame, width=40, height=20)
    asm_zone.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    asm_scrollbar = ttk.Scrollbar(asm_zone, orient="vertical", command=asm_zone.yview)  # Creation of a vertical scrollbar
    asm_scrollbar.pack(side="right", fill="y")
    asm_zone.config(yscrollcommand=asm_scrollbar.set)        # Configuration of the text widget to work with the scrollbar

    # Register frame on the right of the assembly zone
    reg_init(main_frame)
    reg_update(2, 6000)

    # Pipeline frame at the bottom
    pip_frame = ttk.LabelFrame(window, text="Pipeline")
    pip_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

    # Add pipeline stages to the frame (to be adapted)
    pip_stages = []
    for i, stage in enumerate(["Fetch", "Decode", "Execute"]):
        stage_label = ttk.Label(pip_frame, text=stage)
        stage_label.grid(row=0, column=i, padx=5, pady=2)
        pip_stages.append(stage_label)

    # Toolbar buttons
    btn_file_menu_init(toolbar)
    btn_help_menu_init(toolbar)
    btn_run_init(toolbar)
    btn_step_init(toolbar)
    btn_reset_init(toolbar)
    btn_connect_init(toolbar)
    btn_dowload_init(toolbar)
    btn_settings_menu_init(toolbar)

    '''/!\ TO IMPLEMENT'''
    # Create a style object
    style = ttk.Style(window)
    style.theme_use('default')

    window.mainloop()


def create_memory_array_display_frame(main_frame):
    '''Creates the left memory frame and fills it with an array.'''

    # Frame for the memory section
    memory_frame = ttk.LabelFrame(main_frame, text="Memory")
    memory_frame.pack(side="left", fill="y")

    # Creation of the Tree (array)
    memory_tree = ttk.Treeview(memory_frame, columns=("Adress", "Value", "Description"), show='headings')
    memory_tree.heading("Adress", text="Adress")
    memory_tree.heading("Value", text="Value")
    memory_tree.heading("Description", text="Instruction")
    memory_tree.column("Adress", width=70)
    memory_tree.column("Value", width=70)
    memory_tree.column("Description", width=180)

    # Initialization of the memory
    for i in range(30):
        adress = "0x"+format(i*2+134217728, '08x')  # Creates the iterable adress 2 by 2 with a 0x0800000 offset
        value = "0x"+format(0, '08x') 
        description = f"Line {i} of the code to copy here"
        memory_tree.insert("", tk.END, values=(adress, value, description))
    memory_tree.pack(fill="both", expand=True)

    mem_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=memory_tree.yview)  # Creation of a vertical scrollbar
    mem_scrollbar.pack(side="left", fill="y")
    memory_tree.config(yscrollcommand=mem_scrollbar.set)


def reg_init(main_frame):
    '''Initializes the registers' value and window.'''

    global reg_frame
    reg_frame = ttk.LabelFrame(main_frame, text="Registers")
    reg_frame.pack(side="right", fill="y")

    # Creation of the register widgets
    for i in range(16):
        reg_name = f"R{i}:"
        reg_value = tk.StringVar()
        reg_value.set("0x00000000")  # Initial value
        reg_label = ttk.Label(reg_frame, text=reg_name)
        reg_field = ttk.Label(reg_frame, textvariable=reg_value)
        reg_label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        reg_field.grid(row=i, column=1, sticky="w", padx=5, pady=2)
        registers.append(reg_value)


def reg_update(Rx: int, val: int):
    '''Updates the registers' values and window.\n
        Inputs:\n
        Rx: Index of the register (between 0 and 15).\n
        val: New value to put into the register.'''

    hex_val = "0x"+format(val, '08x')
    reg_value = tk.StringVar()
    reg_value.set(hex_val)
    reg_field = ttk.Label(reg_frame, textvariable=reg_value)
    reg_field.grid(row=Rx, column=1, sticky="w", padx=5, pady=2)
    registers[Rx] = reg_value


def btn_file_menu_init(toolbar):
    '''Creates and initializes the file menu.\n
        Input: toolbar: Frame in which to place the button.'''

    file_menu = ttk.Menubutton(toolbar, text="File", direction="below")
    file_menu.pack(side="left")

    file_menu.menu = tk.Menu(file_menu, tearoff=0)
    file_menu["menu"] = file_menu.menu

    file_menu.menu.add_command(label="Import", command=import_code)
    file_menu.menu.add_separator()
    file_menu.menu.add_command(label="Save", command=save)
    file_menu.menu.add_command(label="Save As", command=save_as)
    file_menu.pack()


def btn_help_menu_init(toolbar):
    '''Creates and initializes the help menu.\n
        Input: toolbar: Frame in which to place the button.'''

    help_menu = ttk.Menubutton(toolbar, text="Help", direction="below")
    help_menu.pack(side="right")

    help_menu.menu = tk.Menu(help_menu, tearoff=0)
    help_menu["menu"] = help_menu.menu

    help_menu.menu.add_command(label="ASM Documentation", command=open_asm_documentation)
    help_menu.menu.add_separator()
    help_menu.menu.add_command(label="LCM3 Conventions", command=open_lcm3_conventions)


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




# ---------- Code ---------- #

def main():
    main_window_init()


main()
