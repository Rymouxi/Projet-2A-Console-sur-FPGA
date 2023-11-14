quit -sim 

vlib work

vcom DECODE.vhd
vcom DECODE_tb6.vhd

vsim work.decode_tb6

add wave -position insertpoint  \
sim:/decode_tb6/clk \
sim:/decode_tb6/tb_instruction \
sim:/decode_tb6/oD_enW \
sim:/decode_tb6/oD_enMEM \
sim:/decode_tb6/oD_RW \
sim:/decode_tb6/oD_sel \
sim:/decode_tb6/oD_cond \
sim:/decode_tb6/oD_d \
sim:/decode_tb6/oD_n \
sim:/decode_tb6/oD_m \
sim:/decode_tb6/oD_t \
sim:/decode_tb6/oD_valeurImm \
sim:/decode_tb6/oD_codeOp


run 100 ns