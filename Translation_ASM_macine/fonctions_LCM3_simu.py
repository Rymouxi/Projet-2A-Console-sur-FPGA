from register_recognition import*
from treatment import*

def ADD_simu(instruction,line):
    """ 3 modes de fonctionnement pour la fonction ADD
    """
    n=len(register_recognition(instruction))
    #ADD Rd,Rn,Rm
    if n==3:
        registers=[int(register_recognition(instruction)[i],2) for i in range(n)]
        register_value=[reg_read(register) for register in registers]
        reg_edit(registers[0],register_value[1]+register_value[2])
    
    #ADD Rd,Rn,#immm3
    if n==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in ADD instruction line ",line)
            exit()
        registers=[int(register_recognition(instruction)[i],2) for i in range(n)]
        imm_value=int(imm_recognition(instruction,3),2)
        register_value=[reg_read(register) for register in registers]
        reg_edit(registers[0],register_value[1]+imm_value)

    #ADD Rd,#imm8
    if n==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in ADD instruction line ",line)
            exit()
        registers=int(register_recognition(instruction)[0],2)
        imm_value=int(imm_recognition(instruction,8),2)
        register_value=reg_read(registers)
        reg_edit(registers[0],register_value[0]+imm_value)    
    #ADD
    else:
        print("There is not enough/too much arguments in ADD instruction line ",line)
        exit()

 
def SUB_simu(instruction,line):
    """ 3 modes de fonctionnement pour la fonction SUB
    """
    n=len(register_recognition(instruction))
    #SUB Rd,Rn,Rm
    if n==3:
        registers=[int(register_recognition(instruction)[i],2) for i in range(n)]
        register_value=[reg_read(register) for register in registers]
        reg_edit(registers[0],register_value[1]-register_value[2])
    
    #SUB Rd,Rn,#immm3
    if n==2:
        if imm_recognition(instructions,3)==-1:
            print("There must be a #imm with imm<8 in SUB instruction line ",line)
            exit()
        registers=[int(register_recognition(instruction)[i],2) for i in range(n)]
        imm_value=int(imm_recognition(instruction,3),2)
        register_value=[reg_read(register) for register in registers]
        reg_edit(registers[0],register_value[1]-imm_value)

    #SUB Rd,#imm8
    if n==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in SUB instruction line ",line)
            exit()
        registers=int(register_recognition(instruction)[0],2)
        imm_value=int(imm_recognition(instruction,8),2)
        register_value=reg_read(registers)
        reg_edit(registers[0],register_value[0]-imm_value)    
    #SUB
    else:
        print("There is not enough/too much arguments in ADD instruction line ",line)
        exit()

def MOV_simu(instructions:str,line:int):
    """ Fonctions MOV qui à 2 modes de fonctionnement, 
    2 registres en entrée ou 1 registre et un nombre compris entre 0 et 255
    Notre fonctions prend en entrée une chaine de carractére qui correspond a une ligne d'instruction contenant "MOV" et renvoie l'instruction machine en bianire correspondante.
    """
    #MOV Rd,Rm
    if len(register_recognition(instructions))==2:
        registers=register_recognition(instructions)
        register_value=reg_read(int(registers[1],2))
        reg_edit(registers[0],register_value)
    #MOV Rd,#imm8
    if len(register_recognition(instructions))==1:
        if imm_recognition(instructions,8)==-1:
            print("There must be a #imm with imm<256 in MOV instruction line ",line)
            exit()
        reg_edit(int(register_recognition(instructions)[0],2),int(imm_recognition(instructions,8),2))
    else:
        print("There is not enough/too much arguments in MOV instruction line ",line)
        exit()

def AND_simu(instruction,line):
    """ Fonction renvoyant le code machine de l'instruction AND\n
    En partant du principe qu'il est de la forme: AND Rd,Rm
    """
    #AND Rd,Rm
    if len(register_recognition(instruction))==2:
        registers_value=[DecToBin(reg_read(int(register_recognition(instruction)[0],2))),DecToBin(reg_read(int(register_recognition(instruction)[1],2)))]
        reg_edit(int(register_recognition(instruction),2),int(registers_value[0] and registers_value[1],2))
    else:
        print("Number of arguments in AND line ",line," doesn't match")
        exit()

def EOR_simu(instructions:str,line:int):
    """Fonction renvoyant le code machine de l'instruction EOR\n
    En partant du principe qu'il est de la forme: EOR Rd,Rm
    """    
    if len(register_recognition(instructions))==2:
        return(machine)
    else:
        print("Number of arguments in EOR line ",line," doesn't match")
        exit()
