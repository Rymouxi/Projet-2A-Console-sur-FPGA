from Fonctions_LCM3 import*
def instruction_recognition(str:instruction):
  """Reconnaissance des instructions données
  """
    n=len(instruction)
    l=''
    if instruction.count(':'):
        return l
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
