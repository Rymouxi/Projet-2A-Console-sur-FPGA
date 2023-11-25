"""virtual_register est une variable du fichier que les fichiers externes peuvent modifier pour simuler les registres.\n
Il ne s'agit seulement des valeurs décimales de ces registres (plus simple pour la manipulation)\n
Leur numéros respectifs sont considérés instinctifs\n"""

virtual_register=[0 for i in range(9)]

def virtual_register_reset():
    """Initialisation du tableau de 8 registres: de R0 à R7\n
    R8 est le NZVC"""
    global virtual_register
    for i in range(9):
        virtual_register[i]=0
        

def virtual_register_write(reg_number:int,reg_value:int):
    """reg_number est le numéro du registre à modifier\n
    reg_value est la valeur à mettre dans ce registre\n
    Ce doit être une valeur décimale"""
    virtual_register[reg_number]=reg_value
