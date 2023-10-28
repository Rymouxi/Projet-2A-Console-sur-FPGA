from register_recognition import *
from treatment import *
from Interface import reg_read


#On travaille toujours avec des chaînes de caractères
#Les fonctions appelées renvoient des chaînes de caractère

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

            #Les valeurs de Rd et Rm en binaire
            Rd_value=reg_read(int(Rd,2))
            Rm_value=reg_read(int(Rm,2))

            #Opération simulée sur Rd et Rm
            register_update.append(int(Rd,2))
            register_update.append(int(Rd_value and Rm_value,2))

            bitstream='0100000000'+Rm+Rd

    else:
        error.append('Number of arguments in AND line '+str(line)+" doesn't match. AND instructions must be of form 'AND Rd,Rm'.")
        error.append(line)
        exit()
    
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

            #Les valeurs de Rd et Rm en binaire
            Rd_value=reg_read(int(Rd,2))
            Rm_value=reg_read(int(Rm,2))

            #Opération simulée sur Rd et Rm
            register_update.append(int(Rd,2))
            register_update.append(int(Rm_value,2)<< int(imm5,2))

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

            #Les valeurs de Rd et Rm en binaire
            Rt_value=reg_read(int(Rt,2))
            Rn_value=reg_read(int(Rn,2))

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

            #Les valeurs de Rt et Rn en binaire
            Rt_value=reg_read(int(Rt,2))
            Rn_value=reg_read(int(Rn,2))
            
            #Simulation interne de la mémoire préalablement initialisée
            value=virtual_memory_read(hex(int(Rn_value)))
            register_update.append(Rt)
            register_update.append(int(value,16))
            
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

            #Les valeurs de Rd et Rm en binaire
            Rd_value=reg_read(int(Rd,2))
            Rm_value=reg_read(int(Rm,2))

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rm_value,2)^ int(Rd_value,2))

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

            #Valeur de Rn en binaire
            Rn_value=reg_read(int(Rn,2))

            register_update.append(8)#Le registre 8 correspond au NZVC
            register_update.append(abs(int(Rn_value,2)-int(imm8,2)))

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

            #Les valeurs de Rn et Rm en binaire
            Rn_value=reg_read(int(Rn,2))
            Rm_value=reg_read(int(Rm,2))


            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rn_value,2) + int(Rm_value,2))

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
            imm=imm_recognition(instruction,3)[0]

            #La valeur de Rn en binaire
            Rn_value=reg_read(int(Rn,2))

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rn_value,2) + int(imm,2))

            bitstream='0001110'+imm+Rn+Rd
    
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
            imm=imm_recognition(instruction,8)[0]

            #La valeur de Rd en binaire
            Rd_value=reg_read(int(Rd,2))

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rd_value,2) + int(imm,2))

            bitstream='00110'+Rd+imm    

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

            #Les valeurs de Rn et Rm en binaire
            Rn_value=reg_read(int(Rn,2))
            Rm_value=reg_read(int(Rm,2))


            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rn_value,2) - int(Rm_value,2))

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
            imm=imm_recognition(instruction,3)[0]

            if int(imm,2)>int(Rd_value,2):
                error.append("imm number is too big to substract to register R"+int(Rd,2))
                error.append(line)
            else:
                #La valeur de Rn et en binaire
                Rn_value=reg_read(int(Rn,2))

                #Opération simulée sur Rd
                register_update.append(int(Rd,2))
                register_update.append(int(Rn_value,2) - int(imm,2))

                bitstream='0001111'+imm+Rn+Rd
    
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
            imm=imm_recognition(instruction,8)[0]

            #La valeur de Rd et en binaire
            Rd_value=reg_read(int(Rd,2))
            
            if int(imm,2)>int(Rd_value,2):
                error.append("imm number is too big to substract to register R"+int(Rd,2))
                error.append(line)
            else:
                #Opération simulée sur Rd
                register_update.append(int(Rd,2))
                register_update.append(int(Rd_value,2) - int(imm,2))

                bitstream='00111'+Rd+imm    

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

            #La valeur de Rm en binaire
            Rm_value=reg_read(int(Rm,2))

            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(Rm_value,2))

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
            imm=imm_recognition(instruction,8)[0]          
            
            #Opération simulée sur Rd
            register_update.append(int(Rd,2))
            register_update.append(int(imm,2))

            bitstream='00100'+Rd+imm  
    else:
        error.append("There is not enough/too much arguments in MOV instruction line "+str(line))
        error.append(line)
    return bitstream,register_update,error
