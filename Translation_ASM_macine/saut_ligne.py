def saut_ligne(code_text:str): 
    """Cette fonction prend le code ASM en entier et le convertit en liste d'instruction où le séparateur est le retour à la ligne
    """
    n=len(code_text)
    code_asm=[]
    code_loop=code_text
    while code_loop.find('\n')!=-1:
        code_asm.append(code_loop[0:code_loop.find('\n')])
        code_loop=code_loop[code_loop.find('\n')+1:n]
        n=len(code_loop)
    code_asm.append(code_loop[0:len(code_loop)])
    return code_asm
