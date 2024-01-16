; Fonction de division
; Résultat = R1 / R2
DIV:
    CMP R2, #0          		; Vérifier si le diviseur R2 est nul
    BEQ DIV_ERROR       	; Si c'est le cas, afficher une erreur

    MOV R0, #0         		 ; Initialiser le résultat à zéro

DIV_LOOP:
    CMP R1, #0         		; Vérifier si le dividende est nul
    BEQ DIV_DONE        		; Si c'est le cas, sortir de la boucle

    CMP R1, R2          		; Vérifier si le dividende est inférieur au diviseur
    BLT DIV_DONE        		; Si c'est le cas, sortir de la boucle

    SUB R1, R1, R2      		; Soustraire le diviseur du dividende
    ADD R0, R0, #1      		; Incrémenter le résultat

    B DIV_LOOP          		; Répéter la boucle

DIV_DONE:
    ; À ce stade, le résultat est dans le registre R0
    BX LR               		; Retourner de la fonction

DIV_ERROR:
    ; Gestion de l'erreur de division par zéro
    ; (ajouter ici le code pour gérer cette situation)
    BX LR               		; Retourner de la fonction

