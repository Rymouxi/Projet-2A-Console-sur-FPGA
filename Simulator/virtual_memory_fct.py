"""virtual_memory est une liste contenant les adresses et les valeurs de ces adresses\n
les addresses sont en hexadécimal: str commençant par '0x'\n
Ces valeurs sont en int\n
virtual_memory est de la forme [adresse1,valeur1,adresse2,valeur2...]"""

virtual_memory=[]

def virtual_memory_update(address,value):
    """Ajout d'une case mémoire
    address et value peuvent être sous n'importe quelle forme: décimal, binaire, hexadécimal"""
    global virtual_memory
    if type(address)==int:
        address=hex(address)
    if type(address)==str and address[0:2]=='0b':
        address=hex(int(address,2))
    if type(address)==str and address[0:2]=='0x':
        if   int('20000000',16)>int(address,16)>int('80000000',16):
            if type(value)==str and value[0:2]=='0x':
                value=int(value,16)
            if type(value)==str and value[0:2]=='0b':
                value=int(value,2)
            if type(value)==int:
                if virtual_memory.count(address)==0:
                    virtual_memory.append(address)
                    virtual_memory.append(value)
                elif virtual_memory.count(address)>0:
                    virtual_memory[virtual_memory.index(address)+1]=value
                virtual_memory_sort()
                return ""
        else:
            return "The address is not between 0x20000000 and 0x80000000"

def virtual_memory_read(address):
    value=""
    global virtual_memory
    if type(address)==int:
        address=hex(address)
    if type(address)==str and address[0:2]=='0b':
        address=hex(int(address,2))
    if type(address)==str and address[0:2]=='0x':
        if int('20000000',16)<int(address,16)<int('80000000',16):
            if virtual_memory.count(address)==0:
                return 0
            else:
                return virtual_memory[virtual_memory.index(address)+1]
        else:
            return "The address is not between 0x20000000 and 0x80000000"
            
def virtual_memory_sort():

    global virtual_memory
    n=len(virtual_memory)
    #addresses est la liste des adresses mélangées en int
    addresses_int=[int(virtual_memory[i],16) for i in range(0,len(virtual_memory),2)]
    #addresses_hex est la liste des adresses triées en hexadécimal
    addresses_hex=[]
    #tri de la liste d'adresses
    addresses_int=sorted(addresses_int)
    for address in addresses_int:
        addresses_hex.append(hex(address))
    i=0
    copy=[]
    for address_hex in addresses_hex:

        copy.append(address_hex)
        copy.append(virtual_memory[virtual_memory.index(address_hex)+1])
        i+=2
    for i in range(0,n):
        virtual_memory[i]=copy[i]

def virtual_memory_reset():
    global virtual_memory
    while len(virtual_memory)!=0:
        virtual_memory.pop()

def virtual_memory_address_check(address):
    if type(address)==int:
        address=hex(address)
    if type(address)==str and address[0:2]=='0b':
        address=hex(int(address,2))
    if type(address)==str and address[0:2]=='0x':
        if int('20000000',16)<int(address,16)<int('80000000',16):
            return True
        else:
            return False