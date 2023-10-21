#from Fonctions_LCM3 import *
from DecToBin import *
from instruction_translation import *
from label_recognition import*

code='ADD R1,R5,#3\nAND R5,R3\nlabel:\nMOV R9,R4\nSTR R5,[R0]\nlol:\nBNE lol'

Number=-32
Binary='01001'
liste=['lion','chevre','girafe']

# print(label_recognition(code))
print(instruction_translation(code))
# print(bin(Number))
# print(format(int('101',2)+int('1',2),'b'))
# print(DecToBinCom(-5,10))

