from register_recognition import *
from treatment import *


#On travaille toujours avec des chaînes de caractères
#Les fonctions appelées renvoient des chaînes de caractère

def AND(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction AND\n
    En partant du principe qu'il est de la forme: AND Rd,Rm
    """
    register_update=[]
    bitstream=''
    error=''

    #AND Rd,Rm
    if len(register_recognition(instruction))==2:
        
        #Rd et Rm sont les numéros (en décimal) des registres dans AND
        Rd=int(register_recognition(instruction)[0],2)
        Rm=int(register_recognition(instruction)[1],2)

        #Les valeurs de Rd et Rm en binaire
        Rd_value=reg_read(Rd)
        Rm_value=reg_read(Rm)

        #Opération simulée sur Rd et Rm
        register_update.append(Rd)
        register_update.append(int(Rd_value and Rm_value,2))
        bitstream='0100000000'+Rm+Rd

        return bitstream,register_update
    else:
        error='Number of arguments in AND line '+str(line)+" doesn't match"
        exit()


def LSL(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction LSL \n
    En partant du principe qu'il est de la forme: LSL Rd,Rm,#imm5
    """
    register_update=[]
    bitstream=''
    error=''
    #LSL Rd,Rm,#imm5
    if len(register_recognition(instruction))==2:

        #Rd, Rm et imm5 sont les numéros (en décimal) des registres dans AND
        Rd=int(register_recognition(instruction)[0],2)
        Rm=int(register_recognition(instruction)[1],2)
        imm5=int(imm_recognition(instruction,5)[0],2)

        #Les valeurs de Rd et Rm en binaire
        Rd_value=reg_read(Rd)
        Rm_value=reg_read(Rm)

        #Opération simulée sur Rd et Rm
        register_update.append(Rd)
        register_update.append(int(Rm_value,2)<< imm5)
        bitstream='00000'+Rm+Rd+imm5
        return bitstream,register_update
    else:
        print("Number of argument in LSL line ",line," doesn't match")
        exit()


def STR(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction STR \n
    En partant du principe qu'il est de la forme: STR Rt,[Rn]
    """
    register_update=[]
    bitstream=''
    error=''

    #STR Rt,[Rn]
    if len(register_recognition(instruction))==2:

        #Rt et Rn sont les numéros (en décimal) des registres dans STR
        Rt=int(register_recognition(instruction)[0],2)
        Rm=int(register_recognition(instruction)[1],2)

        bitstream= '0110000000'+Rn+Rt

        return bitstream,register_update
    else:
        print("Number of arguments in STR line ",line," doesn't match")
        exit()


def LDR(instructions:str,line:int):
    """Fonction renvoyant le code machine de l'instruction LDR\n
    En partant du principe qu'il est de la forme: LDR Rt,[Rn]
    """
    register_update=[]
    bitstream=''
    error=''

    #LDR Rt,[Rn]
    if len(register_recognition(instruction))==2:

        #Rt et Rn sont les numéros (en décimal) des registres dans LDR
        Rt=int(register_recognition(instruction)[0],2)
        Rm=int(register_recognition(instruction)[1],2)

        bitstream= '0110100000'+Rn+Rt
        
        return bitstream,register_update
    else:
        print("Number of arguments in LDR line ",line," doesn't match")


def EOR(instructions:str,line:int):
    """Fonction renvoyant le code machine de l'instruction EOR\n
    En partant du principe qu'il est de la forme: EOR Rd,Rm
    """   
    liste_instruction.append(instructions) 
    ligne_instruction.append(line)
    if len(register_recognition(instructions))==2:
        machine='0100000001'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine)
    else:
        print("Number of arguments in EOR line ",line," doesn't match")
        exit()


def CMP(instructions:str,line:int):
    """Traduction de l'instruction and en langage machine de 0 et de 1\n
    L'instruction qu'elle renvoie est de type str"""
    liste_instruction.append(instructions)
    ligne_instruction.append(line)
    #CMP Rn,#imm8
    if len(register_recognition(instructions))==1:
        return '00101'+(register_recognition(instructions)[0])+(imm_recognition(instructions,8))
    else:
        print("Number of arguments in CMP line ", line," doesn't match")


def ADD(instructions:str,line:int):
    """ 3 modes de fonctionnement pour la fonction ADD
    """
    liste_instruction.append(instructions)
    ligne_instruction.append(line)
    #ADD Rd,Rn,Rm
    if len(register_recognition(instructions))==3:
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[1],2)]+register[int(register_recognition(instructions)[2],2)])
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '0001100'+register_recognition(instructions)[2]+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #ADD Rd,Rn,#immm3
    if len(register_recognition(instructions))==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in ADD instruction line ",line)
            exit()
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[1],2)]+int(imm_recognition(instructions,3),2))
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '0001110'+imm_recognition(instructions,3)+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #ADD Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in ADD instruction line ",line)
            exit()
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[0],2)]+int(imm_recognition(instructions,8),2))
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '00110'+register_recognition(instructions)[0]+imm_recognition(instructions,8)
    
    #ADD
    else:
        print("There is not enough/too much arguments in ADD instruction line ",line)
        exit()


def SUB(instructions:str,line:int):
    """3 modes de fonctionnement pour la fonction SUB
    """
    liste_instruction.append(instructions)
    ligne_instruction.append(line)
    #SUB Rd,Rn,Rm
    if len(register_recognition(instructions))==3:
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[1],2)]-register[int(register_recognition(instructions)[2],2)])
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '0001101'+register_recognition(instructions)[2]+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #SUB Rd,Rn,#imm3
    if len(register_recognition(instructions))==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in SUB instruction line ",line)
            exit()
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[1],2)]-int(imm_recognition(instructions,3),2))
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '0001111'+imm_recognition(instructions,3)+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #SUB Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in SUB instruction line ",line)
            exit()
        register[int(register_recognition(instructions)[0],2)]=(register[int(register_recognition(instructions)[0],2)]-int(imm_recognition(instructions,8),2))
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '00111'+register_recognition(instructions)[0]+imm_recognition(instructions,8)
    
    #SUB
    else:
        print("There is not enough/too much arguments in SUB instruction line ",line)
        exit()


def MOV(instructions:str,line:int):
    """ Fonctions MOV qui à 2 modes de fonctionnement, 
    2 registres en entrée ou 1 registre et un nombre compris entre 0 et 255
    Notre fonctions prend en entrée une chaine de carractére qui correspond a une ligne d'instruction contenant "MOV" et renvoie l'instruction machine en bianire correspondante.
    """
    liste_instruction.append(instructions)
    ligne_instruction.append(line)
    #MOV Rd,Rm
    if len(register_recognition(instructions))==2:
        register[int(register_recognition(instructions)[0],2)]=register[int(register_recognition(instructions)[1],2)]
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '0000000000'+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #MOV Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in MOV instruction line ",line)
            exit()
        register[int(register_recognition(instructions)[0],2)]=int(imm_recognition(instructions,8),2)
        register_update.append((int(register_recognition(instructions)[0],2),register[int(register_recognition(instructions)[0],2)]))
        return '00100'+(register_recognition(instructions)[0])+(imm_recognition(instructions,8))
    else:
        print("There is not enough/too much arguments in MOV instruction line ",line)
        exit()
