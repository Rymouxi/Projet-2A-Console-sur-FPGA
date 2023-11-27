import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


file_path = None


class EnseaSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ENSEA's Python LCM3 ASM Simulator")
        self.geometry("980x720")

        self.asm_window = ASMWindow(self)
        self.asm_window.pack(side="bottom", fill="x", expand=True)

        self.toolbar = Toolbar(self, self.asm_window)
        self.toolbar.pack(side="bottom", fill="x")

    def button_callback(self):
        print("button pressed")


class Toolbar(ctk.CTkFrame):
    def __init__(self, master, asm_window):
        super().__init__(master)
        self.pack(side="top", fill="x")

        self.file_menu = FileMenu(self, asm_window)
        self.file_menu.pack(side="left")


class ASMWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.pack(side="top")

    def get_text_content(self):
        '''Gets the content of the text box.'''
        return self.textbox.get("1.0", tk.END)
    
    def delete_content(self):
        '''Deletes the content of the text box.'''
        return self.textbox.delete("1.0", tk.END)
    
    def insert_content(self, content):
        '''Inserts the content in the text box.'''
        return self.textbox.insert(tk.END, content)


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