-- Testbench automatically generated online
-- at https://vhdl.lapinoo.net
-- Generation date : 19.3.2024 14:03:31 UTC

library ieee;
use ieee.std_logic_1164.all;

entity FETCH_DECODE_tb is
end FETCH_DECODE_tb;

architecture tb of FETCH_DECODE_tb is

    component FETCH_DECODE
        port (clk            : in std_logic;
              iF_branchement : in std_logic;
              iF_delta       : in std_logic_vector (31 downto 0);
              oF_adresse     : out std_logic_vector (31 downto 0);
              iD_instruction : in std_logic_vector (15 downto 0);
              oD_enW         : out std_logic;
              oD_enMEM       : out std_logic;
              oD_RW          : out std_logic;
              oD_sel         : out std_logic;
              oD_instBXX     : out std_logic;
              oD_instB       : out std_logic;
              oD_cond        : out std_logic_vector (3 downto 0);
              oD_delta       : out std_logic_vector (31 downto 0);
              oD_d           : out std_logic_vector (2 downto 0);
              oD_n           : out std_logic_vector (2 downto 0);
              oD_m           : out std_logic_vector (2 downto 0);
              oD_t           : out std_logic_vector (2 downto 0);
              oD_valeurImm   : out std_logic_vector (31 downto 0);
              oD_codeOp      : out std_logic_vector (2 downto 0));
    end component;

    signal clk            : std_logic;
    signal iF_branchement : std_logic;
    signal iF_delta       : std_logic_vector (31 downto 0);
    signal oF_adresse     : std_logic_vector (31 downto 0);
    signal iD_instruction : std_logic_vector (15 downto 0);
    signal oD_enW         : std_logic;
    signal oD_enMEM       : std_logic;
    signal oD_RW          : std_logic;
    signal oD_sel         : std_logic;
    signal oD_instBXX     : std_logic;
    signal oD_instB       : std_logic;
    signal oD_cond        : std_logic_vector (3 downto 0);
    signal oD_delta       : std_logic_vector (31 downto 0);
    signal oD_d           : std_logic_vector (2 downto 0);
    signal oD_n           : std_logic_vector (2 downto 0);
    signal oD_m           : std_logic_vector (2 downto 0);
    signal oD_t           : std_logic_vector (2 downto 0);
    signal oD_valeurImm   : std_logic_vector (31 downto 0);
    signal oD_codeOp      : std_logic_vector (2 downto 0);

begin

    dut : FETCH_DECODE
    port map (clk            => clk,
              iF_branchement => iF_branchement,
              iF_delta       => iF_delta,
              oF_adresse     => oF_adresse,
              iD_instruction => iD_instruction,
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

    stimuli : process
    begin
	iD_instruction <= "0011001100001000"; -- ADD R3,#8
	wait until rising_edge(clk); 
	iD_instruction <= "0100000000101010"; -- AND R2,R5
	wait until rising_edge(clk);
	iD_instruction <= "0010001000000100"; -- MOV R2,#4
	wait until rising_edge(clk);
    end process;

    H : process
    begin
        clk <= '0'; wait for 10 ns;
        clk <= '1'; wait for 10 ns;
    end process;


end tb;

-- Configuration block below is required by some simulators. Usually no need to edit.

configuration cfg_tb_FETCH_DECODE of FETCH_DECODE_tb is
    for tb
    end for;
end cfg_tb_FETCH_DECODE;