----------------------------------------------------------------------------------
-- Company: ENSEA
-- Engineer: JIN CLEMENTINE
-- 
-- Create Date: 26.09.2023 16:45:16
-- Design Name: 
-- Module Name: FETCH - Behavioral
-- Project Name: 
-- Target Devices: Arty A7-100
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments: credit GUENEGUES Morgane & ACELDY Alexandre
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

entity FETCH is
    Port ( clk : in STD_LOGIC;
           iF_branchement : in STD_LOGIC;
           iF_delta : in STD_LOGIC_VECTOR (31 downto 0);
           iF_instruction : in STD_LOGIC_VECTOR (15 downto 0);
           oF_adresse : out STD_LOGIC_VECTOR (31 downto 0);
           oF_instruction : out STD_LOGIC_VECTOR (15 downto 0));
end FETCH;

architecture Behavioral of FETCH is

    signal signF_pc : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000000" ;

begin
    increment : process(clk) begin
  
        if ((clk' event)and(clk='1')) then 
            if (iF_branchement='0')
                then signF_pc <= signF_pc+1 ;
            end if ;
            if (iF_branchement='1')
                then signF_pc <= signF_pc+iF_delta-1 ;
            end if ;
        end if;  
         
    end process increment; 
    
oF_adresse <= signF_pc;
oF_instruction <= iF_instruction;

end Behavioral;
