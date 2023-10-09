def Register_recognition(instruction):

    n=len(instruction)
    iteration=instruction.count('R')
    if iteration==0:
        return -1
    l=[]  #La liste des numéros des registres en décimal
    for i in range(iteration):
        m=1
        nombre=''
        while instruction[instruction.find('R')+m].isdigit():
            nombre+=instruction[instruction.find('R')+m:instruction.find('R')+m+1]
            m+=1
        len_Registre=len(nombre)
        instruction=instruction[0:instruction.find('R')]+instruction[instruction.find('R')+len_Registre:n]
        l.append(int(nombre))

    return l

def htag_recognition(instruction):
    #En supposant qu'il n'y en ait un seul et qu'il est à la fin
    n=len(instruction)
    index=instruction.find('#')
    if index==-1:
        return -1
    m=1
    nombre=''
    while (instruction.find('#')+m<n)and(instruction[instruction.find('#')+m].isdigit()):
        nombre+=instruction[instruction.find('#')+m:instruction.find('#')+m+1]
        m+=1
    return int(nombre)