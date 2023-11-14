vlib work

vcom DECODE.vhd
vcom DECODE_tb1.vhd

vsim work.decode_tb1

add wave -position insertpoint  \
sim:/decode_tb1/clk \
sim:/decode_tb1/tb_instruction \
sim:/decode_tb1/oD_enW \
sim:/decode_tb1/oD_enMEM \
sim:/decode_tb1/oD_RW \
sim:/decode_tb1/oD_sel \
sim:/decode_tb1/oD_cond \
sim:/decode_tb1/oD_d \
sim:/decode_tb1/oD_n \
sim:/decode_tb1/oD_m \
sim:/decode_tb1/oD_t \
sim:/decode_tb1/oD_valeurImm \
sim:/decode_tb1/oD_codeOp


run 100 ns