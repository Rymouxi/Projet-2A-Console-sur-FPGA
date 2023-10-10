import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Variable to store the file path
file_path = None

# Save function
def save():
    global file_path

    # If the file hasn't been saved yet, ask the user where to save it
    if file_path is None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # If the user selected a file location, save the content of the text area to the file
    if file_path:
        with open(file_path, 'w') as file:
            saved_code = asm_zone.get("1.0", tk.END)  # Get the code from the text area
            file.write(saved_code)

# Run function (to be implemented)
def run():
    pass

# Run step by step function (to be implemented)
def run_step_by_step():
    pass

# Reset function (to be implemented)
def reset():
    pass

# Connect to board function (to be implemented)
def connect_board():
    pass

# Download code function (to be implemented)
def download_code():
    pass

# Settings function (to be implemented)
def settings():
    pass

# Import function
def import_code():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            imported_code = file.read()
            # Put the imported code into the text area
            asm_zone.delete("1.0", tk.END)  # Clear the current content of the text area
            asm_zone.insert(tk.END, imported_code)  # Insert the imported code into the text area



# Save as code function
def save_as():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            saved_code = asm_zone.get("1.0", tk.END)  # Get the code from the text area
            file.write(saved_code)

# Create the main window
window = tk.Tk()
window.title("Simulator")
window.geometry("800x600")  # Initial size of the window

# Main frame
main_frame = ttk.Frame(window)
main_frame.pack(expand=True, fill="both")

# Frame for the toolbar at the top
toolbar_frame = ttk.Frame(main_frame)
toolbar_frame.pack(side="top", fill="x")

# Add an empty space to the left of the toolbar
empty_space = ttk.Label(toolbar_frame, width=10)  # You can adjust the width as needed
empty_space.pack(side="left")

# Toolbar
toolbar = ttk.Frame(toolbar_frame)
toolbar.pack(side="left")

# File Menu
file_menu = ttk.Menubutton(toolbar, text="File", direction="below")
file_menu.pack(side="left")

file_menu.menu = tk.Menu(file_menu, tearoff=0)
file_menu["menu"] = file_menu.menu

file_menu.menu.add_command(label="Import", command=import_code)
file_menu.menu.add_separator()
file_menu.menu.add_command(label="Save", command=save)
file_menu.menu.add_command(label="Save As", command=save_as)
file_menu.pack()

# Other buttons
button_run = ttk.Button(toolbar, text="Run", command=run)
button_step = ttk.Button(toolbar, text="Run Step by Step", command=run_step_by_step)
button_reset = ttk.Button(toolbar, text="Reset", command=reset)
button_connect = ttk.Button(toolbar, text="Connect Board", command=connect_board)
button_download = ttk.Button(toolbar, text="Download Code", command=download_code)
button_settings = ttk.Button(toolbar, text="Settings", command=settings)

button_run.pack(side="left", padx=5)
button_step.pack(side="left", padx=5)
button_reset.pack(side="left", padx=5)
button_connect.pack(side="left", padx=5)
button_download.pack(side="left", padx=5)
button_settings.pack(side="left", padx=5)

# Assembly code area in the middle
asm_zone = tk.Text(main_frame, width=40, height=20)
asm_zone.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=asm_zone.yview)
scrollbar.pack(side="right", fill="y")

# Configure the text widget to work with the scrollbar
asm_zone.config(yscrollcommand=scrollbar.set)

# Register frame on the right of the assembly zone
reg_frame = ttk.LabelFrame(main_frame, text="Registers")
reg_frame.pack(side="right", fill="y")

# Create register widgets (to be adapted to the number of registers)
registers = []
for i in range(15):
    reg_name = f"R{i + 1}:"
    reg_value = tk.StringVar()
    reg_value.set("0x0000")  # Initial value
    label_reg = ttk.Label(reg_frame, text=reg_name)
    reg_field = ttk.Label(reg_frame, textvariable=reg_value)
    label_reg.grid(row=i, column=0, sticky="w", padx=5, pady=2)
    reg_field.grid(row=i, column=1, sticky="w", padx=5, pady=2)
    registers.append(reg_value)

# Pipeline frame at the bottom
pip_frame = ttk.LabelFrame(window, text="Pipeline")
pip_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

# Add pipeline stages to the frame (to be adapted)
pip_stages = []
for i, stage in enumerate(["Fetch", "Decode", "Execute"]):
    stage_label = ttk.Label(pip_frame, text=stage)
    stage_label.grid(row=0, column=i, padx=5, pady=2)
    pip_stages.append(stage_label)

window.mainloop()