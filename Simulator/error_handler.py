from label_recognition import label_table

"""Il s'agit d'un fichier avec des fonctions prenant une liste d'instruction et regardant si elle convient au format voulu"""

def error_handler_main(split_instruction):

    error_table=[]
    possible_instructions=['ADD ','AND ','BNE ','BEQ ','BGE ','BLT ','BGT ','BLE ','CMP ','EOR ','LDR ','LSL ','MOV ','STR ','SUB ']
    for i,instruction in enumerate(split_instruction):
        if  instruction[0]!='b'and instruction[0]!='B' :
            if instruction.find(':')==-1:
                instruction=instruction.upper()
        else:
            instruction=instruction[:instruction.find(' ')].upper()+instruction[instruction.find(' '):]
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
            error_table.extend((error,line))
    return error_table

def error_handler_add(instruction):
    """There are 3 different possibilities for this action:\n
    ADD Rd,Rn,#imm3\n
    ADD Rd,#imm8\n
    ADD Rd,Rn,Rm"""
    error=[]
    R_count=instruction.count('R')
    if R_count==1 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,8))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('#')))
    elif R_count==2 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,3))       
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(comma_identifier(instruction,register_indice[1]+1,instruction.find('#')))
    elif R_count==3 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.append(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.append(comma_identifier(instruction,register_indice[1]+1,register_indice[2]))
        error.append(check_end(instruction,register_indice[2]+1))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_and (instruction):
    """There is 1 possibility for this action:\n
    AND Rd,Rn\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(check_end_register(instruction,register_indice[1]+1))
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error


def error_handler_cmp (instruction):
    """There is 1 possibility for this action:\n
    CMP Rd,#imm8\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==1 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,8))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('#')))
    elif R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(check_end_register(instruction,register_indice[1]+1))
    else:
        error.append("The number of operand doesn't match for this instruction")
        
    return error

def error_handler_eor (instruction):
    """There is 1 possibility for this action:\n
    EOR Rd,Rm\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(check_end_register(instruction,register_indice[1]+1))
    else:
        error.append("The number of operand doesn't match for this instruction")
        
    return error

def error_handler_ldr (instruction):
    """There is 1 possibility for this action:\n
    LDR Rt,[Rn]\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('[')))
        indice1=instruction.find("[")
        indice2=instruction.find("]")
        if indice1 ==-1 or indice2 ==-1:
            error.append("missing [ or ]")
        else:
            if indice1>register_indice[1] or register_indice[1]>indice2:
                error.append("Brackets at the wrong place")
            else:
                error.extend(space_identifier(instruction,indice1,register_indice[1]))
                error.extend(space_identifier(instruction,register_indice[1]+1,indice2))
                error.extend(check_end_register(instruction,indice2))
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error

def error_handler_lsl (instruction):
    """There is 1 possibility for this action:\n
    LSL Rd,Rm,#imm8\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==2 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,5))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(comma_identifier(instruction,register_indice[1]+1,instruction.find('#')))
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error

def error_handler_mov (instruction):
    """There are 2 possibilities for this action:\n
    MOV Rd,#imm8\n
    MOV Rd,Rm"""
    error=[]
    R_count=instruction.count('R')
    register_indice=[]
    if R_count==1 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,8))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('#')))
    elif R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(check_end_register(instruction,register_indice[1]+1))        
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error


def error_handler_str (instruction):
    """There is 1 possibility for this action:\n
    STR Rt,[Rn]\n"""
    error=[]
    R_count=instruction.count('R')
    if R_count==2 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('[')))
        indice1=instruction.find("[")
        indice2=instruction.find("]")
        if indice1 ==-1 or indice2 ==-1:
            error.append("missing [ or ]")
        else:
            if indice1>register_indice[1] or register_indice[1]>indice2:
                error.append("Brackets at the wrong place")
            else:
                error.extend(space_identifier(instruction,indice1,register_indice[1]))
                error.extend(space_identifier(instruction,register_indice[1]+1,indice2))
                error.extend(check_end_register(instruction,indice2))
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error

def error_handler_sub (instruction):
    """There are 3 different possibilities for this action:\n
    SUB Rd ,Rn,#imm3\n
    SUB Rd,#imm8\n
    SUB Rd,Rn,Rm"""
    error=[]
    R_count=instruction.count('R')
    if R_count==1 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,8))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,instruction.find('#')))
    elif R_count==2 and instruction.count('#')==1:
        error.extend(register_error_handler(instruction))
        error.extend(imm_error_handler(instruction,3))      
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(comma_identifier(instruction,register_indice[1]+1,instruction.find('#')))
    elif R_count==3 and instruction.count('#')==0:
        error.extend(register_error_handler(instruction))
        register_indice=R_indices(instruction)
        error.extend(space_identifier(instruction,0,register_indice[0]))
        error.extend(comma_identifier(instruction,register_indice[0]+1,register_indice[1]))
        error.extend(comma_identifier(instruction,register_indice[1]+1,register_indice[2]))
        error.extend(check_end_register(instruction,register_indice[2]+1)) 
    else:
        error.append("The number of operand doesn't match for this instruction")
    return error

def error_handler_b_instruct(instruction):
    """These kind of instruction only look if the label they indicate exists\n"""
    error=[]
    n=len(instruction)
    label=''
    for (i,string) in enumerate(instruction):
        if string!=' ':
            label+=string
        if string==' ' and label!='':
            break
    if label=='':
        error.append("There is no label")
        return error
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

def imm_error_handler(instruction,size):
    
    error=[]
    hexa=['0','1','2','3','4','5','6','7','8','9','A','a','B','b','C','c','D','d','E','e','F','f']
    n=len(instruction)
    instruction.upper()
    end_imm=0
    if instruction.count('#')==1:
        imm_to_end = instruction[instruction.find('#'):]
        if imm_to_end=='#':
            error.append("There is no number after #")
        else:
            while imm_to_end[-1]==' ':
                imm_to_end=imm_to_end[:len(imm_to_end)-1]
            if imm_to_end.find('#0X')!=-1:
                for i in range(3,len(imm_to_end)):
                    if imm_to_end[i] not in hexa:
                        error.append("Expected a number in hexadecimal")
                        break
                    if i==(len(imm_to_end)-1):
                        if int(imm_to_end[3:],16)>=2**size:
                            error.append("This number is too big for this instruction")
            elif imm_to_end.find('#0B')!=-1:
                for i in range(3,len(imm_to_end)):
                    if imm_to_end[i] not in ['0','1']:
                        error.append("Expected a number in binary")
                        break
                    if i==(len(imm_to_end)-1):
                        if int(imm_to_end[3:],2)>=2**size:
                            error.append("This number is too big for this instruction")
            else:
                for i in range(1,len(imm_to_end)):
                    if imm_to_end[i] not in hexa[0:10]:
                        error.append("Expected a number in decimal")
                        break
                    if i==(len(imm_to_end)-1):
                        if int(imm_to_end[1:])>=2**size:
                            error.append("This number is too big for this instruction")
    else: 
        error.append("There's no immediate number or too many #")

    return error

def comma_identifier(instruction,end_arg1,star_arg2):
    error=[]
    separator=instruction[end_arg1+1:star_arg2]
    comma_count=0
    if separator=='':
        error.append("No comma between operands")
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
    #Knowing the instruction doesn't include the 
    register_indice=[]
    for (i,string) in enumerate(instruction):
        if string=='R':
            register_indice.append(i)
    return register_indice


def space_identifier(instruction,end_arg1,start_arg2):
    error=[]
    separator=instruction[end_arg1+1:start_arg2]
    if end_arg1 ==-1 or start_arg2 ==-1:
        return
    else :
        for string in separator:
            if string!=" ":
                error.append("Unexpected character")
                break
        return error

def check_end_register(instruction, last_operand_indice):
    """This function works only when the last operand is NOT an immediate number"""
    error=[]
    if last_operand_indice!=-1:
        for string in instruction[last_operand_indice+1:]:
            if string!=' ':
                error.append("Unexpected character after last operand")
                break
    return error

