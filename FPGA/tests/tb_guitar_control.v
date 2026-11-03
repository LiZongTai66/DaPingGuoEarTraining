`timescale 1ns/1ps
module tb_guitar_control;
reg clk=0;always #5 clk=~clk;
reg ms=0,sample=0,trig=0,rel=0,mute=0,guitar=1,hold=0;
reg [8:0] bend=0;reg [31:0] inc=23977432;
wire [40:0] bm={9'd0,inc}*bend;
wire signed [23:0] old_audio;
wire [31:0] p1,p2,eff,base;wire [15:0] env;wire g,a;
additive32_voice u(.clk27m(clk),.ms_tick(ms),.sample_tick(sample),.trigger(trig),
 .velocity(8'd110),.guitar_mode(guitar),.note_inc(inc),.note_release(rel),.mute(mute),
 .bend_offset({3'd0,bm[40:12]}),.key_hold(hold),.phase_out(p1),.phase2_out(p2),
 .inc_out(eff),.base_inc_out(base),.env_out(env),.guitar_out(g),.active_out(a));
donor_voice gold(.clk27m(clk),.ms_tick(ms),.sample_tick(sample),.trigger(trig),
 .velocity(8'd110),.guitar_mode(guitar),.note_inc(inc),.note_release(rel),.mute(mute),
 .bend_level(bend),.key_hold(hold),.audio_out(old_audio));
integer n;
always @(negedge clk)begin
 if(u.env_state!==gold.env_state || env!==gold.env_level || a!==gold.active ||
    p1!==gold.phase1 || p2!==gold.phase2)$fatal(1,"donor control mismatch");
end
task tick;begin @(negedge clk);ms=1;sample=1;@(negedge clk);ms=0;sample=0;end endtask
task start;begin @(negedge clk);trig=1;@(negedge clk);trig=0;end endtask
initial begin
 repeat(5)@(negedge clk);hold=1;start();repeat(30)tick();
 if(u.env_state!=u.ENV_SUSTAIN || env!=7056)$fatal(1,"held guitar sustain level");
 bend=511;repeat(10)tick();if(eff!=inc+((inc*64'd511)>>12))$fatal(1,"bend effective pitch");
 hold=0;repeat(1000)tick();if(a)$fatal(1,"guitar release never ends");
 hold=0;bend=0;start();repeat(800)tick();if(a)$fatal(1,"unheld guitar tail never ends");
 guitar=0;start();bend=511;repeat(10)tick();if(eff!=inc)$fatal(1,"piano bent");
 @(negedge clk);rel=1;@(negedge clk);rel=0;repeat(1000)tick();
 if(a)$fatal(1,"piano release never ends");
 start();@(negedge clk);mute=1;@(negedge clk);mute=0;if(a)$fatal(1,"mute failed");
 $display("PASS donor envelope/phase match: guitar sustain, release, detune, bend; piano release and mute preserved");$finish;
end
endmodule
