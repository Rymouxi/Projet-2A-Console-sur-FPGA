-- Testbench automatically generated online
-- at https://vhdl.lapinoo.net
-- Generation date : 17.10.2023 13:55:34 UTC

library ieee;
use ieee.std_logic_1164.all;

entity tb_project1 is
end tb_project1;

architecture tb of tb_project1 is

    component project1
   	 port (clk   		 : in std_logic;
     		 iE_enW		 : in std_logic;
     		 iE_d  		 : in std_logic_vector (2 downto 0);
     		 iE_n  		 : in std_logic_vector (2 downto 0);
     		 iE_m  		 : in std_logic_vector (2 downto 0);
     		 iE_t  		 : in std_logic_vector (2 downto 0);
     		 iE_enMEM  	 : in std_logic;
     		 iE_RW 		 : in std_logic;
     		 iE_valeurImm   : in std_logic_vector (31 downto 0);
     		 iE_sel		 : in std_logic;
     		 iE_codeOp 	 : in std_logic_vector (2 downto 0);
     		 iE_instBXX     : in std_logic;
     		 iE_cond   	 : in std_logic_vector (3 downto 0);
     		 iE_delta  	 : in std_logic_vector (31 downto 0);
     		 iE_portA  	 : in std_logic_vector (31 downto 0);
     		 oE_portB  	 : out std_logic_vector (31 downto 0);
     		 oE_branchement : out std_logic;
     		 oE_delta  	 : out std_logic_vector (31 downto 0);
     		 oE_sortie 	 : out std_logic_vector (31 downto 0);
     		 oE_adresse     : out std_logic_vector (13 downto 0);
     		 oE_enabPortA   : out std_logic;
     		 oE_enabPortB   : out std_logic);
    end component;

    signal clk   		 : std_logic;
    signal iE_enW		 : std_logic;
    signal iE_d  		 : std_logic_vector (2 downto 0);
    signal iE_n  		 : std_logic_vector (2 downto 0);
    signal iE_m  		 : std_logic_vector (2 downto 0);
    signal iE_t  		 : std_logic_vector (2 downto 0);
    signal iE_enMEM  	 : std_logic;
    signal iE_RW 		 : std_logic;
    signal iE_valeurImm   : std_logic_vector (31 downto 0);
    signal iE_sel		 : std_logic;
    signal iE_codeOp 	 : std_logic_vector (2 downto 0);
    signal iE_instBXX     : std_logic;
    signal iE_cond   	 : std_logic_vector (3 downto 0);
    signal iE_delta  	 : std_logic_vector (31 downto 0);
    signal iE_portA  	 : std_logic_vector (31 downto 0);
    signal oE_portB  	 : std_logic_vector (31 downto 0);
    signal oE_branchement : std_logic;
    signal oE_delta  	 : std_logic_vector (31 downto 0);
    signal oE_sortie 	 : std_logic_vector (31 downto 0);
    signal oE_adresse     : std_logic_vector (13 downto 0);
    signal oE_enabPortA   : std_logic;
    signal oE_enabPortB   : std_logic;

    constant TbPeriod : time := 1000 ns; -- EDIT Put right period here
    signal TbClock : std_logic := '0';
    signal TbSimEnded : std_logic := '0';

begin

    dut : project1
    port map (clk   		 => clk,
     		 iE_enW		 => iE_enW,
     		 iE_d  		 => iE_d,
     		 iE_n  		 => iE_n,
     		 iE_m  		 => iE_m,
     		 iE_t  		 => iE_t,
     		 iE_enMEM  	 => iE_enMEM,
     		 iE_RW 		 => iE_RW,
     		 iE_valeurImm   => iE_valeurImm,
     		 iE_sel		 => iE_sel,
     		 iE_codeOp 	 => iE_codeOp,
     		 iE_instBXX     => iE_instBXX,
     		 iE_cond   	 => iE_cond,
     		 iE_delta  	 => iE_delta,
     		 iE_portA  	 => iE_portA,
     		 oE_portB  	 => oE_portB,
     		 oE_branchement => oE_branchement,
     		 oE_delta  	 => oE_delta,
     		 oE_sortie 	 => oE_sortie,
     		 oE_adresse     => oE_adresse,
     		 oE_enabPortA   => oE_enabPortA,
     		 oE_enabPortB   => oE_enabPortB);

    -- Clock generation
    TbClock <= not TbClock after TbPeriod/2 when TbSimEnded /= '1' else '0';

    -- EDIT: Check that clk is really your main clock signal
    clk <= TbClock;

    stimuli : process
    begin
   	 -- EDIT Adapt initialization as needed
   	 iE_enW <= '0';
   	 iE_d <= (others => '0');
   	 iE_n <= (others => '0'), "001" after 4000 ns;
   	 iE_m <= (others => '0');
   	 iE_t <= (others => '0'), "001" after 5000 ns;
   	 iE_enMEM <= '0';
   	 iE_RW <= '0';
   	 iE_valeurImm <= (others => '0');
   	 iE_sel <= '0';
   	 iE_codeOp <= (others => '0');
   	 iE_instBXX <= '0';
   	 iE_cond <= (others => '0');
   	 iE_delta <= (others => '0');
   	 iE_portA <= (others => '0');

   	 -- EDIT Add stimuli here
   	 wait for 100 * TbPeriod;

   	 -- Stop the clock and hence terminate the simulation
   	 TbSimEnded <= '1';
   	 wait;
    end process;

end tb;

-- Configuration block below is required by some simulators. Usually no need to edit.

configuration cfg_tb_project1 of tb_project1 is
    for tb
    end for;
end cfg_tb_project1;


