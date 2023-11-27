# ---------------------- ENSEA's Python LCM3 Simulator ---------------------- #
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
# --------------------------------------------------------------------------- #



import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import webbrowser



# ---------- Variables ---------- #

file_path = None






# ---------- Simulator ---------- #

class EnseaSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Title
        self.title("ENSEA's Python LCM3 ASM Simulator")
        self.geometry("980x720")

        # Coding window creation
        self.asm_window = ASMWindow(self)
        self.asm_window.pack(side="bottom", fill="x", expand=True)

        # Toolbar creation
        self.toolbar = Toolbar(self, self.asm_window)
        self.toolbar.pack(side="bottom", fill="x")






# ---------- Toolbar ---------- #

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, asm_window):
        super().__init__(master)
        self.pack(side="top", fill="x")

        # File menu creation
        self.file_menu = FileMenu(self, asm_window)
        self.file_menu.pack(side="left")

        # Settings menu creation
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.pack(side="left")

        # Help menu creation
        self.help_menu = HelpMenu(self)
        self.help_menu.pack(side="left")






# ---------- Menus ---------- #

class FileMenu(ctk.CTkFrame):
    def __init__(self, master, asm_window):
        super().__init__(master)

        def save_as():
            '''Opens a dialog window to save the current code into a new file.\n
                It wont save it automatically like the 'save' function does.'''

            global file_path

            file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    saved_code = asm_window.get_text_content()  # Gets the code from the text area
                    file.write(saved_code)

        def new_file():
            '''Creates a new blank code page. If code is present in the text window, asks if the user wants to save the current code.\n
                If yes: Calls the 'save_as' function.\n
                If not: The current code will be lost !'''
    
            global file_path

            # Checks if the asm_zone contains text
            if asm_window.get_text_content().strip():
                # Asks the user if they want to save the current content before creating a new file
                response = tk.messagebox.askyesno("Save Before Creating a New File?", "Do you want to save the current code before creating a blank page?")
                if response:
                    save_as()
            if file_path:
                asm_window.delete_content()

        def import_code():
            '''Opens a dialog window to import a code. If code is present in the text window, asks if the user wants to save the current code.\n
                If yes: Calls the 'save_as' function.\n
                If not: The current code will be lost !'''

            global file_path
    
            # Checks if the asm_zone contains text
            if asm_window.get_text_content().strip():
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
                    asm_window.delete_content()               # Clears the text area content
                    asm_window.insert_content(imported_code)  # Pastes the code

        def save():
            '''Overwrites the current save file, or opens a dialog window to create a one.'''

            global file_path

            # If the file hasn't been saved yet, asks the user where to save it
            if file_path is None:
                save_as()
 
            # If the user selected a file location, saves the content of the text area to the file
            if file_path:
                with open(file_path, "w") as file:
                    saved_code = asm_window.get_text_content()  # Gets the code from the text area
                    file.write(saved_code)

        # Create a File menu button
        self = tk.ttk.Menubutton(self, text="File", direction="below")
        self.pack(side="left")

        # Create a dropdown menu for the File button
        self.menu = tk.Menu(self, tearoff=0)
        self["menu"] = self.menu  # Assign the menu to the button

        # Add items to the File menu
        self.menu.add_command(label="New File", command=new_file)
        self.menu.add_command(label="Import", command=import_code)
        self.menu.add_separator()
        self.menu.add_command(label="Save", command=save)
        self.menu.add_command(label="Save As", command=save_as)
        

class SettingsMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        def theme_toggle_dark():
            '''Toggles dark theme.'''

            ctk.set_appearance_mode("dark")

        def theme_toggle_light():
            '''Toggles light theme.'''

            ctk.set_appearance_mode("light")

        # Create a Settings menu button
        self = tk.ttk.Menubutton(self, text="Settings", direction="below")
        self.pack(side="left")

        # Create a dropdown menu for the File button
        self.menu = tk.Menu(self, tearoff=0)
        self["menu"] = self.menu  # Assign the menu to the button

        # Add items to the File menu
        self.menu.add_command(label="Dark mode", command=theme_toggle_dark)
        self.menu.add_command(label="Light mode", command=theme_toggle_light)


class HelpMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
    
        def help_lcm3_docu():
            '''Opens an online documentation of the LCM3 instructions.'''

            webbrowser.open_new("https://moodle.ensea.fr/pluginfile.php/24675/mod_resource/content/1/LCM3_Instructions_2017.pdf")

        self = ttk.Menubutton(self, text="Help", direction="below")  # Help menu button
        self.pack(side="left")

        self.menu = tk.Menu(self, tearoff=0)  # Help menu "menu"
        self["menu"] = self.menu

        self.menu.add_command(label="This Simulator Documentation", command=SimulatorDocumentation)
        self.menu.add_separator()
        self.menu.add_command(label="LCM3 Documentation", command=help_lcm3_docu)


class SimulatorDocumentation(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.text = ("\n"+
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

        self.title("ENSEA's Python LCM3 Simulator - Documentation")
        self.geometry("1200x800")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.text_widget = ctk.CTkTextbox(self.frame, wrap="word")
        self.text_widget.pack(side="left", fill="both", expand=True)

        self.text_widget.insert(tk.END, self.text)
        self.text_widget.configure(state="disabled", font=("Helvetica",12))



# ---------- ASMWindow ---------- #

class ASMWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.pack(side="top", fill="both", expand=True)

    def get_text_content(self):
        '''Gets the content of the text box.'''
        return self.textbox.get("1.0", tk.END)
    
    def delete_content(self):
        '''Deletes the content of the text box.'''
        return self.textbox.delete("1.0", tk.END)
    
    def insert_content(self, content):
        '''Inserts the content in the text box.'''
        return self.textbox.insert(tk.END, content)
    





class Test():
    def __init__():
        super().__init__()
        print("bruh")


class MyCheckboxFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.checkbox_1 = ctk.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = ctk.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_3 = ctk.CTkCheckBox(self, text="checkbox 3")
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        return checked_checkboxes


app = EnseaSimulator()
app.mainloop()
