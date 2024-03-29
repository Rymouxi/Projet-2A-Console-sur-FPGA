; Fonction de multiplication
; Résultat R0 = R1 * R2

; Exemple

;MOV R1, #8
;MOV R2, #7

MULTIPLICATION:
MOV R0, #0		; Initialiser le résultat à zéro

MUL_LOOP:
CMP R2, #0		; Vérifier si le multiplicateur R1 est nul
BEQ MUL_DONE		; Si c'est le cas, sortir de la boucle

CMP R1, #0		; Vérifier si le multiplicand est nul
BEQ MUL_DONE		; Si c'est le cas, sortir de la boucle

ADD R0, R0, R1		; R0 = R0 + R1
SUB  R2, R2, #1		; Décrémenter le multiplicateur   
CMP R2, #0      
BGE MUL_LOOP		; Répéter la boucle si le multiplicateur est >= 0

MUL_DONE:
