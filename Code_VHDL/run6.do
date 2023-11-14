quit -sim 

vlib work

vcom DECODE.vhd
vcom DECODE_tb5.vhd

vsim work.decode_tb5

add wave -position insertpoint  \
sim:/decode_tb5/clk \
sim:/decode_tb5/tb_instruction \
sim:/decode_tb5/oD_enW \
sim:/decode_tb5/oD_enMEM \
sim:/decode_tb5/oD_RW \
sim:/decode_tb5/oD_sel \
sim:/decode_tb5/oD_cond \
sim:/decode_tb5/oD_d \
sim:/decode_tb5/oD_n \
sim:/decode_tb5/oD_m \
sim:/decode_tb5/oD_t \
sim:/decode_tb5/oD_valeurImm \
sim:/decode_tb5/oD_codeOp


run 100 ns