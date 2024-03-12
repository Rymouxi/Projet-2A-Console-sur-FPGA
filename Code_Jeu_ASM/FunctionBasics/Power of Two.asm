; Function POWER_OF_TWO

POWER_OF_TWO:
    MOV R2, #1          ; Initialize R2 to 1 (2^0)
    MOV R0, #Power      ; power value in R0

shift_loop:
    CMP R0, #0          ; Check if the exponent is zero
    BEQ shift_done      ; If so, exit the loop
    LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
    SUB R3, R3, #1      ; Decrement the exponent
    B shift_loop        ; Repeat the process until the exponent is zero

shift_done:
    BX LR               ; Return