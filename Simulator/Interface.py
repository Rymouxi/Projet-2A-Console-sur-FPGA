

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
import math

from instruction_translation import *

# Change values from register manualy + same for memory






# ---------- Variables ---------- #

file_path = None








# ---------- Simulator ---------- #

class EnseaSimulator(ctk.CTk):
    '''Main simulator window. Contains all the interface objects.'''

    def __init__(self):        
        super().__init__()

        self.title("ENSEA's Python LCM3 ASM Simulator")                                  # Simulator title
        self.geometry('980x720')

        self.main_frame = tk.ttk.PanedWindow(self, orient=tk.VERTICAL)                   # Main Frame under the Toolbar
        self.main_frame.pack(side='bottom', expand=True, fill='both', pady=5)

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

        self.toolbar = Toolbar(self, self.asm_window, self.debugger_window, self.register_window, self.mem_and_bin, self.pipeline_window)  # Toolbar at the top
        self.toolbar.pack(fill='x')

        self.theme_toggle_dark()


    def theme_toggle_dark(event=None):
        '''Toggles dark theme.'''
        ctk.set_appearance_mode('dark')


    def theme_toggle_light(event=None):
        '''Toggles light theme.'''
        ctk.set_appearance_mode('light')








# ---------- ASM Code Window ---------- #

class ASMWindow(ctk.CTkFrame):
    '''Contains all the frames and functions linked to the ASM coding area.'''

    def __init__(self, master):
        super().__init__(master)

        def update_btns_on_modif(self, event=None):
            '''Reenables the assembly button and turns off the others on code modification by the user.'''

            if master.master.master.master.toolbar.state != 0:
                master.master.master.master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
                master.master.master.master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
                master.master.master.master.toolbar.runsbs_button.configure(self, fg_color='gray', state='disabled', text='Run Step By Step', hover_color='darkgreen')
                master.master.master.master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal', text='Assemble')
                master.master.master.master.toolbar.state = 0


        def update_line_view(event=None):
            '''Updates the view of the line counter to sync it with the textbox.'''

            textbox_scroll_fraction = self.textbox.yview()[0]      # Get the current vertical scrollbar position of the textbox
            self.line_count.yview_moveto(textbox_scroll_fraction)  # Set the vertical scrollbar position of the line counter to match the textbox
            self.after(10, update_line_view)                       # Schedule the function to run again after 10 milliseconds


        def place_breakpoint(event=None):
            '''Place a breakpoint on the clicked line.'''

            number_of_lines = int(self.textbox.index('end-1c').split('.')[0])  # Get the total number of lines in the text widget
            hidden_part = self.textbox.yview()[0]                              # Get the ratio of what is hidden
            hidden_lines = hidden_part * number_of_lines                       # Get the number of hidden lines
            line_visible_click = event.y / 19 + 1                              # Get the number of the line clicked relative to the frame
            line_number = int(line_visible_click + hidden_lines)               # Get the real number of the line

            # Add or remove the breakpoint
            if line_number in self.break_list:
                self.break_list.remove(line_number)
            else:
                self.break_list.append(line_number)

            # Update the visuals
            self.update_line_count()


        # Frames
        self.frame = ctk.CTkFrame(self, corner_radius=0)                                       # Object Frame
        self.frame.pack(side='top', fill='both', expand=True)
        self.title = ctk.CTkLabel(self.frame, text='ASM Code Window', bg_color='transparent')  # Title
        self.title.pack(side='top', fill='x')
        self.textbox_frame = ctk.CTkFrame(self.frame, corner_radius=0)                         # Frame containing the ASM window and the line numbers
        self.textbox_frame.pack(side='top', fill='both', expand=True)
        self.line_count = ctk.CTkTextbox(self.textbox_frame, width=20, text_color='#C0C0C0', fg_color='#404040', scrollbar_button_hover_color='#404040', scrollbar_button_color='#404040')
        self.line_count.pack(side='left', fill='both', expand=False)                           # Line numbers
        self.textbox = ctk.CTkTextbox(self.textbox_frame, width=700, text_color='#2080C0')     # ASM window text box
        self.textbox.pack(side='right', fill='both', expand=True)

        # Configure tags for syntax highlighting
        self.textbox.tag_config('label', foreground='#B02090')      # Purple
        self.textbox.tag_config('Register', foreground='#509020')   # Green
        self.textbox.tag_config('register', foreground='#509020')   # Green
        self.textbox.tag_config('comma', foreground='#A0A000')      # Yellow
        self.textbox.tag_config('bracket', foreground='#006020')    # Dark Green
        self.textbox.tag_config('hash', foreground='#D08030')       # Orange
        self.textbox.tag_config('comment', foreground='#888888')    # Gray
        self.textbox.tag_config('ERROR', background='#902020')      # Red
        self.textbox.tag_config('next_line', background='#353545')  # Dark Blue Gray
        self.textbox.tag_config('breakline', background='#605010')  # Yellow
        self.line_count.tag_config('breakpoint', foreground='#FF0000', background='#502020')  # Red

        # Breakpoint list
        self.break_list = []

        # Bind events to update syntax highlighting, buttons update,  andline counter update
        self.textbox.bind('<KeyRelease>', self.highlight_syntax)
        self.textbox.bind('<KeyRelease>', update_btns_on_modif)
        self.textbox.bind('<KeyRelease>', self.update_line_count)

        # Bind mouse enter and leave events to change cursor, and breakpoint placing/removing
        self.line_count.bind('<Button-1>', place_breakpoint)
        self.line_count.bind('<Enter>', lambda event: self.line_count.configure(cursor='hand2'))
        self.line_count.bind('<Leave>', lambda event: self.line_count.configure(cursor=''))

        # Set the first number on the line counter and start to update the view
        update_line_view()
        self.update_line_count()


    def update_line_count(self, event=None):
        '''Updates the content of the line counter widget with line numbers.'''

        line_count = int(self.textbox.index('end-1c').split('.')[0])        # Get the number of lines in the textbox
        line_numbers = '\n'.join(str(i) for i in range(1, line_count + 1))  # Generate line numbers
        self.line_count.configure(state='normal')                           # Make text editable
        self.line_count.delete(1.0, tk.END)                                 # Clear previous content
        self.line_count.insert(1.0, line_numbers)                           # Insert new line numbers
        self.line_count.configure(state='disabled')                         # Make text disabled again
        self.line_count.configure(width=35+7*math.floor(math.log10(int(line_numbers.splitlines()[-1]))))  # Sets an appropriate width for the frame

        # Remove existing breakpoints
        self.line_count.tag_remove("breakpoint", '1.0', tk.END)

        # Adding new breakpoints
        for line_number in self.break_list:
            start_index = f"{line_number}.0"  # Calculate the index of the start of the line
            end_index = f"{line_number}.end"  # Calculate the index of the end of the line
            self.line_count.tag_add('breakpoint', start_index, end_index)  # Add the 'breakpoint' tag to highlight the line


    def highlight_syntax(self, event=None, errors=[], next_line:int=-1, breakpoint:int=-1):
        '''Update syntax highlighting.'''

        # Define patterns and corresponding tags
        patterns = {
            ' R': 'Register', ' r': 'register',
            '[\\[\\]]': 'bracket', ',': 'comma',
            '#': 'hash', ';': 'comment',
            'BNE ': 'label', 'bne ': 'label',
            'BEQ ': 'label', 'beq ': 'label',
            'BGE ': 'label', 'bge ': 'label',
            'BLT ': 'label', 'blt ': 'label',
            'BGT ': 'label', 'bgt ': 'label',
            'BLE ': 'label', 'ble ': 'label',
            'B ': 'label', 'b ': 'label'}

        # Remove existing tags
        for tag in patterns.values():
            self.textbox.tag_remove(tag, '1.0', tk.END)

        # Looking for labels

        index = '1.0'
        while True:
            index = self.textbox.search(':', index, tk.END)
            if not index:
                break
            # Tag the text before the semicolon
            start_index = self.textbox.index(f'{index} linestart')
            end_index = self.textbox.index(f'{index}+1c')
            self.textbox.tag_add('label', start_index, end_index)
            index = f'{index}+1c'

        # Colors for the rest of the syntax

        # Iterate through the patterns and tag the text accordingly
        for pattern, tag in patterns.items():
            start_index = '1.0'
            while True:
                start_index = self.textbox.search(pattern, start_index, tk.END, regexp=True)
                if not start_index:
                    break

                # Compute end_index based on the pattern
                if pattern == ',' or pattern == '[\\[\\]]':                                   # tags of length 1
                    end_index = self.textbox.index(f'{start_index}+1c')
                elif pattern == 'b ' or pattern == 'B ':
                    start_index = self.textbox.index(f'{start_index} +2c')                    # Short loops 'B'
                    end_index = self.textbox.index(f'{start_index} lineend')
                elif pattern == ' R' or pattern == ' r' or pattern == '#' or pattern == ';':  # tags of length > 1
                    end_index = self.textbox.index(f'{start_index} lineend')
                else:
                    start_index = self.textbox.index(f'{start_index} +4c')                    # Long Loops 'BXX'
                    end_index = self.textbox.index(f'{start_index} lineend')

                # Tag and jump to next character
                self.textbox.tag_add(tag, start_index, end_index)
                start_index = f'{end_index}+1c'

        # Error highlight
        self.textbox.tag_remove('ERROR', '1.0', tk.END)
        for e in errors:
            start_index = f'{e}.0'
            end_index = f'{e}.end'
            self.textbox.tag_add('ERROR', start_index, end_index)

        # Highlighting the next line to execute in step-by-step
        self.textbox.tag_remove('next_line', '1.0', tk.END)
        if next_line > 0:
            start_index = f'{next_line}.0'
            end_index = f'{next_line}.end'
            self.textbox.tag_add('next_line', start_index, end_index)

        # Highlighting the line were execution stopped
        self.textbox.tag_remove('breakline', '1.0', tk.END)
        if breakpoint > 0:
            start_index = f'{breakpoint}.0'
            end_index = f'{breakpoint}.end'
            self.textbox.tag_add('breakline', start_index, end_index)


    def correct_line(self, line_number: int):
        '''Computes the real line pointed by 'Error' or 'Execute' from the simulator and the empty lines in the ASM window.'''

        content = self.get_text_content().split('\n')  # Get the content of the text box and split it into lines
        n = 0
        real = 0

        for line in content:
            line = line.split(';')[0]  # Ignore comments
            n += (1 if line.strip() or line.find(':')!=-1 else 0)
            real += 1
            if n == line_number:  # Check if we reached the desired line number
                return real

        # If the desired line number is not found
        return -1


    def get_text_content(self):
        '''Gets the content of the text box.'''
        return self.textbox.get('1.0', tk.END)


    def delete_content(self):
        '''Deletes the content of the text box.'''
        return self.textbox.delete('1.0', tk.END)
    

    def insert_content(self, content):
        '''Inserts the content in the text box.'''
        return self.textbox.insert(tk.END, content)
    

    def get_breakpoints(self):
        '''Gives the list of breakpoints.'''
        return self.break_list








# ---------- Debugger Window ---------- #

class DebuggerWindow(ctk.CTkFrame):
    '''Contains all the frames and functions linked to the debugger area.'''

    def __init__(self, master):
        super().__init__(master)

        def update_line_numbers(event=None):
            '''Updates the view of the line counter to sync it with the textbox.'''

            textbox_scroll_fraction = self.textbox.yview()[0]      # Get the current vertical scrollbar position of the textbox
            self.line_count.yview_moveto(textbox_scroll_fraction)  # Set the vertical scrollbar position of the line counter to match the textbox
            self.after(10, update_line_numbers)                    # Schedule the function to run again after 10 milliseconds


        self.frame = ctk.CTkFrame(self, corner_radius=0)                                # Object Frame
        self.frame.pack(side='top', fill='both', expand=True)
        self.title = ctk.CTkLabel(self.frame, text='Debugger', bg_color='transparent')  # Title
        self.title.pack(side='top', fill='x')
        self.textbox_frame = ctk.CTkFrame(self.frame, corner_radius=0)                         # Frame containing the ASM window and the line numbers
        self.textbox_frame.pack(side='top', fill='both', expand=True)
        self.line_count = ctk.CTkTextbox(self.textbox_frame, width=20, text_color='#C0C0C0', fg_color='#404040', scrollbar_button_hover_color='#404040', scrollbar_button_color='#404040')
        self.line_count.pack(side='left', fill='both', expand=False)
        self.textbox = ctk.CTkTextbox(self.textbox_frame)                                       # Debugger text box
        self.textbox.pack(side='right', fill='both', expand=True)
        self.textbox.configure(state='disabled')

        # Set the first number on the line counter and start to update the view
        update_line_numbers()
        self.update_line_count()
    

    def delete_content(self):
        '''Deletes the content of the text box.'''

        self.textbox.configure(state='normal')
        self.textbox.delete('1.0', tk.END)
        self.textbox.configure(state='disabled', text_color='black')
    

    def insert_content(self, content:str, color='silver'):
        '''Inserts the content in the text box with specified color.'''

        self.textbox.configure(state='normal')
        self.textbox.insert(tk.END, content)
        self.textbox.configure(state='disabled', text_color=color)


    def update_line_count(self, event=None):
        '''Updates the content of the line counter widget with line numbers.'''

        line_count = int(self.textbox.index('end-1c').split('.')[0])        # Get the number of lines in the textbox
        line_numbers = '\n'.join(str(i) for i in range(1, line_count + 1))  # Generate line numbers
        self.line_count.configure(state='normal')                           # Make text editable
        self.line_count.delete(1.0, tk.END)                                 # Clear previous content
        self.line_count.insert(1.0, line_numbers)                           # Insert new line numbers
        self.line_count.configure(state='disabled')                         # Make text disabled again
        self.line_count.configure(width=35+7*math.floor(math.log10(int(line_numbers.splitlines()[-1]))))  # Sets an appropriate width for the frame








# ---------- Register Window ---------- #

class RegisterWindow(ctk.CTkFrame):
    '''Contains all the frames and functions linked to the Registers area, and the step counter'''

    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(self, corner_radius=0)  # Object Frame
        self.frame.pack(side='top', fill='both', expand=True)

        # Step Counter
        self.step_counter_title = ctk.CTkLabel(self.frame, text='Step Counter', bg_color='transparent', padx=50)    # Title
        self.step_counter_title.pack(side='top', fill='x')
        self.step_counter_frame = ctk.CTkFrame(self.frame, corner_radius=0)                                         # Sub-frame of the counter
        self.step_counter_frame.pack(side='top', fill='x')
        self.step_counter_label = ctk.CTkLabel(self.step_counter_frame, text='Step:', padx=5, pady=30, anchor='w')  # Label 'Step:'
        self.step_counter_label.pack(side='left')
        self.step_counter_value = ctk.CTkLabel(self.step_counter_frame, text='0', padx=5, pady=30, anchor='w')      # Value
        self.step_counter_value.pack(side='left')

        # Register Frame
        self.title = ctk.CTkLabel(self.frame, text='Registers', bg_color='transparent')  # Title
        self.title.pack(side='top', fill='x')
        self.sub_frame = ctk.CTkFrame(self.frame, corner_radius=0, width=100)            # Sub-frame of the registers
        self.sub_frame.pack(side='top', fill='both')

        # Storing register values
        self.value_labels = []

        # Create data entry widgets for Register 0 to 7
        for i in range(8):
            self.register_label = ctk.CTkLabel(self.sub_frame, text=f'R{i}:', padx=5, pady=2, anchor='w')  # Labels 'RX'
            self.register_label.grid(row=i, column=0, sticky='nsew')
            self.value_label = ctk.CTkLabel(self.sub_frame, text='0', padx=5, pady=2, anchor='w')          # Values
            self.value_label.grid(row=i, column=1, sticky='nsew')
            self.value_labels.append(self.value_label)

        # For NZVC
        self.register_label = ctk.CTkLabel(self.sub_frame, text='NZVC:', padx=5, pady=2, anchor='w')  # Labels 'NZVC'
        self.register_label.grid(row=8, column=0, sticky='nsew')
        self.value_label = ctk.CTkLabel(self.sub_frame, text='0000', padx=5, pady=2, anchor='w')      # Value
        self.value_label.grid(row=8, column=1, sticky='nsew')
        self.value_labels.append(self.value_label)

        # Configure grid weights for resizing
        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.grid_columnconfigure(j, weight=1)

        # Hex-Dec button
        self.button = ctk.CTkButton(self.frame, text='Switch to Hexa', command=self.change_format)
        self.button.pack(side='top')
        self.display = 0  # Variable to keep track of the mode


    def set_register_values(self, index:int, value:str):
        '''Set register values using a list.'''

        if self.display == 0:  # in dec
            self.value_labels[index].configure(text=value)

        else:  # in hex
            self.change_format()
            self.value_labels[index].configure(text=value)
            self.change_format()


    def change_format(self):
        '''Change the format of values to hexadecimal.'''

        if self.display == 0:  # in dec
            for i, label in enumerate(self.value_labels):
                decimal_value = int(label.cget('text'))                                       # Retrieving the value
                hex_value = '0x'+format(decimal_value, '08x') if i<8 else label.cget('text')  # Changing the format
                label.configure(text=hex_value)
                self.display = 1
                self.button.configure(text='Switch to Dec')

        else:  # in hex
            for i, label in enumerate(self.value_labels):
                hex_value = label.cget('text')                                         # Retrieving the value
                decimal_value = int(hex_value[2:], 16) if i<8 else label.cget('text')  # Changing the format
                label.configure(text=str(decimal_value))
                self.display = 0
                self.button.configure(text='Switch to Hexa')


    def set_step(self, value:int):
        '''Changes the step number displayed.'''
        self.step_counter_value.configure(text=str(value))








# ---------- Memory Arrays and Binary ---------- #

class MemAndBin(ctk.CTkTabview):
    '''Contains all the frames and functions linked to the memory and binary tabs.\n
       This includes the Code memory (ROM), User memory (RAM), and Binary window with the bitstream.'''

    def __init__(self, master):
        super().__init__(master)

        # Tabs
        self.add('Code Memory')
        self.add('User Memory')
        self.add('Binary')

        # ---- Code Memory ----
        
        self.code_memory = ctk.CTkFrame(master=self.tab('Code Memory'))
        self.code_memory.pack(expand=True, fill='both')
 
        # Code memory array
        self.code_headers = ['Adress', 'Value', 'Instruction']
        self.code_tree = tk.ttk.Treeview(self.code_memory, columns=self.code_headers, show='headings')
        self.code_tree.tag_configure('even_row', background='#202020', foreground='lightcyan')  # Even row style
        self.code_tree.tag_configure('odd_row', background='#101010', foreground='lightcyan')   # Odd row style

        for header in self.code_headers:
            self.code_tree.heading(header, text=header)
            self.code_tree.column(header, anchor='center', width=100)

        # Filling the code treeview
        for i in range(2048):
            address = '0x'+format(i*2+134217736, '08x')
            hex_value = '0x0000'
            instruction = ''
            tags = ('even_row', 'odd_row')[i % 2 == 1]
            self.code_tree.insert('', 'end', values=(address, hex_value, instruction), tags=(tags,))

        # Vertical scrollbar
        self.code_scrollbar = ctk.CTkScrollbar(self.code_memory, orientation='vertical', command=self.code_tree.yview)
        self.code_tree.configure(yscrollcommand=self.code_scrollbar.set)
        self.code_tree.pack(side='left', fill='both', expand=True)  # Pack components
        self.code_scrollbar.pack(side='right', fill='y')

        # ---- User Memory ----

        self.user_memory = ctk.CTkFrame(master=self.tab('User Memory'))
        self.user_memory.pack(expand=True, fill='both')

        # User memory array
        user_headers = ['Adress', 'Value']
        self.user_tree = tk.ttk.Treeview(self.user_memory, columns=user_headers, show='headings')
        self.user_tree.tag_configure('even_row', background='#202020', foreground='lightcyan')  # Even row style
        self.user_tree.tag_configure('odd_row', background='#101010', foreground='lightcyan')   # Odd row style

        for header in user_headers:
            self.user_tree.heading(header, text=header) 
            self.user_tree.column(header, anchor='center', width=100)

        # Filling the user treeview
        for i in range(2048):
            address = '0x'+format(i*4+536870912, '08x')
            hex_value = '0x00000000'
            tags = ('even_row', 'odd_row')[i % 2 == 1]
            self.user_tree.insert('', 'end', values=(address, hex_value), tags=(tags,))

        # Vertical scrollbar
        self.user_scrollbar = ctk.CTkScrollbar(self.user_memory, orientation='vertical', command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=self.user_scrollbar.set)
        self.user_tree.pack(side='left', fill='both', expand=True)  # Pack components
        self.user_scrollbar.pack(side='right', fill='y')

        # ---- Binary window ----

        self.binary = ctk.CTkFrame(master=self.tab('Binary'))                              # Frame
        self.binary.pack(expand=True, fill='both')
        self.bin_title = ctk.CTkLabel(self.binary, text='Binary', bg_color='transparent')  # Title
        self.bin_title.pack(side='top', fill='x')
        self.bin_textbox = ctk.CTkTextbox(self.binary)                                     # Text box
        self.bin_textbox.pack(side='top', fill='both', expand=True)
        self.bin_textbox.configure(state='disabled')


    def code_mem_set(self, index:str, value:str='0', instruction:str=''):
        '''Set values for a chosen line in the treeview.'''

        self.item_id = self.code_tree.get_children()[int(index)]  # Get the item ID based on the index
        self.code_tree.item(self.item_id, values=('0x'+format(index*2+134217736, '08x'), '0x'+format(int(value, 2), '04x'), instruction))

    
    def user_mem_set(self, index:str, value:int=0):
        '''Set values for a chosen line in the treeview.'''

        self.item_id = self.user_tree.get_children()[int(index[2:], 16)//4-134217728]  # Get the item ID based on the index
        self.user_tree.item(self.item_id, values=('0x'+format((int(index[2:], 16)-536870912)+536870912, '08x'), '0x'+format(value, '08x')))


    def delete_bin(self):
        '''Deletes the content of the text box.'''

        self.bin_textbox.configure(state='normal')
        self.bin_textbox.delete('1.0', tk.END)
        self.bin_textbox.configure(state='disabled')
    

    def insert_bin(self, content:str):
        '''Inserts the content in the text box.'''
        
        self.bin_textbox.configure(state='normal')
        self.bin_textbox.insert(tk.END, content)
        self.bin_textbox.configure(state='disabled')
  







# ---------- Pipeline window ---------- #

class PipelineWindow(ctk.CTkFrame):
    '''Contains all the frames and functions linked to the pipeline.'''

    def __init__(self, master):
        super().__init__(master)

        pip_headers = ['Fetch', 'Decode', 'Execute']

        # Create header labels on the left
        for i, header in enumerate(pip_headers):
            self.header_label = ctk.CTkLabel(self, text=header, padx=5, pady=2, anchor='w')
            self.header_label.grid(row=i, column=0, sticky='nsew')

        # Create data entry widgets on the right
        for i in range(3):
            for j in range(20):
                self.entry = ctk.CTkEntry(self, state='readonly', width=4)
                self.entry.insert(0, '')
                self.entry.grid(row=i, column=j + 1, sticky='nsew')

        # Configure grid weights for resizing
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        for j in range(21):
            self.grid_columnconfigure(j, weight=1)


    def get_cell(self, row:int, col:int):
        '''Get the value in the specified cell.'''

        if 0 <= row <= 2 and 1 <= col <= 20:
            entry_widget = self.grid_slaves(row=row, column=col)[0]
            return entry_widget.get(), entry_widget.cget('fg_color')
        else:
            return None


    def set_cell(self, row:int, col:int, value:str, color:str=None):
        '''Set the value in the specified cell.'''
        
        if 0 <= row <= 2 and 1 <= col <= 20:
            # Fetch the list of widgets at the specified row and column
            slaves = self.grid_slaves(row=row, column=col)
            if slaves:
                entry_widget = slaves[0]
                entry_widget.configure(state='normal')  # Make editable temporarily
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, value)
                if color:
                    entry_widget.configure(fg_color=color)
                entry_widget.configure(state='readonly')  # Make readonly again


    def iter_pip(self, value:str, color:str=None):
        '''Shifts the whole pipeline on the right and creates a new FDE column on the left.'''

        # Shift on the right
        for i in range(3):
            for j in range(19):
                self.prev = self.get_cell(i, 19-j)
                self.set_cell(i, 20-j, self.prev[0], self.prev[1])

        # Add the two old instr in the new column
        self.prev = self.get_cell(1, 1)
        self.set_cell(2, 1, self.prev[0], self.prev[1])
        self.prev = self.get_cell(0, 1)
        self.set_cell(1, 1, self.prev[0], self.prev[1])

        # Add the new instr in the new column
        if value == '':
            self.set_cell(0, 1, value)
        else:
            # Assign a new color for the instruction
            if color:
                new_color = color
            else:
                new_color = self.generate_random_color()
                self.set_cell(0, 1, value, new_color)

    
    def generate_random_color(self):
        '''Generate a random hexadecimal color code.'''
        return '#{:02x}'.format(random.randint(0x40, 0x70))+'{:02x}'.format(random.randint(0x40, 0x70))+'{:02x}'.format(random.randint(0x40, 0x70))








# ---------- Toolbar ---------- #

class Toolbar(ctk.CTkFrame):
    '''Contains all the buttons and corresponding functions from the toolbar at the top of the screen.\n
       The classes and function of the toolbar are located in the FileMenu class and the next ones. '''

    def __init__(self, master, asm_window, debugger_window, register_window, mem_and_bin, pipeline_window):
        super().__init__(master)

        def download_code():
            ''''''


        def connect_board():
            ''''''


        def reset():
            '''Resets the values in registers, pipeline, binary, and memory arrays.'''

            # Updates button states
            master.toolbar.assemble_button.configure(self, fg_color='gray', state='disabled', text='Assemble')
            master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
            master.toolbar.runsbs_button.configure(self, fg_color='gray', state='disabled', text='Run Step By Step', hover_color='darkgreen')
            master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
            master.toolbar.reset_button.configure(self, fg_color='gray', state='disabled')
            self.state = 0

            # Empties debugger
            master.debugger_window.delete_content()
            debugger_window.update_line_count()  # Update the line count in the Debugger

            # Empties registers
            for i in range(8):
                register_window.set_register_values(i, 0)
            register_window.set_register_values(8, '0000')

            # Resets step sounter
            register_window.set_step(0)

            # Empties User Memory
            for i in range(2048):
                mem_and_bin.user_mem_set('0x'+format(4*i+536870912, '08x'))

            # Empties Code Memory
            for i in range(2048):
                mem_and_bin.code_mem_set(i)

            # Empties Bit window
            mem_and_bin.delete_bin()

            # Empties the pipeline
            for i in range(3):
                for j in range(20):
                    pipeline_window.set_cell(i, j+1, '', '#343638')

            # Updates button states
            master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal', text='Assemble')
            master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
            master.toolbar.runsbs_button.configure(self, fg_color='gray', state='disabled', text='Run Step By Step', hover_color='darkgreen')
            master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
            master.toolbar.reset_button.configure(self, fg_color='forestgreen', state='normal')
            self.state = 0

            # Highlight update
            asm_window.highlight_syntax()


        def stop():
            '''Stops the Step-by-step execution.'''

            # Stop the runsbs
            master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
            master.toolbar.runsbs_button.configure(self, fg_color='gray', text='Run Step By Step', state='disabled', hover_color='darkgreen')
            master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
            master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal')
            self.state = 0

            # Display success message in the Debugger
            debugger_window.insert_content('Execution Aborted\n', 'lime')
            debugger_window.update_line_count()  # Update the line count in the Debugger

            # Resets the next line highlighting
            asm_window.highlight_syntax()


        def run_step_by_step():
            '''Launches the step y step execution of the code.'''

            # Updates button states
            master.toolbar.run_button.configure(self, text='Resume')
            master.toolbar.stop_button.configure(self, fg_color='firebrick', state='normal')

            if self.state == 1:
                # starts the runsbs
                master.toolbar.runsbs_button.configure(self, fg_color='forestgreen', text='Step->')
                self.state = 2
            else:
                register_window.set_step(max(self.state-3, 0))

                # Executes a step
                if self.state != len(master.toolbar.line_update) + 2:

                    # Update the Pipeline
                    if master.toolbar.line_update[self.state - 2] == -1:
                        pipeline_window.iter_pip('---')
                    elif self.state < len(master.toolbar.line_update) + 2 and master.toolbar.split_instructions[master.toolbar.line_update[self.state - 2]] != '':
                        pipeline_window.iter_pip(master.toolbar.split_instructions[master.toolbar.line_update[self.state - 2]][:3])
                
                    # Wait 2 more steps because instructions must go through the pipeline before being executed
                    if self.state > 3:

                        # Update the Register
                        if master.toolbar.register_update[self.state - 4] != []:
                            register_window.set_register_values(master.toolbar.register_update[self.state - 4][0], master.toolbar.register_update[self.state - 4][1])
                        # Update the User Mem
                        if master.toolbar.memory_update[self.state - 4] != []:
                            mem_and_bin.user_mem_set('0x'+format(master.toolbar.memory_update[self.state - 4][0], '08x'), master.toolbar.memory_update[self.state - 4][1])

                    # Update the state
                    self.state += 1

                    # Higlight the next line in ASM window
                    next_line = asm_window.correct_line(master.toolbar.line_update[self.state - 4] + 1)  # Corrects for eventual empty lines
                    asm_window.highlight_syntax(None, [], next_line)

                # End of the step-by-step
                
                else:
                    # Updates button states
                    master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
                    master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
                    master.toolbar.runsbs_button.configure(self, fg_color='gray', state='disabled', text='Run Step By Step', hover_color='darkgreen')
                    master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal')
                    self.state = 0

                    # Display success message in the Debugger
                    debugger_window.insert_content('Run Finished\n', 'lime')
                    debugger_window.update_line_count()  # Update the line count in the Debugger


        def run():
            '''Runs the code in one go.\n
               Also allows to resume after a runsbs.'''

            # Get into the state of running
            if self.state < 2:
                self.state = 2  # Corresponds to 0 executions (1decode or 2fetch)

            # Check if there are breakpoints
            breaks = asm_window.get_breakpoints().copy()


            # Get all the breakpoints taking loops into account
            real_breaks = []
            for i,e in enumerate(master.toolbar.line_update):
                if asm_window.correct_line(e) in breaks:
                    real_breaks.append(i)

            # Run until breakpoint
            while real_breaks != [] and real_breaks[0] < self.state - 2:  # Ignore all breakpoints before current step
                real_breaks.pop(0)
            if real_breaks != []:
                while self.state - 3 < real_breaks[0]:  # Gets to the next breakpoint
                    run_step_by_step()
                asm_window.highlight_syntax(None, [], -1, breaks[0])
                debugger_window.insert_content('Breakpoint: Line %d - Step %d (%s)\n\n' % (breaks[0], real_breaks[0], master.toolbar.split_instructions[master.toolbar.line_update[self.state - 4]]), 'yellow')
                debugger_window.update_line_count()  # Update the line count in the Debugger
                

            # No breakpoints -> run everything
            else:

                # Update button states
                master.toolbar.run_button.configure(self, fg_color='gray', state='disabled', text='Run')
                master.toolbar.runsbs_button.configure(self, fg_color='gray', state='disabled', text='Run Step By Step', hover_color='darkgreen')
                master.toolbar.stop_button.configure(self, fg_color='gray', state='disabled')
                master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal')

                # Update register values
                register_window.set_step(len(master.toolbar.line_update) - 1)
                for i in range(8):
                    register_window.set_register_values(i, virtual_register[i])
                for e in master.toolbar.register_update:
                    if e != [] and e[0] == 8:
                        nzvc = e[1]
                        register_window.set_register_values(8, nzvc)

                # Update User RAM values
                for i in range(0, len(virtual_memory), 2):
                    mem_and_bin.user_mem_set(virtual_memory[i], virtual_memory[i+1])

                # Updates the Pipeline
                for e in master.toolbar.line_update[max(-24, self.state - len(master.toolbar.line_update) - 2):]:
                    if e == -1:
                        pipeline_window.iter_pip('---')
                    else:
                        pipeline_window.iter_pip(master.toolbar.split_instructions[e][:3])
                self.state = 0

                # Display success message in the Debugger
                debugger_window.insert_content('Run Finished\n', 'lime')
                debugger_window.update_line_count()  # Update the line count in the Debugger

                # Resets the next line highlighting
                asm_window.highlight_syntax()


        def assemble():
            '''Assembles the code.'''

            # Cleaning
            reset()
            master.toolbar.assemble_button.configure(self, fg_color='gray', state='disabled')
            self.state = 1

            # Fetching the code
            code = asm_window.get_text_content()
        
            # Check if code is empty
            if code == '\n':
                # Funny text variations for when user tries to assemble empty code
                variations = ['sipping a coconut', 'catching some rays', 'in a hammock', 'on a beach', 'snorkeling', 'in a tropical paradise', 'surfing the clouds',
                'on a spa retreat', 'napping in a hammock', 'practicing mindfulness', 'doing yoga', 'enjoying a siesta', 'on a cosmic cruise', 'in a Zen garden',
                'sunbathing', 'in a day spa', 'on a coffee break', 'chilling in a hammock', 'vacationing', 'on a beach', 'gone', 'too short', 'transparent', 'too small']
                random_variation = random.choice(variations)

                debugger_window.insert_content("Assembling air? Your code's "+random_variation+'.', 'blue')
                master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal')
                self.state = 0

            else:
                master.toolbar.split_instructions, master.toolbar.bitstream, master.toolbar.register_update, master.toolbar.line_update, master.toolbar.memory_update, master.toolbar.error = instruction_translation(code)

                # Check if there are errors
                if master.toolbar.error != []:
                    master.toolbar.assemble_button.configure(self, fg_color='forestgreen', state='normal')
                    self.state = 0

                    # Display error in debugger
                    lines = []
                    for i in range(len(master.toolbar.error)//2):
                        error_line = asm_window.correct_line(master.toolbar.error[2*i+1]+1)  # Corrects for eventual empty lines
                        debugger_window.insert_content('%s at line %d\n' % (master.toolbar.error[2*i], error_line), 'red')
                        lines.append(error_line)

                    # Highlight lines with errors
                    asm_window.highlight_syntax(None, lines)

                else:
                    # Fills the Code RAM array and the bitstream frame
                    if len(master.toolbar.bitstream) != 0:
                        offset = 0
                        for l in range(len(master.toolbar.split_instructions)-1):
                            if master.toolbar.split_instructions[l] != '' and master.toolbar.split_instructions[l].find(':') == -1:

                                # Display the instruction in the Code Memory
                                mem_and_bin.code_mem_set(l - offset, master.toolbar.bitstream[l], master.toolbar.split_instructions[l])

                                # Display the instruction in the binary window
                                mem_and_bin.insert_bin(master.toolbar.bitstream[l] + '\n')
                            else:
                                offset += 1
                        mem_and_bin.code_mem_set(l - offset + 1, master.toolbar.bitstream[l+1], master.toolbar.split_instructions[l+1])

                # Display success message in debugger
                debugger_window.insert_content('Assembly complete\n\n', 'lime')
                
                # Enables buttons Run and RSBS
                master.toolbar.run_button.configure(self, fg_color='forestgreen', state='normal')
                master.toolbar.runsbs_button.configure(self, fg_color='forestgreen', state='normal')

            # Update the line count in the Debugger
            debugger_window.update_line_count()
        

        self.download_button = ctk.CTkButton(self, text='Download Code', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='gray', hover_color='darkgreen', state='disabled', command=download_code)
        self.download_button.pack(side='right', padx=5)
        self.connect_button = ctk.CTkButton(self, text='Connect Board', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='forestgreen', hover_color='darkgreen', command=connect_board)
        self.connect_button.pack(side='right')
        self.reset_button = ctk.CTkButton(self, text='Reset', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='forestgreen', hover_color='darkgreen', command=reset)
        self.reset_button.pack(side='right', padx=5)
        self.stop_button = ctk.CTkButton(self, text='STOP', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='gray', hover_color='maroon', state='disabled', command=stop)
        self.stop_button.pack(side='right')
        self.runsbs_button = ctk.CTkButton(self, text='Run Step By Step', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='gray', hover_color='darkgreen', state='disabled', command=run_step_by_step)
        self.runsbs_button.pack(side='right', padx=5)
        self.run_button = ctk.CTkButton(self, text='Run', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='gray', hover_color='darkgreen', state='disabled', command=run)
        self.run_button.pack(side='right')
        self.assemble_button = ctk.CTkButton(self, text='Assemble', width=100, height=10, font=('Arial', 11), corner_radius=25, fg_color='forestgreen', hover_color='darkgreen', command=assemble)
        self.assemble_button.pack(side='right', padx=5)
        self.file_menu = FileMenu(self, asm_window)
        self.file_menu.pack(side='left')
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.pack(side='left')
        self.help_menu = HelpMenu(self)
        self.help_menu.pack(side='left')

        # Variable keeping track of the running state (assembled? runsbs? run? which step?)
        self.state = 0

        self.split_instruction, self.line_instruction, self.bitstream, self.register_update, self.line_update, self.memory_update, self.error = [], [], [], [], [], [], []








# ---------- Menus ---------- #

class FileMenu(ctk.CTkFrame):
    '''Calls specific classes to create the menus in the top left of the toolbar.'''

    def __init__(self, master, asm_window):
        super().__init__(master)

        def save_as():
            '''Opens a dialog window to save the current code into a new file.\n
               It wont save it automatically like the 'save' function does.'''

            global file_path

            file_path = tk.filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
            if file_path:
                with open(file_path, 'w') as file:
                    saved_code = asm_window.get_text_content()  # Gets the code from the text area
                    file.write(saved_code)
                    asm_window.highlight_syntax()


        def new_file():
            '''Creates a new blank code page. If code is present in the text window, asks if the user wants to save the current code.\n
               If yes: Calls the 'save_as' function.\n
               If not: The current code will be lost !'''
    
            global file_path

            # Checks if the asm_zone contains text
            if asm_window.get_text_content().strip():
                # Asks the user if they want to save the current content before creating a new file
                response = tk.messagebox.askyesno('Save Before Creating a New File?', 'Do you want to save the current code before creating a blank page?')
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
                response = tk.messagebox.askyesno('Save Before Import', 'Do you want to save the current code before importing?')
                if response:
                    save_as()

            # Open the file dialog to import code
            file_path = tk.filedialog.askopenfilename(filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
            if file_path:
                with open(file_path, 'r') as file:
                    imported_code = file.read()

                    # Pastes imported code into the text area
                    asm_window.delete_content()               # Clears the text area content
                    asm_window.insert_content(imported_code)  # Pastes the code
                    asm_window.highlight_syntax()             # Updates the colors after import
                    asm_window.update_line_count()            # Updates the line counter after import


        def save():
            '''Overwrites the current save file, or opens a dialog window to create a one.'''

            global file_path

            # If the file hasn't been saved yet, asks the user where to save it
            if file_path is None:
                save_as()
 
            # If the user selected a file location, saves the content of the text area to the file
            if file_path:
                with open(file_path, 'w') as file:
                    saved_code = asm_window.get_text_content()  # Gets the code from the text area
                    file.write(saved_code)
                    asm_window.highlight_syntax()


        # File menu button
        self = tk.ttk.Menubutton(self, text='File', direction='below')
        self.pack(side='left')

        # Dropdown menu for the File button
        self.menu = tk.Menu(self, tearoff=0)
        self['menu'] = self.menu  # Assign the menu to the button

        # Add items to the File menu
        self.menu.add_command(label='New File', command=new_file)
        self.menu.add_command(label='Import', command=import_code)
        self.menu.add_separator()
        self.menu.add_command(label='Save', command=save)
        self.menu.add_command(label='Save As', command=save_as)
        







class SettingsMenu(ctk.CTkFrame):
    '''Settings menu class.'''

    def __init__(self, master):
        super().__init__(master)

        # Settings menu button
        self = tk.ttk.Menubutton(self, text='Settings', direction='below')
        self.pack(side='left')

        # Dropdown menu for the File button
        self.menu = tk.Menu(self, tearoff=0)
        self['menu'] = self.menu  # Assign the menu to the button

        # Add items to the File menu
        self.menu.add_command(label='Dark mode', command=master.master.theme_toggle_dark)
        self.menu.add_command(label='Light mode', command=master.master.theme_toggle_light)








class HelpMenu(ctk.CTkFrame):
    '''Help menu class.'''

    def __init__(self, master):
        super().__init__(master)
    
        def help_lcm3_docu():
            '''Opens an online documentation of the LCM3 instructions.'''

            webbrowser.open_new('https://moodle.ensea.fr/pluginfile.php/24675/mod_resource/content/2/TD_uP_LCM3_1AB_2023-2024_v01_jeu.pdf')


        # Help menu button
        self = tk.ttk.Menubutton(self, text='Help', direction='below')  # Help menu button
        self.pack(side='left')

        # Dropdown menu for the Help Button
        self.menu = tk.Menu(self, tearoff=0)  # Help menu 'menu'
        self['menu'] = self.menu

        # Add items to the File menu
        self.menu.add_command(label='LCM3 DOC NOW HELP!!!', command=LCM3Documentation)
        self.menu.add_command(label='LCM3 Doc on Moodle', command=help_lcm3_docu)
        self.menu.add_separator()
        self.menu.add_command(label='This Simulator Documentation', command=SimulatorDocumentation)
        self.menu.add_separator()
        self.menu.add_command(label='ASM Code Examples', command=CodeExamples)








class CodeExamples(ctk.CTkToplevel):
    '''Contains the written documentation of ASM LCM3.'''

    def __init__(self):
        super().__init__()

        self.text = ('\n\n'+
        '------------------------ LMC3 Assembly Code Examples ------------------------\n\n\n\n'
        '; Multiplication function\n'
        '; Returns R0 = R1 * R2\n\n'
        'MULTIPLICATION:\n'
        '\tMOV R0, #0\t\t\t; Initialize the result at zero\n\n'
        'MUL_LOOP:\n'
        '\tCMP R2, #0\t\t\t; Check if R2 factor is nil\n'
        '\tBEQ MUL_DONE\t\t\t; If yes, break\n\n'
        '\tCMP R1, #0\t\t\t; Check if R1 factor is nil\n'
        '\tBEQ MUL_DONE\t\t\t; If yes, break\n\n'
        '\tADD R0, R0, R1\t\t\t; R0 = R0 + R1\n'
        '\tSUB  R2, R2, #1\t\t\t; Decrement the R2 factor\n'
        '\tCMP R2, #0\n'
        '\tBGE MUL_LOOP\t\t\t; Repeat if R2 >= 0\n\n'
        'MUL_DONE:\n\n\n'
        '------------------------------------------------------------------\n\n\n'
        '; Euclidian Division function\n'
        '; Returns R0 = R1 / R2\n'
        '; And R1 is the remaining (R0 * R2 + R1_out = R1_in)\n\n'
        'DIVISION:\n'
	    '\tCMP R2, #0\t\t\t; Check if R2 is zero\n'
	    '\tBEQ DIV_ERROR\t\t\t; If yes, error\n\n'
    	'\tMOV R0, #0\t\t\t; Initilize the output R0 at zero\n\n'
        'DIV_LOOP:\n'
	    '\tCMP R1, #0\t\t\t; Check if R1 is zero\n'
	    '\tBEQ DIV_DONE\t\t\t; if yes, get out of the loop and show R0 = 0\n\n'
	    '\tCMP R1, R2\t\t\t; Check if R1 smaller than R2\n'
	    '\tBLT DIV_ERROR\t\t\t; if so, error\n\n'
	    '\tSUB R1, R1, R2\t\t\t; R1 - R2\n'
	    '\tADD R0, R0, #1\t\t\t; R0 + 1\n\n'
	    '\tB DIV_LOOP\t\t\t; Repeat the loop\n\n'
        'DIV_DONE:\n'
        'DIV_ERROR:\n\n\n'
        '------------------------------------------------------------------\n\n\n'
        '; PUSH (R3)\n\n'
        '; R0 <- 0x20000004 (adress pointer)\n'
        '; R2 <- 0x20000100 (size of the pile)\n'
        'MOV R0, #1\n'
        'LSL R0, R0, #29\n'
        'MOV R2, R0\n'
        'ADD R0, #4\n'
        'ADD R2, #0x80\n'
        'ADD R2, #0x80\n\n'
        'SHIFT_ALL:\n'
	    '\tLDR R1, [R0]\n'
	    '\tSUB  R0, R0, #4\n'
	    '\tSTR R1, [R0]\n'
	    '\tADD R0, #8\n'
	    '\tCMP R0, R2\n'
	    '\tBNE SHIFT_ALL\n\n'
        'STR R3, [R0]\n\n\n'
        '------------------------------------------------------------------\n\n\n'
        '; POP (R3)\n\n'
        '; R0 <- 0x20000100 (adress pointer)\n'
        '; R2 <- 0x20000000 (size of the pile)\n'
        'MOV R0, #1\n'
        'LSL R0, R0, #29\n'
        'MOV R2, R0\n'
        'ADD R0, #0x80\n'
        'ADD R0, #0x80\n\n'
        'LDR R3, [R0]\t\t; POP R3\n'
        'SUB  R0, R0, #4\n\n'
        'SHIFT_ALL:\n'
	    '\tLDR R1, [R0]\n'
	    '\tADD  R0, R0, #4\n'
	    '\tSTR R1, [R0]\n'
	    '\tSUB R0, #8\n'
	    '\tCMP R0, R2\n'
	    '\tBNE SHIFT_ALL\n'
        '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        self.title('LMC3 Assembly Code Examples')                                 # Title
        self.geometry('500x1000')
        self.frame = ctk.CTkFrame(self)                             # Frame
        self.frame.pack(fill='both', expand=True)
        self.text_widget = ctk.CTkTextbox(self.frame, wrap='word')  # Text box
        self.text_widget.pack(side='left', fill='both', expand=True)
        self.text_widget.insert(tk.END, self.text)
        self.text_widget.configure(state='disabled', font=('Helvetica',12))








class LCM3Documentation(ctk.CTkToplevel):
    '''Contains the written documentation of ASM LCM3.'''

    def __init__(self):
        super().__init__()

        self.text = ('\n\n'+
        '------------------------ LCM3 Instruction Set (alphabetic order) ------------------------\n\n\n\n'
        'Syntax\t\t\tOperation\t\t\tValues\t\t\tCode\n'
        '\t\t\t\t\t\t\t\t\t15   14   13   12   11   10    9     8     7     6     5     4     3     2     1     0\n\n'
        'ADD Rd,Rn,#imm3\t\t\tRd<=Rn+ZE(imm3)\t\t\t0≤imm3≤7\t\t\t 0     0     0     1     1     1     0   |      imm3     |        n         |         d\n'
        'ADD Rd,#imm8\t\t\tRd<=Rd+ZE(imm8)\t\t\t0≤imm8≤255\t\t\t 0     0     1     1     0   |        d         |           imm8 (unsigned)\n'
        'ADD Rd,Rn,Rm\t\t\tRd<=Rn+Rm\t\t\t\t\t\t 0     0     0     1     1     0     0   |        m         |        n         |         d\n'
        'AND Rd,Rm\t\t\tRd<=Rd AND Rm\t\t\t\t\t\t 0     1     0     0     0     0     0     0     0     0   |        m        |         d\n'
        "B label\t\t\tPC<=adr(label)\t\t\t-2^10≤imm11≤2^10-1\t\t\t 1     1     1     0     0   |         imm11 (Δi in 2's complt)\n"
        "BXX label\t\t\tif Z=0 then PC<=adr(label)\t\t\t-2^7≤imm8≤2^7-1\t\t\t 1     1     0     1   |     XX=cond      |           imm8 (Δi in 2's complt)\n"
        'CMP Rn,#imm8\t\t\tNZVC<=Rn-ZE(imm8)\t\t\t0≤imm8≤2^8-1\t\t\t 0     0     1     0     1   |        n         |           imm8 (unsigned)\n'
        'CMP Rd,Rm\t\t\tNZVC<=Rd-Rm\t\t\t\t\t\t 0     1     0     0     0     0     1     0     1     0   |        m        |         d\n'
        'EOR Rd,Rm\t\t\tRd<=Rd xor Rm\t\t\t\t\t\t 0     1     0     0     0     0     0     0     0     1   |        m        |         d\n'
        'LDR Rt,[Rn]\t\t\tRt<=M[align4(Rn)]\t\t\t\t\t\t 0     1     1     0     1     0     0     0     0     0   |        n         |          t\n'
        'LSL Rd,Rm,#imm5\t\t\tRd<=Rm<<imm5\t\t\t0≤imm5≤31\t\t\t 0     0     0     0     0   |             imm5            |        m        |         d\n'
        'MOV Rd,#imm8\t\t\tRd<=ZE(imm8)\t\t\t0≤imm8≤255\t\t\t 0     0     1     0     0   |        d         |           imm8 (unsigned)\n'
        'MOV Rd,Rm\t\t\tRd<=Rm\t\t\t\t\t\t 0     0     0     0     0     0     0     0     0     0   |        m        |         d\n'
        'STR Rt,[Rn]\t\t\tM[align4(Rn)]<=Rt\t\t\t\t\t\t 0     1     1     0     0     0     0     0     0     0   |        n         |          t\n'
        'SUB Rd,Rn,#imm3\t\t\t Rd<=Rn-ZE(imm3)\t\t\t0≤imm3≤7\t\t\t 0     0     0     1     1     1     1   |      imm3     |        n         |         d\n'
        'SUB Rd,#imm8\t\t\tRd<=Rd-ZE(imm8)\t\t\t0≤imm8≤255\t\t\t 0     0     1     1     1   |        d         |           imm8 (unsigned)\n'
        'SUB Rd,Rn,Rm\t\t\tRd<=Rn-Rm\t\t\t\t\t\t 0     0     0     1     1     0     1   |        m         |        n         |         d\n\n\n'
        'In "BXX label", XX : is a condition (if the condition is true then branch to label)'
        '\tXX=NE ↔ Z=0 (Not Equal)\t\t\t\t\t↔ cond=0001\n'
        '\tXX=EQ ↔ Z=1 (is EQual)\t\t\t\t\t↔ cond=0000\n'
        '\tXX=GE ↔ N=V (Greater or Equal)\t\t\t\t\t↔ cond=1010\n'
        '\tXX=LT ↔ N !=V (Lower Than)\t\t\t\t\t↔ cond=1011\n'
        '\tXX=GT ↔ Z=0 et N=V (Greater Than)\t\t\t\t\t↔ cond=1100\n'
        '\tXX=LE ↔ Z=1 ou N !=V (Less or equal)\t\t\t\t\t↔ cond=1101\n\n\n'
        'ZE: Zero Extend; extension of the value to 32 bits (unsigned)\n'
        'The variables n, d, m or imm3 are unsigned.\n'
        "Only one instruction modifies the flags NZVC here: it's 'CMP'.\n"
        'Mw[adr] is a word (32 bits) in memory at address adr.\n'
        'Remark : adr must be a multiple of 4: 0, 4, 8, 0xC, 0x10…\n'
        "The function align4(i)= (i/4)*4 : it's equivalent to clear the 2 LSBs.\n"
        '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        self.title('LCM3 Instruction Set')                          # Title
        self.geometry('900x800')
        self.frame = ctk.CTkFrame(self)                             # Frame
        self.frame.pack(fill='both', expand=True)
        self.text_widget = ctk.CTkTextbox(self.frame, wrap='word')  # Text box
        self.text_widget.pack(side='left', fill='both', expand=True)
        self.text_widget.insert(tk.END, self.text)
        self.text_widget.configure(state='disabled', font=('Helvetica',12))








class SimulatorDocumentation(ctk.CTkToplevel):
    '''Contains the written documentation of this simulator.'''

    def __init__(self):
        super().__init__()

        self.text = ('\n\n\n'+
        "------------------------ ENSEA's Python LCM3 Simulator ------------------------\n\n"
        '    Engineers :\n\n'
        '    APPOURCHAUX Léo, BITTAUD CANOEN Laël, GABORIEAU Cyprien, JIN Clémentine\n'
        '    LATRECHE Loubna, OULAD ALI Rym, XIANG Justine, YE Yumeng\n\n'
        '    Professors :\n\n'
        '    Mr. Kessal, Mr. Laroche, Mr. Monchal\n\n'
        '-------------------------------------------------------------------------------\n\n\n\n'
        "ENSEA's Python LCM3 Simulator Documentation\n\n"
        '1. Introduction\n'
        "    ENSEA's Python LCM3 Simulator is a tool that simulates the execution of programs "
        'written in LCM3 assembly language. This documentation will guide you through all the '
        'features and capabilities of the simulator.\n\n\n'
        '2. Interface Features\n'
        '    2.1 Buttons\n'
        '        The Buttons provides quick access to essential features.\n\n'
        '        File menu:\n'
        '            New File: Creates a new LCM3 code file.\n'
        '            Import: Imports LCM3 code from an external file.\n'
        '            Save: Saves the current file.\n'
        '            Save as: Saves the code to a new file or update the existing one.\n\n'
        '        Settings menu:\n'
        '            Dark mode: Toggles dark mode.\n'
        '            Light mode: Toggles light mode.\n\n'
        '        Help menu:\n'
        '            This Simulator Documentation: Opens this help window.\n'
        "            LCM3 Documentation: Tries to open the ASM LCM3 Doc on Moodle (if your professors didn't delete it). You need to be logged in to see it.\n\n"
        '        Assemble button: Assembles the code (compiles),\n'
        '                         displays syntax errors in the Debugger, displays the binary translation of your code in the Binary window.\n'
        '                         Also resets the Registers, the Memory, the Pipeline, the Debugger and the Binary window.\n\n'
        '        Run button: Runs your code in one go. Also alows you to Resume the execution if you had started a Run step-by-step previously.\n\n'
        '        Run Step-By-Step: Starts a line-by-line execution, then changes to Step, and executes a step when you press it again.\n\n'
        '        STOP: Stops the execution of the code.\n\n'
        '        Reset: Resets the simulator to its initial state. (Is called by the Assemble button)\n\n\n'
        '    2.2 ASM Code Window\n'
        '        In this frame, you can write your LCM3 assembly code. Each instruction must be on a separate line.\n\n\n'
        '    2.3 Debugger\n'
        '        In this frame, you have acces to a feedback on your code, eventual errors, and info about the execution of the simulation.\n\n\n'
        '    2.4 Registers\n'
        "        The register panel displays the current values of the simulator's registers.\n"
        '        You also have a step counter above, useful for debugging and performance assessement.\n'
        '        You can also change the display mode of the values between decimal and hexadecimal.\n\n\n'
        '    2.5 Code Memory tab\n'
        '        This tab shows where your code is saved on the board (the ROM).\n'
        "        You can see the addresses where each instruction is stored along with it's translation in hexadecimal.\n"
        '        As every instruction in the LCM3 is coded on 16 bits, and each memory address can contain 8 bits of information,\n'
        '        instructions are stored in every other address.\n\n\n'
        '    2.6 User Memory tab\n'
        '        This is the part of the memory you can access as a user (the RAM).\n'
        '        You can see where you store your values, and the values themselves.\n'
        '        As the values are stored on 32 bits, and each memory address can contain 8 bits of information,\n'
        '        instructions are stored every 4 addresses.\n\n\n'
        '    2.7 Binary tab\n'
        '        This tab simply displays the translation of your code into binary with the LCM3 convention.\n'
        '        What is displayed corresponds to the bitstream that would be uploaded into a board you would connect to the simulator.\n\n\n'
        '    2.8 Pipeline\n'
        '        The pipeline section illustrates the path of the instructions into the processor (Fetch, Decode, Execute) and the history.\n\n\n'
        '3. Using the Simulator\n'
        '    3.1 Writing LCM3 Code\n'
        '        Each instruction must be on a separate line.\n'
        '        You can use spaces, tabs and new lines at will to improve the visibility of your code.\n'
        "        HOW TO WRITE COMMENTS: Just put a semicolon ';' before your comment.\n\n\n"
        '    3.2 Running the Simulator\n'
        '        1 - ASSEMBLE YOUR CODE!\n\n'
        '        Step-By-Step execution:\n'
        '            2 - Click Run Step by Step to start the execution.\n'
        "            3 - Click Step to execute a step. Don't forget to watch the memory and registers ;)\n\n"
        '        Run in one go:\n'
        '            2bis - Just run the code.\n\n'
        '        You can reset stored values at anytime with the reset button.\n\n\n'
        '    3.3 Monitoring Execution\n'
        '        Check step counter\n'
        '        Check register values\n'
        '        Check the memory content\n'
        '        Next line to execute is highlighted in the ASM Code Window\n'
        '        Watch the path of the instructions in the pipeline\n\n\n'
        '4. Troubleshooting\n'
        '    4.1 Common Errors\n'
        '        - Invalid Syntax: CHECK THE SYNTAX of your LCM3 instructions!\n'
        '        - Undefined Labels: Ensure all labels are DEFINED before use.\n'
        '        - Repeated Labels: Ensure all labels are UNIQUE.\n'
        '        - Values out of range: CHECK THE LCM3, instructions have numbers limited in size\n'
        '                               Moreover you can only acces 0x20000000 to 0x80000000 in the user memory.\n\n\n'
        '    4.2 Debugging Tips\n'
        '        Errors will be highlighted in red\n'
        '        Check the Debugger window\n'
        '        Re-read your code\n'
        '        AND CHECK THE LCM3 SYNTAX!\n\n\n\n'
        '\t\t\t\tHave a nice time coding!\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        self.title("ENSEA's Python LCM3 Simulator - Documentation")  # Title
        self.geometry('1200x800')
        self.frame = ctk.CTkFrame(self)                              # Frame
        self.frame.pack(fill='both', expand=True)
        self.text_widget = ctk.CTkTextbox(self.frame, wrap='word')   # Text box
        self.text_widget.pack(side='left', fill='both', expand=True)
        self.text_widget.insert(tk.END, self.text)
        self.text_widget.configure(state='disabled', font=('Helvetica',12))








# ---------- Code ---------- #

app = EnseaSimulator()  # Calling the simulator
app.mainloop()          # Keeping it up


