from register_recognition import *
from treatment import *
from virtual_memory_fct import *
from virtual_register_fct import*

"""Il s'agit du fichier qui gère toutes les fonctions LCM3 en mode simulation à part les branchements B.\n
Quand les registres sont modifiés ils agissent sur la les registres virtuels pour savoir où ils en sont 
et renvoient un tableau indiquant quel(s) registre(s) il faut modifier et comment.\n
Quand une fonction modifie la mémoire de la carte c'est la même chose sauf que cette fois-ci, c'est seulement interne.
"""


def AND_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction AND
    """
    register_update=[]

    #Rd et Rm sont les numéros (en binaire) des registres dans AND
    Rd,Rm=register_recognition(instruction)

    #Les valeurs de Rd et Rm en décimales
    Rd_value=virtual_register[int(Rd,2)]
    Rm_value=virtual_register[int(Rm,2)]

    #Opération d'instruction AND en décimale
    and_value=(Rd_value & Rm_value)%(2**32)

    #Simulation interne des registres
    virtual_register_write(int(Rd,2),and_value)

    #Renvoi des informations nécessaires à la simulation
    register_update.extend([int(Rd,2),and_value])

    return register_update


def LSL_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction LSL
    """
    register_update=[]

    #LSL Rd,Rm,#imm5
    #Rd, Rm et imm5 sont les numéros (en binaire) des registres dans AND
    Rd,Rm=register_recognition(instruction)
    imm5=imm_recognition(instruction,5)

    #La valeur de Rm en décimale
    Rm_value=virtual_register[int(Rm,2)]

    #Opération d'instruction LSL en décimale
    lsl_value=(Rm_value << int(imm5,2))%(2**32)

    #Simulation interne des registres
    virtual_register_write(int(Rd,2),lsl_value)

    #Renvoi des informations nécessaires à la simulation
    register_update.extend([int(Rd,2),lsl_value])


    return register_update


#---------Les instructions STR et LDR seront simulées en manipulant une mémoire virtuelle--------#

def STR_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de la mémoire virtuelle(en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction STR
    """
    register_update=[]
    memory_update=[]
    error_simu=[]
    error_count=0

    #STR Rt,[Rn]
    if virtual_memory_address_check(virtual_register[int(register_recognition(instruction)[1],2)]):
        error_simu.extend([virtual_memory_address_check(virtual_register[int(register_recognition(instruction)[1],2)]),line])
        error_count+=1 
    if error_count==0:
        #Rt et Rn sont les numéros (en binaire) des registres dans STR
        Rt,Rn=register_recognition(instruction)

        #Les valeurs de Rt et Rn en décimale
        Rt_value=virtual_register[int(Rt,2)]
        Rn_value=virtual_register[int(Rn,2)]
        
        #Simulation interne de la mémoire préalablement initialisée
        virtual_memory_update(hex(Rn_value),hex(Rt_value))

        #Rendu externe de la mémoire
        memory_update.extend([Rn_value,Rt_value])

    return memory_update,error_simu


def LDR_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de la mémoire virtuelle (en attente)\n
    Ainsi que les erreurs éventuelles pour l'instruction LDR
    """
    register_update=[]
    error_count=0
    error_simu=[]

    #LDR Rt,[Rn]
    if type(virtual_memory_read(virtual_register[register_recognition(instruction)[1]]))==str:
        error_simu.append(virtual_memory_read(register_recognition(instruction)[0][1]))
        error_simu.append(line) 
        error_count+=1
    if error_count==0:
        #Rt et Rn sont les numéros (en binaire) des registres dans LDR
        Rt,Rn=register_recognition(instruction)

        #La valeur de Rt et Rn en décimale
        Rn_value=virtual_register[int(Rn,2)]

        #Simulation interne de la mémoire préalablement initialisée
        #value est en int
        value=virtual_memory_read(Rn_value)

        #Simulation interne des registres
        virtual_register_write(int(Rt,2),value)

        #Renvoi des informations nécessaires à la simulation
        register_update.extend([int(Rt,2),value])
            
    return register_update,error_simu


def EOR_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction EOR
    """  
    register_update=[]

    #EOR Rd,Rm
    #Rd et Rm sont les numéros (en binaire) des registres dans LDR
    Rd,Rm=register_recognition(instruction)

    #Les valeurs de Rd et Rm en décimal
    Rd_value=virtual_register[int(Rd,2)]
    Rm_value=virtual_register[int(Rm,2)]

    #Opération d'instruction EOR en décimale
    eor_value=(Rm_value ^ Rd_value)%(2**32)

    #Simulation interne des registres
    virtual_register_write(int(Rd,2),eor_value)

    #Renvoi des informations nécessaires à la simulation
    register_update.extend([int(Rd,2),eor_value])
 

    return register_update


def CMP_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction CMP\n
    Pour la simulation, on stocke le résultat de la comparaison dans le registre temporaire NZVC\n
    Le registre NZVC est le 9ème 
    """
    register_update=[]

    #CMP Rn,#imm8
    #Rn et imm8 sont les numéros (en binaire) des registres dans CMP
    Rn=register_recognition(instruction)[0]
    imm8=imm_recognition(instruction,8)

    #Valeur de Rn en décimale
    Rn_value=virtual_register[int(Rn,2)]

    #Résultat de la comparaison
    cmp_value=Rn_value-int(imm8,2)

    #Simulation interne des registres
    virtual_register_write(8,cmp_value)

    #Renvoi des informations nécessaires à la simulation
    register_update.extend([8,cmp_value])#Le registre 8 correspond au NZVC
        
    return register_update


def ADD_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction ADD
    """
    register_update=[]
    count_R=instruction.count('R')

    #ADD Rd,Rn,Rm
    if count_R==3:
        #Rd, Rn et Rm sont les numéros (en binaire) des registres dans ADD
        Rd,Rn,Rm=register_recognition(instruction)

        #Les valeurs de Rn et Rm en décimale
        Rn_value=virtual_register[int(Rn,2)]
        Rm_value=virtual_register[int(Rm,2)]

        #Opération d'instruction ADD en décimale
        add_value=(Rn_value+Rm_value)%(2**32)

        #Simulation interne des registres
        virtual_register_write(int(Rd,2),add_value)

        #Renvoi des informations nécessaires à la simulation
        register_update.extend([int(Rd,2),add_value])

    
    #ADD Rd,Rn,#immm3
    elif count_R==2:
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans ADD
        Rd,Rn=register_recognition(instruction)
        imm3=imm_recognition(instruction,3)

        #La valeur de Rn en décimale
        Rn_value=virtual_register[int(Rn,2)]

        #Opération d'instruction ADD en décimale
        add_value=(Rn_value+int(imm3,2))%(2**32)

        #Simulation interne des registres
        virtual_register_write(int(Rd,2),add_value)

        #Renvoi des informations nécessaires à la simulation
        register_update.extend([int(Rd,2),add_value])


    
    #ADD Rd,#imm8
    elif count_R==1:
        #Rd et imm sont les numéros (en binaire) des registres dans ADD
        Rd=register_recognition(instruction)
        imm8=imm_recognition(instruction,8)

        #La valeur de Rd en décimale
        Rd_value=virtual_register[int(Rd,2)]

        #Opération d'instruction ADD en décimale
        add_value=(Rd_value+int(imm8,2))%(2**32)

        #Simulation interne des registres
        virtual_register_write(int(Rd,2),add_value)

        #Opération simulée sur Rd
        register_update.extend([int(Rd,2),add_value])

    return register_update


def SUB_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction SUB
    """

    register_update=[]
    error_simu=[]
    count_R=instruction.count('R')

    #SUB Rd,Rn,Rm
    if count_R==3:
            #Rd, Rn et Rm sont les numéros (en binaire) des registres dans SUB
            Rd,Rn,Rm=register_recognition(instruction)

            #Les valeurs de Rn et Rm en décimale
            Rm_value=virtual_register[int(Rm,2)]
            Rn_value=virtual_register[int(Rn,2)]

            #Opération d'instruction SUB en décimale
            sub_value=Rn_value-Rm_value

            if sub_value<0:
                error_simu.extend(["Registers values doesn't match for SUB instruction",line])
            else:
                #Simulation interne des registres
                virtual_register_write(int(Rd,2),sub_value%(2**32))

                #Opération simulée sur Rd
                register_update.extend([int(Rd,2),sub_value%(2**32)])

    
    #SUB Rd,Rn,#immm3
    elif count_R==2:
        #Rd, Rn et imm sont les numéros (en binaire) des registres dans SUB
        Rd,Rn=register_recognition(instruction)
        imm3=imm_recognition(instruction,3)

        #La valeur de Rn et en décimale
        Rn_value=virtual_register[int(Rn,2)]

        #Opération d'instruction SUB en décimale
        sub_value=Rn_value-int(imm3,2)

        if sub_value<0:
            error_simu.extend(["imm number is too big to substract to register R"+str(int(Rd,2)),line])
        else:
            #Simulation interne des registres
            virtual_register_write(int(Rd,2),sub_value%(2**32))

            #Opération simulée sur Rd
            register_update.extend([int(Rd,2),sub_value%(2**32)])
    
    #SUB Rd,#imm8
    elif count_R==1:
        #Rd et imm sont les numéros (en binaire) des registres dans SUB
        Rd=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8)

        #La valeur de Rd et en décimale
        Rd_value=virtual_register[int(Rd,2)]

        #Opération d'instruction SUB en décimale
        sub_value=Rd_value-int(imm8,2)
        
        if sub_value<0:
            error_simu.extend(["imm number is too big to substract to register R"+str(int(Rd,2)),line])
        else:
            #Simulation interne des registres
            virtual_register_write(int(Rd,2),sub_value%(2**32))

            #Opération simulée sur Rd
            register_update.extend([int(Rd,2),sub_value%(2**32)])
        
    return register_update,error_simu


def MOV_simu(instruction:str,line:int):
    """ Fonction renvoyant la mise à jour de registres\n
    Ainsi que les erreurs éventuelles pour l'instruction MOV
    """

    register_update=[]
    count_R=instruction.count('R')

    #MOV Rd,Rm
    if count_R==2:
        #Rd et Rn sont les numéros (en binaire) des registres dans MOV
        Rd,Rm=register_recognition(instruction)[0]

        #La valeur de Rm en decimale
        Rm_value=virtual_register[int(Rm,2)]

        #Simulation interne des registres
        virtual_register_write(int(Rd,2),Rm_value)

        #Opération simulée sur Rd
        register_update.extend([int(Rd,2),Rm_value])

    #MOV Rd,#imm8
    elif count_R==1:
        #Rd et imm sont les numéros (en binaire) des registres dans MOV
        Rd=register_recognition(instruction)[0]
        imm8=imm_recognition(instruction,8)       
    
        #Simulation interne des registres
        virtual_register_write(int(Rd,2),int(imm8,2))

        #Opération simulée sur Rd
        register_update.extend([int(Rd,2),int(imm8,2)])

    return register_update
