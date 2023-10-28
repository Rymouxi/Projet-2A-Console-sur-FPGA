virtual_memory=[]

def virtual_memory_init():
    for i in range(0,50,4):
        global virtual_memory
        virtual_memory.append([hex(i),'0x00000000'])


def virtual_memory_write(address,value):
    """Écrit dans la mémoire value à address\n
    Sachant que ces deux arguments doivent être de la forme 0x00000000 
    """
    global virtual_memory
    addresses=[ad[0] for ad in virtual_memory]    
    virtual_memory[addresses.index(address)][1]=value

def virtual_memory_read(address):
    """Retourne la valeur présente à address
    """
    global virtual_memory
    addresses=[ad[0] for ad in virtual_memory]   
    value=virtual_memory[addresses.index(address)][1]
    return value
