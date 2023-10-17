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
        l=b_instruct(instruction)
    elif instruction[0:3]=='CMP':
        l=CMP(instruction)
    elif instruction[0:3]=='EOR':
        l=EOR(instruction)
    elif instruction[0:3]=='LDR':
        l=LDR(instruction)
    elif instruction[0:3]=='LSL':
        l=LSL(instruction)
    elif instruction[0:3]=='MOV':
        l=MOV(instruction)
    elif instruction[0:3]=='STR':
        l=STR(instruction)
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
    
def LSL(instruction):
    """ Fonction renvoyant le code machine de l'instruction LSL \n
    En partant du principe qu'il est de la forme: LSL Rd,Rm,#imm5
    """
    #LSL Rd,Rm,#imm5
    n=len(instruction)
    return '00000'+register_recognition(instruction)[0]+register_recognition(instruction)[1]+htag_recognition(instruction,5)

def STR(instruction):
    """ Fonction renvoyant le code machine de l'instruction STR \n
    En partant du principe qu'il est de la forme: STR Rt,[Rn]
    """
    #STR Rt,[Rn]
    if len(register_recognition(instruction))==2:
        return '0110000000'+register_recognition(instruction)[1]+register_recognition(instruction)[0]
    else:
        return(print("Number of arguments doesn't match"))
    
def LDR(instructions:str):
    """   
    """
    if len(register_recognition(instructions))==2:
        machine5='0110100000'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine5)
    else:
        return(print("error systéme sur le LDR dans le arguments"))
    
 
def EOR(instructions:str):
    """
    """    
    if len(register_recognition(instructions))==2:
        machine5='0100000001'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine5)
    else:
        return(print("error systéme sur le EOR dans le arguments"))
    
