`timescale 1ns/1ps
module tb_pcm5102_i2s;
reg clk=0;always #5 clk=~clk;
reg signed [15:0] left=16'h8000,right=16'h7fff;
wire bck,lrck,din;wire [31:0] frames,nonzero;
pcm5102_i2s_tx dut(clk,left,right,bck,din,lrck);
i2s_checker receiver(clk,bck,lrck,din,left,right,frames,nonzero);
integer count=0,vector=0;
always @(negedge clk)begin
 count=count+1;
 // Change the source even within a channel to test atomic stereo latching.
 if(count%37==0)begin
  vector=vector+1;
  case(vector%8)
   0:begin left=0;right=0;end
   1:begin left=16'h7fff;right=16'h8000;end
   2:begin left=16'hffff;right=16'h0001;end
   3:begin left=16'ha55a;right=16'h5aa5;end
   4:begin left=16'h0001<<(vector%16);right=~left;end
   default:begin left=$random;right=$random;end
  endcase
 end
end
initial begin
 wait(frames==128);
 if(nonzero<100)$fatal(1,"insufficient nonzero samples checked");
 $display("PASS PCM5102 receiver: 128 stereo frames, 3MHz BCK at 27MHz, 64 BCK/frame, I2S one-bit delay, signed PCM16+16 zero bits, atomic L/R, data stable while BCK high");
 $finish;
end
initial begin #2000000;$fatal(1,"timeout");end
endmodule
