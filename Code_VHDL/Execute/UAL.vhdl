
----------------------------------------------------------------------------------
-- Company: ENSEA
-- Engineer: APPOURCHAUX Léo
--
-- Create Date: 10/10/2023
-- Module Name: UAL - Behavioral
-- Project Name:
-- Target Devices: Arty A7-100
-- Tool versions:
-- Description:
--
-- Credits: GUENEGUES Morgane & ACELDY Alexandre
--
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;


entity UAL is
    Port ( iUAL_A : in STD_LOGIC_VECTOR (31 downto 0);
           iUAL_B : in STD_LOGIC_VECTOR (31 downto 0);
           iUAL_codeOp : in STD_LOGIC_VECTOR (2 downto 0);
           oUAL_sortie : out STD_LOGIC_VECTOR (31 downto 0);
           oUAL_NZVC : out STD_LOGIC_VECTOR (3 downto 0):="0000");
end UAL;


architecture Behavioral of UAL is

    signal signUAL_sortie : STD_LOGIC_VECTOR (31 downto 0);
    signal signUAL_V : STD_LOGIC;
    signal signUAL_C : STD_LOGIC;
    signal signUAL_moinsB : STD_LOGIC_VECTOR (31 downto 0);


begin

    calcul: process(iUAL_A,iUAL_B,iUAL_codeOp)
    begin

        CASE iUAL_codeOp IS

            WHEN "000" => -- ADD

                signUAL_sortie <= iUAL_A+iUAL_B;
                signUAL_V <= (iUAL_A(31) and iUAL_B(31) and (not signUAL_sortie (31))) or ((not iUAL_A(31)) and (not iUAL_B(31)) and signUAL_sortie(31));
                signUAL_C <= (iUAL_A(31) and iUAL_B(31)) or (iUAL_A(31) and (not signUAL_sortie(31))) or (iUAL_B(31) and (not signUAL_sortie(31)));

            WHEN "001" => -- SUB

                signUAL_sortie <= iUAL_A-iUAL_B;
                signUAL_moinsB <= (not iUAL_B) + 1;
                signUAL_V <= ((not iUAL_A(31)) and iUAL_B(31) and signUAL_sortie(31)) or (iUAL_A(31) and (not iUAL_B(31)) and (not signUAL_sortie(31)));
                signUAL_C <= (iUAL_A(31) and signUAL_moinsB(31)) or (iUAL_A(31) and (not signUAL_sortie(31))) or (signUAL_moinsB(31) and (not signUAL_sortie(31)));

            WHEN "010" => -- AND

                signUAL_sortie <= iUAL_A and iUAL_B ;
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN "011" => -- XOR

                signUAL_sortie <= iUAL_A xor iUAL_B;
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN "100" => -- S<-A (A<->Rn)

                signUAL_sortie <= iUAL_A;
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN "101" => -- S<-B (B<->Rm)

                signUAL_sortie <= iUAL_B;
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN ("110") => -- S<-A<<B

                signUAL_sortie (31 downto conv_integer(iUAL_B) ) <= iUAL_A (31-conv_integer(iUAL_B) downto 0) ; --Ces 2 lignes signifient "A sll B"
                signUAL_sortie(conv_integer(iUAL_B)-1 downto 0) <=(others=>'0');
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN ("111") => -- S<-A<<B (même chose, deux possibilités pour iUAL_codeOp)

                signUAL_sortie (31 downto conv_integer(iUAL_B) ) <= iUAL_A (31-conv_integer(iUAL_B) downto 0) ; --Ces 2 lignes signifient "A sll B"
                signUAL_sortie(conv_integer(iUAL_B)-1 downto 0) <=(others=>'0');
                signUAL_V <= '0';
                signUAL_C <= '0';

            WHEN OTHERS => NULL;

        END CASE;

    end process calcul;


oUAL_sortie <= signUAL_sortie;
        oUAL_NZVC(3) <= signUAL_sortie(31);
        oUAL_NZVC(2) <= (not signUAL_sortie(31)) and (not signUAL_sortie(30)) and (not signUAL_sortie(29)) and (not signUAL_sortie(28)) and (not signUAL_sortie(27)) and (not signUAL_sortie(26)) and (not signUAL_sortie(25)) and (not signUAL_sortie(24)) and (not signUAL_sortie(23)) and (not signUAL_sortie(22)) and (not signUAL_sortie(21)) and (not signUAL_sortie(20)) and (not signUAL_sortie(19)) and (not signUAL_sortie(18)) and (not signUAL_sortie(17)) and (not signUAL_sortie(16)) and (not signUAL_sortie(15)) and (not signUAL_sortie(14)) and (not signUAL_sortie(13)) and (not signUAL_sortie(12)) and (not signUAL_sortie(11)) and (not signUAL_sortie(10)) and (not signUAL_sortie(9)) and (not signUAL_sortie(8)) and (not signUAL_sortie(7)) and (not signUAL_sortie(6)) and (not signUAL_sortie(5)) and (not signUAL_sortie(4)) and (not signUAL_sortie(3)) and (not signUAL_sortie(2)) and (not signUAL_sortie(1)) and (not signUAL_sortie(0));
        oUAL_NZVC(1) <= signUAL_V;
        oUAL_NZVC(0) <= signUAL_C;


end Behavioral;
