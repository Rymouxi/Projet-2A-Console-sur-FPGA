; Code Morpion

; We read the 4 bits which indicate the case number

MOV R5, #1                      
LSL R5, R5, #31
MOV R6, #1
LSL R6, R6, #8
ADD R6, #4
EOR R5, R6                      ; memory adress of the game 0X80000104 in R5
LDR R1, [R5]                    ; read the value stocked at this adress and stock this value in R1
MOV R0, #28                     ; we are going to make a shift of 28 bits (because we want to read the first 4 bits)
B POWER_OF_TWO
    MOV R2, #1

    shift_loop:
        CMP R0, #0          ; Check if the exponent is zero
        BEQ shift_done      ; If so, exit the loop
        LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
        SUB R0, R0, #1      ; Decrement the exponent
        B shift_loop        ; Repeat the process until the exponent is zero

    shift_done:
        BX LR               ; Return R2 = 2^28

B DIVISION                  ; R1/R2
    DIV:
        CMP R2, #0          ; check if R2 is zero
        BEQ DIV_ERROR       ; If so, error

    MOV R0, #0         		; Initilize the output R0 at zero

    DIV_LOOP:
        CMP R1, #0         	; check if R1 is zero
        BEQ DIV_DONE        ; if so, get out of the loop and show R0 = 0

        CMP R1, R2          ; check if R1 smaller than R2
        BLT DIV_ERROR       ; if so, error

        SUB R1, R1, R2      ; R1 - R2
        ADD R0, R0, #1      ; R0 + 1

        B DIV_LOOP          ; Repeat the loop

    DIV_DONE:
    ; the result is in R0
        BX LR               

    DIV_ERROR:
        BX LR               

MOV Ra, R0                  ; Ra contains the 4 bits indicating the case number

; We read the bit which indicates the action to take (X/O)

MOV R6, #0x00040000          ; This is the filter (0100)
AND R6, R1                   ; We apply the filter
MOV R0, #18                  ; We are going to redo a division
B POWER_OF_TWO
    MOV R2, #1

    shift_loop:
        CMP R0, #0          ; Check if the exponent is zero
        BEQ shift_done      ; If so, exit the loop
        LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
        SUB R0, R0, #1      ; Decrement the exponent
        B shift_loop        ; Repeat the process until the exponent is zero

    shift_done:
        BX LR               ; Return R2 = 2^18

B DIVISION                  ; R6/R2
    DIV:
        CMP R2, #0          ; check if R2 is zero
        BEQ DIV_ERROR       ; If so, error

    MOV R0, #0         		; Initilize the output R0 at zero

    DIV_LOOP:
        CMP R6, #0         	; check if R1 is zero
        BEQ DIV_DONE        ; if so, get out of the loop and show R0 = 0

        CMP R6, R2          ; check if R1 smaller than R2
        BLT DIV_ERROR       ; if so, error

        SUB R6, R6, R2      ; R6 - R2
        ADD R0, R0, #1      ; R0 + 1

        B DIV_LOOP          ; Repeat the loop

    DIV_DONE:
    ; the result is in R0
        BX LR               

    DIV_ERROR:
        BX LR               
MOV Rb, R0                      ; Rb contains the bit indicating the action X/O

CMP Rb, #0                      
BEQ CIRCLE
    MOV Rc, #3                  ; 3 in binary is 11 (we are goint to change the case value from 00 to 11)
    SUB Ra, #1                  ; because we want a value as 100..00

    MOV R2, #2
    B MULTIPLICATION            ; R0 = Ra*2
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP Ra, #0         ; check if Ra is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP R2, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Ra, Ra, #1     	; Ra = Ra - 1
            CMP Ra, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0
        	BX LR  

    B POWER_OF_TWO
        MOV R2, #1

        shift_loop:
            CMP R0, #0          ; Check if the exponent is zero
            BEQ shift_done      ; If so, exit the loop
            LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
            SUB R0, R0, #1      ; Decrement the exponent
            B shift_loop        ; Repeat the process until the exponent is zero

        shift_done:
            BX LR               ; Return the bit of position where wu put a 1, the result is in R2
    
    B MULTIPLICATION            ; R0 = R2*Rc = 11*Rc
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP R2, #0         ; check if R2 is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP Rc, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Rc, Rc, #1     	; Rc = Rc - 1
            CMP Rc, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0, we have now 1100..00, so can change the value at the position we want by adding this value
        	BX LR
    ADD R1, R1, R0

BNE CROSS
    MOV Rc, #1                  ; 1 in binary is 01 (we are goint to change the case value from 00 to 01)
    SUB Ra, #1                  ; because we want a value as 100..00

    MOV R2, #2
    B MULTIPLICATION            ; R0 = Ra*2
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP Ra, #0         ; check if Ra is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP R2, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Ra, Ra, #1     	; Ra = Ra - 1
            CMP Ra, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0
        	BX LR  

    B POWER_OF_TWO
        MOV R2, #1

        shift_loop:
            CMP R0, #0          ; Check if the exponent is zero
            BEQ shift_done      ; If so, exit the loop
            LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
            SUB R0, R0, #1      ; Decrement the exponent
            B shift_loop        ; Repeat the process until the exponent is zero

        shift_done:
            BX LR               ; Return the bit of position where wu put a 1, the result is in R2
    
    B MULTIPLICATION            ; R0 = R2*Rc = 11*Rc
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP R2, #0         ; check if R2 is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP Rc, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Rc, Rc, #1     	; Rc = Rc - 1
            CMP Rc, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0, we have now 0100..00, so can change the value at the position we want by adding this value
        	BX LR
    ADD R1, R1, R0

