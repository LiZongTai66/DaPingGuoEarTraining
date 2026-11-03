`timescale 1ns/1ps
// Open-drain byte writer. Four phases/bit; 27 MHz / (4*18) = 375 kHz.
// Calls between bytes retain SCL low. A NACK automatically terminates the bus.
module oled_i2c_byte #(
 parameter integer QUARTER_CLKS=18,
 parameter integer TIMEOUT_CLKS=54000
)(input wire clk,input wire send,input wire [7:0] data,
 input wire first,input wire last,
 output reg busy=0,output reg done=0,output reg error=0,
 inout wire scl,inout wire sda);
 localparam IDLE=0,START_WAIT=1,START_LOW=2,START_CLK=3,
 SETUP=4,RISE=5,HIGH=6,FALL=7,STOP_LOW=8,STOP_RISE=9,
 STOP_HIGH=10,STOP_RELEASE=11,FINISH=12;
 reg [3:0] state=IDLE;
 reg scl_low=0,sda_low=0;
 assign scl=scl_low?1'b0:1'bz;
 assign sda=sda_low?1'b0:1'bz;
 reg [1:0] scl_sync=2'b11,sda_sync=2'b11;
 always @(posedge clk)begin scl_sync<={scl_sync[0],scl};sda_sync<={sda_sync[0],sda};end
 reg [15:0] quarter=0;
 reg [31:0] age=0;
 reg [7:0] payload=0;
 reg [3:0] bitpos=0;
 reg stop_after=0;
 always @(posedge clk)begin
  done<=0;
  if(!busy)begin
   quarter<=0;age<=0;
   if(send)begin
    payload<=data;bitpos<=0;stop_after<=last;error<=0;busy<=1;
    if(first)begin scl_low<=0;sda_low<=0;state<=START_WAIT;end
    else state<=SETUP;
   end
  end else if(age==TIMEOUT_CLKS-1)begin
   // Release the bus even if an unplugged/faulty device holds it low.
   busy<=0;done<=1;error<=1;scl_low<=0;sda_low<=0;state<=IDLE;
  end else begin
   age<=age+1'b1;
   if(quarter==QUARTER_CLKS-1)begin
    quarter<=0;
    case(state)
     START_WAIT:if(scl_sync[1]&&sda_sync[1])state<=START_LOW;
     START_LOW:begin sda_low<=1;state<=START_CLK;end
     START_CLK:begin scl_low<=1;state<=SETUP;end
     SETUP:begin
      sda_low<=(bitpos==8)?1'b0:!payload[7];state<=RISE;
     end
     RISE:begin scl_low<=0;state<=HIGH;end
     HIGH:if(scl_sync[1])begin
      if(bitpos==8 && sda_sync[1])error<=1;
      state<=FALL;
     end
     FALL:begin
      scl_low<=1;
      if(bitpos==8)begin
       sda_low<=0;state<=(stop_after||error)?STOP_LOW:FINISH;
      end else begin bitpos<=bitpos+1'b1;payload<={payload[6:0],1'b0};state<=SETUP;end
     end
     STOP_LOW:begin sda_low<=1;state<=STOP_RISE;end
     STOP_RISE:begin scl_low<=0;state<=STOP_HIGH;end
     STOP_HIGH:if(scl_sync[1])state<=STOP_RELEASE;
     STOP_RELEASE:begin sda_low<=0;state<=FINISH;end
     FINISH:begin busy<=0;done<=1;state<=IDLE;end
     default:state<=FINISH;
    endcase
   end else quarter<=quarter+1'b1;
  end
 end
endmodule
