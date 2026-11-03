`timescale 1ns/1ps
// Real PCM scope, independent of the ADC/ESP/touchscreen buses.
// 128 columns * 2 PCM periods = 5.46 ms at 46875 Hz. No FFT or invented waveform.
module oled_audio_scope #(
 parameter [6:0] I2C_ADDR=7'h3c,
 parameter integer SH1106=0,
 parameter integer QUARTER_CLKS=18,
 parameter integer POWERUP_CLKS=5400000,
 parameter integer FRAME_CLKS=1350000,
 parameter integer TRIGGER_SAMPLES=938,
 parameter integer SAMPLE_STRIDE=2
)(input wire clk,input wire sample_tick,input wire signed [15:0] pcm,
 inout wire oled_scl,inout wire oled_sda,
 output reg online=0,output reg [15:0] frames=0);
 localparam POWER=0,INIT_SEND=1,INIT_WAIT=2,FRAME_WAIT=3,
 ARM=4,CAPTURE=5,PAGE_CMD_SEND=6,PAGE_CMD_WAIT=7,
 PAGE_DATA_SEND=8,PAGE_DATA_WAIT=9,RETRY=10;
 reg [3:0] state=POWER;
 reg [31:0] delay_count=0,frame_age=0;
 reg [10:0] trigger_wait=0;
 reg trigger_armed=0;
 reg [6:0] write_col=0;
 reg [7:0] stride=0;
 reg [5:0] trace_y[0:127];
 reg [15:0] peak=0;
 reg [5:0] meter=0;
 reg [5:0] init_index=0;
 reg [2:0] page=0;
 reg [7:0] byte_index=0;
 reg send=0,first=0,last=0;
 reg [7:0] tx_data=0;
 wire busy,done,error;
 oled_i2c_byte #(.QUARTER_CLKS(QUARTER_CLKS)) writer(
 .clk(clk),.send(send),.data(tx_data),.first(first),.last(last),
 .busy(busy),.done(done),.error(error),.scl(oled_scl),.sda(oled_sda));
 // Both controllers use page writes. SH1106 has 132-column RAM, usually +2 offset.
 localparam [3:0] COL_LOW=SH1106?4'd2:4'd0;
 function [7:0] init_byte;
 input [5:0] n;
 begin
  case(n)
   0:init_byte={I2C_ADDR,1'b0}; 1:init_byte=8'h00;
   2:init_byte=8'hae; 3:init_byte=8'hd5; 4:init_byte=8'h80;
   5:init_byte=8'ha8; 6:init_byte=8'h3f;
   7:init_byte=8'hd3; 8:init_byte=8'h00; 9:init_byte=8'h40;
   10:init_byte=SH1106?8'had:8'h8d;
   11:init_byte=SH1106?8'h8b:8'h14;
   12:init_byte=SH1106?8'he3:8'h20;
   13:init_byte=SH1106?8'he3:8'h02;
   14:init_byte=8'ha1; 15:init_byte=8'hc8;
   16:init_byte=8'hda; 17:init_byte=8'h12;
   18:init_byte=8'h81; 19:init_byte=8'h7f;
   20:init_byte=8'hd9; 21:init_byte=SH1106?8'h22:8'hf1;
   22:init_byte=8'hdb; 23:init_byte=8'h40;
   24:init_byte=8'ha4;25:init_byte=8'ha6;
   default:init_byte=8'haf;
  endcase
 end endfunction
 function [5:0] pcm_y;
 input signed [15:0] v;
 reg signed [16:0] y;
 begin
  y=17'sd36-($signed({v[15],v})>>>8);
  if(y<11)pcm_y=11;else if(y>61)pcm_y=61;else pcm_y=y[5:0];
 end endfunction
 wire [15:0] magnitude=pcm[15]?(~pcm+16'd1):pcm;
 // Four 5x7 characters, encoded as vertical columns (bit0 is the top pixel).
 function [7:0] title;
 input [6:0] x;
 begin case(x)
  3:title=8'h3f;4:title=8'h40;5:title=8'h38;6:title=8'h40;7:title=8'h3f;
  9:title=8'h7e;10:title=8'h09;11:title=8'h09;12:title=8'h09;13:title=8'h7e;
  15:title=8'h1f;16:title=8'h20;17:title=8'h40;18:title=8'h20;19:title=8'h1f;
  21:title=8'h7f;22:title=8'h49;23:title=8'h49;24:title=8'h49;25:title=8'h41;
  default:title=0;
 endcase end endfunction
 // Draw a vertical segment between adjacent captured points: no holes on steep edges.
 reg [7:0] pixels;
 reg [6:0] col;
 reg [5:0] y_here,y_prev,y_min,y_max;
 reg [6:0] row;
 reg [7:0] title_bits;
 integer bitnum;
 always @* begin
  col=byte_index[6:0]-7'd2;
  y_here=trace_y[col];y_prev=trace_y[(col==0)?7'd0:col-7'd1];
  y_min=(y_here<y_prev)?y_here:y_prev;y_max=(y_here>y_prev)?y_here:y_prev;
  pixels=0;row=0;title_bits=title(col);
  for(bitnum=0;bitnum<8;bitnum=bitnum+1)begin
   row={1'b0,page,3'b000}+bitnum;
   if(page==0)pixels[bitnum]=title_bits[bitnum];
   // Trace area border and a sparse reference grid.
   else if(row==9||row==63||col==0||col==127)pixels[bitnum]=1;
   else if(row>=11 && row<=61)begin
    if(row>=y_min && row<=y_max)pixels[bitnum]=1;
    else if(row==36 && col[2:0]==0)pixels[bitnum]=1;
    else if(col[4:0]==0 && row[2:0]==4)pixels[bitnum]=1;
   end
   if(page==0 && col>=66 && col<126 && row>=2 && row<=5)
    pixels[bitnum]=(col<66+meter);
  end
 end
 integer i;
 initial for(i=0;i<128;i=i+1)trace_y[i]=36;
 always @(posedge clk)begin
  send<=0;
  if(frame_age<FRAME_CLKS)frame_age<=frame_age+1'b1;
  case(state)
   POWER:if(delay_count==POWERUP_CLKS-1)begin
    delay_count<=0;init_index<=0;state<=INIT_SEND;
   end else delay_count<=delay_count+1'b1;
   INIT_SEND:if(!busy && !send)begin
    tx_data<=init_byte(init_index);first<=(init_index==0);last<=(init_index==26);
    send<=1;state<=INIT_WAIT;
   end
   INIT_WAIT:if(done)begin
    if(error)begin online<=0;delay_count<=0;state<=RETRY;end
    else if(init_index==26)begin frame_age<=FRAME_CLKS;state<=FRAME_WAIT;end
    else begin init_index<=init_index+1'b1;state<=INIT_SEND;end
   end
   FRAME_WAIT:if(frame_age==FRAME_CLKS)begin
    frame_age<=0;trigger_wait<=0;peak<=0;trigger_armed<=0;state<=ARM;
   end
   ARM:if(sample_tick)begin
    // Trigger on an upward zero crossing with a small positive threshold;
    // timeout guarantees quiet or non-crossing inputs still refresh.
    if(pcm < -16'sd128)trigger_armed<=1;
    if((trigger_armed && pcm>16'sd128)||trigger_wait==TRIGGER_SAMPLES-1)begin
     trace_y[0]<=pcm_y(pcm);peak<=magnitude;write_col<=1;stride<=0;state<=CAPTURE;
    end else trigger_wait<=trigger_wait+1'b1;
   end
   CAPTURE:if(sample_tick)begin
    if(magnitude>peak)peak<=magnitude;
    if(stride==SAMPLE_STRIDE-1)begin
     stride<=0;trace_y[write_col]<=pcm_y(pcm);
     if(write_col==127)begin
      meter<=(peak[15:9]>59)?6'd59:peak[14:9];
      page<=0;byte_index<=0;state<=PAGE_CMD_SEND;
     end else write_col<=write_col+1'b1;
    end else stride<=stride+1'b1;
   end
   PAGE_CMD_SEND:if(!busy && !send)begin
    case(byte_index)
     0:tx_data<={I2C_ADDR,1'b0};1:tx_data<=8'h00;
     2:tx_data<=8'hb0|{5'd0,page};
     3:tx_data<={4'b0000,COL_LOW};4:tx_data<=8'h10;
     default:tx_data<=8'he3; // NOP: fixed-length command transaction
    endcase
    first<=(byte_index==0);last<=(byte_index==5);send<=1;state<=PAGE_CMD_WAIT;
   end
   PAGE_CMD_WAIT:if(done)begin
    if(error)begin online<=0;delay_count<=0;state<=RETRY;end
    else if(byte_index==5)begin byte_index<=0;state<=PAGE_DATA_SEND;end
    else begin byte_index<=byte_index+1'b1;state<=PAGE_CMD_SEND;end
   end
   PAGE_DATA_SEND:if(!busy && !send)begin
    if(byte_index==0)tx_data<={I2C_ADDR,1'b0};
    else if(byte_index==1)tx_data<=8'h40;
    else tx_data<=pixels;
    first<=(byte_index==0);last<=(byte_index==129);send<=1;state<=PAGE_DATA_WAIT;
   end
   PAGE_DATA_WAIT:if(done)begin
    if(error)begin online<=0;delay_count<=0;state<=RETRY;end
    else if(byte_index==129)begin
     byte_index<=0;
     if(page==7)begin online<=1;frames<=frames+1'b1;state<=FRAME_WAIT;end
     else begin page<=page+1'b1;state<=PAGE_CMD_SEND;end
    end else begin byte_index<=byte_index+1'b1;state<=PAGE_DATA_SEND;end
   end
   RETRY:if(delay_count==POWERUP_CLKS-1)begin
    delay_count<=0;init_index<=0;state<=INIT_SEND;
   end else delay_count<=delay_count+1'b1;
   default:begin state<=POWER;delay_count<=0;end
  endcase
 end
endmodule
