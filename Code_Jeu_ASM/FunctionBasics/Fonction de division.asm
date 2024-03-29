; Division

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
