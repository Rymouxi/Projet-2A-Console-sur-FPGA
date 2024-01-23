from label_recognition import label_table

"""Il s'agit d'un fichier avec des fonctions prenant une liste d'instruction et regardant si elle convient au format voulu"""

def error_handler_main(split_instruction):

    error_table=[]
    possible_instructions=['ADD ','AND ','BNE ','BEQ ','BGE ','BLT ','BGT ','BLE ','CMP ','EOR ','LDR ','LSL ','MOV ','STR ','SUB ']
    for i,instruction in enumerate(split_instruction):
        if (instruction[0:4] in possible_instructions)or(instruction[0:2]=='B ')or(instruction.count(':')==1)or(instruction==''):
            if instruction[0:4]==possible_instructions[0]:
                error_table.extend(error_table_extension(error_handler_add(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[1]:
                error_table.extend(error_table_extension(error_handler_and(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[2]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[3]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[4]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[5]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[6]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[7]:
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[8]:
                error_table.extend(error_table_extension(error_handler_cmp(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[9]:
                error_table.extend(error_table_extension(error_handler_eor(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[10]:
                error_table.extend(error_table_extension(error_handler_ldr(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[11]:
                error_table.extend(error_table_extension(error_handler_lsl(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[12]:
                error_table.extend(error_table_extension(error_handler_mov(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[13]:
                error_table.extend(error_table_extension(error_handler_str(instruction[4::]),i))
            elif instruction[0:4]==possible_instructions[14]:
                error_table.extend(error_table_extension(error_handler_sub(instruction[4::]),i))
            elif instruction[0:2]=='B ':
                error_table.extend(error_table_extension(error_handler_b_instruct(instruction[2::]),i))
        else:
            error_table.extend(["Syntax error",i])    
    return error_table

def error_table_extension(error_handler_table,line):
    error_table=[]
    for error in error_handler_table:
        if error!=[]:
            error_table.extend([error,line])
    return error_table

def error_handler_add(instruction):
    """There are 3 different possibilities for this action:\n
    ADD Rd,Rn,#imm3\n
    ADD Rd,#imm8\n
    ADD Rd,Rn,Rm"""
    error=[]
    R_count=instruction.count('R')
    if R_count==1:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,8)))
    elif R_count==2:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,3)))       
    elif R_count==3:
        error.extend(register_error_handler(instruction))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_and (instruction):
    """There is 1 possibility for this action:\n
    AND Rd,Rn\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction))
    return error


def error_handler_cmp (instruction):
    """There is 1 possibility for this action:\n
    CMP Rd,#imm8\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=1:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==1:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,8)))
    return error

def error_handler_eor (instruction):
    """There is 1 possibility for this action:\n
    EOR Rd,Rm\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction))
    return error

def error_handler_ldr (instruction):
    """There is 1 possibility for this action:\n
    LDR Rt,[Rn]\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction))
    return error

def error_handler_lsl (instruction):
    """There is 1 possibility for this action:\n
    LSL Rd,Rm,#imm8\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,5)))
    return error

def error_handler_mov (instruction):
    """There are 2 possibilities for this action:\n
    MOV Rd,#imm8\n
    MOV Rd,Rm"""
    error=[]
    R_count=instruction.count('R')
    register_indice=[]
    if R_count==1 and instruction.count('#')==1:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,8)))
        register_indice=R_indices(instruction)
        error.append(comma_identifier(instruction,register_indice[0]+1,instruction.find('#')))
    elif R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.append(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.append(comma_identifier(instruction,register_indice[1]+1,instruction.find('#')))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_str (instruction):
    """There is 1 possibility for this action:\n
    STR Rt,[Rn]\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction))
    return error

def error_handler_sub (instruction):
    """There are 3 different possibilities for this action:\n
    SUB Rd ,Rn,#imm3\n
    SUB Rd,#imm8\n
    SUB Rd,Rn,Rm"""
    error=[]
    R_count=instruction.count('R')
    if R_count==1:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,8)))
    elif R_count==2:
        error.extend((register_error_handler(instruction),imm_error_handler(instruction,3)))       
    elif R_count==3:
        error.extend(register_error_handler(instruction))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_b_instruct(instruction):
    """These kind of instruction only look if the label they indicate exists\n"""
    error=[]
    n=len(instruction)
    label=''
    for i in range(n):
        if instruction[i].isalpha():
            label+=instruction[i]
    if label not in label_table:
        error.append("This label doesn't exist")    
    return error


def register_error_handler(instruction):

    error=[]
    register_number=['0','1','2','3','4','5','6','7']
    count_R=instruction.count('R')
    for i in range(count_R):
        if instruction[instruction.find('R')+1] not in register_number:
            error.append("This register number doesn't exist")
        instruction=instruction[instruction.find('R')+2::]
    return error

# def imm_error_handler(instruction,size):
    
#     error=[]
#     hexa=['0','1','2','3','4','5','6','7','8','9','A','a','B','b','C','c','D','d','E','e','F','f']
#     n=len(instruction)
#     instruction.upper()
#     if instruction.find('#')!=-1:
#         if instruction.find('0X')!=-1:
#             m=0
#             number_hexa=''
#             while(instruction.find('0X')+2+m<n)and(instruction[instruction.find('0X')+2+m] in hexa):
#                 number_hexa+=instruction[instruction.find('0X')+2+m]
#                 m+=1
#             if len(number_hexa)==0:
#                 error.append("No number") 
#             if int(number_hexa,16)>2**size:
#                 error.append("This number is too big for this instruction")

#         elif instruction.find('0B')!=-1:
#             m=0
#             number_binary=''
#             while (instruction.find('0B')+m<n)and(instruction[instruction.find('0B')+m] in hexa[0:2]):
#                 number_binary+=instruction[instruction.find('0B')+m]
#                 m+=1
#             if len(number_binary)==0:
#                 error.append("No number") 
#             if int(number_binary,2)>2**size:
#                 error.append("This number is too big for this instruction")
#         else :
#             m=0
#             number_integer=''
#             while (instruction.find('#')+1+m<n)and(instruction[instruction.find('#')+1+m] in hexa[0:10]):
#                 number_integer+=instruction[instruction.find('#')+m]
#                 m+=1
#             if len(number_integer)==0:
#                 error.append("No number") 
#             if int(number_integer)>2**size:
#                 error.append("This number is too big for this instruction")
#     return error

def imm_error_handler(instruction,size):
    
    error=[]
    hexa=['0','1','2','3','4','5','6','7','8','9','A','a','B','b','C','c','D','d','E','e','F','f']
    n=len(instruction)
    instruction.upper()
    if instruction.count('#')==1:
        imm_to_end = instruction[instruction.find('#'):]
        while imm_to_end[-1]==' ':
            imm_to_end=imm_to_end[:len(imm_to_end)-1]
        if imm_to_end.find('#0X')!=-1:
            for i in range(2,len(imm_to_end)):
                if imm_to_end[i] not in hexa:
                    error.append("Expected a number in hexadecimal")
                    break
                if i==(len(imm_to_end)-1):
                    if int(imm_to_end[3:],16)>=2**size:
                        error.append("This number is too big for this instruction")
        elif imm_to_end.find('#0B')!=-1:
            for i in range(2,len(imm_to_end)):
                if imm_to_end[i] not in ['0','1']:
                    error.append("Expected a number in binary")
                    break
                if i==(len(imm_to_end)-1):
                    if int(imm_to_end[3:],2)>=2**size:
                        error.append("This number is too big for this instruction")
        else:
            for i in range(2,len(imm_to_end)):
                if imm_to_end[i] not in hexa[0,10]:
                    error.append("Expected a number in decimal")
                    break
                if i==(len(imm_to_end)-1):
                    if int(imm_to_end)>=2**size:
                        error.append("This number is too big for this instruction")
    else: 
        error.append("There's no immediate number or too many #")

    return error

def comma_identifier(instruction,end_arg1,star_arg2):
    error=[]
    separator=instruction[end_arg1+1:star_arg2]
    comma_count=0
    for string in separator:
        if string==',':
            comma_count+=1
        elif string!=' ':
            error.append("Unexpected character between two operands")
            break
        if comma_count>1:
            error.append("Too many comma between two operands")
            break
        if comma_count==0:
            error.append("No separator between two operands")
    return error

def R_indices(instruction):
    register_indice=[]
    for (string,i) in enumerate(instruction):
        if string=='R':
            register_indice.append(i)
    return register_indice