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

