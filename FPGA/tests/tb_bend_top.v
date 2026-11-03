`timescale 1ns/1ps
module tb_bend_top;
reg clk=0;always #5 clk=~clk;
reg button=1;tri1 a,b,c,d,oscl,osda;wire tx,et,din,ws,bck,pa,led;
ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(button),.esp_rx(1'b1),.esp_tx(et),
 .uart_rx(1'b1),.uart_tx(tx),.adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),
 .HP_DIN(din),.HP_WS(ws),.HP_BCK(bck),.PA_EN(pa),.play_led(led),.oled_scl(oscl),.oled_sda(osda));
reg [15:0] adc_do=0,adc_re=0;reg ms=0;integer divider=0;
always @(negedge clk)begin divider=(divider+1)%4;ms=(divider==0);end
initial begin
 force dut.ms_tick=ms;force dut.guitar_mode=1;
 force dut.adc1_ch0=adc_do;force dut.adc1_ch1=adc_re;force dut.adc1_ch2=16'd0;force dut.adc1_ch3=16'd0;
 force dut.adc2_ch0=16'd0;force dut.adc2_ch1=16'd0;force dut.adc2_ch2=16'd0;
 repeat(10)@(negedge clk);adc_do=12800;repeat(30)@(negedge clk);
 if(dut.last_key!=1)$fatal(1,"last key Do missing");
 button=0;repeat(50)@(negedge clk);button=1;repeat(50)@(negedge clk);
 if(dut.bend_stable!=1 || dut.bend_level!=0)$fatal(1,"short bounce passed debounce");
 button=0;repeat(136000)@(negedge clk);
 if(dut.bend_stable!=0 || dut.bend_level!=511)$fatal(1,"bend ramp/debounce");
 if(dut.voice_do.inc_out!=32'd26968757 || dut.voice_re.inc_out!=32'd26909955)$fatal(1,"bend pitch or selectivity");
 // Fix for the donor's high-note truncation: high mapped increments use all32bits.
 force dut.voice_do.active_inc=32'd100000000;repeat(10)@(negedge clk);
 if(dut.voice_do.inc_out!=32'd112475585)$fatal(1,"high mapped pitch was truncated");
 release dut.voice_do.active_inc;
 adc_re=12800;repeat(30)@(negedge clk);
 if(dut.last_key!=2 || dut.voice_do.bend_inc!=0 || dut.voice_re.bend_inc==0)$fatal(1,"bend follows latest physical note");
 button=1;repeat(136000)@(negedge clk);
 if(dut.bend_level!=0 || dut.voice_re.bend_inc!=0)$fatal(1,"bend release ramp");
 if(dut.synth_overrun)$fatal(1,"overrun");
 $display("PASS D7 active-low debounce, ramp up/down, last-key bend, unselected pitch unchanged, high mapped note full-width multiply");$finish;
end
initial begin #10000000;$fatal(1,"timeout");end
endmodule
