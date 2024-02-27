
# def saut_ligne(code_text:str): 
#     """Cette fonction prend le code ASM en entier et le convertit en liste d'instructions où le séparateur est le retour à la ligne.\n
#     Il enlève également les éventuelles indentations
#     """
#     index=code_text.find('\n')
#     n=len(code_text)
#     code_asm=[]
#     code_loop=code_text
#     while code_loop.find('\n')!=-1:
#         indent_count=code_loop[0:code_loop.find("\n")].count("\t")
#         if indent_count!=0:
#             for indent in range(indent_count):
#                 code_loop=code_loop[0:code_loop.find("\t")]+code_loop[code_loop.find("\t")+1:n]
#         if code_loop[0:code_loop.find("\n")].count(";")!=0:
#             code_loop=code_loop[0:code_loop.find(';')]+code_loop[code_loop.find("\n"):n]
#         code_asm.append(code_loop[0:code_loop.find('\n')])
#         code_loop=code_loop[code_loop.find('\n')+1:n]
#         n=len(code_loop)

#     indent_count=code_loop[0:code_loop.find("\n")].count("\t")
#     if indent_count!=0:
#         for indent in range(indent_count):
#             code_loop=code_loop[0:code_loop.find("\t")]+code_loop[code_loop.find("\t")+1:n]
#     code_asm.append(code_loop[0:len(code_loop)])

#     for j in range(len(code_asm)):
#         i=0
#         while code_asm[j][i]==' ':
#             code_asm[j]=code_asm[j][1:]
#             i+=1

#     return code_asm

def saut_ligne(ASM:str):
    """Cette fonction prend le code ASM en entier et le convertit en liste d'instructions où le séparateur est le retour à la ligne.\n
    Il enlève également les éventuelles indentations
    """
    code_ASM=[]
    break_line_count=ASM.count("\n")
    for i in range(break_line_count):
        line=ASM[:ASM.find("\n")]

        #indentation
        while line.find("\t")!=-1:
            indent_index=line.find("\t")
            line=line[:indent_index]+line[indent_index+1:]
        
        #commentaires
        if line.find(";")!=-1:
            line=line[:line.find(";")]
        
        if line!='':
            copy_line=line
            for character in copy_line:
                if character==' ':
                    line=line[1:]
                if character!=' ':
                    break
            for character in copy_line[::-1]:
                if character==' ':
                    line=line[:-1]
                if character!=' ':
                    break
        
        if line!='':
            code_ASM.append(line)
        ASM=ASM[ASM.find("\n")+1:]
    return code_ASM

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