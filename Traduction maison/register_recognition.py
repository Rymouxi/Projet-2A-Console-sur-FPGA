from DecToBin import*

def register_recognition(instruction:str):
    """Reconnaissance du ou des registres dans l'instruction dans l'ordre où ils sont écrits qui doit être de type str\n
    Elle renvoie une liste des numéros en str des registres convertis en binaire d'une taille de 3"""
    n=len(instruction)
    iteration=instruction.count('R')
    if iteration==0:
        return -1
    register_dec=[]  #La liste des numéros des registres en décimal
    if instruction.find('R')<4:
        instruction=instruction[3:n]
        iteration-=1
    for i in range(iteration):
        m=1
        register=''
        n_=len(instruction)
        while (instruction.find('R')+m<n_)and(instruction[instruction.find('R')+m].isdigit()):
            register+=instruction[instruction.find('R')+m:instruction.find('R')+m+1]
            m+=1
        len_register=len(register)
        instruction=instruction[0:instruction.find('R')]+instruction[instruction.find('R')+len_register:n]
        register_dec.append(int(register))

    #Mise en binaire des registres
    register_bin=[str(DecToBin(register_dec[i])) for i in range(len(register_dec))] #register_bin est une liste de str

    #Complétion des numéros binaires de registres par des 0, si nécessaires
    register_final=[]
    for i,j in enumerate(register_bin):
        d=3-len(register_bin[i]) #Différence entre la taille des numéros binaires des registres souhaités et obtenues précedemment
        if d>0:
            for k in range(d):
                j='0'+j
            register_final.append(j)
        elif d<0:
            print('Le registre R',register_dec[i],' est trop grand pour la convention LCM3')
            exit()
        else:
            register_final.append(j)

    return register_final

def htag_recognition(instruction:str,size:int):
    """Reconnaissance d'un #imm3 ou #imm8 dans l'instruction qui doit être de type str\n
    Size correspond à la taille du #imm possible soit 3,5 ou 8\n
    Elle renvoie le nombre correspondant à #imm3/8 en int\n
    En supposant qu'il n'y en ait un seul et qu'il est à la fin"""
    n=len(instruction)
    index=instruction.find('#')
    if index==-1:
        return -1
    #Acquisition du nombre de imm
    m=1
    imm=''
    while (instruction.find('#')+m<n)and(instruction[instruction.find('#')+m].isdigit()):
        imm+=instruction[instruction.find('#')+m:instruction.find('#')+m+1]
        m+=1
    
    #Mise en binaire des registres
    imm_bin=str(DecToBin(int(imm))) #imm_bin est un str

    #Complétion des numéros binaires de imm par des 0, si nécessaires
    imm_final=[]
    d=size-len(imm_bin) #Différence entre la taille des numéros binaires des imm souhaités et obtenues précedemment
    if d>0:
        for k in range(d):
            imm_bin='0'+imm_bin
        imm_final=imm_bin
    elif d<0:
        print('Le nombre #',imm,' est trop grand pour la convention LCM3')
        exit()
    else:
        imm_final=imm_bin
    
    return imm_final
