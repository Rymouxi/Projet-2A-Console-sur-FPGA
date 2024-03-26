from register_recognition import *
from treatment import *
from virtual_memory_fct import *
from virtual_register_fct import*

"""Il s'agit du fichier qui gère toutes les fonctions LCM3 lors de la génération du BitStream à part les branchements B.\n
Chaque fonction renvoie le code binaire correspondant à l'instruction qui lui et propre.\n
"""


def AND_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction AND
    """
    bitstream=''

    #AND Rd,Rm   
    #Rd et Rm sont les numéros (en binaire) des registres dans AND
    Rd,Rm=register_recognition(instruction)
    #Bitstream
    bitstream='0100000000'+Rm+Rd
    
    return bitstream


def LSL_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction LSL
    """
    bitstream=''

    #LSL Rd,Rm,#imm5
    
    #Rd, Rm et imm5 sont les numéros (en binaire) des registres dans AND
    Rd,Rm=register_recognition(instruction)
    imm5=imm_recognition(instruction,5)[0]

    #Bitstream
    bitstream='00000'+Rm+Rd+imm5

    return bitstream


#---------Les instructions STR et LDR seront simulées en manipulant une mémoire virtuelle--------#

def STR_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de la mémoire virtuelle(en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction STR
    """
    bitstream=''
    #STR Rt,[Rn] 
    #Rt et Rn sont les numéros (en binaire) des registres dans STR
    Rt,Rn=register_recognition(instruction)

    #Bitstream
    bitstream= '0110000000'+Rn+Rt
        
    return bitstream


def LDR_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de la mémoire virtuelle (en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction LDR
    """

    bitstream=''

   #LDR Rt,[Rn]
    #Rt et Rn sont les numéros (en binaire) des registres dans LDR
    Rt,Rn=register_recognition(instruction)
    #Bitstream
    bitstream= '0110100000'+Rn+Rt
        
    return bitstream


def EOR_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction EOR
    """  
    bitstream=''

    #EOR Rd,Rm
    #Rd et Rm sont les numéros (en binaire) des registres dans LDR
    Rd,Rm=register_recognition(instruction)
    #Bitstream
    bitstream= '0100000001'+Rm+Rd
        
    return bitstream


def CMP_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction CMP\n 
    """
    bitstream=''
    R_count=instruction.count('R')
    count_imm=instruction.count('#')
    #CMP Rn,#imm8
    #Rn et imm8 sont les numéros (en binaire) des registres dans CMP
    if R_count==1 and count_imm==1:
        Rn=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8) 
        #Bitstream
        bitstream='00101'+Rn+imm8
        
    if R_count==2 and count_imm==0:
        Rn=register_recognition(instruction)[0]
        Rm=register_recognition(instruction)[1]
        #Bitstream
        bitstream='0100001010' +Rm+Rn

    return bitstream


def ADD_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction ADD
    """
    bitstream=''
    R_count=instruction.count('R')
    #ADD Rd,Rn,Rm
    if R_count==3:

        #Rd, Rn et Rm sont les numéros (en binaire) des registres dans ADD
        Rd,Rn,Rm=register_recognition(instruction)
    
        #Bitstream
        bitstream='0001100'+Rm+Rn+Rd
    
    #ADD Rd,Rn,#immm3
    elif R_count==2:
        
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans ADD
        Rd,Rn=register_recognition(instruction)
        imm3=imm_recognition(instruction,3)

        #Bitstream
        bitstream='0001110'+imm3+Rn+Rd
    
    #ADD Rd,#imm8
    elif R_count==1:
        
        #Rd et imm sont les numéros (en binaire) des registres dans ADD
        Rd=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8)

        #Bitstream
        bitstream='00110'+Rd+imm8   

    return bitstream


def SUB_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction SUB
    """
    bitstream=''
    R_count=instruction.count('R')

    #SUB Rd,Rn,Rm
    if R_count==3:
        
        #Rd, Rn et Rm sont les numéros (en binaire) des registres dans SUB
        Rd,Rn,Rm=register_recognition(instruction)
        
        bitstream='0001101'+Rm+Rn+Rd
    
    #SUB Rd,Rn,#immm3
    elif R_count==2:
        
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans SUB
        Rd,Rn=register_recognition(instruction)
        imm3=imm_recognition(instruction,3)

        #Bitstream
        bitstream='0001111'+imm3+Rn+Rd
    
    #SUB Rd,#imm8
    elif R_count==1:
       
        #Rd et imm sont les numéros (en binaire) des registres dans SUB
        Rd=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8)

        bitstream='00111'+Rd+imm8    
    
    return bitstream


def MOV_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction MOV
    """

    bitstream=''
    R_count=instruction.count('R')

    #MOV Rd,Rm
    if R_count==2:
        
        #Rd et Rn sont les numéros (en binaire) des registres dans MOV
        Rd,Rm=register_recognition(instruction)
        
        #Bitstream
        bitstream='0000000000'+Rm+Rd
    
    #MOV Rd,#imm8
    elif R_count==1:
       
        #Rd et imm sont les numéros (en binaire) des registres dans MOV
        Rd=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8)        
        
        #Bitstream
        bitstream='00100'+Rd+imm8
    
    return bitstream
