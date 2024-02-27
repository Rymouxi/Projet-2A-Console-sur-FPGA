; Code Morpion

; We read the 4 bits which indicate the case number

MOV R5, #0x80000104             ; memory adress of the game 
LDR R1, [R5]                    ; read the value stocked at this adress and stock this value in R1
MOV R0, #28                     ; we are going to make a shift of 28 bits (because we want to read the first 4 bits)
B POWER_OF_TWO
    ...
    2^28 = R2
B DIVISION 
    ...
    R1/2^28 = R0
MOV Ra, R0                      ; Ra contains the 4 bits indicating the case number

; We read the bit which indicates the action to take (X/O)

MOV R6, #0x00040000             ; This is the filter 
AND R6, R1                      ; We apply the filter
MOV R7, #18                     ; We are going to make a division 
B POWER_OF_TWO
    ...
    2^18 = R2
B DIVISION 
    ...
    R6/2^18 = R0
MOV Rb, R0                      ; Rb contains the bit indicating the action X/of

CMP Rb, #0
BEQ CIRCLE
BNE CROSS

; CIRCLE (11)



; CROSS (01)
