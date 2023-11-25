from treatment import DecToBinCom
from virtual_register_fct import virtual_register

"""La génération du bitstream des instructions de branchement B.
"""

def B_instruct_bitstream(instruction:str,line:int):
    """Fonction référençant chaque possibilités pour un branchement:
    """
    #Ici on peut, au besoin, rajouter BGE, BLT, BGT, BLE
    if instruction[0:3]=='BEQ':
        #BEQ label
        bitstream=BEQ_label_bitstream(instruction,line)
    elif instruction[0:3]=='BNE':
        #BNE label
        bitstream=BNE_label_bitstream(instruction,line)
    elif instruction[0:3]=='BGE':
        #BNE label
        bitstream=BGE_label_bitstream(instruction,line)
    elif instruction[0:3]=='BLT':
        #BNE label
        bitstream=BLT_label_bitstream(instruction,line)
    elif instruction[0:3]=='BGT':
        #BNE label
        bitstream=BGT_label_bitstream(instruction,line)
    elif instruction[0:3]=='BLE':
        #BNE label
        bitstream=BLE_label_bitstream(instruction,line)
    elif instruction[0:2]=='B ':
        #B label
        bitstream=B_label_bitstream(instruction,line)

    return bitstream


def B_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction B label
    """ 
    

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[2:n+1],line,10)

    bitstream= '11100'+jumpBin

    return bitstream


def BNE_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction BNE label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream= '11010001'+jumpBin

    return bitstream

def BEQ_label_bitstream(instruction:str,code_ASM,line:int):
    """Traduction de l'instruction BEQ label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream='11010000'+jumpBin

    return bitstream

def BGE_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction BGE label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream= '11011010'+jumpBin

    return bitstream

def BLT_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction BLT label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream= '11011011'+jumpBin

    return bitstream

def BGT_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction BGT label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream= '11011100'+jumpBin

    return bitstream

def BLE_label_bitstream(instruction:str,line:int):
    """Traduction de l'instruction BLE label
    """

    n=len(instruction)
    jumpBin=jump_length_bitstream(instruction[4:n+1],line,7)
    bitstream= '11011101'+jumpBin

    return bitstream

def jump_length_bitstream(label:str,line:int,size:int):
    """Cette fonction prend l'instruction sans l'embranchement même conditionnelle\n
    Par exemple, si l'instruction première est BNE label, l'argument en entrée de cette fonction sera label\n
    Cette instruction renvoie le saut converti en binaire complément à 2"""

    from label_recognition import label_table
    jumpBin=''    
    index=label_table.index(label)
    #Taille du saut en décimale
    jumpDec=label_table[index+1]-line

    #Taille du saut en binaire complément à 2
    jumpBin=DecToBinCom(jumpDec,size)
    return jumpBin
