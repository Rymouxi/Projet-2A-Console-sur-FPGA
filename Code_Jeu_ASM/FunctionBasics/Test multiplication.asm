;Test multiplication

MOV R1, #3
MOV R2, #4

BL MUL

MUL:
    MOV R0, #0
    MOV R3, #0 

ADD R3, R0, R1
    CMP R3, R0
    BNE MUL_DONE

MUL_LOOP:
    CMP R2, #0
    BEQ MUL_DONE

    ADD R0, R0, R1
    SUB R2, R2, #1
    B MUL_LOOP

MUL_DONE:
