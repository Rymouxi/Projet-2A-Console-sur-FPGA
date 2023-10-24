from register_recognition import *

#On travaille toujours avec des chaînes de caractères
#Les fonctions appelées renvoient des chaînes de caractère

def AND(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction AND\n
    En partant du principe qu'il est de la forme: AND Rd,Rm
    """
    #AND Rd,Rm
    if len(register_recognition(instruction))==2:
        return '0100000000'+register_recognition(instruction)[1]+register_recognition(instruction)[0]
    else:
        print("Number of arguments in AND line ",line," doesn't match")
        exit()


def LSL(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction LSL \n
    En partant du principe qu'il est de la forme: LSL Rd,Rm,#imm5
    """
    #LSL Rd,Rm,#imm5
    if len(register_recognition(instruction))==2:
        return '00000'+register_recognition(instruction)[0]+register_recognition(instruction)[1]+imm_recognition(instruction,5)
    else:
        print("Number of argument in LSL line ",line," doesn't match")
        exit()


def STR(instruction:str,line:int):
    """ Fonction renvoyant le code machine de l'instruction STR \n
    En partant du principe qu'il est de la forme: STR Rt,[Rn]
    """
    #STR Rt,[Rn]
    if len(register_recognition(instruction))==2:
        return '0110000000'+register_recognition(instruction)[1]+register_recognition(instruction)[0]
    else:
        print("Number of arguments in STR line ",line," doesn't match")
        exit()


def LDR(instructions:str,line:int):
    """Fonction renvoyant le code machine de l'instruction LDR\n
    En partant du principe qu'il est de la forme: LDR Rt,[Rn]
    """
    if len(register_recognition(instructions))==2:
        machine='0110100000'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine)
    else:
        print("Number of arguments in LDR line ",line," doesn't match")


def EOR(instructions:str,line:int):
    """Fonction renvoyant le code machine de l'instruction EOR\n
    En partant du principe qu'il est de la forme: EOR Rd,Rm
    """    
    if len(register_recognition(instructions))==2:
        machine='0100000001'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine)
    else:
        print("Number of arguments in EOR line ",line," doesn't match")
        exit()


def CMP(instructions:str,line:int):
    """Traduction de l'instruction and en langage machine de 0 et de 1\n
    L'instruction qu'elle renvoie est de type str"""
    #CMP Rn,#imm8
    if len(register_recognition(instructions))==1:
        return '00101'+(register_recognition(instructions)[0])+(imm_recognition(instructions,8))
    else:
        print("Number of arguments in CMP line ", line," doesn't match")


def ADD(instructions:str,line:int):
    """ 3 modes de fonctionnement pour la fonction ADD
    """

    #ADD Rd,Rn,Rm
    if len(register_recognition(instructions))==3:
        return '0001100'+register_recognition(instructions)[2]+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #ADD Rd,Rn,#immm3
    if len(register_recognition(instructions))==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in ADD instruction line ",line)
            exit()
        return '0001110'+imm_recognition(instructions,3)+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #ADD Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in ADD instruction line ",line)
            exit()
        return '00110'+register_recognition(instructions)[0]+imm_recognition(instructions,8)
    
    #ADD
    else:
        print("There is not enough/too much arguments in ADD instruction line ",line)
        exit()


def SUB(instructions:str,line:int):
    """3 modes de fonctionnement pour la fonction SUB
    """

    #SUB Rd,Rn,Rm
    if len(register_recognition(instructions))==3:
        return '0001101'+register_recognition(instructions)[2]+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #SUB Rd,Rn,#imm3
    if len(register_recognition(instructions))==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in SUB instruction line ",line)
            exit()
        return '0001111'+imm_recognition(instructions,3)+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #SUB Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in SUB instruction line ",line)
            exit()
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
    #MOV Rd,Rm
    if len(register_recognition(instructions))==2:
        return '0000000000'+register_recognition(instructions)[1]+register_recognition(instructions)[0]
    
    #MOV Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in MOV instruction line ",line)
            exit()
        return '00100'+(register_recognition(instructions)[0])+(imm_recognition(instructions,8))
    else:
        print("There is not enough/too much arguments in MOV instruction line ",line)
        exit()
