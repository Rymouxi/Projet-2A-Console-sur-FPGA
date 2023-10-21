from DecToBin import*
from Register_recognition import*

def ADD(instructions:str):
    """ 3 modes de fonctionnement pour la fonction ADD
    
    """
    if len(register_recognition(instructions))==3:
        machine1='0001100'+(register_recognition(instructions)[2])+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine1)
    if len(register_recognition(instructions))==2:
        if htag_recognition(instructions,3)==-1:
            return(print("Tu dois mettre un nombre dans le add si 2 registre"))
        machine2='0001110'+(htag_recognition(instructions,3))+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine2)
    if len(register_recognition(instructions))==1:
        if htag_recognition(instructions,8)==-1:
            return(print("Tu dois mettre un nombre dans le add si 1 registre"))
        machine3='00110'+(register_recognition(instructions)[0])+(htag_recognition(instructions,8))
        return(machine3)
    else:
        return(print("error systéme"))




def SUB(instructions:str):
    """ a compléter comme le add"""
    
    if len(register_recognition(instructions))==3:
        machine1='0001101'+(register_recognition(instructions)[2])+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine1)
    if len(register_recognition(instructions))==2:
        if htag_recognition(instructions,3)==-1:
            return(print("Tu dois mettre un nombre dans le SUB si 2 registre"))
        machine2='0001111'+(htag_recognition(instructions,3))+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine2)
    if len(register_recognition(instructions))==1:
        if htag_recognition(instructions,8)==-1:
            return(print("Tu dois mettre un nombre dans le SUB si 1 registre"))
        machine3='00111'+(register_recognition(instructions)[0])+(htag_recognition(instructions,8))
        return(machine3)
    else:
        return(print("error systéme"))    





def MOV(instructions:str):
    """ Fonctions MOV qui à 2 modes de fonctionnement, 
    2 registre en entrées ou 1 registre et un nombre compris entre 0 et 255
    Notre fonctions prend en entrée une chaine de carractére qui correspond a une ligne d'instruction contenant "MOV" et renvoie l'instruction machine en bianire correspondante.
    """
    if len(register_recognition(instructions))==2:
        machine1='0000000000'+(register_recognition(instructions)[1])+(register_recognition(instructions)[0])
        return(machine1)
    if len(register_recognition(instructions))==1:
        if (htag_recognition(instructions,8))>255 or (htag_recognition(instructions,8))<0:
            return(print("Dans le MOV ton chiffre et trop grand COn****d ou trop petit"))  
                                                                
        machine2='00100'+(register_recognition(instructions)[0])+(htag_recognition(instructions,8))
        return(machine2)
    
  
