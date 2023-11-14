vlib work 

vcom FETCH.vhd
vcom FETCH_tb1.vhd

vsim work.fetch_tb1

add wave -position insertpoint  \
sim:/fetch_tb1/clk \
sim:/fetch_tb1/tb_delta \
sim:/fetch_tb1/tb_branchement \
sim:/fetch_tb1/tb_instruction \
sim:/fetch_tb1/oF_adresse \
sim:/fetch_tb1/oF_instruction


run 100 ns