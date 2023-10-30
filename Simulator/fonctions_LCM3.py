from register_recognition import *
from treatment import *
from virtual_memory_fct import *
from virtual_register_fct import*

"""Il s'agit du fichier qui gère toutes les fonctions LCM3 à part les branchements B.\n
Quand les registres sont modifiés ils agissent sur la les registres virtuels pour savoir où ils en sont 
et renvoient un tableau indiquant quel(s) registre(s) il faut modifier et comment.\n
Quand une fonction modifie la mémoire de la carte c'est la même chose sauf que cette fois-ci, c'est seulement interne.
"""


def AND(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction AND
    """
    register_update=[]
    bitstream=''
    error=[]

    #AND Rd,Rm
    if len(register_recognition(instruction)[0])==2:
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:#Rd et Rm sont les numéros (en binaire) des registres dans AND
            Rd=register_recognition(instruction)[0][0]
            Rm=register_recognition(instruction)[0][1]

            #Les valeurs de Rd et Rm en décimales
            Rd_value=virtual_register[int(Rd,2)]
            Rm_value=virtual_register[int(Rm,2)]

            #Opération d'instruction AND en décimale
            and_value=Rd_value & Rm_value

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),and_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(int(Rd,2))
            register_update.append(and_value)

            #Bitstream
            bitstream='0100000000'+Rm+Rd

    else:
        error.append('Number of arguments in AND line '+str(line)+" doesn't match. AND instructions must be of form 'AND Rd,Rm'.")
        error.append(line)
    
    return bitstream,register_update,error


def LSL(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction LSL
    """
    register_update=[]
    bitstream=''
    error=[]

    #LSL Rd,Rm,#imm5
    if (len(register_recognition(instruction)[0])==2) and (instruction.count('#')>0):
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,5)[1])!=0:
            for i in range(len(imm_recognition(instruction,5)[1])):
                error.append(imm_recognition(instruction,5)[1][i])
                error.append(line)            
        else:
            #Rd, Rm et imm5 sont les numéros (en binaire) des registres dans AND
            Rd=register_recognition(instruction)[0][0]
            Rm=register_recognition(instruction)[0][1]
            imm5=imm_recognition(instruction,5)[0]

            #La valeur de Rm en décimale
            Rm_value=virtual_register[int(Rm,2)]

            #Opération d'instruction LSL en décimale
            lsl_value=Rm_value << int(imm5,2)

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),lsl_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(int(Rd,2))
            register_update.append(lsl_value)

            #Bitstream
            bitstream='00000'+Rm+Rd+imm5

    else:
        error.append("Number of argument in LSL line "+str(line)+" doesn't match. LSL instructions must be of form 'LSL Rd,Rm,#imm5'.")
        error.append(line)

    return bitstream,register_update,error


#---------Les instructions STR et LDR seront simulées en manipulant une mémoire virtuelle--------#

def STR(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de la mémoire virtuelle(en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction STR
    """
    register_update=[]
    bitstream=''
    error=[]

    #STR Rt,[Rn]
    if len(register_recognition(instruction)[0])==2:
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:
            #Rt et Rn sont les numéros (en binaire) des registres dans STR
            Rt=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]

            #Les valeurs de Rt et Rn en décimale
            Rt_value=virtual_register[int(Rt,2)]
            Rn_value=virtual_register[int(Rn,2)]
            
            #Simulation interne de la mémoire préalablement initialisée
            virtual_memory_write(hex(Rn_value),hex(Rt_value))

            #Bitstream
            bitstream= '0110000000'+Rn+Rt
        
    else:
        error.append("Number of arguments in STR line "+str(line)+" doesn't match. STR instructions must be of form 'STR Rt,[Rn]'.")
        error.append(line)

    return bitstream,register_update,error


def LDR(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de la mémoire virtuelle (en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction LDR
    """
    register_update=[]
    bitstream=''
    error=[]

    #LDR Rt,[Rn]
    if len(register_recognition(instruction)[0])==2:
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:
            #Rt et Rn sont les numéros (en binaire) des registres dans LDR
            Rt=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]

            #La valeur de Rt et Rn en décimale
            Rn_value=virtual_register[int(Rn,2)]

            #Simulation interne de la mémoire préalablement initialisée
            #value est en hexadécimale
            value=virtual_memory_read(hex(Rn_value))

            #Simulation interne des registres
            virtual_register_write(int(Rt,2),int(value,16))

            #Renvoi des informations nécessaires à la simulation
            register_update.append(Rt)
            register_update.append(int(value,16))

            #Bitstream
            bitstream= '0110100000'+Rn+Rt
        
        
    else:
        error.append("Number of arguments in LDR line "+str(line)+" doesn't match")
        error.append(line)

    return bitstream,register_update,error


def EOR(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction EOR
    """  
    register_update=[]
    bitstream=''
    error=[]

    #EOR Rd,Rm
    if len(register_recognition(instruction)[0])==2:
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:
            #Rd et Rm sont les numéros (en binaire) des registres dans LDR
            Rd=register_recognition(instruction)[0][0]
            Rm=register_recognition(instruction)[0][1]

            #Les valeurs de Rd et Rm en décimal
            Rd_value=virtual_register[int(Rd,2)]
            Rm_value=virtual_register[int(Rm,2)]

            #Opération d'instruction EOR en décimale
            eor_value=Rm_value ^ Rd_value

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),eor_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(int(Rd,2))
            register_update.append(eor_value)

            #Bitstream
            bitstream= '0100000001'+Rm+Rd
        
    else:
        error.append("Number of arguments in EOR line "+str(line)+" doesn't match. EOR instructions must be of form 'EOR Rd,Rm'.")
        error.append(line)

    return bitstream,register_update,error


def CMP(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction CMP\n
    Pour la simulation, on stocke le résultat de la comparaison dans le registre temporaire NZVC\n
    Le registre NZVC est le 9ème 
    """
    register_update=[]
    bitstream=''
    error=[]

    #CMP Rn,#imm8
    if (len(register_recognition(instruction)[0])==1)and(instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,8)[1])!=0:
            for i in range(len(imm_recognition(instruction,8)[1])):
                error.append(imm_recognition(instruction,8)[1][i])
                error.append(line)
        
        else:

            #Rn et imm8 sont les numéros (en binaire) des registres dans CMP
            Rn=register_recognition(instruction)[0][0]
            imm8=register_recognition(instruction,8)[0]

            #Valeur de Rn en décimale
            Rn_value=virtual_register[int(Rn,2)]

            #Opération d'instruction CMP en décimale
            cmp_value=abs(Rn_value-int(imm8,2))

            #Simulation interne des registres
            virtual_register_write(8,cmp_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(8)#Le registre 8 correspond au NZVC
            register_update.append(cmp_value)

            #Bitstream
            bitstream='00101'+Rn+imm8
        
    else:
        error.append("Number of arguments in CMP line "+str(line)+" doesn't match. CMP instructions must be of form 'CMP Rn,#imm8'.")

    return bitstream,register_update,error


def ADD(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction ADD
    """
    register_update=[]
    bitstream=''
    error=[]

    #ADD Rd,Rn,Rm
    if (len(register_recognition(instruction)[0])==3)and (instruction.count('#')==0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:
            #Rd, Rn et Rm sont les numéros (en binaire) des registres dans ADD
            Rd=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]
            Rm=register_recognition(instruction)[0][2]

            #Les valeurs de Rn et Rm en décimale
            Rn_value=virtual_register[int(Rn,2)]
            Rm_value=virtual_register[int(Rm,2)]

            #Opération d'instruction ADD en décimale
            add_value=Rn_value+Rm_value

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),add_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(int(Rd,2))
            register_update.append(add_value)

            #Bitstream
            bitstream='0001100'+Rm+Rn+Rd
    
    #ADD Rd,Rn,#immm3
    elif (len(register_recognition(instruction)[0])==2)and(instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,3)[1])!=0:
            for i in range(len(imm_recognition(instruction,3)[1])):
                error.append(imm_recognition(instruction,3)[1][i])
                error.append(line)
        else:
            #Rd, Rn et imm sont les numéros (en binaire) des registres dans ADD
            Rd=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]
            imm3=imm_recognition(instruction,3)[0]

            #La valeur de Rn en décimale
            Rn_value=virtual_register[int(Rn,2)]

            #Opération d'instruction ADD en décimale
            add_value=Rn_value+int(imm3,2)

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),add_value)

            #Renvoi des informations nécessaires à la simulation
            register_update.append(int(Rd,2))
            register_update.append(add_value)

            #Bitstream
            bitstream='0001110'+imm3+Rn+Rd
    
    #ADD Rd,#imm8
    elif (len(register_recognition(instruction)[0])==1) and (instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,8)[1])!=0:
            for i in range(len(imm_recognition(instruction,8)[1])):
                error.append(imm_recognition(instruction,8)[1][i])
                error.append(line)
        else:
            #Rd et imm sont les numéros (en binaire) des registres dans ADD
            Rd=register_recognition(instruction)[0][0]
            imm8=imm_recognition(instruction,8)[0]

            #La valeur de Rd en décimale
            Rd_value=virtual_register[int(Rd,2)]

            #Opération d'instruction ADD en décimale
            add_value=Rd_value+int(imm8,2)

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),add_value)

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(add_value)

            #Bitstream
            bitstream='00110'+Rd+imm8   

    else:
        error.append("There is not enough/too much arguments in ADD instruction line "+str(line))
        error.append(line)

    return bitstream,register_update,error


def SUB(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction SUB
    """

    register_update=[]
    bitstream=''
    error=[]

    #SUB Rd,Rn,Rm
    if (len(register_recognition(instruction)[0])==3)and (instruction.count('#')==0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        else:
            #Rd, Rn et Rm sont les numéros (en binaire) des registres dans SUB
            Rd=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]
            Rm=register_recognition(instruction)[0][2]

            #Les valeurs de Rn et Rm en décimale
            Rm_value=virtual_register[int(Rm,2)]
            Rn_value=virtual_register[int(Rn,2)]

            #Opération d'instruction SUB en décimale
            sub_value=Rn_value-Rm_value

            if sub_value<0:
                error.append("Registers values doesn't match for SUB instruction")
                error.append(line)
            else:
                #Simulation interne des registres
                virtual_register_write(int(Rd,2),sub_value)

                #Opération simulée sur Rd
                register_update.append(int(Rd,2))
                register_update.append(sub_value)

                bitstream='0001101'+Rm+Rn+Rd
    
    #SUB Rd,Rn,#immm3
    elif (len(register_recognition(instruction)[0])==2)and(instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,3)[1])!=0:
            for i in range(len(imm_recognition(instruction,3)[1])):
                error.append(imm_recognition(instruction,3)[1][i])
                error.append(line)
        else:
            #Rd, Rn et imm sont les numéros (en binaire) des registres dans SUB
            Rd=register_recognition(instruction)[0][0]
            Rn=register_recognition(instruction)[0][1]
            imm3=imm_recognition(instruction,3)[0]

            #La valeur de Rn et en décimale
            Rn_value=virtual_register[int(Rn,2)]

            #Opération d'instruction SUB en décimale
            sub_value=Rn_value-DecToBin(imm3)

            if sub_value<0:
                error.append("imm number is too big to substract to register R"+int(Rd,2))
                error.append(line)
            else:
                #Simulation interne des registres
                virtual_register_write(int(Rd,2),sub_value)

                #Opération simulée sur Rd
                register_update.append(int(Rd,2))
                register_update.append(sub_value)

                #Bitstream
                bitstream='0001111'+imm3+Rn+Rd
    
    #SUB Rd,#imm8
    elif (len(register_recognition(instruction)[0])==1) and (instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,8)[1])!=0:
            for i in range(len(imm_recognition(instruction,8)[1])):
                error.append(imm_recognition(instruction,8)[1][i])
                error.append(line)
        else:
            #Rd et imm sont les numéros (en binaire) des registres dans SUB
            Rd=register_recognition(instruction)[0][0]
            imm8=imm_recognition(instruction,8)[0]

            #La valeur de Rd et en décimale
            Rd_value=virtual_register[int(Rd,2)]

            #Opération d'instruction SUB en décimale
            sub_value=Rd_value-DecToBin(imm8)
            
            if sub_value<0:
                error.append("imm number is too big to substract to register R"+int(Rd,2))
                error.append(line)
            else:
                #Simulation interne des registres
                virtual_register_write(int(Rd,2),sub_value)

                #Opération simulée sur Rd
                register_update.append(int(Rd,2))
                register_update.append(sub_value)

                bitstream='00111'+Rd+imm8    

    else:
        error.append("There is not enough/too much arguments in SUB instruction line "+str(line))
        error.append(line)
        
    return bitstream,register_update,error


def MOV(instruction:str,line:int):
    """ Fonction renvoyant le bitstream, la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction MOV
    """

    register_update=[]
    bitstream=''
    error=[]

    #MOV Rd,Rm
    if (len(register_recognition(instruction))==2)and(instruction.find('#')==0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)

        else:
            #Rd et Rn sont les numéros (en binaire) des registres dans MOV
            Rd=register_recognition(instruction)[0][0]
            Rm=register_recognition(instruction)[0][1]

            #La valeur de Rm en decimale
            Rm_value=virtual_register[int(Rm,2)]

            #Simulation interne des registres
            virtual_register_write(int(Rd,2),Rm_value)

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(Rm_value,2)

            #Bitstream
            bitstream='0000000000'+Rm+Rd
    
    #MOV Rd,#imm8
    elif (len(register_recognition(instruction))==1)and(instruction.count('#')>0):
        #Détection d'erreurs
        if len(register_recognition(instruction)[1])!=0:
            for i in range(len(register_recognition(instruction)[1])):
                error.append(register_recognition(instruction)[1][i])
                error.append(line)
        elif len(imm_recognition(instruction,8)[1])!=0:
            for i in range(len(imm_recognition(instruction,8)[1])):
                error.append(imm_recognition(instruction,8)[1][i])
                error.append(line)

        else:
            #Rd et imm sont les numéros (en binaire) des registres dans MOV
            Rd=register_recognition(instruction)[0][0]
            imm8=imm_recognition(instruction,8)[0]          
            
            #Simulation interne des registres
            virtual_register_write(int(Rd,2),int(imm8,2))

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(imm8,2))

            #Bitstream
            bitstream='00100'+Rd+imm8
    else:
        error.append("There is not enough/too much arguments in MOV instruction line "+str(line))
        error.append(line)

    return bitstream,register_update,error
