; Function R0 = 2^R1

POWER_OF_TWO:
	MOV R0, #1		; Initialize R0 to 1 (2^0)

SHIFT_LOOP:
	CMP R1, #0		; Check if the exponent is zero
	BEQ SHIFT_DONE		; If yes, break
	LSL R0, R0, #1		; Shifts R0 1 to the left (Doubles it)
	SUB R1, #1		; Decrement the exponent
	B SHIFT_LOOP		; Repeat the process until the exponent is zero

SHIFT_DONE:
