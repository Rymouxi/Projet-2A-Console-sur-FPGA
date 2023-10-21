def DecToBin(Number:int):
    """Number doit être un int \n
    Elle renvoie ce même nombre converti en binaire"""
    Binary=''
    Copy=Number
    if Copy==0:
        return '0'
    while Copy!=1:
        if Copy%2==0:
            Binary+='0'
        else:
            Binary+='1'
        Copy=Copy//2
    if Copy%2==0:
        Binary+='0'
    else:
        Binary+='1'
        
    return Binary[::-1]


def DecToBinCom(Number:int,size:int):
    """Conversion de Number qui est un int relatif\n
    size correspond à la taille du nombre que l'on veut\n
    sachant que cette fonction renvoie la valeur binaire de Number\n
    et la taille de cette chaîne de caractère est size+1
    """
    BinaryCom=''
    Copy=Number
    #Vérification que 2**size est supérieur ou égal à Number
    if 2**size<Number:
        print("The Size doesn't match the Number")
        exit()
    
    #Séparation de la fonction dépendamment du signe du Nombre
    if Number<0:
        Copy=-1*Copy
        Binary=DecToBin(Copy)
        d=size-len(Binary)
        if d>0:
            for i in range(d):
                Binary='0'+Binary
        BinaryCopy=''
        for i in range(len(Binary)):
            if Binary[i]=='0':
                BinaryCopy+='1'
            elif Binary[i]=='1':
                BinaryCopy+='0'
        BinaryCom=format(int(BinaryCopy,2)+int('1',2),'b')
    elif Number>=0:
        Binary=DecToBin(Copy)
        d=size-len(Binary)
        if d>0:
            for i in range(d):
                Binary='0'+Binary
        BinaryCom=Binary

    #Rajout du bit de signe au MSB
    if Number>=0:
        BinaryCom='0'+BinaryCom
    elif Number<0:
        BinaryCom='1'+BinaryCom

    return BinaryCom
