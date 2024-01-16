quit -sim 

vlib work 

vcom RAM.vhd
vcom RAM_tb1.vhd

vsim work.ram_tb1

add wave -radix Decimal -position insertpoint  \
sim:/RAM_tb1/clk \
sim:/RAM_tb1/tb_adresse \
sim:/RAM_tb1/tb_idata \
sim:/RAM_tb1/tb_enW \
sim:/RAM_tb1/tb_enMEM \
sim:/RAM_tb1/tb_enRW \
sim:/RAM_tb1/tb_odata


run 500 ns