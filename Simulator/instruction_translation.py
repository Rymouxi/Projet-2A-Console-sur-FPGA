from instruction_recognition import*
from treatment import*
from virtual_register_fct import virtual_register_init

def instruction_translation(ASM:str):
    """Programme global de traduction d'un code ASM en code machine
    code_ASM correspond au code brut tel qu'il est mis dans le terminal
    code-machine renvoie une liste instruction par instruction du code transcrit en code machine selon la convention LCM3
    """
    split_instructions=saut_ligne(ASM)
    #Les lignes des instructions sont numérotées à partir de 1
    line_instruction=[i+1 for i in range(len(split_instructions))]
    bitstream=''
    line_pointer=1
    line_update=[1]
    register_update=[]
    error=[]
    virtual_register_init()
    
    #Réalisation du bitstream
    i=0
    for instruction in split_instructions:
        bitstream+=instruction_recognition(instruction,i,split_instructions,simu='OFF')
        i+=1
    
    #Réalisation de la simulation
    for instruction in split_instructions:
        register_update_instruction,line_pointer,error_instruction=instruction_recognition(instruction,line_pointer,split_instructions,simu='ON')
        register_update.append(register_update_instruction)
        line_update.append(line_pointer)
        error+=error_instruction
    return split_instructions,line_instruction,bitstream,register_update,line_update,error


