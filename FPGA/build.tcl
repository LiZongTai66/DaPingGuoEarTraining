add_file -type verilog src/ear_training.v
set_device -name GW2A-18C GW2A-LV18PG256C8/I7
add_file -type verilog src/ads1115_pressure_test.v
add_file -type verilog src/pcm5102_i2s_tx.v
add_file -type verilog src/additive32_bank.v
add_file -type verilog src/dpg_uart.v
add_file -type verilog src/dpg_bridge.v
add_file -type verilog src/oled_audio_scope.v
add_file -type verilog src/oled_i2c_byte.v
add_file -type sdc src/fourth_app.sdc
set_option -top_module ads1115_pressure_test
set_option -verilog_std v2001
add_file -type cst src/fifth_oled.cst
set_option -use_sspi_as_gpio 1
set_option -output_base_name fifth_pcm5102_ear
set_option -place_option 0
set_option -route_option 0
run all




