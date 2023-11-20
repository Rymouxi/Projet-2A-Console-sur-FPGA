----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 17.10.2023 16:08:16
-- Design Name: 
-- Module Name: DECODE_tb1 - Behavioral
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

entity DECODE_tb1 is
--  Port ( );
end DECODE_tb1;

architecture Behavioral of DECODE_tb1 is
    component DECODE
   Port (   clk : in STD_LOGIC;
            iD_instruction : in STD_LOGIC_VECTOR (15 downto 0);
            oD_enW : out STD_LOGIC;
            oD_enMEM : out STD_LOGIC;
            oD_RW : out STD_LOGIC;
            oD_sel : out STD_LOGIC;
            oD_instBXX : out STD_LOGIC;
            oD_instB : out STD_LOGIC;
            oD_cond : out STD_LOGIC_VECTOR (3 downto 0);
            oD_delta : out STD_LOGIC_VECTOR (31 downto 0);
            oD_d : out STD_LOGIC_VECTOR (2 downto 0);
            oD_n : out STD_LOGIC_VECTOR (2 downto 0);
            oD_m : out STD_LOGIC_VECTOR (2 downto 0);
            oD_t : out STD_LOGIC_VECTOR (2 downto 0);
            oD_valeurImm : out STD_LOGIC_VECTOR (31 downto 0);
            oD_codeOp : out STD_LOGIC_VECTOR (2 downto 0));
    end component;
   
    signal clk : STD_LOGIC;
    signal tb_instruction : STD_LOGIC_VECTOR (15 downto 0);
    signal oD_enW : STD_LOGIC;
    signal oD_enMEM : STD_LOGIC;
    signal oD_RW : STD_LOGIC;
    signal oD_sel : STD_LOGIC;
    signal oD_instBXX : STD_LOGIC;
    signal oD_instB : STD_LOGIC;
    signal oD_cond : STD_LOGIC_VECTOR (3 downto 0);
    signal oD_delta : STD_LOGIC_VECTOR (31 downto 0);
    signal oD_d : STD_LOGIC_VECTOR (2 downto 0);
    signal oD_n : STD_LOGIC_VECTOR (2 downto 0);
    signal oD_m : STD_LOGIC_VECTOR (2 downto 0);
    signal oD_t : STD_LOGIC_VECTOR (2 downto 0);
    signal oD_valeurImm :STD_LOGIC_VECTOR (31 downto 0);
    signal oD_codeOp : STD_LOGIC_VECTOR (2 downto 0); 
    
begin
    DUT : DECODE port map(
              clk            => clk,
              iD_instruction => tb_instruction,
              oD_enW         => oD_enW,
              oD_enMEM       => oD_enMEM,
              oD_RW          => oD_RW,
              oD_sel         => oD_sel,
              oD_instBXX     => oD_instBXX,
              oD_instB       => oD_instB,
              oD_cond        => oD_cond,
              oD_delta       => oD_delta,
              oD_d           => oD_d,
              oD_n           => oD_n,
              oD_m           => oD_m,
              oD_t           => oD_t,
              oD_valeurImm   => oD_valeurImm,
              oD_codeOp      => oD_codeOp);

    testDecode : process
    begin 
        tb_instruction <= "0011001100001000"; -- ADD R3,#8
        wait until rising_edge(clk);
        wait for 3 ns;
        tb_instruction <= "0100000000101010"; -- AND R2,R5
        wait until rising_edge(clk);
        wait for 3 ns;  
        
    end process;

    H : process
    begin
        clk <= '0'; wait for 10 ns;
        clk <= '1'; wait for 10 ns;
    end process;

end Behavioral;
