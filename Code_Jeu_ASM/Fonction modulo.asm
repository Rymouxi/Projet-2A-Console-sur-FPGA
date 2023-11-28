;Fonction modulo : (On retourne R0 qui contient le reste)

MODULO : 
	CMP R2, #0          ;vérifier si le diviseur est nul
	BEQ MODULO_ERROR
	
	MOV R0, R1          ;R0 est le le quotient et R1 est la dividende
	MOV R3, #0          ;R3 est le reste

MODULO_LOOP : 
	CMP R0, R2          ;Comparer le quotient (la dividende) et le diviseur
	BEQ MODULO_DONE     ;Si dividende = diviseur, reste = 0

SUB R0, R0, R2          ;Soustraire le diviseur de la dividende
ADD R3, R3, #1          ;Ajouter 1 au reste
B MODULO_LOOP

MODULO_DONE : 
MOV R0, R3

MODULO_ERROR : 
