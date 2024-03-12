; Fonction de multiplication
; Résultat = R1 * R2
MULTIPLICATION:
MOV R0, #0      		; Initialiser le résultat à zéro

    	MUL_LOOP:
       		 CMP R2, #0          	; Vérifier si le multiplicateur R1 est nul
       		 BEQ MUL_DONE        	; Si c'est le cas, sortir de la boucle

CMP R1, #0         	; Vérifier si le multiplicand est nul
       		BEQ MUL_DONE        	; Si c'est le cas, sortir de la boucle

ADD R0, R0, R1      	; R0 = R0 + R1
       		SUB  R2, R2, #1     	; Décrémenter le multiplicateur   
CMP R2, #0      
BGE MUL_LOOP        	; Répéter la boucle si le multiplicateur est >= 0

    	MUL_DONE:
        	; À ce stade, le résultat est dans le registre R0
        	BX LR              			 ; Retourner de la fonction

