

def reconnaissance_instruction(instruction):
    n=len(instruction)
    if instruction[0:2]=='ADD':
        add(instruction)
    elif instruction[0:2]=='AND':
        and_(instruction)
    elif instruction[0]=='B':
        b_instruct(instruction)
    elif instruction[0:2]=='CMP':
        cmp(instruction)
    elif instruction[0:2]=='EOR':
        eor(instruction)
    elif instruction[0:2]=='LDR':
        ldr(instruction)
    elif instruction[0:2]=='LSL':
        lsl(instruction)
    elif instruction[0:2]=='MOV':
        mov(instruction)
    elif instruction[0:2]=='STR':
        str_(instruction)
    elif instruction[0:2]=='SUB':
        sub(instruction)
    else:
        print("Cette instruction n'appartient pas au LCM3")


def add(instruction):
    return 1
def and_(instruction):
    return 1
def b_instruct(instruction):
    return 1
def cmp(instruction):
    return 1
def eor(instruction):
    return 1
def ldr(instruction):
    return 1
def lsl(instruction):
    return 1
def mov(instruction):
    return 1
def str_(instruction):
    return 1
def sub(instruction):
    return 1

