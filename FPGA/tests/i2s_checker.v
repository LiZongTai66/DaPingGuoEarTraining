`timescale 1ns/1ps
// Receiver-side checker: observe only pins, reconstruct standard I2S 32-bit words.
module i2s_checker(input clk,input bck,input lrck,input din,
 input signed [15:0] source_left,source_right,
 output reg [31:0] frames=0,output reg [31:0] nonzero_words=0);
reg [15:0] before_left=0,before_right=0,pair_left=0,pair_right=0;
reg previous_ws=1,synced=0,channel=0;
reg [31:0] word=0,expected_word=0;
integer bits=0,clocks=0,last_rise=-1,last_edge=-1;
always @(posedge clk)begin
 clocks=clocks+1;
 before_left<=source_left;before_right<=source_right;
end
always @(negedge lrck)begin pair_left=before_left;pair_right=before_right;end
always @(bck)begin
 if(last_edge>=0)begin
  if(bck===1'b1 && clocks-last_edge!=5)$fatal(1,"BCK low time must be five master clocks");
  if(bck===1'b0 && clocks-last_edge!=4)$fatal(1,"BCK high time must be four master clocks");
 end
 last_edge=clocks;
end
always @(din or lrck)if($time>0 && bck===1'b1)$fatal(1,"DIN/WS changed while BCK high");
always @(posedge bck)begin
 if(last_rise>=0 && clocks-last_rise!=9)$fatal(1,"BCK period not nine master clocks");
 last_rise=clocks;
 if(synced)begin
  word={word[30:0],din};bits=bits+1;
  if(bits==32)begin
   if(word!==expected_word)begin
    $display("I2S channel=%d got=%h expected=%h",channel,word,expected_word);
    $fatal(1,"I2S MSB delay/padding/sign/stereo snapshot mismatch");
   end
   if(word!=0)nonzero_words=nonzero_words+1;
   if(channel)frames=frames+1;
  end
 end
 if(lrck!=previous_ws)begin
  if(synced&&bits!=32)$fatal(1,"I2S slot length not 32 BCK");
  synced=1;channel=lrck;bits=0;word=0;
  expected_word=lrck?{pair_right,16'd0}:{pair_left,16'd0};
 end else if(bits>=32)$fatal(1,"LRCK failed to alternate channels");
 previous_ws=lrck;
end
endmodule
