# ASM IDE in Python for our VHDL - Programmed FPGA
## 1. Introduction
## 2. Software
### 2.1 Simulator
The simulator processes ASM code received from the UI as a string. Here's an overview of its functionalities:
#### 2.1.1 Global Structure
We transform the string into a data table where each element represents a string-type instruction.
#### 2.1.2 Text Slicing
We split the instructions based on the newline characters ('\n'). This process results in an array of instructions, making it easier to handle individual instructions for further processing.

Example:
```python
def line_jump(codeASM):
    split_instructions = []
    while codeASM.count('\n'):
        split_instructions.append(codeASM[0: codeASM.find('\n')])
        codeASM = codeASM[codeASM.find('\n') + 2::]
    return split_instructions
```

#### 2.1.3 Instruction Recognition
Since we're dealing with LCM3 instructions, we have a predefined set of instructions to recognize. We identify instructions by comparing the first few characters and categorize them accordingly.

#### 2.1.4 Resgister Recognition
Recognizing registers is important for the simulator's functionality. We extract information from instructions to identify which registers are being used.

#### 2.1.5 Numer-type Argument Recognition
This simulator also recognizes numerical arguments within instructions for further processing.

#### 2.1.6 Internal Register Simulation
Simulation of internal registers is performed to emulate the behaviour of registers during instruction execution.

#### 2.1.7 Internal Memory Simulation
Similarly, internal memory is carried out to simulate memory operations during execution.

#### 2.1.8 Handling Branching
We handle branching instructions by label recognition and manage jumps to specific lines in the code.

#### 2.1.9 Error Handling
This simulator has mechanisms to handle errors that lay occur during execution.

#### 2.2.0 Bitstream Generation
To facilitate further processing, the simulator generates a bitstream representing the processed ASM code.

### 2.2 Interface

#### 2.2.1 Introduction

The interface of the simulator provides an ergonomic platform to code in ASM. The goals are creating a visually appealing user interface, providing accurate syntax and error highlighting, and establishing an environment where users can learn the fundamental concepts of assembly language. The user can also save or import code, connect a board, and download code on it.

Primary objectives of the interface are:
- Create an ASM window in which we can read and write code.
- Create a debugger to display all potential errors.
- Create a register window to display register values.
- Create memory windows to display where the code is stored and where the user can edit the RAM.
- Create a pipeline in which we can see the instructions going through Fetch, Decode, and Execute.
- Create a binary window in which we can read the binary corresponding to our code.
- Create buttons to save, import, assemble, run, run step by step, reset, connect a board, and download code.
- Provide documentation about the LCM3 and the simulator itself.
- Have re-sizable frames, light and dark themes, syntax highlighting, and a bit of color.

#### 2.2.2 Modules Used

To code the interface, we used several modules:
- Tkinter: The graphical user interface is built using Tkinter, a popular GUI toolkit used in Python.
- CustomTkinter: An extension of Tkinter with a more modern look.
- Random: The classic random library to pick random numbers or elements.
- Webbrowser: Useful to open an online documentation of the ASM LCM3.

#### 2.2.3 Interface Architecture and Features

The interface contains different frames in which we can write code or read information. They are:

- **ASM Zone:** This is the text frame in which the user will code. It provides syntax color highlighting and error highlighting. The text is also locked in the upper-case to ease coding of the instructions such as ’MOV’ or ’B’.
- **Debugger:** The debugger frame displays errors or information about the assembly of the code. The color of the text also varies depending on if it’s an error or not.
- **Register frame:** This frame displays the values of all registers. It works with the run and the run step-by-step. There also is an option to switch between decimal and hexadecimal displays.
- **Code memory array:** This array shows the memory where the code is stored. It displays the instruction in text format and their corresponding binary code in hexadecimal.
- **User memory array:** This array, on the other hand, shows the part of the memory that is accessible by the user. It’s the readable and editable RAM.
- **Binary frame:** This frame displays the binary translation of the code that will be sent to the board if one is connected.
- **Pipeline array:** This array displays the path of instructions in the Fetch, Decode, and Execute.

Three menus are accessible in the top left corner:
- **File Menu:** This menu allows creating a new file, importing code from an external file, and saving the current code. These actions ensure efficient code management within the simulator.
- **Settings Menu:** So far this menu allows you to switch between dark and light themes. This feature enhances the user experience by accommodating different preferences for visual appearance.
- **Help Menu:** This menu provides quick access to documentation, including both simulator-specific help and external LCM3 documentation, facilitating learning and troubleshooting.

You can also access several simulation buttons in the top right corner:
- **Assemble Button:** Allows to assemble the code. Displays the result, including potential errors, in the debugger window. Also calls the simulation function to prepare a run or step-by-step.
- **Run Button:** Simulates the code in one go. Also Enables you to resume simulation if in mode step-by-step.
- **Run Step-by-step Button:** Simulates the code incrementally. This facilitates debugging by enabling a detailed inspection of each instruction execution.
- **Step Button:** Button to execute one step when in step-by-step mode.
- **Reset Button:** Resets the values in the User memory, the Code memory, the pipeline, the registers, the binary window, and the debugger. It also reduces the lag by re-initializing some of the frames.
- **Connect Board Button:** Allows to connect a board to the computer running the simulator. Opens a pop-up to configure the port, the baud rate, and other connection parameters.
- **Download Code Button:** Once a board is connected, this button allows you to download the bit stream of the ASM code onto the board. And triggers the running of the code on the board.

### 2.3 Connection to the Board

#### Goal of Having a Connection

The goal of establishing a connection is to test the user’s code behavior on the simulator. It facilitates communication between the IDE and the board, enabling the sending and receiving of information.

#### Connection Process

The connection process is designed to be user-friendly. When the user clicks on "connect board," a pop-up appears allowing the user to input specific parameters to establish the serial connection. These parameters include selecting the Communication (COM) port, baudrate, timeout, parity, stopbits, and bytesize. These parameters are essential for configuring the serial communication protocol between the simulator and the Arty A7 board.

We utilize the tkinter library to create an interactive interface, ensuring accessibility for users.

#### Parameters to Configure and Send to the Board

- **COM Ports:** The available COM ports are retrieved using the serial.tools.list_ports library, ensuring that users can select from the available options. If no COM port is available, it will be indicated on the connection pop-up, and the connection won’t be possible.

- **Baudrate:** Represents the speed of data transmission between the simulator and the Arty A7 board. Users can select from a range of baudrate values, such as 300, 1200, 2400, etc. The default baudrate is set to 9600.

- **Timeout:** Defines the maximum time the simulator should wait for data from the Arty A7 board. Users can customize this value based on specific requirements. The default timeout is set to 1.

- **Parity:** A mechanism for error-checking during data transmission. Users can select from options including 'None,' 'Even,' 'Odd,' etc. The default parity is set to 'None.'

- **Stopbit:** Indicates the number of bits used to signal the end of a data byte. Users can choose between 0 and 1 stopbit options. The default stopbit is set to 0.

- **Bytesize:** Refers to the number of data bits in each character. Users can choose from values such as 8, 16, and 32. The default bytesize is set to 8.

In the connect board function, we create a serial.Serial object containing the parameters defined by the user. This object serves as the communication link between the simulator and the Arty A7 board. Once the user finalizes their selections and clicks on the "ok" button, the pop-up closes, leaving the simulator connected and ready for interaction.

#### Disconnect Management

The disconnection process is handled by the disconnect board function:

1. **User Confirmation:** Displays a message box asking the user whether they want to close the serial connection. The user can choose "Yes" or "No."

2. **Handling User Response:** If the user selects "Yes," the code proceeds to close the serial connection using ser.close(). If "No" is selected, the connection remains open.

3. **Print Statements:** Prints messages to the console indicating whether the serial connection was closed or left open based on the user’s choice.

4. **Global Variables:** Uses the global keyword to access and modify the global variables ser and connect state within the function.

5. **Integration with the Interface:** Typically called when the user interacts with the GUI, specifically in response to a button press.

The user’s choice ("Yes" or "No") determines whether the serial connection should be closed. If closed, resources are released, and the system returns to a clean state; if not, the connection remains active for further communication.

