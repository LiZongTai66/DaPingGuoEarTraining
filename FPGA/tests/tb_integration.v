`timescale 1ns/1ps
module tb_integration;
 reg clk=0;always #5 clk=~clk;
 tri1 a,b,c,d;wire hp_din,hp_ws,hp_bck,pa,screen_tx,led,esp_tx;
 ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),.adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),
 .HP_DIN(hp_din),.HP_WS(hp_ws),.HP_BCK(hp_bck),.PA_EN(pa),.uart_rx(1'b1),.uart_tx(screen_tx),.play_led(led),.esp_rx(1'b1),.esp_tx(esp_tx));
 task check;input cond;input[511:0] text;begin if(!cond)begin $display("FAIL %0s",text);$fatal(1);end end endtask
 reg[7:0] screen_value=0;reg screen_valid=0;
 reg[31:0] app_value=0;reg app_valid=0;
 initial begin
  force dut.tjc_rx_data=screen_value;force dut.tjc_rx_valid=screen_valid;
  force dut.app_bridge.command=app_value;force dut.app_bridge.command_valid=app_valid;
 end
 task screen;input[7:0] value;begin @(negedge clk);screen_value=value;screen_valid=1;@(negedge clk);screen_valid=0;repeat(20)@(negedge clk);end endtask
 task app;input[31:0] value;begin @(negedge clk);app_value=value;app_valid=1;@(negedge clk);app_valid=0;repeat(20)@(negedge clk);end endtask
 initial begin
  repeat(20)@(negedge clk);
  check(dut.play_mode==1,"initial play mode preserved");
  screen(8'hE0);check(dut.touch_key_down==1&&dut.voice_do.active_inc==23977432,"screen virtual C4 preserved");
  screen(8'hE8);check(dut.touch_key_down==0,"screen release preserved");
  app(32'h30004800);screen(8'hE0);check(dut.voice_do.active_inc==dut.app_bridge.midi_inc(72),"screen/physical key mapping connected to voice");screen(8'hE8);
  app(32'h04010000);check(dut.guitar_mode==1,"App timbre reaches original register owner");
  screen(8'hB1);check(dut.demo_mode==1&&dut.demo_song==0,"B1 screen demo preserved");
  force dut.demo_trigger=7'b1;repeat(3)@(negedge clk);release dut.demo_trigger;
  check(dut.demo_voice.active_inc==23977432 && !dut.voice_do.active,"demo has fixed pitch on its independent voice");
  screen(8'hA0);check(!dut.demo_mode&&!dut.game_mode&&!dut.play_mode,"screen home preserved");
  app(32'h013e6400);check(dut.app_voices[0].voice.active_inc==26909955,"phone remote voice independent of screen mode");
  app(32'h05000000);repeat(10)@(negedge clk);check(dut.audio_sample==0,"volume zero mutes output");
  app(32'h03000000);check(!dut.app_voices[0].voice.active,"App emergency stop reaches remote voice");
  screen(8'hA1);check(dut.play_mode,"screen free play preserved");
  screen(8'hC1);check(dut.game_mode&&!dut.play_mode,"screen game mode preserved");
  $display("PASS: original touch E0/E8, modes A0/A1/B1/C1, fixed demo pitch, dynamic key mapping, separate App voice, timbre, volume and stop");$finish;
 end
 initial begin #1000000;$fatal(1,"timeout");end
endmodule


