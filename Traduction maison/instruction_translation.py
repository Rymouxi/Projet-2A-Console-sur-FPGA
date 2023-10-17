from instruction_recognition import*
from saut_ligne import*
def instruction_translation(texte_ASM:str):
    """
    """
    code_machine=[]
    for i in saut_ligne(texte_ASM):
        code_machine.append(instruction_recognition(i))
    return(code_machine)
