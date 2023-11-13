----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 17.10.2023 14:27:58
-- Design Name: 
-- Module Name: FETCH_tb1 - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity FETCH_tb1 is
--  Port ( );
end FETCH_tb1;

architecture Behavioral of FETCH_tb1 is
    component FETCH
        Port ( clk : in STD_LOGIC;
               iF_branchement : in STD_LOGIC;
               iF_delta : in STD_LOGIC_VECTOR (31 downto 0);
               iF_instruction : in STD_LOGIC_VECTOR (15 downto 0);
               oF_adresse : out STD_LOGIC_VECTOR (31 downto 0);
               oF_instruction : out STD_LOGIC_VECTOR (15 downto 0));
    end component;
    
         
    signal clk : STD_LOGIC;
    signal tb_delta : STD_LOGIC_VECTOR (31 downto 0);
    signal tb_branchement : STD_LOGIC;
    signal tb_instruction : STD_LOGIC_VECTOR (15 downto 0);
    signal oF_adresse : STD_LOGIC_VECTOR (31 downto 0);
    signal oF_instruction : STD_LOGIC_VECTOR (15 downto 0);

begin
    
    UUT : FETCH port map(clk=>clk, iF_branchement=>tb_branchement, iF_delta=>tb_delta, iF_instruction => tb_instruction, oF_adresse=>oF_adresse, oF_instruction=>oF_instruction);

    testFetch : process 
    begin 
        tb_instruction <= "0000000000000000";
        tb_delta <= "00000000000000000000000000000011";
        wait for 1 ns;
        tb_branchement <= '0';
        wait until rising_edge(clk);
        wait for 1 ns;
        tb_branchement <= '1';
        wait until rising_edge(clk);


    end process;
    
    H : process
    begin
        clk <= '0'; wait for 10 ns;
        clk <= '1'; wait for 10 ns;
    end process;

end Behavioral;
