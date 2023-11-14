from label_recognition import*
from virtual_register_fct import virtual_register

"""La simulation des instructions de branchement B.\n
Dans le cas des branchements conditionnels, la simulation choisit ce qu'elle fait en fonction
de la valeur dans le registre NZVC qui, je le rappelle est le 9ème élément de virtual_register.\n
Pour que la simulation puisse renvoyer le branchement au bon endroit dans le code, on ajoute une variable de retour
qui est line_update.\n
Cette variable indiquera à quelle ligne le programme doit aller pendant la simulation.
"""

def B_instruct_simu(instruction:str,split_instructions:list,line:int):
    """Fonction référençant chaque possibilités pour un branchement:
    """
    #Ici on peut, au besoin, rajouter BGE, BLT, BGT, BLE
    label_list=label_recognition(split_instructions)
    line_update=0
    error=[]
    if instruction[0:3]=='BEQ ':
        #BEQ label
        line_update,error=BEQ_label_simu(instruction,label_list,line)
    elif instruction[0:3]=='BNE ':
        #BNE label
        line_update,error=BNE_label_simu(instruction,label_list,line)
    elif instruction[0:2]=='B ':
        #B label
        line_update,error=B_label_simu(instruction,label_list,line)
    else:
        error.append("Syntax Error")
        error.append(line)
    return line_update,error


def B_label_simu(instruction:str,label_list,line:int):
    """Traduction de l'instruction B label
    """ 
    line_update=0

    error=[]

    n=len(instruction)
    jumpDec,error=jump_length_simu(instruction[2:n+1],label_list,line,10)

    line_update=line+jumpDec

    return line_update,error


def BNE_label_simu(instruction:str,label_list,line:int):
    """Traduction de l'instruction BNE label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error=jump_length_simu(instruction[4:n+1],label_list,line,7)

    if virtual_register[8]!=0:
        line_update=line+jumpDec

    return line_update,error

def BEQ_label_simu(instruction:str,label_list,code_ASM,line:int):
    """Traduction de l'instruction B label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error=jump_length_simu(instruction[4:n+1],label_list,line,7)

    if virtual_register[8]==0:
        line_update=line+jumpDec
        
    return line_update,error


def jump_length_simu(label:str,label_list:list,line:int,size:int):
    """Cette fonction prend l'instruction sans l'embranchement même conditionnelle\n
    Par exemple, si l'instruction première est BNE label, l'argument en entrée de cette fonction sera label\n
    Cette instruction renvoie le saut à faire"""

    error=[]
    if label not in label_list:
        error.append("The label of branch line "+line+" is not defined" )
        error.append(line)

    else:
    
        index=label_list.index(label)
        #Taille du saut en décimale
        jumpDec=label_list[index+1]-line

        #Détection d'un label trop éloigné 
        if 2**size-1<jumpDec:
            error.append("The label of branch line"+line+"is too far")
            error.append(line)

    return jumpDec,error
