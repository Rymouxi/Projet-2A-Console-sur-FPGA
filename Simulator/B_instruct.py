from treatment import*
from label_recognition import*


def B_instruct(instruction:str,code_ASM:str,line:int):
    """Fonction référençant chaque possibilités pour un branchement:
    """
    #Ici on peut, au besoin, rajouter BGE, BLT, BGT, BLE
    label_list=label_recognition(code_ASM)
    machine=''

    if instruction[0:3]=='BEQ':
        #BEQ label
        machine=BEQ_label(instruction,label_list,line)
    elif instruction[0:3]=='BNE':
        #BNE label
        machine=BNE_label(instruction,label_list,line)
    elif instruction[0:2]=='B ':
        #B label
        machine=B_label(instruction,label_list,line)
    return machine


def B_label(instruction:str,label_list,line:int):
    """Traduction de l'instruction B label
    """ 
    liste_instruction.append(instruction)
    ligne_instruction.append(line)
    n=len(instruction)
    return '11100'+jump_length(instruction[2:n+1],label_list,line,10)

def BNE_label(instruction:str,label_list,line:int):
    """Traduction de l'instruction B label
    """
    liste_instruction.append(instruction)
    ligne_instruction.append(line)
    n=len(instruction)
    return '11010001'+jump_length(instruction[4:n+1],label_list,line,7)

def BEQ_label(instruction:str,label_list,code_ASM,line:int):
    """Traduction de l'instruction B label
    """
    liste_instruction.append(instruction)
    ligne_instruction.append(line)
    n=len(instruction)
    return '11010000'+jump_length(instruction[4:n+1],label_list,line,7)

def jump_length(label:str,label_list:list,line:int,size:int):
    """Cette fonction prend l'instruction sans l'embranchement même conditionnelle\n
    Par exemple, si l'instruction première est BNE label, l'argument en entrée de cette fonction sera label\n
    Cette instruction renvoie le saut converti en binaire complément à 2"""
    jumpBin=''
    if label not in label_list:
        print("The label of branch line ",line," is not defined" )
        exit()
    index=label_list.index(label)
    jump=label_list[index+1]-line
    jumpBin=DecToBinCom(jump,size)

    return jumpBin
