quit -sim 

vlib work

vcom FETCH_DECODE.vhd
vcom FETCH_DECODE_tb.vhd

vsim work.FETCH_DECODE_tb

add wave -position insertpoint  \
sim:/FETCH_DECODE_tb/clk \
sim:/FETCH_DECODE_tb/oF_adresse \
sim:/FETCH_DECODE_tb/iD_instruction \
sim:/FETCH_DECODE_tb/oD_enW \
sim:/FETCH_DECODE_tb/oD_enMEM \
sim:/FETCH_DECODE_tb/oD_RW \
sim:/FETCH_DECODE_tb/oD_sel \
sim:/FETCH_DECODE_tb/oD_instBXX \
sim:/FETCH_DECODE_tb/oD_instB \
sim:/FETCH_DECODE_tb/oD_cond \
sim:/FETCH_DECODE_tb/oD_delta \
sim:/FETCH_DECODE_tb/oD_d \
sim:/FETCH_DECODE_tb/oD_n \
sim:/FETCH_DECODE_tb/oD_m \
sim:/FETCH_DECODE_tb/oD_t \
sim:/FETCH_DECODE_tb/oD_valeurImm \
sim:/FETCH_DECODE_tb/oD_codeOp


run 100 ns