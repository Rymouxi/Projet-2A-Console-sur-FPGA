quit -sim 

vlib work

vcom DECODE.vhd
vcom DECODE_tb2.vhd

vsim work.decode_tb2

add wave -position insertpoint  \
sim:/decode_tb2/clk \
sim:/decode_tb2/tb_instruction \
sim:/decode_tb2/oD_enW \
sim:/decode_tb2/oD_enMEM \
sim:/decode_tb2/oD_RW \
sim:/decode_tb2/oD_sel \
sim:/decode_tb2/oD_cond \
sim:/decode_tb2/oD_d \
sim:/decode_tb2/oD_n \
sim:/decode_tb2/oD_m \
sim:/decode_tb2/oD_t \
sim:/decode_tb2/oD_valeurImm \
sim:/decode_tb2/oD_codeOp


run 100 ns
