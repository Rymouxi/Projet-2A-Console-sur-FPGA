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

from instruction_translation import *
from connection_board import *

# Code a working dark theme
# Line counter
# optimize the pip run by filling it from the end to the start



# ---------- Variables ---------- #


file_path = None          # Stores whether the file is saved somewhere

registers = []            # Registers' array

run_state = 0             # 0 : unassembled, 1 : assembled, 2 : ran sbs

txt_color = "black"       # Default text color for themes

bkg_color = "whitesmoke"  # Default background color for themes


''' Other global variables:

    Defined in main_window_init()
    - window:           Simulator window
    - main_frame:       Right frame with the arrays
    - paned_window:     Left frame with the text zones
    - debugger_frame:   Debugger frame

    Defined in memory_arrays_init()
    - notebook:         Tabs of arrays and bitstream
    - ram_code_tree:    Code RAM array
    - ram_user_tree:    User RAM array
    - binary_text:      Bitstream text frame

    Defined in asm_zone_init()
    - asm_zone:         Left coding area

    Defined in registers_init()
    - reg_frame:        Register frame
    - display_mode:     Allows to chose between hex and dec modes

    Defined in pipeline_init()
    - pip_frame:        Pipeline frame

    Defined in debugger_init()
    - debugger_text:    Debugger frame

    Defined in theme_toggle_dark() and theme_toggle_light()
    - txt_color:        Foreground color theme
    - bkg_color         Backgrounf color theme

    Redefined in save(), import(), and save_as()
    - file_path:

    Defined in btn_runsbs_init()
    - button_runsbs:    Step_by_step button

    Defined in btn_step_init()
    - button_step:      Step-> button
    
    Defined in run_step_by_step()
    - run_state:        Stores the state of the buttons to display
'''






# ---------- Interface Edition Functions (for simulation) ---------- #


def reg_edit(Rx: int, value: int):
    '''Edits the registers' values and colors. Intended for direct use by run and runsbs.\n
        Inputs:\n
        Rx: Index of the register (between 0 and 15).\n
        value: New value to put into the register.'''

    current_mode = display_mode.get()  # Gets the current mode (hex or dec)

    # Update the displayed values according to the mode (hex or dec)
    if 0 <= Rx < 8:
        new_value = "0x"+format(value, "08x") if current_mode == "Switch to dec" else str(value)      # Register value
        reg_label = ttk.Label(reg_frame, text=f"R{Rx}:", foreground=txt_color, background=bkg_color)  # Register name and its color

    # The 8th reg is the NZVC to be displayed in binary, not hex
    elif Rx == 8:
        new_value = "0b"+format(value, "04b") if current_mode == "Switch to dec" else str(value)     # Register value
        reg_label = ttk.Label(reg_frame, text=f"NZVC:", foreground=txt_color, background=bkg_color)  # Register name and its color

    registers[Rx].set(new_value)  # Global variable of registers

    reg_field = ttk.Label(reg_frame, textvariable=registers[Rx], foreground=txt_color, background=bkg_color)  # Register value and its color
    reg_label.grid(row=Rx, column=0, sticky="w", padx=5, pady=2)  # Register names config and size
    reg_field.grid(row=Rx, column=1, sticky="w", padx=5, pady=2)  # Register values config and size


def mem_edit(memory_tree, line: int, binary_value="0", instruction="", type="Code", color="black"):
    '''Edits the array values, instructions, and colors. Intended for direct use by run and runsbs.\n
        Inputs:\n
        memory_tree: Array to edit.\n
        line: Number of the line to modify.\n
        binary_value: Binary value to insert in the second column.\n
        instruction: Text to insert in the third column.\n
        type: Type of the Array (Code or User).\n
        color: Name of the color in which the line will be displayed.'''

    hex_value = "0x"+format(int(binary_value, 2), "04x") if type == "Code" else "0x"+format(int(binary_value, 2), "08x")  # Changes from binary to hex
    tags = "even" if line % 2 == 0 else "odd"  # Tags of the lines background

    if line < len(memory_tree.get_children()):
        # Line exists, update the values
        item_id = memory_tree.get_children()[line]  # Gets the item ID for the line
        memory_tree.item(item_id, values=(memory_tree.item(item_id, "values")[0], hex_value, instruction), tags=tags)  # Updates the values

    else:
        # Line doesn't exist, insert a new line
        address = "0x"+format(line*2+134217728, "08x") if type == "Code" else "0x"+format(line*4+536870912, "08x")
        memory_tree.insert("", tk.END, values=(address, hex_value, instruction), tags=(tags))

    memory_tree.tag_configure("even", background="gainsboro", foreground=color)  # One color on even numbered lines
    memory_tree.tag_configure("odd", background="whitesmoke", foreground=color)  # Other one on odd numbered lines


def textbox_add_line(text_widget, line: str, color="black"):
    '''Adds a line to a text_widget.\n
        Inputs:\n
        text_widget: Text frame, such as the debugger or the bitstream.\n
        line: String you wanna display.\n
        color: color of the text.'''

    text_widget.configure(state="normal")               # Set the widget to normal state to allow editing
    text_widget.tag_configure(color, foreground=color)  # Configure a tag with the specified color
    text_widget.insert("end", line + "\n", (color,))    # Add the line to the end and include a newline character
    text_widget.configure(state="disabled")             # Set the widget back to disabled state


def pip_edit(pip_text: str):
    '''Iterates the pipeline and adds a new instruction column.\n
        Intended to run_step_by_step, not optimised to run a high number of instructions in one go.'''

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






# ---------- Interface Initialization Functions ---------- #


def main_window_init():
    '''This function initializes the main window and calls all the other initialisation functions.'''

    global window, main_frame, toolbar_frame, paned_window, debugger_frame

    # Creation of the main window
    window = ctk.CTk()
    window.title("ENSEA's Python LCM3 ASM Simulator") 
    window.geometry("980x720")         # Initial size of the window
    main_frame = ctk.CTkFrame(window)  # Main frame
    main_frame.pack(expand=True, fill="both")

    # Creation of the other frames
    toolbar_frame = ctk.CTkFrame(main_frame)  # Top toolbar frame
    toolbar_frame.pack(side="top", fill="x")

    texts_frame = ctk.CTkFrame(main_frame)  # ASM and debugger frame
    texts_frame.pack(side="left", fill="both", expand=True, pady=8)
    paned_window = ttk.Panedwindow(texts_frame, orient=tk.VERTICAL)  # Panned window for the ASM and the debugger
    paned_window.pack(expand=True, fill="both")

    asm_zone_frame = ttk.LabelFrame(paned_window, text="ASM Zone")  # ASM frame
    asm_zone_frame.grid(row=0, column=0, sticky="nsew")
    debugger_frame = ttk.LabelFrame(paned_window, text="Debugger")  # debugger frame
    debugger_frame.grid(row=1, column=0, sticky="nsew")
    paned_window.add(asm_zone_frame, weight=4)
    paned_window.add(debugger_frame, weight=1)

    memory_arrays_init()           # Memory array frame on the left of the assembly zone
    asm_zone_init(asm_zone_frame)  # Assembly code area in the middle
    debugger_init()                # Debugger in the middle
    registers_init()               # Register list frame on the right of the assembly zone
    pipeline_init()                # Pipeline array frame at the bottom

    # Buttons creation 
    btn_file_menu_init()           # File menu button
    btn_settings_menu_init()       # Settings menu button
    btn_help_menu_init()           # Help menu button
    btn_dowload_init()             # Download code button
    btn_connect_init()             # Connect board button
    btn_reset_init()               # Reset button
    btn_step_init()                # Step-> button
    btn_runsbs_init()              # Run step by step button
    btn_run_init()                 # Run in one shot button
    btn_assemble_init()            # Code assembly button

    ctk.set_appearance_mode("Light")  # Light theme is the default theme

    window.mainloop()  # All the code must be contained in this loop


def scrollbar_init(frame, scrollable):
        '''Creates a scrollbar.\n
            Inputs:\n
            frame: frame in which the scrollbar will be placed.\n
            scrollable: widget/frame that will be scrolled. may be different from frame.'''

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=scrollable.yview)  # Creation of a vertical scrollbar
        scrollbar.pack(side="right", fill="y")
        scrollable.config(yscrollcommand=scrollbar.set)  # Assignation to a scrollable element


def memory_arrays_init():
    '''Creates the left frames with memory arrays and the bitstream.'''

    global notebook, ram_code_tree, ram_user_tree, binary_text

    # Creation of the two tabs (Code and User Ram)
    notebook = ttk.Notebook(main_frame)
    notebook.pack(side="right", fill="both", pady=10)
    ram_code_frame = ttk.Frame(notebook)
    ram_user_frame = ttk.Frame(notebook)
    binary_frame = ttk.Frame(notebook)
    notebook.add(ram_code_frame, text="Code RAM")     # Display "Code RAM" on the tab
    notebook.add(ram_user_frame, text="User RAM")     # Display "User RAM" on the tab
    notebook.add(binary_frame, text="Binary Code")    # Display "Binary" on the tab

    # Creation of the Code RAM Tree (array)
    ram_code_tree = ttk.Treeview(ram_code_frame, columns=("Address", "Value", "Instruction"), show="headings")
    ram_code_tree.heading("Address", text="Address")  # Title/heading text
    ram_code_tree.heading("Value", text="Value")
    ram_code_tree.heading("Instruction", text="Instruction")
    ram_code_tree.column("Address", width=70)         # Column widths
    ram_code_tree.column("Value", width=50)
    ram_code_tree.column("Instruction", width=180)
    scrollbar_init(ram_code_frame, ram_code_tree)     # Code RAM scrollbar

    # Creation of the User RAM Tree (array)
    ram_user_tree = ttk.Treeview(ram_user_frame, columns=("Address", "Value"), show="headings")
    ram_user_tree.heading("Address", text="Address")  # Title/heading text
    ram_user_tree.heading("Value", text="Value")
    ram_user_tree.column("Address", width=150)        # Column widths
    ram_user_tree.column("Value", width=150)
    scrollbar_init(ram_user_frame, ram_user_tree)     # User RAM scrollbar

    # Initialization of the Code RAM
    for i in range(256):
        mem_edit(ram_code_tree, i)
    ram_code_tree.pack(fill="both", expand=True, padx=3, pady=3)

    # Initialization of the User RAM
    for i in range(256):
        mem_edit(ram_user_tree, i, type="User")
    ram_user_tree.pack(fill="both", expand=True, padx=3, pady=3)

    # Creation of the Bitstream window
    binary_text = tk.Text(binary_frame, width=40, height=10, state=tk.DISABLED)
    binary_text.pack(side="left", fill="both", expand=True, padx=3, pady=3)
    scrollbar_init(binary_text, binary_text)  # Binary window scrollbar


def asm_zone_init(asm_zone_frame):
    '''Creates the asm text frame.\n
        Input: asm_zone_frame: Frame in which the asm window will be created.'''
    
    global asm_zone

    def on_key(event=None):
        '''Takes care of the buttons depending on assembled state and changes letters to upper case.\n
            Input:\n
            event: Usually the pressing of a key.'''

        global run_state

        # Reinitializes the buttons so assembly needs to be done again
        button_assemble.configure(fg_color="forestgreen", state="!disabled")    
        button_runsbs.configure(text="Run Step by Step", fg_color="gray", state="disabled")
        button_run.configure(state="disabled", fg_color="gray")
        button_step.configure(state="disabled", fg_color="gray")
        run_state = 0

        # Raises letters to upper case
        if event.char.islower() and event.char.isalpha():
            # If the typed character is lowercase, replace it with uppercase
            asm_zone.insert(tk.INSERT, event.char.upper())
            update_colors()
            return "break"  # Prevent the default action for lowercase characters
        else:
            return None  # Let the default action proceed for other keys
        
    def update_colors(event=None):
        '''Manages the colors in the asm text frame.\n
            Input:\n
            event: Usually the release of a key.'''

        # Color for labels
        asm_zone.tag_remove("label", "1.0", tk.END)
        index = "1.0"
        while True:
            index = asm_zone.search(":", index, tk.END)
            if not index:
                break

            # Tag the text before the semicolon
            start_index = asm_zone.index(f"{index} linestart")
            end_index = asm_zone.index(f"{index}+1c")
            asm_zone.tag_add("label", start_index, end_index)
            index = f"{index}+1c"

        # Other colors

        # Define patterns and corresponding tags
        patterns = {
            " R": "register",
            "[\\[\\]]": "bracket",
            ",": "comma",
            "#": "hash",
            "0X": "hexa",
            "0B": "binary",
            ";": "comment"}

        # Remove existing tags
        for tag in patterns.values():
            asm_zone.tag_remove(tag, "1.0", tk.END)

        # Iterate through the patterns and tag the text accordingly
        for pattern, tag in patterns.items():
            start_index = "1.0"
            while True:
                start_index = asm_zone.search(pattern, start_index, tk.END, regexp=True)
                if not start_index:
                    break

                # Compute end_index based on the pattern
                if pattern == "," or pattern == "[\\[\\]]":
                    end_index = asm_zone.index(f"{start_index}+1c")
                else:
                    end_index = asm_zone.index(f"{start_index} lineend")

                asm_zone.tag_add(tag, start_index, end_index)  # Tags the part we want to colorise
                start_index = f"{end_index}+1c"                # Goes to next character

    # Create the text zone
    asm_zone = tk.Text(asm_zone_frame, width=40, height=30, bg="white", fg="blue")
    asm_zone.pack(side="left", fill="both", expand=True)
    scrollbar_init(asm_zone, asm_zone)

    # Initialize tags for different types of text
    asm_zone.tag_configure("label", foreground="red")
    asm_zone.tag_configure("register", foreground="forestgreen")
    asm_zone.tag_configure("comma", foreground="black")
    asm_zone.tag_configure("bracket", foreground="limegreen")
    asm_zone.tag_configure("hash", foreground="darkorange")
    asm_zone.tag_configure("hexa", foreground="orange")
    asm_zone.tag_configure("binary", foreground="gold")
    asm_zone.tag_configure("comment", foreground="gray")

    # Bind functions to key events
    asm_zone.bind("<Key>", on_key)
    asm_zone.bind("<KeyRelease>", update_colors)


def registers_init():
    '''Initializes the registers' value and window.'''

    global reg_frame, display_mode

    def toggle_display():
        '''Toggles between decimal and hex display for registers.'''

        current_mode = display_mode.get()
        new_mode = "Switch to hex" if current_mode == "Switch to dec" else "Switch to dec"
        display_mode.set(new_mode)
        
        reg_update()

    style = ttk.Style()  # Style for light and dark themes
    style.configure("Theme.TLabelframe", background=bkg_color)

    reg_frame = ttk.LabelFrame(main_frame, text="Registers", style="Theme.TLabelframe")  # Refister frame
    reg_frame.pack(side="right", fill="y", pady=10, padx=5)

    # Button to toggle between decimal and hex display
    display_mode = tk.StringVar()
    display_mode.set("Switch to dec")  # Initial display mode is hex
    display_button = ttk.Button(reg_frame, textvariable=display_mode, command=toggle_display)
    display_button.grid(row=10, column=0, columnspan=2, pady=5)

    # Creation of the register widgets
    for i in range(9):
        reg_value = tk.StringVar()
        registers.append(reg_value)
        reg_edit(i, 0)


def reg_update():
    '''Updates the registers.\n
        Usually to change the mode (hex or dec), the theme, or the text color.'''

    for i in range(8):
        current_value_str = registers[i].get()
        current_value = int(current_value_str[2:], 16) if current_value_str and len(current_value_str) > 2 else int(current_value_str)  # Interprets current value as hex or dec
        reg_edit(i, current_value)  # Updates R0 to R7
    current_value_str = registers[8].get()
    current_value = int(current_value_str[2:], 2) if current_value_str and len(current_value_str) > 2 else int(current_value_str)  # Interprets current value as binary or dec
    reg_edit(8, current_value)  # Updates NZVC


def pipeline_init():
    '''Creates the pipeline frame.'''
    
    global pip_frame

    # Pipeline frame at the bottom
    pip_frame = ttk.LabelFrame(window, text="Pipeline")
    pip_frame.pack(side="bottom", fill="both", padx=10, pady=10)

    # Fetch Decode Execute
    pip_fde_frame = ttk.LabelFrame(pip_frame)
    pip_fde_frame.grid(row=0, column=0, sticky="w", padx=5)  # Creation of the column
    pip_fde_lines = ["Fetch", "Decode", "Execute"]           # Text array to copy in the column
    for i, header in enumerate(pip_fde_lines):
        header_label = ttk.Label(pip_fde_frame, text=header, width=8)    # Column text
        header_label.grid(row=i, column=0, padx=12, pady=8, sticky="w")  # Column shape and place config

    for i in range(19):
        pip_modify_column(c=i+1)


def pip_modify_column(pip_column_text=["", "", "",], c=0, color_array=["black", "black", "black"]):
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


def debugger_init():
    '''Creates the debugger text frame.'''

    global debugger_text

    debugger_text = tk.Text(debugger_frame, width=40, height=10, state=tk.DISABLED, background="gainsboro")
    debugger_text.pack(side="left", fill="both", expand=True, padx=6, pady=6)
    scrollbar_init(debugger_text, debugger_text)






# ---------- Button Functions ---------- #


def btn_file_menu_init():
    '''Creates and initializes the file menu.'''

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
            with open(file_path, "r") as file:
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
            with open(file_path, "w") as file:
                saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
                file.write(saved_code)

    def save_as():
        '''Opens a dialog window to save the current code into a new file.\n
            It wont save it automatically like the 'save' function does.'''

        global file_path

        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                saved_code = asm_zone.get("1.0", tk.END)  # Gets the code from the text area
                file.write(saved_code)

    # File menu setup
    file_menu = ttk.Menubutton(toolbar_frame, text="File", direction="below")  # File menu button
    file_menu.pack(side="left")

    file_menu.menu = tk.Menu(file_menu, tearoff=0)  # File menu "menu"
    file_menu["menu"] = file_menu.menu

    file_menu.menu.add_command(label="New File", command=new_file)
    file_menu.menu.add_command(label="Import", command=import_code)
    file_menu.menu.add_separator()
    file_menu.menu.add_command(label="Save", command=save)
    file_menu.menu.add_command(label="Save As", command=save_as)
    file_menu.pack()
    

def btn_settings_menu_init():
    '''Creates and initializes the settings menu'''
    
    def theme_toggle_dark():
        '''Toggles dark theme.'''

        global txt_color, bkg_color

        txt_color = "white"  # Default text color for themes
        bkg_color = "#424242"  # Default background color for themestxt_color
        ctk.set_appearance_mode("dark")
        asm_zone.config(background="dimgray", fg="white")
        reg_update()
        style = ttk.Style()
        style.configure("Theme.TLabelframe", background=bkg_color)

        custom_label = tk.Label(reg_frame, text="Registers", background=bkg_color, foreground=txt_color)  # Replace colors
        reg_frame["labelwidget"] = custom_label  # Set the custom label widget

    def theme_toggle_light():
        '''Toggles light theme.'''

        global txt_color, bkg_color

        txt_color = "black"  # Default text color for themes
        bkg_color = "whitesmoke"  # Default background color for themestxt_color
        ctk.set_appearance_mode("light")
        asm_zone.config(bg="white", fg="black")
        reg_update()
        style = ttk.Style()
        style.configure("Theme.TLabelframe", background=bkg_color)

        custom_label = tk.Label(reg_frame, text="Registers", background=bkg_color, foreground=txt_color)  # Replace colors
        reg_frame["labelwidget"] = custom_label  # Set the custom label widget
    
    # Settings menu setup
    settings_menu = ttk.Menubutton(toolbar_frame, text="Settings", direction="below")
    settings_menu.pack(side="left")

    settings_menu.menu = tk.Menu(settings_menu, tearoff=0)  # File menu "menu"
    settings_menu["menu"] = settings_menu.menu

    settings_menu.menu.add_command(label="Dark mode", command=theme_toggle_dark)
    settings_menu.menu.add_command(label="Light mode", command=theme_toggle_light)
    settings_menu.pack()


def btn_help_menu_init():
    '''Creates and initializes the help menu.'''

    def help_lcm3_docu():
        '''Opens an online documentation of the LCM3 instructions.'''

        webbrowser.open_new("https://moodle.ensea.fr/pluginfile.php/24675/mod_resource/content/1/LCM3_Instructions_2017.pdf")

    # Help menu setup
    help_menu = ttk.Menubutton(toolbar_frame, text="Help", direction="below")  # Help menu button
    help_menu.pack(side="left")

    help_menu.menu = tk.Menu(help_menu, tearoff=0)  # Help menu "menu"
    help_menu["menu"] = help_menu.menu

    help_menu.menu.add_command(label="This Simulator Documentation", command=help_simulator_docu)
    help_menu.menu.add_separator()
    help_menu.menu.add_command(label="LCM3 Documentation", command=help_lcm3_docu)


def btn_assemble_init():
    '''Create the assemble button'''

    global button_assemble

    def assemble():
        '''Assembles the code'''

        global run_state, code, split_instructions, bitstream, register_update, line_update, memory_update

        reset()

        # Buttons states update
        button_assemble.configure(fg_color="gray", state="disabled")
        run_state = 1

        asm_zone.tag_remove("highlight_error", "1.0", "end")  # Removes the "highlight_error" tag

        code = asm_zone.get("1.0", tk.END)                    # Gets the code from the ASM text window

        # Funny text variations for when user tries to assemble empty code
        variations = ["sipping a coconut", "catching some rays", "in a hammock", "on a beach", "snorkeling", "in a tropical paradise", "surfing the clouds",
        "on a spa retreat", "napping in a hammock", "practicing mindfulness", "doing yoga", "enjoying a siesta", "on a cosmic cruise", "in a Zen garden",
        "sunbathing", "in a day spa", "on a coffee break", "chilling in a hammock", "vacationing", "on a beach", "gone", "too short", "transparent", "too small"]
        random_variation = random.choice(variations)

        # Check if code is empty
        if code == "\n":
            textbox_add_line(debugger_text, "Assembling air? Your code's "+random_variation+".", "blue")

            # Buttons states update
            button_assemble.configure(fg_color="forestgreen", state="!disabled")
            run_state = 0
        
        else:
            split_instructions, _, bitstream, register_update, line_update, memory_update, error = instruction_translation(code)

            # Fills the Code RAM array and the bitstream frame
            for l in range(len(line_update)-2):
                if len(bitstream) != 0:
                    if bitstream[line_update[l]] != "":
                        mem_edit(ram_code_tree, line_update[line_update[l]], bitstream[line_update[l]], split_instructions[line_update[l]])
                        textbox_add_line(binary_text, bitstream[line_update[l]])

            for e in range(len(error)//2):
                # Print the error in the debugger window
                textbox_add_line(debugger_text, str(error[e])+" at line "+f"{error[e+1]}", "red")  # Usually the error is on the last line as the

                # Highlight the specific line with a red background
                start_index = f"{error[e+1]+1}.0 linestart"
                end_index = f"{error[e+1]+1}.0 lineend"
                asm_zone.tag_add("highlight_error", start_index, end_index)
                asm_zone.tag_configure("highlight_error", background="salmon", foreground="darkred")

            # Check is code is empty of errors
            if error == []:
                textbox_add_line(debugger_text, "Assembly complete", "forestgreen")

                # Buttons states update
                button_runsbs.configure(text="Run Step by Step", fg_color="forestgreen", state="!disabled")
                button_run.configure(state="!disabled", fg_color="forestgreen")

            else:
                # Buttons states update
                button_assemble.configure(fg_color="forestgreen", state="!disabled")
                run_state = 0

    # Assembly button setup
    button_assemble = ctk.CTkButton(toolbar_frame, text="Assemble", command=assemble, width=90, height=18, font = ("Arial", 10), fg_color="forestgreen", state="!disabled")
    button_assemble.pack(side="right", padx=18)


def btn_run_init():
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.'''

    global button_run

    def run():
        '''Simulates on the computer the execution of the code, all at once.'''

        button_run.configure(text="Run", state="disabled", fg_color="gray")
        button_runsbs.configure(text="Run Step by Step", fg_color="gray", state="disabled")
        button_step.configure(state="disabled", fg_color="gray")

        for i in range(8):
            reg_edit(i, virtual_register[i])
        for i in range(0, len(virtual_memory), 2):
            mem_edit(ram_user_tree, i, virtual_memory[i], virtual_memory[i+1])

        for l in range(len(line_update)-2):
            if len(line_update)-l > 23:  # Only generates the last 22 instructions that can be see in the pipeline
                pass
            if l < run_state-2:  # Only execute remaining instructions if clicked on resume
                pass
            else:
                if len(bitstream) != 0:
                    if bitstream[line_update[l]] != "":
                        pip_edit(split_instructions[line_update[l]])

        button_assemble.configure(fg_color="forestgreen", state="!disabled")

    # Run button setup
    button_run = ctk.CTkButton(toolbar_frame, text="Run", command=run, width=90, height=18, font = ("Arial", 10), fg_color="gray", state="disabled")
    button_run.pack(side="right", padx=0)


def btn_runsbs_init():
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.'''

    global button_runsbs

    def run_step_by_step():
        '''Simulates on the computer the execution of the code, step by step.'''

        global run_state

        if run_state == 1:  # If just assembled, allows the step and the stop
            
            button_runsbs.configure(text="S T O P", fg_color="firebrick")
            button_run.configure(text="Resume")
            button_step.configure(state="!disabled", fg_color="forestgreen")
            run_state = 2

        elif run_state > 1:  # If in a sbs, requires new assembly
            button_runsbs.configure(text="Run Step by Step", fg_color="gray", state="disabled")
            button_run.configure(text="Run", state="disabled", fg_color="gray")
            button_step.configure(state="disabled", fg_color="gray")
            button_assemble.configure(fg_color="forestgreen", state="!disabled")
            run_state = 0

    # Run step by setp button setup
    button_runsbs = ctk.CTkButton(toolbar_frame, text="Run Step by Step", command=run_step_by_step, width=90, height=18, font = ("Arial", 10), fg_color="gray", state="disabled")
    button_runsbs.pack(side="right", padx=18)


def btn_step_init():
    '''Creates the run_step_by_step button which allows to simulate the code, one line at a time, on the computer.'''

    global button_step

    def step_iter():
        '''Simulates on the computer the execution of the code, step by step.'''

        global run_state

        # Iterates through the instructions
        if run_state < (len(line_update)):
            if len(bitstream)!=0:
                if bitstream[line_update[run_state-2]] != "":
                    pip_edit(split_instructions[line_update[run_state-2]])
            if memory_update[line_update[run_state-2]] != []:
                mem_edit(ram_user_tree, memory_update[line_update[run_state-2]][0], memory_update[line_update[run_state-2]][1], "User")
            if register_update[line_update[run_state-2]] != []:
                reg_edit(register_update[line_update[run_state-2]][0], register_update[line_update[run_state-2]][1])
            
            run_state += 1

        # Disables the buttons when the sbs is finished
        if run_state == (len(line_update)):
            button_assemble.configure(fg_color="forestgreen", state="!disabled")
            button_runsbs.configure(text="Run Step by Step", fg_color="gray", state="disabled")
            button_run.configure(text="Run", state="disabled", fg_color="gray")
            button_step.configure(state="disabled", fg_color="gray")
            run_state = 0

    # Step-> button setup
    button_step = ctk.CTkButton(toolbar_frame, text="Step ->", command=step_iter, width=90, height=18, font = ("Arial", 10), fg_color="gray")
    button_step.pack(side="right", padx=0)
    button_step.configure(state="disabled")


def btn_reset_init():
    '''Creates the reset button which resets the registers, the memory, and the pipeline.'''

    # Reset button setup
    button_reset = ctk.CTkButton(toolbar_frame, text="Reset", command=reset, width=90, height=18, font = ("Arial", 10), fg_color="forestgreen")
    button_reset.pack(side="right", padx=18)
    button_reset.configure(state="!disabled")


def btn_connect_init():
    '''Creates the connect button which automatically connects the simulator to a connected board, if there's one.'''

    def connect_update():
        if ser:
            disconnect_board()
            button_connect.configure(text="Disconnect Board", fg_color="firebrick")
        else:
            connect_board()
            button_connect.configure(text="Connect Board", fg_color="forestgreen")

    # Connect board button setup
    button_connect = ctk.CTkButton(toolbar_frame, text="Connect Board", command=connect_update, width=90, height=18, font = ("Arial", 10), fg_color="forestgreen")
    button_connect.pack(side="right", padx=0)
    button_connect.configure(state="!disabled")


def btn_dowload_init():
    '''Creates the download button which downloads the code in the text window into the board, and executes it.'''

    # Download code button setup
    button_download = ctk.CTkButton(toolbar_frame, text="Download Code", command=download_code, width=90, height=18, font = ("Arial", 10), fg_color="gray")
    button_download.pack(side="right", padx=18)
    button_download.configure(state="disabled")
    # To remove as soon as the simulator is connected to a board !


def reset():
    '''Resets the registers, the memory, and the pipeline.'''

    # Resets the info frames
    notebook.destroy()
    memory_arrays_init()
    reg_frame.destroy()
    registers_init()
    pip_frame.destroy()
    pipeline_init()
    debugger_text.destroy()
    debugger_init()

    # Resets buttons that can change state
    button_step.destroy()
    button_runsbs.destroy()
    button_run.destroy()
    button_assemble.destroy()

    btn_step_init()
    btn_runsbs_init()
    btn_run_init()
    btn_assemble_init()


# (To be implemented)
def download_code():
    '''Downloads the binary conversion of the asm code onto a connected board.'''


def help_simulator_docu():
    '''Onpens an online documentation of the simulator.'''

    documentation_text = ("\n"+
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
    
    popup_frame = ttk.Frame(popup)  # Frame to hold the text widget and scrollbar
    popup_frame.pack(fill=tk.BOTH, expand=True)

    documentation_text_widget = tk.Text(popup_frame, wrap=tk.WORD, height=20, width=60)  # Text widget for the documentation
    documentation_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_init(popup_frame, documentation_text_widget)

    documentation_text_widget.insert(tk.END, documentation_text)  # Insert the text
    documentation_text_widget.configure(state="disabled", font=("Helvetica",12))  # Make it un-editable






# ---------- Code ---------- #


main_window_init()

