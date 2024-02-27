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
import random
import webbrowser

from instruction_translation import *

# change the color of the title of the debugger window when error

# Bug with switch between hex and dec in regs when assemble
# -> Fair un register update avec un stockage interne pour pouvoir enlever ce bug

# Executer 2 tours après pour être fidèle au pipeline



# ---------- Variables ---------- #

file_path = None






# ---------- Simulator ---------- #

class EnseaSimulator(ctk.CTk):
    def __init__(self):        
        super().__init__()

        def theme_toggle_dark():
            '''Toggles dark theme.'''

            ctk.set_appearance_mode("dark")


        def theme_toggle_light():
            '''Toggles light theme.'''

            ctk.set_appearance_mode("light")


        self.title("ENSEA's Python LCM3 ASM Simulator")                                  # Simulator title
        self.geometry("980x720")

        self.main_frame = tk.ttk.PanedWindow(self, orient=tk.VERTICAL)                   # Main Frame under the Toolbar
        self.main_frame.pack(side="bottom", expand=True, fill="both", pady=5)

        self.central_frame = tk.ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)   # Central Frame above the Pipeline
        self.main_frame.add(self.central_frame, weight=5)

        self.coding_frame = tk.ttk.PanedWindow(self.central_frame, orient=tk.VERTICAL)   # Coding Frame on the left
        self.central_frame.add(self.coding_frame, weight=3)

        self.asm_window = ASMWindow(self.coding_frame)                                   # ASM Window at the top of Coding Frame
        self.coding_frame.add(self.asm_window, weight=1)

        self.debugger_window = DebuggerWindow(self.coding_frame)                         # Debugger at the bottom of Coding Frame
        self.coding_frame.add(self.debugger_window, weight=1)

        self.right_frame = tk.ttk.PanedWindow(self.central_frame, orient=tk.HORIZONTAL)  # Right Frame
        self.central_frame.add(self.right_frame, weight=1)

        self.register_window = RegisterWindow(self.right_frame)                          # Register Frame on the left of Right Frame
        self.right_frame.add(self.register_window, weight=1)

        self.mem_and_bin = MemAndBin(self.right_frame)                                   # Memory and binary arrays on the right of Right Frame
        self.right_frame.add(self.mem_and_bin, weight=1)

        self.pipeline_window = PipelineWindow(self)                                      # Pipeline window at the bottom
        self.main_frame.add(self.pipeline_window, weight=1)

        self.toolbar = Toolbar(self, self.asm_window, self.debugger_window, self.register_window, self.mem_and_bin, self.pipeline_window, theme_toggle_dark, theme_toggle_light)  # Toolbar at the top
        self.toolbar.pack(fill="x")






# ---------- ASM Window ---------- #

class ASMWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(side="top", fill="both", expand=True)

        self.title = ctk.CTkLabel(self.frame, text="ASM Code Window", bg_color="transparent")
        self.title.pack(side="top", fill="x")

        self.textbox = ctk.CTkTextbox(self.frame, width=700, text_color="#1020FF")
        self.textbox.pack(side="top", fill="both", expand=True)

        # Configure tags for syntax highlighting
        self.textbox.tag_config("label", foreground="#FF0000")
        self.textbox.tag_config("Register", foreground="#00FF00")
        self.textbox.tag_config("register", foreground="#00FF00")
        self.textbox.tag_config("comma", foreground="fuchsia")
        self.textbox.tag_config("bracket", foreground="#00A000")
        self.textbox.tag_config("hash", foreground="#FF8000")
        self.textbox.tag_config("number", foreground="#FFB000")
        self.textbox.tag_config("comment", foreground="#888888")

        # Bind events to update syntax highlighting
        self.textbox.bind("<KeyRelease>", self.highlight_syntax)


    def highlight_syntax(self, event=None):
        '''Update syntax highlighting.'''
        
        # Color for labels
        self.textbox.tag_remove("label", "1.0", tk.END)
        index = "1.0"
        while True:
            index = self.textbox.search(":", index, tk.END)
            if not index:
                break

            # Tag the text before the semicolon
            start_index = self.textbox.index(f"{index} linestart")
            end_index = self.textbox.index(f"{index}+1c")
            self.textbox.tag_add("label", start_index, end_index)
            index = f"{index}+1c"

        # Other colors

        # Define patterns and corresponding tags
        patterns = {
            " R": "Register",
            " r": "register",
            "[\\[\\]]": "bracket",
            ",": "comma",
            "#": "hash",
            ";": "comment"}

        # Remove existing tags
        for tag in patterns.values():
            self.textbox.tag_remove(tag, "1.0", tk.END)

        # Iterate through the patterns and tag the text accordingly
        for pattern, tag in patterns.items():
            start_index = "1.0"
            while True:
                start_index = self.textbox.search(pattern, start_index, tk.END, regexp=True)
                if not start_index:
                    break

                # Compute end_index based on the pattern
                if pattern == "," or pattern == "[\\[\\]]" or pattern == '#':
                    end_index = self.textbox.index(f"{start_index}+1c")
                else:
                    end_index = self.textbox.index(f"{start_index} lineend")

                # Tag and jump to next character
                self.textbox.tag_add(tag, start_index, end_index)
                start_index = f"{end_index}+1c"

                # Handles numbers after hash (including hex and bin)
                if pattern == "#":
                    start_index = self.textbox.index(f"{start_index}-1c")
                    end_index = self.textbox.index(f"{start_index} lineend")
                    self.textbox.tag_add("number", start_index, end_index)
                    start_index = f"{end_index}+1c"


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
        self.textbox.pack(side="top", fill="both", expand=True)
        self.textbox.configure(state="disabled")
    

    def delete_content(self):
        '''Deletes the content of the text box.'''
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.configure(state="disabled", text_color="black")
    

    def insert_content(self, content:str, color="silver"):
        '''Inserts the content in the text box with specified color.'''
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, content)
        self.textbox.configure(state="disabled", text_color=color)






# ---------- Register Window ---------- #

class RegisterWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame
        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(side="top", fill="both", expand=True)

        # Title
        self.title = ctk.CTkLabel(self.frame, text="Registers", bg_color="transparent")
        self.title.pack(side="top", fill="x")

        self.sub_frame = ctk.CTkFrame(self.frame, corner_radius=0)
        self.sub_frame.pack(side="top", fill="both")

        self.value_labels = []

        # Create data entry widgets
        for i in range(7):
            self.register_label = ctk.CTkLabel(self.sub_frame, text=f"R{i}:", padx=5, pady=2, anchor="w")
            self.register_label.grid(row=i, column=0, sticky="nsew")

            self.value_label = ctk.CTkLabel(self.sub_frame, text="0", padx=5, pady=2, anchor="w")
            self.value_label.grid(row=i, column=1, sticky="nsew")
            self.value_labels.append(self.value_label)

        self.register_label = ctk.CTkLabel(self.sub_frame, text="NZVC", padx=5, pady=2, anchor="w")
        self.register_label.grid(row=7, column=0, sticky="nsew")

        self.value_label = ctk.CTkLabel(self.sub_frame, text="0", padx=5, pady=2, anchor="w")
        self.value_label.grid(row=7, column=1, sticky="nsew")
        self.value_labels.append(self.value_label)

        # Configure grid weights for resizing
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.grid_columnconfigure(j, weight=1)

        self.display = 0
        self.button = ctk.CTkButton(self.frame, text="Switch to hex", command=self.change_format)
        self.button.pack(side="top")


    def set_register_values(self, index:int, value:str):
        '''Set register values using a list.'''
        self.value_labels[index].configure(text=value)


    def change_format(self):
        '''Change the format of values to hexadecimal.'''
        if self.display == 0:
            for i, label in enumerate(self.value_labels):
                decimal_value = int(label.cget("text"))
                hex_value = "0x"+format(decimal_value, "08x") if i<7 else "0b"+format(decimal_value, "04b")
                label.configure(text=hex_value)
                self.display = 1
                self.button.configure(text="Switch to dec")
        else:
            for label in self.value_labels:
                hex_value = label.cget("text")
                hex_value = hex_value[2:]
                decimal_value = int(hex_value, 16)
                label.configure(text=str(decimal_value))
                self.state = 0
                self.button.configure(text="Switch to dec")






# ---------- Memory Arrays and Binary ---------- #

class MemAndBin(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # Tabs
        self.add("Code Memory")
        self.add("User Memory")
        self.add("Binary")

        # ---- Code Memory ----
        
        self.code_memory = ctk.CTkFrame(master=self.tab("Code Memory"))
        self.code_memory.pack(expand=True, fill="both")
 
        self.code_headers = ["Adress", "Value", "Instruction"]
        self.code_tree = tk.ttk.Treeview(self.code_memory, columns=self.code_headers, show="headings")
        self.code_tree.tag_configure("even_row", background="#202020", foreground="lightcyan")  # Even row style
        self.code_tree.tag_configure("odd_row", background="#101010", foreground="lightcyan")   # Odd row style

        for header in self.code_headers:
            self.code_tree.heading(header, text=header)
            self.code_tree.column(header, anchor="center", width=100)

        # Filling the code treeview
        for i in range(256):
            address = "0x"+format(i*2+134217736, "08x")
            hex_value = "0x0000"
            instruction = ""
            tags = ("even_row", "odd_row")[i % 2 == 1]
            self.code_tree.insert("", "end", values=(address, hex_value, instruction), tags=(tags,))

        # Vertical scrollbar
        self.code_scrollbar = ctk.CTkScrollbar(self.code_memory, orientation="vertical", command=self.code_tree.yview)
        self.code_tree.configure(yscrollcommand=self.code_scrollbar.set)

        # Pack components
        self.code_tree.pack(side="left", fill="both", expand=True)
        self.code_scrollbar.pack(side="right", fill="y")

        # ---- User Memory ----

        self.user_memory = ctk.CTkFrame(master=self.tab("User Memory"))
        self.user_memory.pack(expand=True, fill="both")

        user_headers = ["Adress", "Value"]
        self.user_tree = tk.ttk.Treeview(self.user_memory, columns=user_headers, show="headings")
        self.user_tree.tag_configure("even_row", background="#202020", foreground="lightcyan")  # Even row style
        self.user_tree.tag_configure("odd_row", background="#101010", foreground="lightcyan")   # Odd row style

        for header in user_headers:
            self.user_tree.heading(header, text=header) 
            self.user_tree.column(header, anchor="center", width=100)

        # Filling the user treeview
        for i in range(256):
            address = "0x"+format(i*4+536870912, "08x")
            hex_value = "0x0000000"
            tags = ("even_row", "odd_row")[i % 2 == 1]
            self.user_tree.insert("", "end", values=(address, hex_value), tags=(tags,))

        # Vertical scrollbar
        self.user_scrollbar = ctk.CTkScrollbar(self.user_memory, orientation="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=self.user_scrollbar.set)

        # Pack components
        self.user_tree.pack(side="left", fill="both", expand=True)
        self.user_scrollbar.pack(side="right", fill="y")

        # ---- Binary window ----

        self.binary = ctk.CTkFrame(master=self.tab("Binary"))
        self.binary.pack(expand=True, fill="both")

        self.bin_frame = ctk.CTkFrame(self.binary, corner_radius=0)
        self.bin_frame.pack(side="top", fill="both", expand=True)

        self.bin_title = ctk.CTkLabel(self.bin_frame, text="Binary", bg_color="transparent")
        self.bin_title.pack(side="top", fill="x")

        self.bin_textbox = ctk.CTkTextbox(self.bin_frame)
        self.bin_textbox.pack(side="top", fill="both", expand=True)
        self.bin_textbox.configure(state="disabled")


    def code_mem_set(self, index:str, value:str, instruction:str):
        '''Set values for a chosen line in the treeview.'''
        self.item_id = self.code_tree.get_children()[int(index)]  # Get the item ID based on the index
        self.code_tree.item(self.item_id, values=("0x"+format(index*2+134217736, "08x"), "0x"+format(int(value, 2), "04x"), instruction))

    
    def user_mem_set(self, index:str, value:str):
        '''Set values for a chosen line in the treeview.'''
        self.item_id = self.user_tree.get_children()[int(index)]  # Get the item ID based on the index
        self.user_tree.item(self.item_id, values=("0x"+format(index*4+536870912, "08x"), "0x"+format(int(value, 2), "04x")))


    def delete_bin(self):
        '''Deletes the content of the text box.'''
        self.bin_textbox.configure(state="normal")
        self.bin_textbox.delete("1.0", tk.END)
        self.bin_textbox.configure(state="disabled")
    

    def insert_bin(self, content:str):
        '''Inserts the content in the text box.'''
        self.bin_textbox.configure(state="normal")
        self.bin_textbox.insert(tk.END, content)
        self.bin_textbox.configure(state="disabled")
  





# ---------- Pipeline window ---------- #

class PipelineWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        headers = ["Fetch", "Decode", "Execute"]

        # Create header labels on the left
        for i, header in enumerate(headers):
            self.header_label = ctk.CTkLabel(self, text=header, padx=5, pady=2, anchor="w")
            self.header_label.grid(row=i, column=0, sticky="nsew")

        # Create data entry widgets on the right
        for i in range(3):
            for j in range(20):
                self.entry = ctk.CTkEntry(self, state="readonly", width=4)
                self.entry.insert(0, "")
                self.entry.grid(row=i, column=j + 1, sticky="nsew")

        # Configure grid weights for resizing
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        for j in range(21):
            self.grid_columnconfigure(j, weight=1)


    def get_cell(self, row:int, col:int):
        '''Get the value in the specified cell.'''

        if 0 <= row <= 3 and 1 <= col <= 21:
            entry_widget = self.grid_slaves(row=row, column=col)[0]
            return entry_widget.get()
        
        else:
            return None


    def set_cell(self, row:int, col:int, value:str):
        '''Set the value in the specified cell.'''
        
        if 0 <= row <= 3 and 1 <= col <= 21:
            # Fetch the list of widgets at the specified row and column
            slaves = self.grid_slaves(row=row, column=col)
            if slaves:
                entry_widget = slaves[0]
                entry_widget.configure(state="normal")  # Make editable temporarily
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, value)
                entry_widget.configure(state="readonly")  # Make readonly again
            else:
                print(f"No widget found at row {row} and column {col}")

        else:
            print("Row or column index out of range")
            return None


    def iter_pip(self, value:str):
        '''Shifts the whole pipeline on the right and creates a new FDE column on the left.'''

        # Shift on the right
        for i in range(3):
            for j in range(19):
                self.prev = self.get_cell(i, 19-j)
                self.set_cell(i, 20-j, self.prev)

        # Add the two old instr in the new column
        self.prev = self.get_cell(1, 1)
        self.set_cell(2, 1, self.prev)
        self.prev = self.get_cell(0, 1)
        self.set_cell(1, 1, self.prev)

        # Add the new instr in the new column
        self.set_cell(0, 1, value)






# ---------- Toolbar ---------- #

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, asm_window, debugger_window, register_window, mem_and_bin, pipeline_window, theme_toggle_dark, theme_toggle_light):
        super().__init__(master)

        def download_code():
            ''''''


        def connect_board():
            ''''''


        def reset():
            '''Resets the values in registers, pipeline, binary, and memory arrays.'''

            # Updates button states
            master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")
            master.toolbar.run_button.configure(self, fg_color="gray", state="disabled", text="Run")
            master.toolbar.runsbs_button.configure(self, fg_color="gray", state="disabled", text="Run Step By Step", hover_color="darkgreen")
            master.toolbar.step_button.configure(self, fg_color="gray", state="disabled")

            # Empties debugger
            master.debugger_window.delete_content()

            # Empties registers
            for i in range(8):
                register_window.set_register_values(i, 0)

            # Empties memories and bit window
            mem_and_bin.delete_bin()

            # Empties the pipeline
            for i in range(22):
                pipeline_window.iter_pip("")


        def step():
            '''Executes a step of the code.'''

            if self.state != len(master.toolbar.line_update):
                # Update the Register
                if master.toolbar.register_update[self.state - 1] != []:
                    register_window.set_register_values(master.toolbar.register_update[self.state - 1][0], master.toolbar.register_update[self.state - 1][1])

                # Update the User Mem
                if master.toolbar.memory_update[self.state - 1] != []:
                    mem_and_bin.user_mem_set(self.state - 1, master.toolbar.memory_update[self.state - 1][0], master.toolbar.memory_update[self.state - 1][1])

                # Update the Pipeline
                if master.toolbar.split_instructions[self.state - 1] != "":
                    pipeline_window.iter_pip(master.toolbar.split_instructions[self.state - 1][:3])

                # Update the state
                self.state += 1

            else:
                master.toolbar.step_button.configure(self, fg_color="gray", state="disabled")
                master.toolbar.run_button.configure(self, fg_color="gray", state="disabled", text="Run")
                master.toolbar.runsbs_button.configure(self, fg_color="gray", state="disabled", text="Run Step By Step", hover_color="darkgreen")
                master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")
                self.state = 0


        def run_step_by_step():
            '''Launches the step y step execution of the code.'''

            # Updates button states
            master.toolbar.run_button.configure(self, text="Resume")
            master.toolbar.step_button.configure(self, fg_color="forestgreen", state="normal")

            if self.state == 0:
                master.toolbar.runsbs_button.configure(self, fg_color="firebrick", text="STOP", hover_color="maroon")
                self.state = 1
            else:
                master.toolbar.run_button.configure(self, fg_color="gray", state="disabled", text="Run")
                master.toolbar.runsbs_button.configure(self, fg_color="gray", text="Run Step By Step", state="disabled", hover_color="darkgreen")
                master.toolbar.step_button.configure(self, fg_color="gray", state="disabled")
                master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")
                self.state = 0


        def run():
            '''Runs the code in one go.\n
                Also allows to resume after a runsbs.'''
            
            # Update button states
            master.toolbar.run_button.configure(self, fg_color="gray", state="disabled", text="Run")
            master.toolbar.runsbs_button.configure(self, fg_color="gray", state="disabled", text="Run Step By Step", hover_color="darkgreen")
            master.toolbar.step_button.configure(self, fg_color="gray", state="disabled")
            master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")
            self.state = 0

            # Update register values
            for i in range(8):
                register_window.set_register_values(i, virtual_register[i])

            # Update User RAM values
            for i in range(0, len(virtual_memory), 2):
                mem_and_bin.user_mem_set(i, virtual_memory[i], virtual_memory[i+1])

            # Updates the Pipeline
            for e in master.toolbar.split_instructions[-24:]:
                if e != "":
                    pipeline_window.iter_pip(e[:3])


        def assemble():
            '''Assembles the code.'''

            # Cleaning
            reset()
            master.toolbar.assemble_button.configure(self, fg_color="gray", state="disabled")

            # Fetching the code
            code = asm_window.get_text_content()
            master.toolbar.split_instructions, _, master.toolbar.bitstream, master.toolbar.register_update, master.toolbar.line_update, master.toolbar.memory_update, master.toolbar.error = instruction_translation(code)

            # Funny text variations for when user tries to assemble empty code
            variations = ["sipping a coconut", "catching some rays", "in a hammock", "on a beach", "snorkeling", "in a tropical paradise", "surfing the clouds",
            "on a spa retreat", "napping in a hammock", "practicing mindfulness", "doing yoga", "enjoying a siesta", "on a cosmic cruise", "in a Zen garden",
            "sunbathing", "in a day spa", "on a coffee break", "chilling in a hammock", "vacationing", "on a beach", "gone", "too short", "transparent", "too small"]
            random_variation = random.choice(variations)

            # Check if code is empty
            if code == "\n":
                debugger_window.insert_content("Assembling air? Your code's "+random_variation+".", "blue")
                master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")

            # Check if there are errors
            elif master.toolbar.error != []:
                master.toolbar.assemble_button.configure(self, fg_color="forestgreen", state="normal")

                # Display error in debugger
                for i in range(len(master.toolbar.error)//2):
                    debugger_window.insert_content("%s at line %d\n" % (master.toolbar.error[2*i], master.toolbar.error[2*i+1]+1), "red")

            else:
                # Fills the Code RAM array and the bitstream frame
                for l in range(len(master.toolbar.line_update)-2):
                    if len(master.toolbar.bitstream) != 0:
                        if master.toolbar.bitstream[master.toolbar.line_update[l]] != "":

                            # Display the instruction in the Code Memory
                            mem_and_bin.code_mem_set(master.toolbar.line_update[l], master.toolbar.bitstream[master.toolbar.line_update[l]], master.toolbar.split_instructions[master.toolbar.line_update[l]])
                            
                            # Display the instruction in the binary window
                            mem_and_bin.insert_bin(master.toolbar.bitstream[master.toolbar.line_update[l]])

                # Display success message in debugger
                debugger_window.insert_content("Assembly complete", "lime")
                
                # Enables buttons Run and RSBS
                master.toolbar.run_button.configure(self, fg_color="forestgreen", state="normal")
                master.toolbar.runsbs_button.configure(self, fg_color="forestgreen", state="normal")
        

        self.download_button = ctk.CTkButton(self, text="Download Code", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="gray", hover_color="darkgreen", state="disabled", command=download_code)
        self.download_button.pack(side="right", padx=5)

        self.connect_button = ctk.CTkButton(self, text="Connect Board", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="forestgreen", hover_color="darkgreen", command=connect_board)
        self.connect_button.pack(side="right")

        self.reset_button = ctk.CTkButton(self, text="Reset", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="forestgreen", hover_color="darkgreen", command=reset)
        self.reset_button.pack(side="right", padx=5)

        self.step_button = ctk.CTkButton(self, text="Setp->", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="gray", hover_color="darkgreen", state="disabled", command=step)
        self.step_button.pack(side="right")

        self.runsbs_button = ctk.CTkButton(self, text="Run Step By Step", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="gray", hover_color="darkgreen", state="disabled", command=run_step_by_step)
        self.runsbs_button.pack(side="right", padx=5)

        self.run_button = ctk.CTkButton(self, text="Run", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="gray", hover_color="darkgreen", state="disabled", command=run)
        self.run_button.pack(side="right")

        self.assemble_button = ctk.CTkButton(self, text="Assemble", width=100, height=10, font = ("Arial", 11), corner_radius=25, fg_color="forestgreen", hover_color="darkgreen", command=assemble)
        self.assemble_button.pack(side="right", padx=5)

        self.file_menu = FileMenu(self, asm_window)
        self.file_menu.pack(side="left")

        self.settings_menu = SettingsMenu(self, theme_toggle_dark, theme_toggle_light)
        self.settings_menu.pack(side="left")

        self.help_menu = HelpMenu(self)
        self.help_menu.pack(side="left")

        self.state = 0

        self.split_instruction, self.line_instruction, self.bitstream, self.register_update, self.line_update, self.memory_update, self.error = [], [], [], [], [], [], []






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
    def __init__(self, master, theme_toggle_dark, theme_toggle_light):
        super().__init__(master)

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
