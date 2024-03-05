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
