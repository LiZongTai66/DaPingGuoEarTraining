`timescale 1ns/1ps
module dpg_uart_rx #(parameter CLKS=234)(input clk,input rx,output reg [7:0] data=0,output reg valid=0);
 reg meta=1,sync=1;reg [2:0] state=0;reg [15:0] count=0;reg[2:0] bitno=0;reg[7:0] word=0;
 always @(posedge clk) begin
  meta<=rx;sync<=meta;valid<=0;
  case(state)
   0:if(!sync)begin count<=CLKS/2-1;state<=1;end
   1:if(count!=0)count<=count-1'b1;else if(!sync)begin count<=CLKS-1;bitno<=0;state<=2;end else state<=0;
   2:if(count!=0)count<=count-1'b1;else begin word[bitno]<=sync;count<=CLKS-1;if(bitno==7)state<=3;else bitno<=bitno+1'b1;end
   3:if(count!=0)count<=count-1'b1;else begin if(sync)begin data<=word;valid<=1;end state<=0;end
   default:state<=0;
  endcase
 end
endmodule

module dpg_frame_rx(input clk,input[7:0] data,input valid,output reg[31:0] payload=0,output reg frame_valid=0);
 reg[47:0] window=0;reg[2:0] fill=0;reg[15:0] idle=0;
 wire[47:0] candidate={window[39:0],data};
 wire[7:0] checksum=~(candidate[39:32]+candidate[31:24]+candidate[23:16]+candidate[15:8]);
 always @(posedge clk) begin
  frame_valid<=0;
  if(valid)begin
   idle<=0;window<=candidate;
   if(fill==5)begin
    if(candidate[47:40]==8'hAA&&candidate[7:0]==checksum)begin payload<=candidate[39:8];frame_valid<=1;fill<=0;end
   end else fill<=fill+1'b1;
  end else if(idle==16'd53999)begin fill<=0;window<=0;end else idle<=idle+1'b1;
 end
endmodule

// 64 whole-frame entries. Never interleave bytes from ACKs and telemetry.
module dpg_frame_tx #(parameter CLKS=234)(input clk,input[47:0] in_frame,input in_valid,output in_ready,output tx);
 reg[47:0] fifo[0:63];reg[5:0] wp=0,rp=0;reg[6:0] used=0;
 reg active=0;reg[47:0] frame=0;reg[2:0] byteidx=0;reg[3:0] bitidx=0;
 reg[15:0] ticks=0;reg[9:0] shift=10'h3ff;
 wire pop=!active&&used!=0;
 wire push=in_valid&&in_ready;
 assign in_ready=used<64;
 assign tx=active?shift[0]:1'b1;
 always @(posedge clk)begin
  if(push)begin fifo[wp]<=in_frame;wp<=wp+1'b1;end
  case({push,pop})2'b10:used<=used+1'b1;2'b01:used<=used-1'b1;default:;endcase
  if(pop)begin
   frame<=fifo[rp];shift<={1'b1,fifo[rp][47:40],1'b0};rp<=rp+1'b1;
   active<=1;byteidx<=0;bitidx<=0;ticks<=CLKS-1;
  end else if(active)begin
   if(ticks!=0)ticks<=ticks-1'b1;
   else begin
    ticks<=CLKS-1;
    if(bitidx==9)begin
     if(byteidx==5)begin active<=0;shift<=10'h3ff;end
     else begin byteidx<=byteidx+1'b1;bitidx<=0;shift<={1'b1,frame[39-byteidx*8 -:8],1'b0};end
    end else begin bitidx<=bitidx+1'b1;shift<={1'b1,shift[9:1]};end
   end
  end
 end
endmodule
