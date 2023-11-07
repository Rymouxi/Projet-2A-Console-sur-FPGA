from fonctions_LCM3 import*
from B_instruct import B_instruct

def instruction_recognition(instruction:str,line:int):
    """Reconnaissance des instructions données
    line_update pointe vers la prochaine ligne qui va être simulée par le programme
    """
    n=len(instruction)
    bitstream=''
    register_update=[]
    error=[]
    line_update=line+1

    if n>0:
        if instruction=='':
            return bitstream,register_update,error,line_update
        elif instruction.count(':')==1:
            return bitstream,register_update,error,line_update
        elif instruction[0:3]=='ADD':
            bitstream,register_update,error=ADD(instruction,line)
        elif instruction[0:3]=='AND':
            bitstream,register_update,error=AND(instruction,line)
        elif instruction[0]=='B':
            bitstream,error,line_update=B_instruct(instruction,line)
        elif instruction[0:3]=='CMP':
            bitstream,register_update,error=CMP(instruction,line)
        elif instruction[0:3]=='EOR':
            bitstream,register_update,error=EOR(instruction,line)
        elif instruction[0:3]=='LDR':
            bitstream,register_update,error=LDR(instruction,line)
        elif instruction[0:3]=='LSL':
            bitstream,register_update,error=LSL(instruction,line)
        elif instruction[0:3]=='MOV':
            bitstream,register_update,error=MOV(instruction,line)
        elif instruction[0:3]=='STR':
            bitstream,register_update,error=STR(instruction,line)
        elif instruction[0:3]=='SUB':
            bitstream,register_update,error=SUB(instruction,line)

        else:
            error.append("Syntax error")
            error.append(line)
    return bitstream,register_update,error,line_update
    
