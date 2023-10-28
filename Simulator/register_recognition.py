from treatment import*

def register_recognition(instruction:str):
    """Reconnaissance du ou des registres dans l'instruction dans l'ordre où ils sont écrits qui doit être de type str\n
    Elle renvoie une liste des numéros en str des registres convertis en binaire d'une taille de 3\n
    Ainsi que les erreurs éventuelles"""

    n=len(instruction)

    #Suppression de l'action de l'instruction: si l'instruction est 'ADD R5,R6' alors la chaîne de caractère devient ' R5,R6'
    #Tout cela pour éviter les problèmes avec les instructions contenant des R dans leur action telles que EOR ou LDR
    instruction=instruction[3:n]
    iteration=instruction.count('R')
    register_dec=[]  #La liste des numéros des registres en décimal

    error=[]

    if iteration==0:
        error.append("There's no register in this instruction")
    
    else:
        for i in range(iteration):
            m=1
            register=''
            n_=len(instruction)
            while (instruction.find('R')+m<n_)and(instruction[instruction.find('R')+m].isdigit()):
                register+=instruction[instruction.find('R')+m:instruction.find('R')+m+1]
                m+=1
            instruction=instruction[0:instruction.find('R')]+instruction[instruction.find('R')+len(register):n]
            register_dec.append(int(register))

    #Mise en binaire des registres
    register_bin=[DecToBin(register_dec[i]) for i in range(len(register_dec))] #register_bin est une liste de str

    #Complétion des numéros binaires de registres par des 0, si nécessaires
    register_final=[]
    
    for i,j in enumerate(register_bin):

        d=3-len(register_bin[i]) #Différence entre la taille des numéros binaires des registres souhaités et obtenues précedemment
        if d>0:
            for k in range(d):
                j='0'+j
            register_final.append(j)
        elif d<0:
            error.append('Register R'+str(register_dec[i])+' is too big.')
        else:
            register_final.append(j)

    return register_final,error

def imm_recognition(instruction:str,size:int):
    """Reconnaissance d'un #imm3, #imm5 ou #imm8 dans l'instruction qui doit être de type str\n
    Size correspond à la taille du #imm possible soit 3,5 ou 8\n
    Elle renvoie le nombre correspondant à #imm3/5/8 en binaire str\n
    Ainsi que les erreurs éventuelles"""
    
    n=len(instruction)
    count=instruction.count('#')
    error=[]

    if count==0:
        error.append("There's no # before the number in this instruction.")
    #Acquisition du nombre de imm
    elif count>1:
        error.append("There's too much # in the instruction.")
    else:
        m=1
        imm=''
        if instruction[(instruction.find('#')+1)].isdigit==True:
            while (instruction.find('#')+m<n)and(instruction[instruction.find('#')+m].isdigit()):
                imm+=instruction[instruction.find('#')+m:instruction.find('#')+m+1]
                m+=1
        else:
            error.append("There's no number after #.")
    #Mise en binaire du nombre
    imm_bin=DecToBin(int(imm)) #imm_bin est un str

    #Complétion des numéros binaires de imm par des 0, si nécessaires
    imm_final=''
    d=size-len(imm_bin) #Différence entre la taille des numéros binaires des imm souhaités et obtenues précedemment
    if d>0:
        for k in range(d):
            imm_bin='0'+imm_bin
        imm_final=imm_bin
    elif d<0:
        error.append('Number #'+imm+' is too big for this instruction.')
    else:
        imm_final=imm_bin
    
    return imm_final,error
