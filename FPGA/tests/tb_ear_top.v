`timescale 1ns/1ps
module tb_ear_top;
reg clk=0;always #5 clk=~clk;
reg app_rx=1,tick=0;tri1 a,b,c,d,oscl,osda;
wire tx,app_tx;reg [15:0] adc[0:6];
wire [15:0] adc0=adc[0],adc1=adc[1],adc2=adc[2],adc3=adc[3],adc4=adc[4],adc5=adc[5],adc6=adc[6];
ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),.esp_rx(app_rx),.esp_tx(app_tx),
 .uart_rx(1'b1),.uart_tx(tx),.adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),.oled_scl(oscl),.oled_sda(osda));
wire [7:0] rb;wire rbvalid;wire [31:0] response;wire rv;
dpg_uart_rx monitor(clk,app_tx,rb,rbvalid);dpg_frame_rx decoder(clk,rb,rbvalid,response,rv);
integer logfd,tones=0,audio=0,finals=0,live_count=0,undo=0,snapshots=0,i,j;reg saw_input=0;reg [2:0] pitch[0:6];
initial begin
 logfd=$fopen("validation/ear-uart.hex","w");
 force dut.ms_tick=tick;
 force dut.adc1_ch0=adc0;force dut.adc1_ch1=adc1;force dut.adc1_ch2=adc2;force dut.adc1_ch3=adc3;
 force dut.adc2_ch0=adc4;force dut.adc2_ch1=adc5;force dut.adc2_ch2=adc6;
end
always @(posedge clk)begin
 if(rbvalid)$fwrite(logfd,"%02x ",rb);
 if(dut.ear_trigger && dut.ear_core.state==dut.ear_core.PLAY)begin
  if(dut.ear_note!==pitch[tones%7])$fatal(1,"playback ordering");tones=tones+1;
 end
 if(dut.sample_tick && dut.ear_active && dut.audio_sample!=0)audio=audio+1;
 if(rv)begin
  if(response[31:24]==8'hB0 && response[7:0]==2)saw_input=1;
  if(response[31:24]==8'hB1)live_count=live_count+1;
  if(response[31:24]==8'hB5)undo=undo+1;
  if(response[31:24]==8'hB6)snapshots=snapshots+1;
  if(response[31:24]==8'hB2)finals=finals+1;
 end
end
task byte_app;input [7:0]v;integer k;begin
 @(negedge clk);app_rx=0;repeat(234)@(negedge clk);
 for(k=0;k<8;k=k+1)begin app_rx=v[k];repeat(234)@(negedge clk);end
 app_rx=1;repeat(234)@(negedge clk);
end endtask
task command;input [7:0]cc,x,y,z;reg [7:0]check;begin
 check=~(cc+x+y+z);byte_app(8'hAA);byte_app(cc);byte_app(x);byte_app(y);byte_app(z);byte_app(check);
 repeat(300)@(negedge clk);
end endtask
task ms;input integer n;integer k;begin for(k=0;k<n;k=k+1)begin
 @(negedge clk);tick=1;@(negedge clk);tick=0;repeat(198)@(negedge clk);
end end endtask
task pressure;input integer n;integer k;begin
 for(k=0;k<7;k=k+1)adc[k]=0;ms(4);
 adc[n]=16'd14080;ms(4);repeat(16000)@(negedge clk);
end endtask
initial begin
 pitch[0]=0;pitch[1]=0;pitch[2]=2;pitch[3]=4;pitch[4]=6;pitch[5]=5;pitch[6]=1;
 for(i=0;i<7;i=i+1)adc[i]=0;repeat(30)@(negedge clk);
 command(8'h30,0,80,0);if(dut.app_bridge.mapping[0]!=80)$fatal(1,"setup remap failed");
 pressure(3);if(!dut.voice_fa.active)$fatal(1,"setup physical held voice");
 command(8'h40,0,123,7);repeat(20)@(negedge clk);
 if(!dut.ear_active || dut.app_bridge.mapping[0]!=60 || dut.app_bridge.mapping[6]!=71)$fatal(1,"prepare/reset map or immediate abort");
 if(dut.voice_fa.active)$fatal(1,"prepare must silence previously held physical voice");
 for(i=0;i<7;i=i+1)command(8'h41,0,123,(i<<3)|pitch[i]);
 command(8'h42,0,123,0);pressure(6);ms(4200);repeat(20000)@(negedge clk);
 if(!saw_input || tones!=7 || dut.ear_core.count!=0 || audio==0)$fatal(1,"demo/gating/audio failed");
 pressure(0);pressure(0);pressure(2);
 command(8'h45,0,123,1);command(8'h45,0,123,2);command(8'h45,0,123,2);repeat(20000)@(negedge clk);
 if(dut.ear_core.count!=1)$fatal(1,"undo retry applied twice");
 command(8'h44,0,123,0);ms(4200);repeat(20000)@(negedge clk);
 if(tones!=14 || dut.ear_core.count!=0)$fatal(1,"replay failed");
 for(i=0;i<7;i=i+1)pressure(pitch[i]);
 if(finals!=0 || dut.ear_core.count!=7)$fatal(1,"must allow editing before submit");
 command(8'h45,0,123,3);repeat(20000)@(negedge clk);if(dut.ear_core.count!=6)$fatal(1,"undo seventh");
 pressure(1);command(8'h46,0,123,0);repeat(200000)@(negedge clk);
 if(finals!=1 || snapshots!=7 || live_count!=11 || undo!=4)$fatal(1,"upload result frames finals=%0d snaps=%0d live=%0d undo=%0d",finals,snapshots,live_count,undo);
 $fclose(logfd);
 $display("PASS full-top ear: real115200 UART, pressure edges, automatic remap reset, 14 demo tones, PCM audio=%0d, live_count11, undo/retry4, final7+end, replay clears input",audio);$finish;
end
initial begin #100000000;$fatal(1,"timeout");end
endmodule

