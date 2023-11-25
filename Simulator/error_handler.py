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
        error_table.extend([error,line])
    return error_table

def error_handler_add(instruction_without_action):
    """There are 3 different possibilities for this action:\n
    ADD Rd,Rn,#imm3\n
    ADD Rd,#imm8\n
    ADD Rd,Rn,Rm"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count==1:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,8))
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,3))       
    elif R_count==3:
        error.extend(register_error_handler(instruction_without_action))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_and (instruction_without_action):
    """There is 1 possibility for this action:\n
    AND Rd,Rn\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
    return error


def error_handler_cmp (instruction_without_action):
    """There is 1 possibility for this action:\n
    CMP Rd,#imm8\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=1:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==1:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,8))
    return error

def error_handler_eor (instruction_without_action):
    """There is 1 possibility for this action:\n
    EOR Rd,Rm\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
    return error

def error_handler_ldr (instruction_without_action):
    """There is 1 possibility for this action:\n
    LDR Rt,[Rn]\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
    return error

def error_handler_lsl (instruction_without_action):
    """There is 1 possibility for this action:\n
    LSL Rd,Rm,#imm8\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,5))
    return error

def error_handler_mov (instruction_without_action):
    """There are 2 possibilities for this action:\n
    MOV Rd,#imm8\n
    MOV Rd,Rm"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count==1:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,8))
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_str (instruction_without_action):
    """There is 1 possibility for this action:\n
    STR Rt,[Rn]\n"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count!=2:
        error.append("The number of register doesn't match for this instruction")
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
    return error

def error_handler_sub (instruction_without_action):
    """There are 3 different possibilities for this action:\n
    SUB Rd,Rn,#imm3\n
    SUB Rd,#imm8\n
    SUB Rd,Rn,Rm"""
    error=[]
    R_count=instruction_without_action.count('R')
    if R_count==1:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,8))
    elif R_count==2:
        error.extend(register_error_handler(instruction_without_action))
        error.extend(imm_error_handler(instruction_without_action,3))       
    elif R_count==3:
        error.extend(register_error_handler(instruction_without_action))
    else:
        error.append("The number of register doesn't match for this instruction")
    return error

def error_handler_b_instruct(instruction_without_action):
    """These kind of instruction only look if the label they indicate exists\n"""
    error=[]
    n=len(instruction_without_action)
    label=''
    for i in range(n):
        if instruction_without_action[i].isalpha():
            label+=instruction_without_action[i]
    if label not in label_table:
        error.append("This label doesn't exist")    
    return error


def register_error_handler(instruction_without_action):

    error=[]
    register_number=['0','1','2','3','4','5','6','7']
    count_R=instruction_without_action.count('R')
    for i in range(count_R):
        if instruction_without_action[instruction_without_action.find('R')+1] not in register_number:
            error.append("This register number doesn't exist")
        instruction_without_action=instruction_without_action[instruction_without_action.find('R')+2::]
    return error

def imm_error_handler(instruction_without_action,size):
    
    error=[]
    hexa=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    n=len(instruction_without_action)

    if instruction_without_action.find('0X')!=-1:
        m=2
        number_hexa=''
        while(instruction_without_action.find('0X')+m<n)and(instruction_without_action[instruction_without_action.find('0X')+m] in hexa):
            number_hexa+=instruction_without_action[instruction_without_action.find('0X')+m]
            m+=1
        if len(number_hexa)==0:
            error.append("No number") 
        if int(number_hexa,16)>2**size:
            error.append("This number is too big for this instruction")

    elif instruction_without_action.find('0B')!=-1:
        m=2
        number_binary=''
        while (instruction_without_action.find('0B')+m<n)and(instruction_without_action[instruction_without_action.find('0B')+m] in hexa[0:2]):
            number_hexa+=instruction_without_action[instruction_without_action.find('0B')+m]
            m+=1
        if len(number_binary)==0:
            error.append("No number") 
        if int(number_binary,2)>2**size:
            error.append("This number is too big for this instruction")
    elif instruction_without_action.find('#')!=-1:
        m=1
        number_integer=''
        while (instruction_without_action.find('#')+m<n)and(instruction_without_action[instruction_without_action.find('#')+m] in hexa[0:10]):
            number_integer+=instruction_without_action[instruction_without_action.find('#')+m]
            m+=1
        if len(number_integer)==0:
            error.append("No number") 
        if int(number_integer)>2**size:
            error.append("This number is too big for this instruction")
    else:
        error.append("The number format doesn't correspond to the expected ones")
    return error