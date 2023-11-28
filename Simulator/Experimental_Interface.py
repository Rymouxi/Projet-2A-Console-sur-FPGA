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
import customtkinter as ctk
import webbrowser



# ---------- Variables ---------- #

file_path = None






# ---------- Simulator ---------- #

class EnseaSimulator(ctk.CTk):
    def __init__(self):        
        super().__init__()

        # Simulator title
        self.title("ENSEA's Python LCM3 ASM Simulator")
        self.geometry("980x720")

        # Main Frame under the Toolbar
        self.main_frame = tk.ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.main_frame.pack(side="bottom", expand=True, fill="both")

        # Central Frame above the Pipeline
        self.central_frame = tk.ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.main_frame.add(self.central_frame, weight=5)

        # Coding Frame on the left
        self.coding_frame = tk.ttk.PanedWindow(self.central_frame, orient=tk.VERTICAL)
        self.central_frame.add(self.coding_frame, weight=1)

        # ASM Window at the top of Coding Frame
        self.asm_window = ASMWindow(self.coding_frame)
        self.coding_frame.add(self.asm_window, weight=1)

        # Debugger at the bottom of Coding Frame
        self.debugger_window = DebuggerWindow(self.coding_frame)
        self.coding_frame.add(self.debugger_window, weight=1)

        # Right Frame
        self.right_frame = tk.ttk.PanedWindow(self.central_frame, orient=tk.HORIZONTAL)
        self.central_frame.add(self.right_frame, weight=1)

        # Register Frame on the left of Right Frame
        self.register_window = RegisterWindow(self.right_frame)
        self.right_frame.add(self.register_window, weight=1)

        # Memory and binary arrays on the right of Right Frame
        self.mem_and_bin = MemAndBin(self.right_frame)
        self.right_frame.add(self.mem_and_bin, weight=1)

        # Pipeline window at the bottom
        self.pipeline_window = PipelineWindow(self)
        self.main_frame.add(self.pipeline_window, weight=1)

        # Toolbar at the top
        self.toolbar = Toolbar(self, self.asm_window)
        self.toolbar.pack(fill="x")







# ---------- ASM Window ---------- #

class ASMWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(side="top", fill="both", expand=True)

        self.title = ctk.CTkLabel(self.frame, text="ASM Code Window", bg_color="transparent")
        self.title.pack(side="top", fill="x")

        self.textbox = ctk.CTkTextbox(self.frame)
        self.textbox.pack(side="top", fill="both")

    def get_text_content(self):
        '''Gets the content of the text box.'''
        return self.textbox.get("1.0", tk.END)
    
    def delete_content(self):
        '''Deletes the content of the text box.'''
        return self.textbox.delete("1.0", tk.END)
    
    def insert_content(self, content):
        '''Inserts the content in the text box.'''
        return self.textbox.insert(tk.END, content)
    





# ---------- Debugger Window ---------- #

class DebuggerWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(side="top", fill="both", expand=True)

        self.title = ctk.CTkLabel(self.frame, text="Debugger", bg_color="transparent")
        self.title.pack(side="top", fill="x")

        self.textbox = ctk.CTkTextbox(self.frame)
        self.textbox.pack(side="top", fill="both")
        self.textbox.configure(state="disabled")
    
    def delete_content(self):
        '''Deletes the content of the text box.'''
        return self.textbox.delete("1.0", tk.END)
    
    def insert_content(self, content):
        '''Inserts the content in the text box.'''
        return self.textbox.insert(tk.END, content)






# ---------- Register Window ---------- #

class RegisterWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(side="top", fill="both", expand=True)

        self.title = ctk.CTkLabel(self.frame, text="Registers", bg_color="transparent")
        self.title.pack(side="top", fill="x")






# ---------- Memory Arrays and Binary ---------- #

class MemAndBin(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # create tabs
        self.add("tab 1")
        self.add("tab 2")

        # add widgets on tabs
        self.label = ctk.CTkLabel(master=self.tab("tab 1"))
        self.label.grid(row=0, column=0, padx=20, pady=0)






# ---------- Pipeline window ---------- #

class PipelineWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        headers = ["Fetch", "Decode", "Execute"]


        # Create header labels on the left
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self, text=header, padx=5, pady=2, anchor="w")
            header_label.grid(row=i, column=0, sticky="nsew")

        # Create data entry widgets on the right
        for i in range(3):
            for j in range(20):
                entry = ctk.CTkEntry(self, state="readonly", width=4)
                entry.insert(0, "")
                entry.grid(row=i, column=j + 1, sticky="nsew")

        # Configure grid weights for resizing
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        for j in range(21):
            self.grid_columnconfigure(j, weight=1)

    def get_cell(self, row, col):
        '''Get the value in the specified cell.'''

        if 0 <= row <= 3 and 1 <= col <= 21:
            return self.entry_widgets[row][col - 1].get()

    def set_cell(self, row, col, value):
        '''Set the value in the specified cell.'''
        
        if 0 <= row <= 3 and 1 <= col <= 21:
            self.entry_widgets[row][col - 1].configure(state="normal")  # Make editable temporarily
            self.entry_widgets[row][col - 1].delete(0, tk.END)
            self.entry_widgets[row][col - 1].insert(0, value)
            self.entry_widgets[row][col - 1].configure(state="readonly")  # Make readonly again






# ---------- Toolbar ---------- #

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, asm_window):
        super().__init__(master)
        
        # File menu
        self.file_menu = FileMenu(self, asm_window)
        self.file_menu.pack(side="left")

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.pack(side="left")

        # Help menu
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

        # File menu button
        self = tk.ttk.Menubutton(self, text="File", direction="below")
        self.pack(side="left")

        # Dropdown menu for the File button
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

        # Settings menu button
        self = tk.ttk.Menubutton(self, text="Settings", direction="below")
        self.pack(side="left")

        # Dropdown menu for the File button
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

        # Help menu button
        self = tk.ttk.Menubutton(self, text="Help", direction="below")  # Help menu button
        self.pack(side="left")

        # Dropdown menu for the Help Button
        self.menu = tk.Menu(self, tearoff=0)  # Help menu "menu"
        self["menu"] = self.menu

        # Add items to the File menu
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






# ---------- Code ---------- #

app = EnseaSimulator()
app.mainloop()