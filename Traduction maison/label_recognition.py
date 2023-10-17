def label_recognition(code_asm_brute):
    split_instruction=saut_ligne(code_asm_brute)
    listelabel=[]
    for line,instruction in enumerate(split_instruction):
        if instruction.find(":")==1:
            listelabel.append((instruction[0:instruction.find(':')]),line)
    return listelabel
 
