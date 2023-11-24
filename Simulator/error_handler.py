"""Il s'agit d'un fichier avec des fonctions prenant une liste d'instruction et regardant si elle convient au format voulu"""

def error_handler_main(split_instruction):

    error_table=[]
    possible_instructions=['ADD ','AND ','BNE ','BEQ ','BGE ','BLT ','BGT ','BLE ','CMP ','EOR ','LDR ','LSL ','MOV ','STR ','SUB ']
    for instruction in split_instruction:

        if (instruction[0:4] in possible_instructions)or(instruction[0:2]=='B '):
            if instruction[0:4]==possible_instructions[0]:
                error_table.append(error_handler_add(instruction[4::]))
            if instruction[0:4]==possible_instructions[1]:
                error_table.append(error_handler_and(instruction[4::]))
            if instruction[0:4]==possible_instructions[2]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[3]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[4]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[5]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[6]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[7]:
                error_table.append(error_handler_b_instruct(instruction[4::]))
            if instruction[0:4]==possible_instructions[8]:
                error_table.append(error_handler_cmp(instruction[4::]))
            if instruction[0:4]==possible_instructions[9]:
                error_table.append(error_handler_eor(instruction[4::]))
            if instruction[0:4]==possible_instructions[10]:
                error_table.append(error_handler_ldr(instruction[4::]))
            if instruction[0:4]==possible_instructions[11]:
                error_table.append(error_handler_lsl(instruction[4::]))
            if instruction[0:4]==possible_instructions[12]:
                error_table.append(error_handler_mov(instruction[4::]))
            if instruction[0:4]==possible_instructions[13]:
                error_table.append(error_handler_str(instruction[4::]))
            if instruction[0:4]==possible_instructions[14]:
                error_table.append(error_handler_sub(instruction[4::]))
            if instruction[0:2]=='B ':
                error_table.append(error_handler_b_instruct(instruction[2::]))
            
    return error_table


def error_handler_add():
    error=[]
    return error
def error_handler_and ():
    error=[]
    return error
def error_handler_b_instruct():
    error=[]
    return error

def error_handler_cmp ():
    error=[]
    return error
def error_handler_eor ():
    error=[]
    return error
def error_handler_ldr ():
    error=[]
    return error
def error_handler_lsl ():
    error=[]
    return error
def error_handler_mov ():
    error=[]
    return error
def error_handler_str ():
    error=[]
    return error
def error_handler_sub ():
    error=[]
    return error
def error_handler_b ():
    error=[]
    return error





