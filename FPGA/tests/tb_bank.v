`timescale 1ns/1ps
module tb_bank;
reg clk=0;always #5 clk=~clk;
reg tick=0;reg [1709:0] inputs=0;
wire [359:0] audio;wire busy,overrun,done;
additive32_bank dut(.clk(clk),.sample_tick(tick),.phase_bus(inputs[479:0]),
 .phase2_bus(inputs[959:480]),.inc_bus(inputs[1439:960]),.env_bus(inputs[1679:1440]),.guitar_bus(inputs[1694:1680]),
 .active_bus(inputs[1709:1695]),.audio_bus(audio),.busy(busy),.overrun(overrun),.frame_done(done));
reg [1709:0] vectors[0:63];reg [359:0] expected[0:63];
reg [359:0] previous=0;integer f,cycles,max_cycles=0;
initial begin
 $readmemh("tests/input.hex",vectors);$readmemh("tests/expected.hex",expected);
 repeat(3)@(negedge clk);
 for(f=0;f<64;f=f+1)begin
  inputs=vectors[f];tick=1;@(negedge clk);tick=0;inputs=0;cycles=0;
  while(!done && cycles<575)begin
   if(audio!==previous)$fatal(1,"non-atomic output frame");
   @(negedge clk);cycles=cycles+1;
  end
  if(!done || cycles>406 || overrun)$fatal(1,"missed sample deadline %0d",cycles);
  if(audio!==expected[f])begin $display("frame=%0d got=%h expected=%h",f,audio,expected[f]);$fatal(1,"reference mismatch");end
  if(cycles>max_cycles)max_cycles=cycles;
  previous=audio;repeat(576-cycles-1)@(negedge clk);
 end
 $display("PASS 960 bit-exact voice results, 32-partial piano and exact donor guitar integer waveform, Nyquist/wide increments, zero/maximum envelope, snapshot isolation, atomic frame, worst=%0d clocks <576, no overrun",max_cycles);$finish;
end
initial begin #10000000;$fatal(1,"timeout");end
endmodule
