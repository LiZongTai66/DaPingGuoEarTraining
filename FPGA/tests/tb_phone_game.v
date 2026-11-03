`timescale 1ns/1ps
module tb_phone_game;
reg clk=0;always #5 clk=~clk;
reg app_rx=1,screen_rx=1;tri1 a,b,c,d,oscl,osda;
wire tx,app_tx,din,ws,bck,pa,led;
ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),
 .esp_rx(app_rx),.esp_tx(app_tx),.uart_rx(screen_rx),.uart_tx(tx),
 .adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),
 .HP_DIN(din),.HP_WS(ws),.HP_BCK(bck),.PA_EN(pa),.play_led(led),.oled_scl(oscl),.oled_sda(osda));
wire [7:0] rb;wire rv;wire [31:0] response;wire valid;
dpg_uart_rx monitor(clk,app_tx,rb,rv);dpg_frame_rx frames(clk,rb,rv,response,valid);
reg saw_pong=0;integer nonzero=0,magnitude=0,peak=0;
reg [15:0] adc=0;
always @(posedge clk)begin
 if(valid && response==32'h83010203)saw_pong=1;
 if(dut.sample_tick)begin
  magnitude=$signed(dut.audio_sample);if(magnitude<0)magnitude=-magnitude;
  if(magnitude>0)nonzero=nonzero+1;if(magnitude>peak)peak=magnitude;
 end
end
initial begin
 force dut.adc1_ch0=adc;force dut.adc1_ch1=16'd0;force dut.adc1_ch2=16'd0;force dut.adc1_ch3=16'd0;
 force dut.adc2_ch0=16'd0;force dut.adc2_ch1=16'd0;force dut.adc2_ch2=16'd0;
end
task byte_app;input [7:0]v;integer j;begin
 @(negedge clk);app_rx=0;repeat(234)@(negedge clk);
 for(j=0;j<8;j=j+1)begin app_rx=v[j];repeat(234)@(negedge clk);end
 app_rx=1;repeat(234)@(negedge clk);
end endtask
task command;input [7:0]cmd,x,y,z;reg[7:0]check;
begin check=~(cmd+x+y+z);byte_app(8'haa);byte_app(cmd);byte_app(x);byte_app(y);byte_app(z);byte_app(check);end endtask
task screen;input[7:0]v;integer j;begin
 @(negedge clk);screen_rx=0;repeat(2813)@(negedge clk);
 for(j=0;j<8;j=j+1)begin screen_rx=v[j];repeat(2813)@(negedge clk);end
 screen_rx=1;repeat(2813)@(negedge clk);
end endtask
initial begin
 repeat(20)@(negedge clk);command(8'h20,1,2,3);repeat(16000)@(negedge clk);
 wait(saw_pong); // Startup now includes a complete seven-key snapshot.
 command(8'h04,1,0,0);if(!dut.guitar_mode)$fatal(1,"phone guitar selection");
 command(8'h01,60,110,0);repeat(135000)@(negedge clk);
 if(!dut.app_voices[0].voice.active || !dut.app_voices[0].voice.note_guitar || nonzero<100 || peak<300)$fatal(1,"phone guitar audio missing");
 command(8'h02,60,0,0);repeat(20)@(negedge clk);
 if(!dut.app_voices[0].voice.released)$fatal(1,"phone note off missing");
 command(8'h03,0,0,0);repeat(20)@(negedge clk);
 if(dut.app_voices[0].voice.active)$fatal(1,"phone all off missing");
 command(8'h05,0,0,0);repeat(20)@(negedge clk);if(dut.app_gain!=0)$fatal(1,"phone volume zero");
 screen(8'hc1);screen(8'hd0);repeat(27000)@(negedge clk);
 nonzero=0;peak=0;adc=12800;repeat(216000)@(negedge clk);
 if(dut.game_judge.score!=60 || !dut.demo_voice.note_guitar || nonzero<100 || peak<300)$fatal(1,"game guitar missing");
 if(dut.synth_overrun)$fatal(1,"sample deadline overrun");
 $display("PASS actual115200 App PING/PONG, guitar selection, NOTE_ON audio/NOTE_OFF, ALL_OFF, volume; actual9600 C1/D0 game guitar sounds with App volume0; peak=%0d",peak);$finish;
end
initial begin #30000000;$fatal(1,"timeout");end
endmodule
