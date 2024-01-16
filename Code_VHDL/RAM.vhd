
----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 16.01.2024 15:03:05
-- Design Name: 
-- Module Name: RAM - Behavioral
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
use IEEE.STD_LOGIC_arith.ALL;
use IEEE.STD_LOGIC_unsigned.ALL;

--use IEEE.Numeric_Std.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity RAM is
    Port ( clk : in STD_LOGIC;
           iRAM_adresse : in STD_LOGIC_VECTOR (31 downto 0);
           iRAM_data : in STD_LOGIC_VECTOR (31 downto 0);
           iRAM_enW : in STD_LOGIC;
           iRAM_enMEM : in STD_LOGIC;
           iRAM_enRW : in STD_LOGIC;
           oRAM_data : out STD_LOGIC_VECTOR (31 downto 0));
end RAM;

architecture Behavioral of RAM is

    type ram_type is array (0 to (2**8)-1) of std_logic_vector(31 downto 0);
    signal ram : ram_type;
    signal signRAM_data : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000000" ;

begin
    memory : process(clk) begin

        if rising_edge(clk) then 
            
            -- ecriture en memoire 
            if (iRAM_enW='1') then 
                ram(conv_integer(iRAM_adresse)) <= iRAM_data;
            
            -- lecture en memoire 
            elsif (iRAM_enMEM='1') then
                signRAM_data <= ram(conv_integer(iRAM_adresse));
            
            end if;
            
        end if;

    end process memory; 

oRAM_data <= signRAM_data;

end Behavioral;
