from DecToBin import*

def add(instruction):
    #Partons du principe que l'instruction ne prend qu'un certain type de forme
    #Nous avons donc: ADD Rd,Rn,#imm3
    #ADD Rd,#imm8
    #ADD Rd,Rn,Rm
    n=len(instruction)

    if copie.count(',')==1:
    #ADD Rd,#imm8
        add_rd_imm8(instruction)

    elif copie.count(',')==2:
        if copie.count('#')==0:
        #ADD Rd,Rn,Rm

        elif copie.count('#')==1:
        #ADD Rd,Rn,#imm3  
            

    return assembleur_offset

def add_rd_imm8(instruction):
    
    return 1

def add_rd_rn_imm3(instruction):
    return 1

def add_rd_rn_rm(instruction):
    return 1