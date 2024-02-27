
----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06.02.2024 13:53:05
-- Design Name: 
-- Module Name: ROM - Behavioral
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

entity R0M is
    Port ( clk : in STD_LOGIC;
           iR0M_adresse : in STD_LOGIC_VECTOR (31 downto 0);
           iR0M_data : in STD_LOGIC_VECTOR (15 downto 0);
           iR0M_enW : in STD_LOGIC;
           iR0M_enMEM : in STD_LOGIC;
           iR0M_enRW : in STD_LOGIC;
           oR0M_data : out STD_LOGIC_VECTOR (15 downto 0));
end ROM;

architecture Behavioral of ROM is

    type rom_type is array (0 to (2**8)-1) of std_logic_vector(15 downto 0);
    signal rom : rom_type;
    signal signROM_data : STD_LOGIC_VECTOR (31 downto 0) := "0000000000000000" ;

begin
    memory : process(clk) begin

        if rising_edge(clk) then 
            
            -- ecriture en memoire 
            if (iROM_enW='1') then 
                rom(conv_integer(iROM_adresse)) <= iROM_data;
            
            -- lecture en memoire 
            elsif (iROM_enMEM='1') then
                signROM_data <= rom(conv_integer(iROM_adresse));
            
            end if;
            
        end if;

    end process memory; 

oROM_data <= signROM_data;

end Behavioral;