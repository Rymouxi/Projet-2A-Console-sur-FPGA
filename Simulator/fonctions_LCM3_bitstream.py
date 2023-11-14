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
    Rd=register_recognition(instruction)[0][0]
    Rm=register_recognition(instruction)[0][1]

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
    Rd=register_recognition(instruction)[0][0]
    Rm=register_recognition(instruction)[0][1]
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
    Rt=register_recognition(instruction)[0][0]
    Rn=register_recognition(instruction)[0][1]

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
    Rt=register_recognition(instruction)[0][0]
    Rn=register_recognition(instruction)[0][1]

    #Bitstream
    bitstream= '0110100000'+Rn+Rt
        
    return bitstream


def EOR_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction EOR
    """  
    bitstream=''

    #EOR Rd,Rm
    
    #Rd et Rm sont les numéros (en binaire) des registres dans LDR
    Rd=register_recognition(instruction)[0][0]
    Rm=register_recognition(instruction)[0][1]

    #Bitstream
    bitstream= '0100000001'+Rm+Rd
        
    return bitstream


def CMP_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction CMP\n 
    """
    bitstream=''

    #CMP Rn,#imm8

    #Rn et imm8 sont les numéros (en binaire) des registres dans CMP
    Rn=register_recognition(instruction)[0][0]
    imm8=imm_recognition(instruction,8)[0]
           
    #Bitstream
    bitstream='00101'+Rn+imm8
           
    return bitstream


def ADD_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction ADD
    """

    bitstream=''


    #ADD Rd,Rn,Rm
    if (len(register_recognition(instruction)[0])==3)and (instruction.count('#')==0):

        #Rd, Rn et Rm sont les numéros (en binaire) des registres dans ADD
        Rd=register_recognition(instruction)[0][0]
        Rn=register_recognition(instruction)[0][1]
        Rm=register_recognition(instruction)[0][2]
    
        #Bitstream
        bitstream='0001100'+Rm+Rn+Rd
    
    #ADD Rd,Rn,#immm3
    elif (len(register_recognition(instruction)[0])==2)and(instruction.count('#')>0):
        
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans ADD
        Rd=register_recognition(instruction)[0][0]
        Rn=register_recognition(instruction)[0][1]
        imm3=imm_recognition(instruction,3)[0]

        #Bitstream
        bitstream='0001110'+imm3+Rn+Rd
    
    #ADD Rd,#imm8
    elif (len(register_recognition(instruction)[0])==1) and (instruction.count('#')>0):
        
        #Rd et imm sont les numéros (en binaire) des registres dans ADD
        Rd=register_recognition(instruction)[0][0]
        imm8=imm_recognition(instruction,8)[0]

        #Bitstream
        bitstream='00110'+Rd+imm8   

    return bitstream


def SUB_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction SUB
    """

    bitstream=''


    #SUB Rd,Rn,Rm
    if (len(register_recognition(instruction)[0])==3)and (instruction.count('#')==0):
        
        #Rd, Rn et Rm sont les numéros (en binaire) des registres dans SUB
        Rd=register_recognition(instruction)[0][0]
        Rn=register_recognition(instruction)[0][1]
        Rm=register_recognition(instruction)[0][2]
        
        bitstream='0001101'+Rm+Rn+Rd
    
    #SUB Rd,Rn,#immm3
    elif (len(register_recognition(instruction)[0])==2)and(instruction.count('#')>0):
        
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans SUB
        Rd=register_recognition(instruction)[0][0]
        Rn=register_recognition(instruction)[0][1]
        imm3=imm_recognition(instruction,3)[0]

        #Bitstream
        bitstream='0001111'+imm3+Rn+Rd
    
    #SUB Rd,#imm8
    elif (len(register_recognition(instruction)[0])==1) and (instruction.count('#')>0):
       
        #Rd et imm sont les numéros (en binaire) des registres dans SUB
        Rd=register_recognition(instruction)[0][0]
        imm8=imm_recognition(instruction,8)[0]

        bitstream='00111'+Rd+imm8    

    
    return bitstream


def MOV_bitstream(instruction:str,line:int):
    """ Fonction renvoyant le bitstream pour l'instruction MOV
    """

    bitstream=''


    #MOV Rd,Rm
    if (len(register_recognition(instruction)[0])==2)and(instruction.count('#')==0):
        
        #Rd et Rn sont les numéros (en binaire) des registres dans MOV
        Rd=register_recognition(instruction)[0][0]
        Rm=register_recognition(instruction)[0][1]
        
        #Bitstream
        bitstream='0000000000'+Rm+Rd
    
    #MOV Rd,#imm8
    elif (len(register_recognition(instruction)[0])==1)and(instruction.count('#')>0):
       
        #Rd et imm sont les numéros (en binaire) des registres dans MOV
        Rd=register_recognition(instruction)[0][0]
        imm8=imm_recognition(instruction,8)[0]          
        
        
        #Bitstream
        bitstream='00100'+Rd+imm8
    
    return bitstream
