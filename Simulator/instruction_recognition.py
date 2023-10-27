from fonctions_LCM3 import*
from B_instruct import B_instruct

def instruction_recognition(instruction:str,code_asm,line:int):
    """Reconnaissance des instructions données
    """
    n=len(instruction)
    machine=''
    if n>0:
        if instruction.count(':')==1:
            return machine
        if instruction[0:3]=='ADD':
            machine=ADD(instruction,line)
        elif instruction[0:3]=='AND':
            machine=AND(instruction,line)
        elif instruction[0]=='B':
            machine=B_instruct(instruction,code_asm,line)
        elif instruction[0:3]=='CMP':
            machine=CMP(instruction,line)
        elif instruction[0:3]=='EOR':
            machine=EOR(instruction,line)
        elif instruction[0:3]=='LDR':
            machine=LDR(instruction,line)
        elif instruction[0:3]=='LSL':
            machine=LSL(instruction,line)
        elif instruction[0:3]=='MOV':
            machine=MOV(instruction,line)
        elif instruction[0:3]=='STR':
            machine=STR(instruction,line)
        elif instruction[0:3]=='SUB':
            machine=SUB(instruction,line)
        elif instruction=='':
            return machine
        else:
            print("Error Syntax")
            exit()
    return machine
    
