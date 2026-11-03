`timescale 1ns/1ps
module tb_note_out;
reg clk=0;always #18.5185 clk=~clk;
tri1 a,b,c,d,e,f;wire [6:0] pins;
ads1115_pressure_test dut(.clk27m(clk),.key_s0(1'b1),.key_bend(1'b1),.esp_rx(1'b1),.uart_rx(1'b1),
 .adc1_sda(a),.adc1_scl(b),.adc2_sda(c),.adc2_scl(d),.oled_scl(e),.oled_sda(f),
 .note_do_out(pins[0]),.note_re_out(pins[1]),.note_mi_out(pins[2]),.note_fa_out(pins[3]),
 .note_sol_out(pins[4]),.note_la_out(pins[5]),.note_si_out(pins[6]));
reg [479:0] incs=0;reg [239:0] envs=0;reg [14:0] act=0;
reg mute_all=0,mute_remote=0,shared_mute=0,demo=0,game=0;reg [15:0] gain=32768;
integer i,k,checks=0;reg [31:0] pitch[0:6];
task check;input[6:0] expected;begin
 #2000;if(pins!==expected)$fatal(1,"pins=%b expected=%b",pins,expected);checks=checks+1;
end endtask
initial begin
 force dut.synth_base_inc=incs;force dut.synth_env=envs;force dut.synth_active=act;
 force dut.app_mute_all=mute_all;force dut.app_mute_remote=mute_remote;
 force dut.shared_voice_mute=shared_mute;force dut.demo_mode=demo;force dut.game_mode=game;
 force dut.effective_gain=gain;
 pitch[0]=23977432;pitch[1]=26909955;pitch[2]=30205976;pitch[3]=32001891;
 pitch[4]=35931274;pitch[5]=40354080;pitch[6]=45294589;
 check(0);
 if(dut.note_out_decode(32'd2519714)!==7'd32)$fatal(1,"MIDI 21 decode");checks=checks+1;
 if(dut.note_out_decode(32'd2669544)!==7'd0)$fatal(1,"MIDI 22 decode");checks=checks+1;
 if(dut.note_out_decode(32'd2828284)!==7'd64)$fatal(1,"MIDI 23 decode");checks=checks+1;
 if(dut.note_out_decode(32'd2996462)!==7'd1)$fatal(1,"MIDI 24 decode");checks=checks+1;
 if(dut.note_out_decode(32'd3174641)!==7'd0)$fatal(1,"MIDI 25 decode");checks=checks+1;
 if(dut.note_out_decode(32'd3363415)!==7'd2)$fatal(1,"MIDI 26 decode");checks=checks+1;
 if(dut.note_out_decode(32'd3563414)!==7'd0)$fatal(1,"MIDI 27 decode");checks=checks+1;
 if(dut.note_out_decode(32'd3775306)!==7'd4)$fatal(1,"MIDI 28 decode");checks=checks+1;
 if(dut.note_out_decode(32'd3999797)!==7'd8)$fatal(1,"MIDI 29 decode");checks=checks+1;
 if(dut.note_out_decode(32'd4237637)!==7'd0)$fatal(1,"MIDI 30 decode");checks=checks+1;
 if(dut.note_out_decode(32'd4489620)!==7'd16)$fatal(1,"MIDI 31 decode");checks=checks+1;
 if(dut.note_out_decode(32'd4756587)!==7'd0)$fatal(1,"MIDI 32 decode");checks=checks+1;
 if(dut.note_out_decode(32'd5039428)!==7'd32)$fatal(1,"MIDI 33 decode");checks=checks+1;
 if(dut.note_out_decode(32'd5339088)!==7'd0)$fatal(1,"MIDI 34 decode");checks=checks+1;
 if(dut.note_out_decode(32'd5656567)!==7'd64)$fatal(1,"MIDI 35 decode");checks=checks+1;
 if(dut.note_out_decode(32'd5992924)!==7'd1)$fatal(1,"MIDI 36 decode");checks=checks+1;
 if(dut.note_out_decode(32'd6349282)!==7'd0)$fatal(1,"MIDI 37 decode");checks=checks+1;
 if(dut.note_out_decode(32'd6726830)!==7'd2)$fatal(1,"MIDI 38 decode");checks=checks+1;
 if(dut.note_out_decode(32'd7126828)!==7'd0)$fatal(1,"MIDI 39 decode");checks=checks+1;
 if(dut.note_out_decode(32'd7550611)!==7'd4)$fatal(1,"MIDI 40 decode");checks=checks+1;
 if(dut.note_out_decode(32'd7999594)!==7'd8)$fatal(1,"MIDI 41 decode");checks=checks+1;
 if(dut.note_out_decode(32'd8475274)!==7'd0)$fatal(1,"MIDI 42 decode");checks=checks+1;
 if(dut.note_out_decode(32'd8979240)!==7'd16)$fatal(1,"MIDI 43 decode");checks=checks+1;
 if(dut.note_out_decode(32'd9513174)!==7'd0)$fatal(1,"MIDI 44 decode");checks=checks+1;
 if(dut.note_out_decode(32'd10078857)!==7'd32)$fatal(1,"MIDI 45 decode");checks=checks+1;
 if(dut.note_out_decode(32'd10678177)!==7'd0)$fatal(1,"MIDI 46 decode");checks=checks+1;
 if(dut.note_out_decode(32'd11313134)!==7'd64)$fatal(1,"MIDI 47 decode");checks=checks+1;
 if(dut.note_out_decode(32'd11985848)!==7'd1)$fatal(1,"MIDI 48 decode");checks=checks+1;
 if(dut.note_out_decode(32'd12698564)!==7'd0)$fatal(1,"MIDI 49 decode");checks=checks+1;
 if(dut.note_out_decode(32'd13453659)!==7'd2)$fatal(1,"MIDI 50 decode");checks=checks+1;
 if(dut.note_out_decode(32'd14253656)!==7'd0)$fatal(1,"MIDI 51 decode");checks=checks+1;
 if(dut.note_out_decode(32'd15101222)!==7'd4)$fatal(1,"MIDI 52 decode");checks=checks+1;
 if(dut.note_out_decode(32'd15999188)!==7'd8)$fatal(1,"MIDI 53 decode");checks=checks+1;
 if(dut.note_out_decode(32'd16950549)!==7'd0)$fatal(1,"MIDI 54 decode");checks=checks+1;
 if(dut.note_out_decode(32'd17958481)!==7'd16)$fatal(1,"MIDI 55 decode");checks=checks+1;
 if(dut.note_out_decode(32'd19026348)!==7'd0)$fatal(1,"MIDI 56 decode");checks=checks+1;
 if(dut.note_out_decode(32'd20157713)!==7'd32)$fatal(1,"MIDI 57 decode");checks=checks+1;
 if(dut.note_out_decode(32'd21356353)!==7'd0)$fatal(1,"MIDI 58 decode");checks=checks+1;
 if(dut.note_out_decode(32'd22626268)!==7'd64)$fatal(1,"MIDI 59 decode");checks=checks+1;
 if(dut.note_out_decode(32'd23977432)!==7'd1)$fatal(1,"MIDI 60 decode");checks=checks+1;
 if(dut.note_out_decode(32'd25397127)!==7'd0)$fatal(1,"MIDI 61 decode");checks=checks+1;
 if(dut.note_out_decode(32'd26909955)!==7'd2)$fatal(1,"MIDI 62 decode");checks=checks+1;
 if(dut.note_out_decode(32'd28507311)!==7'd0)$fatal(1,"MIDI 63 decode");checks=checks+1;
 if(dut.note_out_decode(32'd30205976)!==7'd4)$fatal(1,"MIDI 64 decode");checks=checks+1;
 if(dut.note_out_decode(32'd32001891)!==7'd8)$fatal(1,"MIDI 65 decode");checks=checks+1;
 if(dut.note_out_decode(32'd33901097)!==7'd0)$fatal(1,"MIDI 66 decode");checks=checks+1;
 if(dut.note_out_decode(32'd35931274)!==7'd16)$fatal(1,"MIDI 67 decode");checks=checks+1;
 if(dut.note_out_decode(32'd38052695)!==7'd0)$fatal(1,"MIDI 68 decode");checks=checks+1;
 if(dut.note_out_decode(32'd40354080)!==7'd32)$fatal(1,"MIDI 69 decode");checks=checks+1;
 if(dut.note_out_decode(32'd42712706)!==7'd0)$fatal(1,"MIDI 70 decode");checks=checks+1;
 if(dut.note_out_decode(32'd45294589)!==7'd64)$fatal(1,"MIDI 71 decode");checks=checks+1;
 if(dut.note_out_decode(32'd47943392)!==7'd1)$fatal(1,"MIDI 72 decode");checks=checks+1;
 if(dut.note_out_decode(32'd50794254)!==7'd0)$fatal(1,"MIDI 73 decode");checks=checks+1;
 if(dut.note_out_decode(32'd53814638)!==7'd2)$fatal(1,"MIDI 74 decode");checks=checks+1;
 if(dut.note_out_decode(32'd57014623)!==7'd0)$fatal(1,"MIDI 75 decode");checks=checks+1;
 if(dut.note_out_decode(32'd60404889)!==7'd4)$fatal(1,"MIDI 76 decode");checks=checks+1;
 if(dut.note_out_decode(32'd63996750)!==7'd8)$fatal(1,"MIDI 77 decode");checks=checks+1;
 if(dut.note_out_decode(32'd67802195)!==7'd0)$fatal(1,"MIDI 78 decode");checks=checks+1;
 if(dut.note_out_decode(32'd71833923)!==7'd16)$fatal(1,"MIDI 79 decode");checks=checks+1;
 if(dut.note_out_decode(32'd76105391)!==7'd0)$fatal(1,"MIDI 80 decode");checks=checks+1;
 if(dut.note_out_decode(32'd80630853)!==7'd32)$fatal(1,"MIDI 81 decode");checks=checks+1;
 if(dut.note_out_decode(32'd85425413)!==7'd0)$fatal(1,"MIDI 82 decode");checks=checks+1;
 if(dut.note_out_decode(32'd90505072)!==7'd64)$fatal(1,"MIDI 83 decode");checks=checks+1;
 if(dut.note_out_decode(32'd95886784)!==7'd1)$fatal(1,"MIDI 84 decode");checks=checks+1;
 if(dut.note_out_decode(32'd101588509)!==7'd0)$fatal(1,"MIDI 85 decode");checks=checks+1;
 if(dut.note_out_decode(32'd107629276)!==7'd2)$fatal(1,"MIDI 86 decode");checks=checks+1;
 if(dut.note_out_decode(32'd114029245)!==7'd0)$fatal(1,"MIDI 87 decode");checks=checks+1;
 if(dut.note_out_decode(32'd120809777)!==7'd4)$fatal(1,"MIDI 88 decode");checks=checks+1;
 if(dut.note_out_decode(32'd127993500)!==7'd8)$fatal(1,"MIDI 89 decode");checks=checks+1;
 if(dut.note_out_decode(32'd135604390)!==7'd0)$fatal(1,"MIDI 90 decode");checks=checks+1;
 if(dut.note_out_decode(32'd143667847)!==7'd16)$fatal(1,"MIDI 91 decode");checks=checks+1;
 if(dut.note_out_decode(32'd152210781)!==7'd0)$fatal(1,"MIDI 92 decode");checks=checks+1;
 if(dut.note_out_decode(32'd161261705)!==7'd32)$fatal(1,"MIDI 93 decode");checks=checks+1;
 if(dut.note_out_decode(32'd170850825)!==7'd0)$fatal(1,"MIDI 94 decode");checks=checks+1;
 if(dut.note_out_decode(32'd181010144)!==7'd64)$fatal(1,"MIDI 95 decode");checks=checks+1;
 if(dut.note_out_decode(32'd191773567)!==7'd1)$fatal(1,"MIDI 96 decode");checks=checks+1;
 if(dut.note_out_decode(32'd203177017)!==7'd0)$fatal(1,"MIDI 97 decode");checks=checks+1;
 if(dut.note_out_decode(32'd215258551)!==7'd2)$fatal(1,"MIDI 98 decode");checks=checks+1;
 if(dut.note_out_decode(32'd228058491)!==7'd0)$fatal(1,"MIDI 99 decode");checks=checks+1;
 if(dut.note_out_decode(32'd241619554)!==7'd4)$fatal(1,"MIDI 100 decode");checks=checks+1;
 if(dut.note_out_decode(32'd255987001)!==7'd8)$fatal(1,"MIDI 101 decode");checks=checks+1;
 if(dut.note_out_decode(32'd271208780)!==7'd0)$fatal(1,"MIDI 102 decode");checks=checks+1;
 if(dut.note_out_decode(32'd287335693)!==7'd16)$fatal(1,"MIDI 103 decode");checks=checks+1;
 if(dut.note_out_decode(32'd304421563)!==7'd0)$fatal(1,"MIDI 104 decode");checks=checks+1;
 if(dut.note_out_decode(32'd322523411)!==7'd32)$fatal(1,"MIDI 105 decode");checks=checks+1;
 if(dut.note_out_decode(32'd341701651)!==7'd0)$fatal(1,"MIDI 106 decode");checks=checks+1;
 if(dut.note_out_decode(32'd362020288)!==7'd64)$fatal(1,"MIDI 107 decode");checks=checks+1;
 if(dut.note_out_decode(32'd383547135)!==7'd1)$fatal(1,"MIDI 108 decode");checks=checks+1;
 // Each of 15 slots, each natural C4..B4. Covers remote/shared/physical paths.
 for(i=0;i<15;i=i+1)for(k=0;k<7;k=k+1)begin
  act=15'd1<<i;envs=0;envs[i*16+:16]=1000;incs=0;incs[i*32+:32]=pitch[k];check(7'd1<<k);
 end
 // Two voices of different octaves. C4 plus E5 from actual bridge ROM.
 act=(15'd1<<0)|(15'd1<<8);envs=0;envs[15:0]=1000;envs[8*16+:16]=1000;
 incs=0;incs[31:0]=23977432;incs[8*32+:32]=60404889;check(7'b0000101);
 mute_remote=1;check(7'b0000100);mute_remote=0;
 demo=1;check(7'b0000001);demo=0;game=1;check(7'b0000001);game=0;
 mute_all=1;check(0);mute_all=0;
 gain=0;check(0);gain=32768;check(7'b0000101);
 // Active voice with zero envelope is not an audible voice.
 envs=0;check(0);
 act=15'd1<<7;envs[7*16+:16]=500;incs=0;
 incs[7*32+:32]=pitch[6]>>1;check(7'b1000000);
 shared_mute=1;check(0);shared_mute=0;
 // Unsupported sharp is not silently mislabeled as a natural note.
 incs[7*32+:32]=25397127;check(0);
 // A held tail remains on after release until voice/envelope ends.
 incs[7*32+:32]=pitch[1];envs[7*16+:16]=1;check(7'b0000010);
 act=0;check(0);
 $display("PASS note outputs: %0d checks, all 15 slots, seven pitches, octave aliases, polyphony, mute, zero gain/envelope, tail, sharp",checks);
 $finish;
end
endmodule
