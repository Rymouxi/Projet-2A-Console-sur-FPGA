from treatment import*
from label_recognition import*
from virtual_register_fct import virtual_register

"""La génération du bitstream des instructions de branchement B.\n
Dans le cas des branchements conditionnels, la simulation choisit ce qu'elle fait en fonction
de la valeur dans le registre NZVC qui, je le rappelle est le 9ème élément de virtual_register.\n
Pour que la simulation puisse renvoyer le branchement au bon endroit dans le code, on ajoute une variable de retour
qui est line_update.\n
Cette variable indiquera à quelle ligne le programme doit revenir pendant la simulation.
"""

def B_instruct(instruction:str,code_ASM:str,line:int):
    """Fonction référençant chaque possibilités pour un branchement:
    """
    #Ici on peut, au besoin, rajouter BGE, BLT, BGT, BLE
    label_list=label_recognition(code_ASM)
    bitstream=''
    line_update=0
    error=[]
    if instruction[0:3]=='BEQ':
        #BEQ label
        bitstream,error,line_update=BEQ_label(instruction,label_list,line)
    elif instruction[0:3]=='BNE':
        #BNE label
        bitstream,error,line_update=BNE_label(instruction,label_list,line)
    elif instruction[0:2]=='B ':
        #B label
        bitstream,error,line_update=B_label(instruction,label_list,line)

    return bitstream,error,line_update


def B_label(instruction:str,label_list,line:int):
    """Traduction de l'instruction B label
    """ 
    line_update=0
    bitstream=''
    error=[]

    n=len(instruction)
    jumpBin,jumpDec,error=jump_length(instruction[2:n+1],label_list,line,10)

    bitstream= '11100'+jumpBin
    line_update=line+jumpDec

    return bitstream,error,line_update


def BNE_label(instruction:str,label_list,line:int):
    """Traduction de l'instruction BNE label
    """
    line_update=line+1
    n=len(instruction)
    jumpBin,jumpDec,error=jump_length(instruction[4:n+1],label_list,line,7)
    bitstream= '11010001'+jumpBin
    if virtual_register[8]!=0:
        line_update=line+jumpDec

    return bitstream,error,line_update

def BEQ_label(instruction:str,label_list,code_ASM,line:int):
    """Traduction de l'instruction B label
    """
    line_update=line+1
    n=len(instruction)
    jumpBin,jumpDec,error=jump_length(instruction[4:n+1],label_list,line,7)
    bitstream='11010000'+jumpBin
    if virtual_register[8]==0:
        line_update=line+jumpDec
        
    return bitstream,error,line_update


def jump_length(label:str,label_list:list,line:int,size:int):
    """Cette fonction prend l'instruction sans l'embranchement même conditionnelle\n
    Par exemple, si l'instruction première est BNE label, l'argument en entrée de cette fonction sera label\n
    Cette instruction renvoie le saut converti en binaire complément à 2"""
    jumpBin=''
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
        else:
            #Taille du saut en binaire complément à 2
            jumpBin=DecToBinCom(jumpDec,size)

    return jumpDec,jumpBin,error
