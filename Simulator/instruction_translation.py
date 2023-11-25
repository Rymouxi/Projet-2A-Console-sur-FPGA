from instruction_recognition import*
from treatment import*
from virtual_register_fct import virtual_register_reset
from virtual_memory_fct import virtual_memory_reset
from label_recognition import label_recognition

def instruction_translation(ASM:str):
    """Programme global de traduction d'un code ASM en code machine
    code_ASM correspond au code brut tel qu'il est mis dans le terminal
    code-machine renvoie une liste instruction par instruction du code transcrit en code machine selon la convention LCM3
    """
    split_instruction=saut_ligne(ASM)
    #Les lignes des instructions sont numérotées à partir de 1
    line_instruction=[i+1 for i in range(len(split_instruction))]
    bitstream=[]
    register_update=[]
    line_pointer=0
    line_update=[0]
    memory_update=[]
    error=[]
    virtual_register_reset()
    virtual_memory_reset()
    label_recognition(split_instruction)

    #Vérification d'erreurs de syntaxe
    from error_handler import error_handler_main
    error_syntax=error_handler_main(split_instruction)
    error.extend(error_syntax)
    #Réalisation de la simulation
    if len(error_syntax)==0:
        split_instructions_with_END=split_instruction+["END"]
        j=0
        while split_instructions_with_END[line_pointer]!="END":
            instruction=split_instructions_with_END[line_pointer]
            register_update_instruction,line_pointer,memory_update_instruction,error_simu=instruction_recognition(instruction,line_pointer,simu='ON')
            register_update.append(register_update_instruction)
            line_update.append(line_pointer)
            memory_update.append(memory_update_instruction)
            error.extend(error_simu)
            j+=1
            if j>1000:
                error.extend(["There's an infinite loop" ,line_pointer])
                break
        
#Réalisation du bitstream seulement si il n'y a pas d'erreurs
    if len(error)==0:
        i=0
        for instruction in split_instruction:
            bitstream.append(instruction_recognition(instruction,i,simu='OFF'))
            i+=1
    return split_instruction,line_instruction,bitstream,register_update,line_update,memory_update,error


