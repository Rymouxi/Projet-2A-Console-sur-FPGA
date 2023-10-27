from instruction_recognition import*
from treatment import*
from treatment import line


def instruction_translation(code_ASM:str):
    """Programme global de traduction d'un code ASM en code machine
    code_ASM correspond au code brut tel qu'il est mis dans le terminal
    code-machine renvoie une liste instruction par instruction du code transcrit en code machine selon la convention LCM3
    """
    
    code_machine=[]
    global line
    
    for instruction in saut_ligne(code_ASM):
        line+=1
        code_machine.append(instruction_recognition(instruction,code_ASM,line))
        
    return (code_machine,liste_instruction,ligne_instruction,register_update)


