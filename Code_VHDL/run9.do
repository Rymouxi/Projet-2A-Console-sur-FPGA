quit -sim 

vlib work

vcom DECODE.vhd
vcom DECODE_tb8.vhd

vsim work.decode_tb8

add wave -position insertpoint  \
sim:/decode_tb8/clk \
sim:/decode_tb8/tb_instruction \
sim:/decode_tb8/oD_enW \
sim:/decode_tb8/oD_enMEM \
sim:/decode_tb8/oD_RW \
sim:/decode_tb8/oD_sel \
sim:/decode_tb8/oD_d \
sim:/decode_tb8/oD_n \
sim:/decode_tb8/oD_m \
sim:/decode_tb8/oD_t \
sim:/decode_tb8/oD_delta \
sim:/decode_tb8/oD_cond \
sim:/decode_tb8/oD_valeurImm \
sim:/decode_tb8/oD_codeOp


run 100 ns