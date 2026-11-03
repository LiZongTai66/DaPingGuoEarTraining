`timescale 1ns/1ps
// PCM5102 hardware mode: FMT=0 (I2S), SCK=GND (BCK PLL), XSMT=1.
// No derived FPGA clock is used internally: every register uses the 27MHz clock.
// Each 32-bit channel word is signed PCM16 in bits31:16, followed by 16 zero bits.
module pcm5102_i2s_tx(
 input wire clk,
 input wire signed [15:0] pcm_left,pcm_right,
 output reg bck=1'b0,
 output reg din=1'b0,
 output reg lrck=1'b1
);
reg [3:0] divider=0;
reg [5:0] bit_index=0;
reg [15:0] frame_left=0,frame_right=0;
always @(posedge clk)begin
 if(divider==4'd8)begin
  divider<=0;bck<=0;
  // Data/WS change only on falling BCK; DAC samples rising BCK 5 clocks later.
  if(bit_index==0)begin
   frame_left<=pcm_left;frame_right<=pcm_right;
   lrck<=0;din<=0; // One-bit I2S delay; previous channel's last padding bit.
  end else if(bit_index<=16)begin
   din<=frame_left[16-bit_index];
  end else if(bit_index==32)begin
   lrck<=1;din<=0;
  end else if(bit_index>=33 && bit_index<=48)begin
   din<=frame_right[48-bit_index];
  end else din<=0;
  bit_index<=bit_index+1'b1;
 end else begin
  divider<=divider+1'b1;
  if(divider==4'd4)bck<=1;
 end
end
endmodule
