;Fonction de division (On retourne R0 qui contient le quotient)

DIVIDE : 
	CMP R2, #0	        ;vérifier si le diviseur R2 est nul
	BEQ DIVIDE_ERROR

	MOV R0, 0	        ;initialiser le quotient à 0
	MOV R3, R1	        ;R1 la dividende
	
DIVIDE_LOOP
	CMP R3, R0	        ;Vérifier si R3 dividende = 0
	BEQ DIVIDE_DONE

	CMP R3, R2	        ;Vérifier si R3 dividende = R2 diviseur 
	BNE DIVIDE_INCREMENT

	SUB R3, R3, R2
	ADD R0, R0, #1
	B DIVIDE_LOOP

DIVIDE_INCREMENT
ADD R0, R0, #1
B DIVIDE_DONE

DIVIDE_DONE : 
DIVIDE_ERROR :
