`timescale 1ns/1ps
module tb_game_stats;
reg clk=0;always #5 clk=~clk;
reg tick=0,rv=0;reg [7:0] data=0;reg [6:0] keys=0;
wire [47:0] event_frame,qframe;wire ev,qvalid,qready;
wire [6:0] hits;wire [31:0] snapshot;wire enabled,tx;
reg app_rx=1;
rhythm_game_core judge(.clk(clk),.ms_tick(tick),.rx_valid(rv),.rx_data(data),.key_trigger(keys),
 .hit_trigger(hits),.snapshot(snapshot),.telemetry_enable(enabled),.event_frame(event_frame),.event_valid(ev));
game_event_queue queue(clk,event_frame,ev,qframe,qvalid,qready);
dpg_bridge bridge(.clk(clk),.ms_tick(tick),.esp_rx(app_rx),.esp_tx(tx),
 .actual_voice(1'b0),.game_frame(qframe),.game_valid(qvalid),.game_ready(qready),.live_keys(7'd0),.pressures(56'd0));
wire [7:0] rb;wire rbvalid;wire [31:0] response;wire response_valid;
dpg_uart_rx monitor(clk,tx,rb,rbvalid);
dpg_frame_rx decoder(clk,rb,rbvalid,response,response_valid);
reg [31:0] expected[0:100];integer sent=0,received=0;reg pong=0;
reg [7:0] check;
integer wirelog;
initial wirelog=$fopen("validation/game-uart.hex","w");
always @(posedge clk)begin
 if(rbvalid)$fwrite(wirelog,"%02x ",rb);
 if(ev)begin
  check=~(event_frame[39:32]+event_frame[31:24]+event_frame[23:16]+event_frame[15:8]);
  if(event_frame[7:0]!==check)$fatal(1,"bad checksum");
 end
 if(response_valid)begin
  if(response==32'h83010203)pong=1;
  else if(response[31:24]>=8'hA0 && response[31:24]<=8'hA5)begin
   if(received>=sent || response!==expected[received])$fatal(1,"event %0d got %h expected %h",received,response,expected[received]);
   received=received+1;
  end else if(response[31:24]==8'hAF)$fatal(1,"unexpected overflow");
 end
end
task expect;input [7:0] c;input [15:0] index;input [7:0] age;begin expected[sent]={c,index,age};sent=sent+1;end endtask
task screen;input [7:0] v;begin @(negedge clk);data=v;rv=1;@(negedge clk);rv=0;end endtask
task waitms;input integer n;integer i;begin for(i=0;i<n;i=i+1)begin @(negedge clk);tick=1;@(negedge clk);tick=0;end end endtask
task press;input [6:0] mask;begin @(negedge clk);keys=mask;@(negedge clk);keys=0;end endtask
task flush;begin repeat(50000)@(negedge clk);end endtask
task appbyte;input [7:0] v;integer j;begin
 @(negedge clk);app_rx=0;repeat(234)@(negedge clk);
 for(j=0;j<8;j=j+1)begin app_rx=v[j];repeat(234)@(negedge clk);end
 app_rx=1;repeat(234)@(negedge clk);
end endtask

// Independent stalled queue: overflow must be explicit, with intact earlier frames.
reg ovvalid=0,ovready=0;reg [47:0] ovframe=0;wire [47:0] ovout;wire ovoutvalid;
game_event_queue stalled(clk,ovframe,ovvalid,ovout,ovoutvalid,ovready);
integer i,n;
initial begin
 repeat(10)@(negedge clk);
 for(i=0;i<20;i=i+1)begin ovvalid=1;ovframe=i;@(negedge clk);end
 ovvalid=0;ovready=1;
 for(i=0;i<16;i=i+1)begin if(!ovoutvalid || ovout!==i)$fatal(1,"queue damaged");@(negedge clk);end
 if(ovout!==48'hAAAF0000014F)$fatal(1,"overflow marker missing");
 @(negedge clk);ovready=0;if(ovoutvalid)$fatal(1,"queue failed to drain");
 expect(8'hA0,1,1);screen(8'hC1);
 // Real UART command competes with game transmission without corrupting frames.
 appbyte(8'hAA);appbyte(8'h20);appbyte(1);appbyte(2);appbyte(3);appbyte(8'hD9);flush;
 wait(pong); // Bounded by the existing global timeout; startup includes mapping telemetry.
 expect(8'hA1,1,75);screen(8'hD0);waitms(150);press(1);flush;
 expect(8'hA2,2,10);screen(8'hD1);waitms(20);press(2);flush;
 expect(8'hA4,3,50);screen(8'hD2);waitms(100);press(1);flush;
 expect(8'hA3,4,255);screen(8'hD0);waitms(300);flush;
 // Replacing a pending target reports its miss before accepting next target.
 expect(8'hA3,5,255);screen(8'hD0);screen(8'hD1);flush;
 expect(8'hA3,6,255);expect(8'hA5,6,0);screen(8'hF0);flush;
 expect(8'hA0,2,1);screen(8'hC1);flush;
 // Event indices remain accurate after the legacy TJC counters saturate at 63.
 for(n=1;n<=70;n=n+1)begin
  expect(8'hA1,n,75);screen(8'hD0);waitms(150);press(1);flush;
 end
 expect(8'hA5,70,0);screen(8'hF0);flush;
 expect(8'hA0,3,1);screen(8'hC1);flush;
 expect(8'hA3,1,255);expect(8'hA5,1,1);screen(8'hD0);screen(8'hA0);flush;
 if(received!=sent)$fatal(1,"missing events %0d/%0d",received,sent);
 $display("PASS game statistics: %0d actual UART frames; perfect/good/bad/miss/replacement/pending end/abort/70-hit sequence/overflow/PING",received);
 $fclose(wirelog);
 $finish;
end
initial begin #100000000;$fatal(1,"timeout");end
endmodule
