from DecToBin import *
from add_sub_mov import *
from Register_recognition import *

#On travaille toujours avec des chaînes de caractères
#Les fonctions appelées renvoient des chaînes de caractère

def recognition_instruction(instruction):
    n=len(instruction)
    l=''
    if instruction[0:3]=='ADD':
        l=ADD(instruction)
    elif instruction[0:3]=='AND ':
        l=AND_(instruction)
    elif instruction[0]=='B':
        b_instruct(instruction)
    elif instruction[0:3]=='CMP':
        cmp(instruction)
    elif instruction[0:3]=='EOR':
        eor(instruction)
    elif instruction[0:3]=='LDR':
        ldr(instruction)
    elif instruction[0:3]=='LSL':
        lsl(instruction)
    elif instruction[0:3]=='MOV':
        l=MOV(instruction)
    elif instruction[0:3]=='STR':
        str_(instruction)
    elif instruction[0:3]=='SUB':
        l=SUB(instruction)
    else:
        print("Error Syntax")
    return l


def AND_(instruction:str):
    """Traduction de l'instruction and en langage machine de 0 et de 1\n
    L'instruction qu'elle renvoie est de type str"""
    #AND Rd,Rm
    register=register_recognition(instruction)
    machine='0100000000'+register[1]+register[0]
    return machine

def b_instruct(instruction):
    return 1

def cmp(instruction):
    """Traduction de l'instruction and en langage machine de 0 et de 1\n
    L'instruction qu'elle renvoie est de type str"""
    #CMP Rn,#imm8
    
    return 1
def eor(instruction):
    return 1
def ldr(instruction):
    return 1
def lsl(instruction):
    return 1
def mov(instruction):
    return 1
def STR(instruction:str):
    """ MY name is STR 
    """
    if len(register_recognition(instruction))==2:
        machine5='0110000000'+(register_recognition(instruction)[1])+(register_recognition(instruction)[0])
        return(machine5)
    else:
        return(print("error systéme sur le STR dans le arguments"))
    
