from DecToBin import*

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
   
