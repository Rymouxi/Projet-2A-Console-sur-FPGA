def saut_ligne(code_text):    
    n=len(code_text)
    code_asm=[]
    code_loop=code_text
    while code_loop.find('\n')!=-1:
        code_asm.append(code_loop[0:code_loop.find('\n')])
        code_loop=code_loop[code_loop.find('\n')+1:n]
        n=len(code_loop)
    code_asm.append(code_loop[0:len(code_loop)])
    return code_asm

print(saut_ligne("bonjour\nmoi c'est\nlael"))
