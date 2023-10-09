from DecToBin import *
from add_sub import *

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
    #Partons du principe que l'instruction ne prend qu'un certain type de forme
    #Nous avons donc: ADD Rd,Rn,#imm3
    #ADD Rd,#imm8
    #ADD Rd,Rn,Rm
    n=len(instruction)
    assembleur_offset='0001110'
    assembleur=''
    copie=instruction[4:n]

    if copie.count(',')==1:
    #ADD Rd,#imm8
        assembleur+=DecToBin(int(copie[copie.find('R')+1]))
        assembleur+=DecToBin(int(copie[copie.find('#')+1:n]))

    elif copie.count(',')==2:
        if copie.count('#')==0:
        #ADD Rd,Rn,Rm
            assembleur+=DecToBin(int(copie[copie.find('R')+1]))
            copie=copie[0:copie.find('R')-1]+copie[copie.find(','):len(copie)]
            assembleur+=DecToBin(int(copie[copie.find('R')+1]))
            copie=copie[0:copie.find('R')-1]+copie[copie.find(','):len(copie)]
            assembleur+=DecToBin(int(copie[copie.find('R')+1]))

        elif copie.count('#')==1:
        #ADD Rd,Rn,#imm3  
            assembleur+=DecToBin(int(copie[copie.find('#')+1]))
            assembleur+=DecToBin(int(copie[copie.find('R')+1]))
            copie=copie[0:copie.find('R')-1]+copie[copie.find(','):len(copie)]
            assembleur+=DecToBin(int(copie[copie.find('R')+1]))
            

    return assembleur_offset

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