`timescale 1ns/1ps
module tb_tjc_modes;
 reg clk=0;always #5 clk=~clk;
 reg ms=0;integer divider=0,ticks=0;
 always @(negedge clk)begin
  divider=(divider+1)%4;ms=(divider==0);
 end
 always @(posedge clk)if(ms)ticks=ticks+1;
 tri1 a,b,c,d,oscl,osda;
 wire din,ws,bck,pa,tx,led,esp_tx;
 ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),.adc1_sda(a),.adc1_scl(b),
 .adc2_sda(c),.adc2_scl(d),.HP_DIN(din),.HP_WS(ws),.HP_BCK(bck),.PA_EN(pa),
 .uart_rx(1'b1),.uart_tx(tx),.play_led(led),.esp_rx(1'b1),.esp_tx(esp_tx),
 .oled_scl(oscl),.oled_sda(osda));
 reg [7:0] command=0;reg valid=0;
 reg [15:0] adc=0;
 initial begin
  force dut.ms_tick=ms;force dut.tjc_rx_data=command;force dut.tjc_rx_valid=valid;
  force dut.adc1_ch0=adc;force dut.adc1_ch1=16'd0;force dut.adc1_ch2=16'd0;force dut.adc1_ch3=16'd0;
  force dut.adc2_ch0=16'd0;force dut.adc2_ch1=16'd0;force dut.adc2_ch2=16'd0;
 end
 task check;input ok;input[511:0]msg;
 begin if(!ok)begin $display("FAIL: %0s (ticks=%0d)",msg,ticks);$fatal(1);end end endtask
 task screen;input[7:0]v;
 begin @(negedge clk);command=v;valid=1;@(negedge clk);valid=0;repeat(12)@(negedge clk);end endtask
 task press;
 begin @(negedge clk);adc=12800;repeat(20)@(negedge clk);end endtask
 task lift;
 begin @(negedge clk);adc=0;repeat(20)@(negedge clk);end endtask
 task wait_ms;input integer n;integer stop_tick;
 begin stop_tick=ticks+n;while(ticks<stop_tick)@(negedge clk);end endtask

 // Independently specified familiar melodies, not read from the RTL song table.
 function integer expected_note;
 input integer song,index;
 integer k;
 begin
  expected_note=60;
  if(song==0)begin
   if(index>=28)k=index-28;else k=index;
   if(k>=14)begin
    k=(k-14)%7;
    case(k)0,1:expected_note=67;2,3:expected_note=65;4,5:expected_note=64;6:expected_note=62;endcase
   end else case(k)
    0,1,13:expected_note=60;2,3,6:expected_note=67;4,5:expected_note=69;
    7,8:expected_note=65;9,10:expected_note=64;11,12:expected_note=62;
   endcase
  end else if(song==1)begin
   if(index<8)case(index%4)0,3:expected_note=60;1:expected_note=62;2:expected_note=64;endcase
   else if(index<14)case((index-8)%3)0:expected_note=64;1:expected_note=65;2:expected_note=67;endcase
   else if(index<26)case((index-14)%6)
    0,2:expected_note=67;1:expected_note=69;3:expected_note=65;4:expected_note=64;5:expected_note=60;
   endcase
   else case((index-26)%3)0,2:expected_note=60;1:expected_note=55;endcase
  end else begin
   if(index>=30 && index<47)begin
    case(index-30)
     0,1,4,9,13,15:expected_note=62;
     2,5,7,10,12:expected_note=64;
     3,8,14:expected_note=60;
     6,11:expected_note=65;
     16:expected_note=67;
    endcase
   end else begin
    k=(index>=47)?index-47:((index>=15)?index-15:index);
    case(k)
     0,1,6,11:expected_note=64;2,5:expected_note=65;3,4:expected_note=67;
     7,10:expected_note=62;8,9:expected_note=60;
     12:expected_note=(index<15)?64:62;
     13,14:expected_note=(index<15)?62:60;
    endcase
   end
  end
 end endfunction
 function integer expected_units;
 input integer song,index;
 integer k;
 begin
  expected_units=2;
  if(song==0)begin if(index%7==6)expected_units=4;end
  else if(song==1)begin
   if(index==10||index==13||index==28||index==31)expected_units=4;
   else if(index>=14 && index<26 && (index-14)%6<4)expected_units=1;
  end else if(index>=30 && index<47)begin
   k=index-30;
   if(k==5||k==6||k==10||k==11)expected_units=1;
   else if(k==16)expected_units=4;
  end else begin
   k=(index>=47)?index-47:((index>=15)?index-15:index);
   if(k==12)expected_units=3;else if(k==13)expected_units=1;else if(k==14)expected_units=4;
  end
 end endfunction
 function [31:0] increment;
 input integer midi;
 begin case(midi)
  55:increment=17965637;60:increment=23977432;62:increment=26909955;
  64:increment=30205976;65:increment=32001891;67:increment=35931274;
  69:increment=40354080;default:increment=0;
 endcase end endfunction

 reg monitor=0;integer song=0,count=0,total_notes=0,last_tick=0,previous_units=0;
 reg[31:0] expected_inc;
 integer note_events=0;
 reg restart_seen=0;
 always @(negedge clk)begin
  if(restart_seen)check(!dut.demo_voice.active,"restart clears old demo voice before next note");
  restart_seen=dut.demo_restart;
 end
 always @(negedge clk)if(monitor && (|dut.demo_trigger))begin
  check(dut.demo_index==count%total_notes,"all song indices play in order and loop");
  expected_inc=increment(expected_note(song,count%total_notes));
  check(dut.demo_pitch==expected_inc,"demo MIDI pitch and low octave match melody");
  check(dut.demo_duration==expected_units(song,count%total_notes)*175,"note duration matches score");
  check(dut.voice_trigger==0,"demo never triggers physical/game voices");
  if(count>0)check(ticks-last_tick==previous_units*175+1,"note onset spacing, including loop");
  previous_units=expected_units(song,count%total_notes);last_tick=ticks;
  note_events=note_events+1;count=count+1;
 end
 task run_song;input integer selected,n;
 begin
  song=selected;total_notes=n;count=0;monitor=1;screen(8'hb1+selected);
  $display("Start song %0d, demo_mode=%b index=%0d duration=%0d ticks=%0d",selected,dut.demo_mode,dut.demo_index,dut.demo_duration,ticks);
  wait(count==n+1);monitor=0;
  repeat(3)@(negedge clk);
  check(dut.demo_voice.active && dut.demo_voice.active_inc==increment(expected_note(selected,0)),"independent demo voice actually starts notes");
  screen(8'hb0);
  check(!dut.demo_mode && !dut.demo_voice.active && dut.audio_demo==0,"B0 silences demo without waiting for decay");
 end endtask
 initial begin
  repeat(20)@(negedge clk);
  screen(8'ha0);press();
  check(dut.voice_do.active && dut.voice_do.env_peak>0,"pressure sounds on home page after A0");lift();
  screen(8'ha2);press();
  check(dut.physical_play_enable && dut.voice_do.env_state==dut.voice_do.ENV_DECAY,"pressure sounds on demo selection page");lift();
  screen(8'ha1);screen(8'he0);
  check(dut.touch_key_down[0] && dut.voice_do.active,"screen virtual key still works in play page");screen(8'he8);
  run_song(0,42);run_song(1,32);run_song(2,62);
  // A song switch must restart at index zero and discard the previous voice.
  screen(8'hb1);wait_ms(50);check(dut.demo_voice.active,"demo playing before switch");
  screen(8'hb2);check(dut.demo_index==0 && dut.demo_song==1,"song change restarts selected song at index zero");
  wait_ms(1);repeat(4)@(negedge clk);
  check(dut.demo_voice.active_inc==23977432,"new song starts at C4");
  press();check(!dut.voice_do.active,"pressure cannot contaminate demo");lift();
  screen(8'ha0);check(!dut.demo_voice.active,"home exits and silences demo");
  screen(8'hc1);screen(8'hd0);wait_ms(100);press();
  check(dut.game_mode && dut.game_judge.score==100 && dut.demo_voice.active && dut.demo_voice.active_inc==23977432,"game still judges a fresh correct pressure hit");lift();
  screen(8'hf0);press();check(dut.physical_play_enable && dut.voice_do.active,"physical playing resumes after game finish");
  $display("PASS: pressure home/selection/play, TJC virtual key, 42/32/62-note melodies+loops, 175ms units/half/dotted notes, low G3, independent demo, B0/switch/A0, game judgement; checked note events=%0d",note_events);
  $finish;
 end
 initial begin #20000000;$display("DEBUG mode=%b song=%0d index=%0d duration=%0d elapsed=%0d count=%0d ms=%b ticks=%0d",dut.demo_mode,dut.demo_song,dut.demo_index,dut.demo_duration,dut.demo_elapsed,count,ms,ticks);$fatal(1,"test timeout");end
endmodule
