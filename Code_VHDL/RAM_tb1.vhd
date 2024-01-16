
----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 16.01.2024 16:01:52
-- Design Name: 
-- Module Name: RAM_tb2 - Behavioral
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
use IEEE.Numeric_Std.all;


-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity RAM_tb1 is
--  Port ( );
end RAM_tb1;

architecture Behavioral of RAM_tb1 is
    component RAM
    Port ( clk : in STD_LOGIC;
           iRAM_adresse : in STD_LOGIC_VECTOR (31 downto 0);
           iRAM_data : in STD_LOGIC_VECTOR (31 downto 0);
           iRAM_enW : in STD_LOGIC;
           iRAM_enMEM : in STD_LOGIC;
           iRAM_enRW : in STD_LOGIC;
           oRAM_data : out STD_LOGIC_VECTOR (31 downto 0));
    end component; 
    
    signal clk : STD_LOGIC;
    signal tb_adresse : STD_LOGIC_VECTOR (31 downto 0);
    signal tb_idata : STD_LOGIC_VECTOR (31 downto 0);
    signal tb_enW : STD_LOGIC;
    signal tb_enMEM : STD_LOGIC;
    signal tb_enRW : STD_LOGIC;
    signal tb_odata : STD_LOGIC_VECTOR (31 downto 0);
    
begin
    UT : RAM port map(clk=>clk, iRAM_adresse=>tb_adresse, iRAM_data=>tb_idata, iRAM_enW => tb_enW, iRAM_enMEM=>tb_enMEM, iRAM_enRW=>tb_enRW, oRAM_data=>tb_odata);

    testRAM : process 
    begin 
        tb_enW <= '0'; 
        tb_enMEM <= '0'; 
	tb_enRW <= '0';
        tb_adresse <= "00000000000000000000000000000000"; 
        wait for 1 ns;
        tb_enW <= '1';
        tb_enMEM <= '0';  
	tb_enRW <= '0';
        tb_adresse <= "00000000000000000000000000000011"; 
        tb_idata <= "00000000000000000000000000001010";
        wait until rising_edge(clk);
        wait for 1 ns;
        tb_enW <= '1';
        tb_enMEM <= '0';  
	tb_enRW <= '0';
        tb_adresse <= "00000000000000000000000000000111"; 
        tb_idata <= "00000000000000000000000000010100";
        wait until rising_edge(clk);
        wait for 1 ns;
        tb_enW <= '1';
        tb_enMEM <= '0';  
	tb_enRW <= '0';
        tb_adresse <= "00000000000000000000000000000011"; 
        tb_idata <= "00000000000000000000000000001111";
        wait until rising_edge(clk);
        wait for 1 ns;
        tb_enMEM <= '1'; 
        tb_enW <= '0';
	tb_enRW <= '0';
        tb_adresse <= "00000000000000000000000000000011"; 
        wait until rising_edge(clk);
        wait for 1 ns;
    end process;
    
    H : process
    begin
        clk <= '0'; wait for 10 ns;
        clk <= '1'; wait for 10 ns;
    end process;

end Behavioral;
