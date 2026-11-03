`timescale 1ns/1ps
module tb_octave;
reg clk=0;always #5 clk=~clk;
reg down=1,up=1,tick=0,rx=1;reg[15:0]adc=0;
tri1 a,b,c,d,e,f;wire tx;wire[6:0] pins;
ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),
 .key_oct_down(down),.key_oct_up(up),.esp_rx(rx),.esp_tx(tx),.uart_rx(1'b1),
 .adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),.oled_scl(e),.oled_sda(f),
 .note_do_out(pins[0]),.note_re_out(pins[1]),.note_mi_out(pins[2]),.note_fa_out(pins[3]),
 .note_sol_out(pins[4]),.note_la_out(pins[5]),.note_si_out(pins[6]));
wire[7:0] rb;wire bv;wire[31:0] frame;wire fv;
dpg_uart_rx monitor(clk,tx,rb,bv);dpg_frame_rx decoder(clk,rb,bv,frame,fv);
integer logfd,completed=0,mute_count=0,j;reg[6:0] seen=0;reg[7:0] rev,mode;reg[7:0] received[0:6];
reg[7:0] offsets[0:6];
always @(posedge clk)begin
 if(dut.octave_mute_physical)mute_count=mute_count+1;
 if(bv)$fwrite(logfd,"%02x ",rb);
 if(fv)case(frame[31:24])
  8'h87:begin rev=frame[23:16];mode=frame[15:8];seen=0;if(frame[7:0]!=7)$fatal(1,"begin count");end
  8'h88:begin
   if(frame[23:16]!=rev||frame[15:8]>6)$fatal(1,"snapshot revision/index");
   received[frame[15:8]]=frame[7:0];seen[frame[15:8]]=1;
  end
  8'h89:begin
   if(frame[23:16]!=rev||frame[15:8]!=mode||seen!=127)$fatal(1,"torn snapshot");
   if(mode<3)for(j=0;j<7;j=j+1)if(received[j]!=48+12*mode+offsets[j])$fatal(1,"preset values");
   completed=completed+1;
  end
 endcase
end
task ms;input integer n;integer i;begin
 for(i=0;i<n;i=i+1)begin @(negedge clk);tick=1;@(negedge clk);tick=0;repeat(98)@(negedge clk);end
end endtask
task button;input integer dir;begin
 down=(dir==0)?0:1;up=(dir==1)?0:1;ms(23);
 down=1;up=1;ms(23);wait(dut.app_bridge.outq.used==0 && !dut.app_bridge.outq.active);repeat(50)@(negedge clk);
end endtask
task expect_map;input[7:0] root;input[1:0] m;integer i;begin
 for(i=0;i<7;i=i+1)if(dut.app_bridge.mapping[i]!=root+offsets[i])$fatal(1,"map index%0d actual=%0d expected=%0d mode=%0d expectedmode=%0d time=%0t",i,dut.app_bridge.mapping[i],root+offsets[i],dut.app_bridge.map_mode,m,$time);
 if(dut.app_bridge.map_mode!=m)$fatal(1,"mode");
end endtask
task byte_uart;input[7:0] v;integer i;begin
 @(negedge clk);rx=0;repeat(234)@(negedge clk);
 for(i=0;i<8;i=i+1)begin rx=v[i];repeat(234)@(negedge clk);end
 rx=1;repeat(234)@(negedge clk);
end endtask
task cmd;input[7:0]cc,x,y,z;reg[7:0]s;begin
 s=~(cc+x+y+z);byte_uart(8'hAA);byte_uart(cc);byte_uart(x);byte_uart(y);byte_uart(z);byte_uart(s);
 repeat(20)@(negedge clk);
end endtask
integer saved;
initial begin
 offsets[0]=0;offsets[1]=2;offsets[2]=4;offsets[3]=5;offsets[4]=7;offsets[5]=9;offsets[6]=11;
 logfd=$fopen("validation/octave-uart.hex","w");
 force dut.ms_tick=tick;
 force dut.adc1_ch0=adc;force dut.adc1_ch1=16'd0;force dut.adc1_ch2=16'd0;force dut.adc1_ch3=16'd0;
 force dut.adc2_ch0=16'd0;force dut.adc2_ch1=16'd0;force dut.adc2_ch2=16'd0;
 wait(dut.app_bridge.outq.used==0 && !dut.app_bridge.outq.active);expect_map(60,1);
 // Short bounce is ignored; 20 stable ms creates one request only.
 down=0;ms(7);down=1;ms(23);expect_map(60,1);
 down=0;ms(19);expect_map(60,1);ms(5);expect_map(48,0);
 saved=mute_count;ms(80);if(mute_count!=saved)$fatal(1,"held auto repeat");
 down=1;ms(23);saved=mute_count;button(0);expect_map(48,0);if(mute_count!=saved)$fatal(1,"lower limit must not cut sound");
 button(1);expect_map(60,1);button(1);expect_map(72,2);button(1);expect_map(72,2);
 button(0);expect_map(60,1);
 // App custom mapping is reset to natural notes by either octave button.
 cmd(8'h30,0,80,0);if(dut.app_bridge.map_mode!=3)$fatal(1,"custom mode");
 button(0);expect_map(48,0);
 adc=14080;ms(4);repeat(10000)@(negedge clk);
 if(!dut.synth_active[8]||dut.synth_base_inc[8*32+:32]!=11985848||pins[0]!==1)$fatal(1,"low Do sound/pin");
 button(1);expect_map(60,1);if(dut.synth_active[8])$fatal(1,"old tone survived octave change");
 // Still held: no accidental new note. Release then re-press uses C4.
 ms(5);if(dut.synth_active[8])$fatal(1,"held retrigger");
 adc=0;ms(3);adc=14080;ms(3);repeat(10000)@(negedge clk);
 if(dut.synth_base_inc[8*32+:32]!=23977432||pins[0]!==1)$fatal(1,"normal Do retrigger");
 adc=0;ms(3);
 down=0;up=0;ms(25);down=1;up=1;ms(25);expect_map(60,1);
 button(1);expect_map(72,2);
 cmd(8'h40,0,55,7);wait(dut.app_bridge.outq.used==0 && !dut.app_bridge.outq.active);expect_map(60,1);
 button(0);expect_map(60,1);if(!dut.ear_active)$fatal(1,"button aborted training");
 cmd(8'h43,0,55,0);ms(2);button(0);expect_map(48,0);
 saved=completed;cmd(8'h20,0,0,5);wait(dut.app_bridge.outq.used==0 && !dut.app_bridge.outq.active);repeat(10)@(negedge clk);
 if(completed<=saved)$fatal(1,"PING did not refresh mapping");
 $fclose(logfd);$display("PASS octave: debounce/bounce/hold/limits/down/up/custom reset/old voice mute/LED/ear reset+lock/PING snapshot; %0d complete snapshots",completed);$finish;
end
initial begin #100000000;$fatal(1,"timeout");end
endmodule

