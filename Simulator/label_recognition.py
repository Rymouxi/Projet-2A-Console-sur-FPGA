from treatment import *

def label_recognition(split_instruction):
    """Code ASM brute est le code en entier avec les sauts de ligne\n
    En considérant que l'instruction est de la forme:\nlabel:\n
    Ce qui est retourné est une liste des label suivi du numéro des lignes auquels ils sont:\n
    listelabel=[label1,label1line,label2,label2line,...,labeln,labelnline]
    """
    #Séparation du code en lignes d'instruction
    listelabel=[]
    for line,instruction in enumerate(split_instruction):
        #Recherche des ':' dans l'instruction
        if instruction.count(":")==1:
            listelabel.append(instruction[0:instruction.find(':')])
            listelabel.append(line+1)
    return listelabel
 
