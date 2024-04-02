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
                        

    DIV_ERROR:
                        

MOV Ra, R0                  ; Ra contains the 4 bits indicating the case number
MOV Re, R0                  ; Re contains also the 4 bits indicating the case number but we use it to check the succes or not

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
                        ; Return R2 = 2^18

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
                        

    DIV_ERROR:
                        
MOV Rb, R0                      ; Rb contains the bit indicating the action X/O

CMP Rb, #0                      
BEQ CIRCLE
    MOV Rc, #3                  ; 3 in binary is 11 (we are goint to change the case value from 00 to 11)
    SUB Re, #1                  ; because we want a value as 100..00

    MOV R2, #2
    B MULTIPLICATION            ; R0 = Ra*2
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP Re, #0         ; check if Ra (Re) is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP R2, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Re, Re, #1     	; Ra = Ra - 1
            CMP Re, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0
        	   

    B POWER_OF_TWO
        MOV R2, #1

        shift_loop:
            CMP R0, #0          ; Check if the exponent is zero
            BEQ shift_done      ; If so, exit the loop
            LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
            SUB R0, R0, #1      ; Decrement the exponent
            B shift_loop        ; Repeat the process until the exponent is zero

        shift_done:
                            ; Return the bit of position where wu put a 1, the result is in R2
    
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
        	 
    ADD R1, R1, R0

BNE CROSS
    MOV Rc, #1                  ; 1 in binary is 01 (we are goint to change the case value from 00 to 01)
    SUB Re, #1                  ; because we want a value as 100..00

    MOV R2, #2
    B MULTIPLICATION            ; R0 = Ra*2
        MOV R0, #0      		; Initialize the result R0 as 0

    	MUL_LOOP:
       		CMP Re, #0         ; check if Ra is 0
       		BEQ MUL_DONE       ; if so return R0 = 0

            CMP R2, #0         	; check if Ra is 0
       		BEQ MUL_DONE        ; if so return R0 = 0

            ADD R0, R0, R2      ; R0 = R0 + R2 = R0 + 2
       		SUB Re, Re, #1     	; Ra = Ra - 1
            CMP Re, #0      
            BGE MUL_LOOP        ; Repeat the loop until Ra is zero

    	MUL_DONE:
        	; the result is in R0
        	   

    B POWER_OF_TWO
        MOV R2, #1

        shift_loop:
            CMP R0, #0          ; Check if the exponent is zero
            BEQ shift_done      ; If so, exit the loop
            LSL R2, R2, #1      ; Left shift R2 by one position (equivalent to multiplying by 2)
            SUB R0, R0, #1      ; Decrement the exponent
            B shift_loop        ; Repeat the process until the exponent is zero

        shift_done:
                            ; Return the bit of position where wu put a 1, the result is in R2
    
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
        	 
    ADD R1, R1, R0

; Now we check the corresponded line, column and diagonalline to verify if anybody wins
; We know that Ra contains the case number 
; during all the previous test, we did the modification with Re (which contains the case number but modfied during the test)

; Function to check if a player wins
CheckWin:
    ; First, let's check rows
    MOV R0, #0       ; Counter for rows
    CHECK_ROW:
        ; Compute the starting address of the row
        MOV R4, R0       ; Copy the row index to R4
        LSL R4, R4, #2   ; Multiply by 4 (assuming each cell occupies 4 bytes)
        ADD R4, R5, R4   ; Add the base address of the game to get the starting address of the row
        ; Load the first cell of the row
        LDR R6, [R4]

        ; Check if all cells in the row match the symbol of the current player
        MOV R7, #0       ; Counter for matching cells
        MOV R8, R6       ; Copy the symbol of the first cell to R8
        CHECK_CELL:
            CMP R8, R6        ; Compare the symbol of the current cell with the symbol of the first cell
            BNE ROW_END       ; If symbols are not equal, exit the loop
            ADD R7, R7, #1    ; Increment the counter of matching cells
            ADD R4, R4, #4    ; Move to the next cell in the row
            LDR R6, [R4]      ; Load the symbol of the next cell
            CMP R7, #3        ; Check if we have found 3 matching cells
            BEQ WINNER_FOUND  ; If so, the player wins
            B CHECK_CELL      ; Repeat the loop for the next cell
        ROW_END:
        ADD R0, R0, #1    ; Move to the next row
        CMP R0, #3        ; Check if we have checked all rows
        BLT CHECK_ROW     ; If not, repeat the loop for the next row

    ; If we reached here, the player didn't win with rows, let's check columns and diagonals
    ; You can implement similar checks for columns and diagonals here

    ; If no winner is found, return 0
    MOV R0, #0
     

WINNER_FOUND:
    ; If a winner is found, return 1
    MOV R0, #1
     
