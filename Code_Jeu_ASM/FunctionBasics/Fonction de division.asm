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

MOV R6, #0x00040000             ; This is the filter (0100)
AND R6, R1                      ; We apply the filter
MOV R0, #18                     ; We are going to redo a division
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
BNE CROSS

; CIRCLE (11)



; CROSS (01)

