; Multiplication function
; Returns R0 = R1 * R2

MULTIPLICATION:
MOV R0, #0		; Initialize the result at zero

MUL_LOOP:
CMP R2, #0		; Check if R2 factor is nil
BEQ MUL_DONE		; If yes, break

CMP R1, #0		; Check if R1 factor is nil
BEQ MUL_DONE		; If yes, break

ADD R0, R0, R1		; R0 = R0 + R1
SUB  R2, R2, #1		; Decrement the R2 factor
CMP R2, #0      
BGE MUL_LOOP		; Repeat if R2 >= 0

MUL_DONE:
