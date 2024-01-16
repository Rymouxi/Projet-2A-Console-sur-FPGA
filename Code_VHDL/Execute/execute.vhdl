----------------------------------------------------------------------------------
-- Company:
-- Engineer:
--
-- Create Date: 10.10.2023 14:21:45
-- Design Name:
-- Module Name: project1 - Behavioral
-- Project Name:
-- Target Devices:
-- Tool Versions:
-- Description:
--
-- Dependencies:
--
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity project1 is
    Port ( clk : in STD_LOGIC;
  		 iE_enW : in STD_LOGIC;
  		 iE_d : in STD_LOGIC_VECTOR (2 downto 0);
  		 iE_n : in STD_LOGIC_VECTOR (2 downto 0);
  		 iE_m : in STD_LOGIC_VECTOR (2 downto 0);
  		 iE_t : in STD_LOGIC_VECTOR (2 downto 0);
  		 iE_enMEM : in STD_LOGIC;
  		 iE_RW : in STD_LOGIC;
  		 iE_valeurImm : in STD_LOGIC_VECTOR (31 downto 0);
  		 iE_sel : in STD_LOGIC;
  		 iE_codeOp : in STD_LOGIC_VECTOR (2 downto 0);
  		 iE_instBXX : in STD_LOGIC;
  		 iE_cond : in STD_LOGIC_VECTOR (3 downto 0);
  		 iE_delta : in STD_LOGIC_VECTOR (31 downto 0);
  		 iE_portA : in STD_LOGIC_VECTOR (31 downto 0);
  		 oE_portB : out STD_LOGIC_VECTOR (31 downto 0);
  		 oE_branchement : out STD_LOGIC;
  		 oE_delta : out STD_LOGIC_VECTOR (31 downto 0);
  		 oE_sortie : out STD_LOGIC_VECTOR (31 downto 0);
  		 oE_adresse : out STD_LOGIC_VECTOR (13 downto 0);
  		 oE_enabPortA : out STD_LOGIC;
  		 oE_enabPortB : out STD_LOGIC);
      		 
 		 
end project1;

architecture Behavioral of project1 is

    Type etat is (etat1, etat2, etat3) ;
    Signal present, futur : etat ;

    Type etatReg is (attente, maj) ;
    signal presentReg, futurReg : etatReg ;

    signal signE_sortie : STD_LOGIC_VECTOR (31 downto 0):=
"00000000000000000000000000000000";
    signal signE_adresse : STD_LOGIC_VECTOR (13 downto 0):="00000000000000";
    signal signE_portB : STD_LOGIC_VECTOR (31 downto 0):=
"00000000000000000000000000000000";
    signal signE_A : STD_LOGIC_VECTOR (31 downto 0):="00000000000000000000000000000000";
    signal signE_B : STD_LOGIC_VECTOR (31 downto 0):="00000000000000000000000000000000";
    
 signal signE_R0 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000011110000";
     signal signE_R1 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000001111000000";
     signal signE_R2 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000000000000";
     signal signE_R3 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000111000011";
     signal signE_R4 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000000000000";
     signal signE_R5 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000000000000";
     signal signE_R6 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000000000000";
     signal signE_R7 : STD_LOGIC_VECTOR (31 downto 0):=
 "00000000000000000000000000000000";
 
	--- Number of Slave Registers 32
	constant NREG : natural := 8;
	type array_reg is array (0 to NREG-1) of std_logic_vector(31 downto 0);
	signal signE_R : array_reg;
    
-- 	signE_R3 = signE_R(3)
    signal signE_branchement: STD_LOGIC;
    signal signE_delta: STD_LOGIC_VECTOR (31 downto 0):=
"00000000000000000000000000000000";
    signal signE_NZVC: STD_LOGIC_VECTOR (3 downto 0);
    signal signE_t: STD_LOGIC_VECTOR (2 downto 0);
    signal signE_enabPortA : STD_LOGIC;
    signal signE_enabPortB : STD_LOGIC;
    signal signE_enableEXECUTE: STD_LOGIC;
    signal signE_enableMajReg: STD_LOGIC;
    
    type MonTableauType is array (INTEGER range <>) of STD_LOGIC_VECTOR (31 downto 0);
    signal MonTableauSignals : MonTableauType(0 to 6);

COMPONENT UAL
PORT (iUAL_A : in STD_LOGIC_VECTOR (31 downto 0);
    iUAL_B : in STD_LOGIC_VECTOR (31 downto 0);
    iUAL_codeOp : in STD_LOGIC_VECTOR (2 downto 0);
    oUAL_sortie : out STD_LOGIC_VECTOR (31 downto 0);
    oUAL_NZVC : out STD_LOGIC_VECTOR (3 downto 0):="0000"
);
END COMPONENT;


begin
--calcul
    calcul: UAL
   	 PORT MAP(iUAL_A=>signE_A,
       		 iUAL_B=>signE_B,
       		 iUAL_codeOp=>iE_codeOp,
       		 oUAL_sortie=>signE_sortie,
       		 oUAL_NZVC=>signE_NZVC);

--selection entrée 1
signE_A <= signE_R(conv_integer(iE_n));


--selection entrée 2
signE_B<=iE_valeurImm WHEN (iE_sel = '1')else
   	 signE_R(conv_integer(iE_m));


----------detection d'un branchement effectif (B ou BXX avec condition vérifiée)
detectionBranchement: process
begin
wait on iE_instBXX, iE_instBXX, iE_cond, signE_NZVC(2), present;
--signE_enableEXECUTE;

    if (present=etat2 or present=etat2) then signE_branchement <= '0';
    else
   	 if (iE_instBXX='1') --B label
   		 then signE_branchement <= '1';

   	 elsif (iE_instBXX='1' and iE_cond="0000") --BEQ
   		 then
       		 if(signE_NZVC(2)='1') then signE_branchement <= '1';
       		 end if;

   	 elsif (iE_instBXX='1' and iE_cond="0001") --BNE
   		 then
       		 if(signE_NZVC(2)='0') then signE_branchement <= '1';
       		 end if;

   	 else
   		 signE_branchement <= '0';
   	 end if;
    end if;
    signE_delta <= iE_delta;
end process detectionBranchement;




 ----------séquenceur pour bloquer l'execution pendant 2 tops d'horloge si un branchement est détécté
----partie synchrone
sequenceur: process(clk)
begin

    IF(clk'event)AND(clk='1') THEN present <= futur;
    END IF;

end process sequenceur;

----partie asynchrone
definitionEtats: process(present, signE_branchement)
begin
    case present is

   	 when etat1 =>
   		 if signE_branchement = '1' then futur <= etat2;
   		 end if;
   	 when etat2 =>
   		 futur <= etat3;
   	 when etat3 =>
   		 futur <= etat1;

    end case;
end process definitionEtats;



----------séquenceur pour effectuer la maj des registres lors de la lecture en RAM,
-- 1 top après l'arrivée de l'instruction LDR (le temps que la RAM envoie la donnée)
----partie synchrone
sequenceurReg: process(clk)
begin

    IF(clk'event)AND(clk='1') THEN presentReg <= futurReg;
    END IF;

end process sequenceurReg;

----partie asynchrone
definitionEtatsReg: process(presentReg, signE_enabPortA)
begin
    case presentReg is

   	 when attente =>
   		 if signE_enabPortA = '1' then futurReg <= maj;
   		 signE_t <= iE_t;
   		 end if;
   	 when maj =>
   		 futurReg <= attente;

    end case;
end process definitionEtatsReg;

--A faire
-- mettre un multiplexeur pour d, n , m ,t qui renvoi à Rd, Rt, Rn et Rm
--Rt sort de la ram et va dans le multiplexeur


 ----------gestion de l'écriture en registre et en RAM
lecture: process (clk)
begin

 --   IF(clk'event)AND(clk='1') THEN
  --     IF signE_enableEXECUTE= '1' THEN

              		 
 --écriture de la sortie dans le registre Rd
    IF ((iE_enW = '1')) THEN
   	 signE_R(conv_integer(iE_d))<=signE_sortie;
    END IF;

    IF ((iE_enMEM='1' AND iE_RW='0')) THEN --lecture de la RAM
		 signE_enabPortA <= '1';
		 signE_enabPortB <= '0';
		 signE_adresse <= signE_sortie(13 downto 0);
		 signE_A<=signE_R(conv_integer(iE_t));
    END IF;


   IF ((iE_enMEM='1' AND iE_RW='1')) THEN --écriture dans la RAM
     	  signE_enabPortA <= '0';
     	  signE_enabPortB <= '1';
     	  signE_adresse <= signE_sortie(13 downto 0);
   	 signE_B<=signE_R(conv_integer(iE_t));
    END IF;

   	 if (iE_t="000") then
   		 signE_portB<=signE_R0;
   		 else
   		 signE_portB<=signE_R1;
   	 end if;


---------maj registres

   if(futurReg=maj) then
signE_R(conv_integer(iE_t))<=iE_portA;
 
    end if;

end process lecture;




oE_sortie <= signE_sortie;

oE_portB <= signE_portB;
oE_delta <= signE_delta;
oE_branchement <= signE_branchement;
signE_enableEXECUTE <= '1' when present=etat1
else '0';
signE_enableMajReg <= '1' when presentReg=maj
else '0';

oE_enabPortB <= signE_enabPortB;


oE_enabPortA <= signE_enabPortA;


oE_adresse <= signE_adresse;


end Behavioral;


