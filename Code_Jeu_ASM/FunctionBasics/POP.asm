; POP (R3)

; R0 <- 0x20000100 (adress pointer)
; R2 <- 0x20000000 (size of the pile)
MOV R0, #1
LSL R0, R0, #29
MOV R2, R0
ADD R0, #0x80
ADD R0, #0x80

LDR R3, [R0]		; POP R3
SUB  R0, R0, #4

SHIFT_ALL:
	LDR R1, [R0]
	ADD  R0, R0, #4
	STR R1, [R0]
	SUB R0, #8
	CMP R0, R2
	BNE SHIFT_ALL
