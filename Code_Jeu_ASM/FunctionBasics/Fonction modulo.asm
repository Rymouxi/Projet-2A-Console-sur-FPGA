; Fonction de modulo
; Résultat = R1 % R2
MOD:
    CMP R2, #0          ; Vérifier si le diviseur R2 est nul
    BEQ MOD_ERROR       ; Si c'est le cas, afficher une erreur

    MOV R0, #0          ; Initialiser le résultat à zéro

MOD_LOOP:
    CMP R1, #0          ; Vérifier si le dividende est nul
    BEQ MOD_DONE        ; Si c'est le cas, sortir de la boucle

    CMP R1, R2          ; Vérifier si le dividende est inférieur au diviseur
    BLT MOD_DONE        ; Si c'est le cas, sortir de la boucle

    SUB R1, R1, R2      ; Soustraire le diviseur du dividende

    B MOD_LOOP          ; Répéter la boucle

MOD_DONE:
    ; À ce stade, le résultat (le modulo) est dans le registre R1
    MOV R0, R1          ; Copier le modulo dans le registre de résultat (R0)
    BX LR               ; Retourner de la fonction

MOD_ERROR:
    ; Gestion de l'erreur de modulo par zéro
    ; (ajouter ici le code pour gérer cette situation)
    BX LR               ; Retourner de la fonction

