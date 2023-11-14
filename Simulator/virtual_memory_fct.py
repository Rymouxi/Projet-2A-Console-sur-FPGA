"""virtual_memory est une liste contenant les adresses et les valeurs de ces adresses\n
Ces valeurs sont en décimal\n
virtual_memory est de la forme [adresse1,valeur1,adresse2,valeur2...]"""

virtual_memory=[]


def virtual_memory_init():
    for i in range(0,50):
        global virtual_memory
        virtual_memory.append(i)
        virtual_memory.append(0)


def virtual_memory_write(address,value):
    """Écrit dans la mémoire value à address\n
    Sachant que ces deux arguments doivent être de type int
    """
    global virtual_memory  
    virtual_memory[2*i+1]=value

def virtual_memory_read(address):
    """Retourne la valeur présente à address
    """
    global virtual_memory
    value=virtual_memory[2*i+1]
    return value
