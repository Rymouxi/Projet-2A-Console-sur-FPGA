from virtual_register_fct import virtual_register


"""La simulation des instructions de branchement B.\n
Dans le cas des branchements conditionnels, la simulation choisit ce qu'elle fait en fonction
de la valeur dans le registre NZVC qui, je le rappelle est le 9ème élément de virtual_register.\n
Pour que la simulation puisse renvoyer le branchement au bon endroit dans le code, on ajoute une variable de retour
qui est line_update.\n
Cette variable indiquera à quelle ligne le programme doit aller pendant la simulation.
"""

def B_instruct_simu(instruction:str,line:int):
    """Fonction référençant chaque possibilités pour un branchement:
    """
    #Ici on peut, au besoin, rajouter BGE, BLT, BGT, BLE
    line_update=0
    error_simu=[]
    if instruction[0:4]=='BEQ ':
        #BEQ label
        line_update,error_simu=BEQ_label_simu(instruction,line)
    elif instruction[0:4]=='BNE ':
        #BNE label
        line_update,error_simu=BNE_label_simu(instruction,line)
    elif instruction[0:4]=='BGE ':
        #BNE label
        line_update,error_simu=BGE_label_simu(instruction,line)
    elif instruction[0:4]=='BLT ':
        #BNE label
        line_update,error_simu=BLT_label_simu(instruction,line)
    elif instruction[0:4]=='BGT ':
        #BNE label
        line_update,error_simu=BGT_label_simu(instruction,line)
    elif instruction[0:4]=='BLE ':
        #BNE label
        line_update,error_simu=BLE_label_simu(instruction,line)
    elif instruction[0:2]=='B ':
        #B label
        line_update,error_simu=B_label_simu(instruction,line)

    return line_update,error_simu


def B_label_simu(instruction:str,line:int):
    """Traduction de l'instruction B label
    """ 
    line_update=0
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[2:n+1],line,10)

    line_update=line+jumpDec

    return line_update,error_simu


def BNE_label_simu(instruction:str,line:int):
    """Traduction de l'instruction BNE label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]!=0:
        line_update=line+jumpDec

    return line_update,error_simu

def BEQ_label_simu(instruction:str,line:int):
    """Traduction de l'instruction B label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]==0:
        line_update=line+jumpDec
        
    return line_update,error_simu

def BGE_label_simu(instruction:str,line:int):
    """Traduction de l'instruction BGE label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]>=0:
        line_update=line+jumpDec
        
    return line_update,error_simu

def BLT_label_simu(instruction:str,line:int):
    """Traduction de l'instruction BLT label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]<0:
        line_update=line+jumpDec
        
    return line_update,error_simu
    
def BGT_label_simu(instruction:str,line:int):
    """Traduction de l'instruction BGT label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]>0:
        line_update=line+jumpDec
        
    return line_update,error_simu

def BLE_label_simu(instruction:str,line:int):
    """Traduction de l'instruction BLE label
    """
    line_update=line+1
    n=len(instruction)
    jumpDec,error_simu=jump_length_simu(instruction[4:n+1],line,7)

    if virtual_register[8]<=0:
        line_update=line+jumpDec
        
    return line_update,error_simu



def jump_length_simu(label:str,line:int,size:int):
    """Cette fonction prend l'instruction sans l'embranchement même conditionnelle\n
    Par exemple, si l'instruction première est BNE label, l'argument en entrée de cette fonction sera label\n
    Cette instruction renvoie le saut à faire"""
    
    from label_recognition import label_table
    error_simu=[]
    index=label_table.index(label)
    #Taille du saut en décimale
    jumpDec=label_table[index+1]-line

    #Détection d'un label trop éloigné 
    if 2**size-1<jumpDec:
        error_simu.extend(["The label of branch line"+line+"is too far",line])

    return jumpDec,error_simu
