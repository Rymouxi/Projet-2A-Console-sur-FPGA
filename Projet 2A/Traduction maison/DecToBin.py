def DecToBin(Nombre):
    Binaire=''
    Copie=Nombre
    while Copie!=1:
        if Copie%2==0:
            Binaire+='0'
        else:
            Binaire+='1'
        Copie=Copie//2
    if Copie%2==0:
        Binaire+='0'
    else:
        Binaire+='1'
    return Binaire[::-1]