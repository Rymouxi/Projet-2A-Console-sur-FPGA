----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 23.01.2024 15:14:42
-- Design Name: 
-- Module Name: FEDEC - Behavioral
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

entity FEDEC is
    Port ( clk : in STD_LOGIC;
    -- FETCH
           iF_branchement : in STD_LOGIC;
           iF_delta : in STD_LOGIC_VECTOR (31 downto 0);
           iF_instruction : in STD_LOGIC_VECTOR (15 downto 0);
           oF_adresse : out STD_LOGIC_VECTOR (31 downto 0);
    -- DECODE 
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
           
end FEDEC;

architecture Behavioral of FEDEC is
    signal fd_instruction : STD_LOGIC_VECTOR (15 downto 0);

component FETCH
    Port ( clk : in STD_LOGIC;
           iF_branchement : in STD_LOGIC;
           iF_delta : in STD_LOGIC_VECTOR (31 downto 0);
           iF_instruction : in STD_LOGIC_VECTOR (15 downto 0);
           oF_adresse : out STD_LOGIC_VECTOR (31 downto 0);
           oF_instruction : out STD_LOGIC_VECTOR (15 downto 0));
end component;

component DECODE 
    Port ( clk : in STD_LOGIC;
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

begin
    FET : FETCH port map(clk=>clk, iF_branchement=>iF_branchement, iF_delta=>iF_delta, iF_instruction=>iF_instruction, oF_adresse=>oF_adresse, oF_instruction=>fd_instruction);
    DEC : DECODE port map (clk=>clk, iD_instruction=>fd_instruction, oD_enW=>oD_enW, oD_enMEM=>oD_enMEM, oD_RW=>oD_RW, oD_sel=>oD_sel, oD_instBXX=>oD_instBXX, oD_instB=>oD_instB, oD_cond=>oD_cond, oD_delta=>oD_delta, oD_d=>oD_d, oD_n=>oD_n, oD_m=>oD_m, oD_t=>oD_t, oD_valeurImm=>oD_valeurImm, oD_codeOp=>oD_codeOp);
end Behavioral;
