; Euclidian Division function
; Returns R0 = R1 / R2
; And R1 is the remaining (R0 * R2 + R1_out = R1_in)

MOV R1, #128
MOV R2, #3

DIVISION:
	CMP R2, #0		; Check if R2 is zero
	BEQ DIV_ERROR		; If yes, error

    	MOV R0, #0		; Initilize the output R0 at zero

DIV_LOOP:
	CMP R1, #0		; Check if R1 is zero
	BEQ DIV_DONE		; if yes, get out of the loop and show R0 = 0

	CMP R1, R2		; Check if R1 smaller than R2
	BLT DIV_ERROR		; if so, error

	SUB R1, R1, R2      	; R1 - R2
	ADD R0, R0, #1      	; R0 + 1

	B DIV_LOOP          	; Repeat the loop

DIV_DONE:   
DIV_ERROR:
