;Fonction de multiplication
;Résultat = R1 * R2

MUL:
    MOV R0, #0      ; Initialiser le résultat à zéro
    MOV R3, #0      ; Initialiser un registre temporaire à zéro

ADD R3, R0, R1      ; Ajouter le multiplicand au résultat temporaire
CMP R3, R0          ; Vérifier s'il y a eu un dépassement (overflow)
BNE MUL_DONE        ; Si oui, sortir de la boucle (si R1 = R3 = 0 )

MUL_LOOP:
    CMP R2, #0      ; Vérifier si le multiplicateur est nul
    BEQ MUL_DONE    ; Si c'est le cas, sortir de la boucle

    ADD R0, R0, R1  ; Ajouter le multiplicand au résultat (R0 = R1)
    SUB R2, R2, #1  ; Décrémenter le multiplicateur
    B MUL_LOOP      ; Répéter la boucle

MUL_DONE:
    ; le résultat est dans le registre R0
    BX LR           ; Retourner de la fonction

