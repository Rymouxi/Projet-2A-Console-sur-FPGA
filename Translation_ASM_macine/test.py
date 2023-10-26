#from fonctions_LCM3 import *
#from treatment import *
from instruction_translation import *
from label_recognition import*

code='MOV R0,#10\nADD R0,#10\nAND R7,R3\nlabel:\nSTR R5,[R0]\nlol:\nBNE lol'

Number=-32
Binary='01001'
liste=['lion','chevre','girafe']

# print(label_recognition(code))
print(instruction_translation(code))
# print(bin(Number))
# print(format(int('101',2)+int('1',2),'b'))
# print(DecToBinCom(-5,10))

