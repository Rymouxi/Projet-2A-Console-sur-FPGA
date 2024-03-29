; PUSH (R3)
 
; R0 <- 0x20000004 (adress pointer)
; R2 <- 0x20000100 (size of the pile)
MOV R0, #1
LSL R0, R0, #29
ADD R2, R2, R0
ADD R0, #4
ADD R2, #0x80
ADD R2, #0x80

SHIFT_ALL:
	LDR R1, [R0]
	SUB  R0, R0, #4
	STR R1, [R0]
	ADD R0, #8
	CMP R0, R2
	BNE SHIFT_ALL

STR R3, [R0]
