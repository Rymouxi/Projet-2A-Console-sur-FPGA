from instruction_recognition import*
from treatment import*
from virtual_register_fct import virtual_register_reset
from virtual_memory_fct import virtual_memory_reset
from label_recognition import *
from error_handler import error_handler_main

def instruction_translation(ASM:str):
    """Programme global de traduction d'un code ASM en code machine
    code_ASM correspond au code brut tel qu'il est mis dans le terminal
    code-machine renvoie une liste instruction par instruction du code transcrit en code machine selon la convention LCM3
    """
    split_instruction=treatment(ASM)
    #Les lignes des instructions sont numérotées à partir de 1
    line_instruction=[i+1 for i in range(len(split_instruction))]
    bitstream=[]
    register_update=[]
    line_pointer=0
    line_update=[0]
    memory_update=[]
    error=[]
    sequence_break=False
    virtual_register_reset()
    virtual_memory_reset()
    label_recognition(split_instruction)

    #Vérification d'erreurs de syntaxe
    error_syntax=error_handler_main(split_instruction)
    error.extend(error_syntax)
    #Réalisation de la simulation
    if len(error_syntax)==0:
        split_instructions_with_END=split_instruction+["END"]
        j=0
        while split_instructions_with_END[line_pointer]!="END":
            instruction=split_instructions_with_END[line_pointer]
            #Rupture de séquence dans le cas d'un branchement
            register_update_instruction,sequence_break,line_pointer,memory_update_instruction,error_simu=instruction_recognition(instruction,line_pointer,simu='ON')
            if sequence_break==False and is_instruction_b_instruct(instruction)==True:
                line_update.append(-1)
                line_update.append(-1)
                memory_update.append([])
                memory_update.append([])
                register_update.append([])
                register_update.append([])
            if register_update_instruction!=[]:
                if type(register_update_instruction[0])==list:
                    register_update.extend(register_update_instruction)
                else:
                    register_update.append(register_update_instruction)
            else:
                register_update.append(register_update_instruction)
            line_update.append(line_pointer)
            memory_update.append(memory_update_instruction)
            if error_simu!=[]:
                error.extend(error_simu)
                error.append(j)
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
#je rajoute le code pour la fin du programme c'est peut être foireux 
        split_instruction.extend(["ENDENDEND:","MOV R0,R0","MOV R0,R0","BNE ENDENDEND"])
        bitstream.extend(["0000000000000000",'0000000000000000','1101000111111110'])
        register_update.append([])
        register_update.append([])
        register_update.append([])
        line_update.extend([line_update[-1]+1,line_update[-1]+2,line_update[-1]+3])
        memory_update.append([])
        memory_update.append([])
        memory_update.append([])
        
    for line in line_update:
        if line in label_table:
            line_update.remove(line)

    return split_instruction,bitstream,register_update,line_update,memory_update,error

def is_instruction_b_instruct(instruction):
    result=False
    if instruction[0]=='B' or instruction[0]=='b':
        result=True
    else:
        instruction=instruction.upper()
        if instruction[:4]=='BNE' or instruction[:4]=='BEQ' or instruction[:4]=='BGE' or instruction[:4]=='BLT' or instruction[:4]=='BGT' or instruction[:4]=='BLE':
            result = True
    return result
