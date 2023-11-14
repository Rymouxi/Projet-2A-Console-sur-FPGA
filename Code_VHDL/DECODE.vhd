----------------------------------------------------------------------------------
-- Company: ENSEA
-- Engineer: JIN CLEMENTINE
-- 
-- Create Date: 03.10.2023 14:19:34
-- Design Name: 
-- Module Name: DECODE - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity DECODE is
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
end DECODE;

architecture Behavioral of DECODE is

    signal signD_enW : STD_LOGIC:='0';
    signal signD_enMEM : STD_LOGIC:='0';
    signal signD_RW : STD_LOGIC:='0';
    signal signD_sel : STD_LOGIC:='0';
    signal signD_instBXX: STD_LOGIC;
    signal signD_instB: STD_LOGIC;
    signal signD_cond: STD_LOGIC_VECTOR (3 downto 0);
    signal signD_d : STD_LOGIC_VECTOR (2 downto 0):="000";
    signal signD_n : STD_LOGIC_VECTOR (2 downto 0):="000";
    signal signD_m : STD_LOGIC_VECTOR (2 downto 0):="000";
    signal signD_t : STD_LOGIC_VECTOR (2 downto 0):="000";
    signal signD_valeurImm : STD_LOGIC_VECTOR (31 downto 0):="00000000000000000000000000000000";
    signal signD_codeOp : STD_LOGIC_VECTOR (2 downto 0):="000";
    signal signD_delta : STD_LOGIC_VECTOR (31 downto 0);

begin

    translate: process(clk)
    begin 
        
        IF (clk' event)AND(clk='1') then 
            
        signD_enW <='0';
        signD_enMEM <='0';
        signD_RW <='0';
        signD_sel <='0';
        signD_instBXX <='0';
        signD_instB <='0';
        signD_cond <="0000";
        signD_d <="000";
        signD_n <="000";
        signD_m <="000";
        signD_t <="000";
        signD_valeurImm <="00000000000000000000000000000000";
        signD_codeOp <="000";
        signD_delta <="00000000000000000000000000000000";
        
        
            if (iD_instruction(15 downto 9)="0001110") --ADD Rd, Rn,#imm3
                then    signD_valeurImm (2 downto 0)<=iD_instruction (8 downto 6);
                        signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_d<=iD_instruction(2 downto 0);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;
    
            if (iD_instruction(15 downto 11)="00110") --ADD Rd, #imm8
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_d<=iD_instruction(10 downto 8);
                        signD_n<=iD_instruction(10 downto 8);
                        signD_valeurImm (7 downto 0)<=iD_instruction (7 downto 0);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;
            
            if (iD_instruction(15 downto 9)="0001100") --ADD Rd, Rn,Rm
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_d<=iD_instruction(2 downto 0);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_m<=iD_instruction(8 downto 6);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;    
    
            if (iD_instruction(15 downto 6)="0100000000") --AND Rd, Rm
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_d<=iD_instruction(2 downto 0);
                        signD_n<=iD_instruction(2 downto 0);
                        signD_m<=iD_instruction(5 downto 3);
                        signD_codeOp<="010";
                        signD_cond <="1111";
            end if;  

            if (iD_instruction(15 downto 11)="11100") --B label 
                then    
                    if (iD_instruction(10)='0')
                        then signD_delta <=  ("000000000000000000000")&(iD_instruction(10 downto 0));
                    else
                        signD_delta <= ("111111111111111111111")&(iD_instruction(10 downto 0));
                    end if;
                        signD_enW<='0';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '1';
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;  
            
            if (iD_instruction(15 downto 12)="1101") --BXX label 
                then    
                    if (iD_instruction(7)='0')
                        then signD_delta <=  ("000000000000000000000000")&(iD_instruction(7 downto 0));
                    else
                        signD_delta <= ("111111111111111111111111")&(iD_instruction(7 downto 0));
                    end if;
                        signD_enW<='0';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '1';
                        signD_instB <= '0';
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;             
           
            if (iD_instruction(15 downto 11)="00101") --CMP, Rn, imm8
                then    signD_enW<='0';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_n<=iD_instruction(10 downto 8);
                        signD_valeurImm(7 downto 0)<=iD_instruction(7 downto 0);
                        signD_codeOp<="001";
                        signD_cond <="1111";
            end if;             

            if (iD_instruction(15 downto 6)="0100000001") --EOR Rd, Rm
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_n<=iD_instruction(2 downto 0);
                        signD_m<=iD_instruction(5 downto 3);
                        signD_d<=iD_instruction(2 downto 0);
                        signD_codeOp<="011";
                        signD_cond <="1111";
            end if;  
            
            if (iD_instruction(15 downto 9)="0101100") --LDR Rt, Rn, Rm
                then    signD_enW<='0';
                        signD_enMEM<='1';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_m<=iD_instruction(8 downto 6);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_t<=iD_instruction(2 downto 0);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;  

            if (iD_instruction(15 downto 6)="0110100000") --LDR Rt,[Rn]
                then    signD_enW<='0';
                        signD_enMEM<='1';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_n<=iD_instruction(5 downto 3);
                        signD_t<=iD_instruction(2 downto 0);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;  

            if (iD_instruction(15 downto 11)="00000") --LSL Rd, Rm, #imm5
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_valeurImm(4 downto 0)<=iD_instruction(10 downto 6);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_d<=iD_instruction(2 downto 0);
                        signD_codeOp<="111";
                        signD_cond <="1111";
            end if;

            if (iD_instruction(15 downto 11)="00100") --MOV Rd, #imm5
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_valeurImm(7 downto 0)<=iD_instruction(7 downto 0);
                        signD_d<=iD_instruction(10 downto 8);
                        signD_codeOp<="101";
                        signD_cond <="1111";
            end if;

            if (iD_instruction(15 downto 6)="0000000000") --MOV Rd, Rm
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_d<=iD_instruction(2 downto 0);
                        signD_m<=iD_instruction(5 downto 3);
                        signD_codeOp<="100";
                        signD_cond <="1111";
            end if;
                            
            if (iD_instruction(15 downto 9)="0101000") --STR Rt, Rn, Rm
                then    signD_enW<='0';
                        signD_enMEM<='1';
                        signD_RW<='1';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_m<=iD_instruction(8 downto 6);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_t<=iD_instruction(2 downto 0);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;

            if (iD_instruction(15 downto 6)="0110000000") --STR Rt, [Rn]
                then    signD_enW<='0'; -- acces a la memoire ou pas
                        signD_enMEM<='1';
                        signD_RW<='1';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_n<=iD_instruction(5 downto 3);
                        signD_t<=iD_instruction(2 downto 0);
                        signD_codeOp<="000";
                        signD_cond <="1111";
            end if;

            if (iD_instruction(15 downto 9)="0001111") --SUB Rd, Rn, #imm3
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_valeurImm(2 downto 0)<=iD_instruction(8 downto 6);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_d<=iD_instruction(2 downto 0);
                        signD_codeOp<="001";
                        signD_cond <="1111";
            end if;

            if (iD_instruction(15 downto 11)="00111") --SUB Rd, #imm8
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='1';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_valeurImm(7 downto 0)<=iD_instruction(7 downto 0);
                        signD_n<=iD_instruction(10 downto 8);
                        signD_d<=iD_instruction(10 downto 8);
                        signD_codeOp<="001";
                        signD_cond <="1111";
            end if;
            
            if (iD_instruction(15 downto 9)="0001101") --SUB Rd, Rn, Rm
                then    signD_enW<='1';
                        signD_enMEM<='0';
                        signD_RW<='0';
                        signD_sel<='0';
                        signD_instBXX <= '0';
                        signD_instB <= '0';
                        signD_m<=iD_instruction(8 downto 6);
                        signD_n<=iD_instruction(5 downto 3);
                        signD_d<=iD_instruction(2 downto 0);
                        signD_codeOp<="001";
                        signD_cond <="1111";
            end if;
            
        END if; 
    end process translate; 

    oD_enW <= signD_enW;
    oD_enMEM <= signD_enMEM;
    oD_RW <= signD_RW;
    oD_sel <= signD_sel;
    oD_d <= signD_d;
    oD_n <= signD_n;
    oD_m <= signD_m;
    oD_t <= signD_t;
    oD_valeurImm <= signD_valeurImm;
    oD_codeOp <= signD_codeOp;
    oD_instBXX <= signD_instBXX;
    oD_instB <= signD_instB;
    oD_delta <= signD_delta;
    oD_cond <= signD_cond;

end Behavioral;
