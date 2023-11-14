from fonctions_LCM3_simu import*
from fonctions_LCM3_bitstream import*
from B_instruct_simu import B_instruct_simu
from B_instruct_bitstream import B_instruct_bitstream

"""Fichier contenant la fonction permettant d'identifier les differentes instructions (MOV, ADD ...)\n
Elle réalise les appels aux fonctions permettant de traduire ces instructions en binaire si nous sommes en mode bitstream 
ou remplit le tableaux de l'évolution des registres et de la mémoire si nous sommes en mode simulation.\n
La fonction prend donc en arguments "ON" ou "OFF" selon le mode.
"""


def instruction_recognition(instruction:str,line:int,split_instructions:list,simu='OFF'):
    """Reconnaissance des instructions données
    line_update pointe vers la prochaine ligne qui va être simulée par le programme
    """
    n=len(instruction)
    bitstream=''
    register_update=[]
    memory_update=[]
    line_update=line+1
    error=[]


    if simu=='OFF':
        if n>0:
            if instruction.count(':')==1:
                return bitstream
            elif instruction[0:3]=='ADD':
                bitstream=ADD_bitstream(instruction,line)
            elif instruction[0:3]=='AND':
                bitstream=AND_bitstream(instruction,line)
            elif instruction[0]=='B':
                bitstream=B_instruct_bitstream(instruction,split_instructions,line)
            elif instruction[0:3]=='CMP':
                bitstream=CMP_bitstream(instruction,line)
            elif instruction[0:3]=='EOR':
                bitstream=EOR_bitstream(instruction,line)
            elif instruction[0:3]=='LDR':
                bitstream=LDR_bitstream(instruction,line)
            elif instruction[0:3]=='LSL':
                bitstream=LSL_bitstream(instruction,line)
            elif instruction[0:3]=='MOV':
                bitstream=MOV_bitstream(instruction,line)
            elif instruction[0:3]=='STR':
                bitstream=STR_bitstream(instruction,line)
            elif instruction[0:3]=='SUB':
                bitstream=SUB_bitstream(instruction,line)
        return bitstream

    elif simu=='ON':
        if n>0:
            if instruction.count(':')==1:
                return register_update,line_update,memory_update,error
            elif instruction[0:4]=='ADD ':
                register_update,error=ADD_simu(instruction,line)
            elif instruction[0:4]=='AND ':
                register_update,error=AND_simu(instruction,line)
            elif instruction[0]=='B':
                line_update,error=B_instruct_simu(instruction,split_instructions,line)
            elif instruction[0:4]=='CMP ':
                register_update,error=CMP_simu(instruction,line)
            elif instruction[0:4]=='EOR ':
                register_update,error=EOR_simu(instruction,line)
            elif instruction[0:4]=='LDR ':
                register_update,error=LDR_simu(instruction,line)
            elif instruction[0:4]=='LSL ':
                register_update,error=LSL_simu(instruction,line)
            elif instruction[0:4]=='MOV ':
                register_update,error=MOV_simu(instruction,line)
            elif instruction[0:4]=='STR ':
                register_update,memory_update,error=STR_simu(instruction,line)
            elif instruction[0:4]=='SUB ':
                register_update,error=SUB_simu(instruction,line)

            else:
                error.append("Syntax error")
                error.append(line)
        return register_update,line_update,memory_update,error
    
