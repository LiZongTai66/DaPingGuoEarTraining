`timescale 1ns/1ps
module tb_ear;
reg clk=0;always #5 clk=~clk;
reg ms=0,cv=0,abort=0;reg [31:0] cmd=0;reg [6:0] trig=0,down=0;
wire active,tt,sound,ev;wire [2:0] note;wire [47:0] frame;
ear_training #(.NOTE_MS(10),.SOUND_MS(6),.INPUT_MS(100)) u(clk,ms,cmd,cv,abort,trig,down,active,tt,note,sound,frame,ev);
integer tones=0,inputs=0,finals=0,snapshots=0,i;reg [2:0] pitch[0:6];
always @(posedge clk)begin
 if(tt && u.state==u.PLAY)begin
  if(note!==pitch[tones%7])$fatal(1,"wrong demonstration pitch");tones=tones+1;
 end
 if(ev)begin
  if(frame[39:32]==8'hB1)inputs=inputs+1;
  if(frame[39:32]==8'hB6)begin
   if(frame[10:8]!==pitch[snapshots])$fatal(1,"snapshot mismatch");snapshots=snapshots+1;
  end
  if(frame[39:32]==8'hB2)finals=finals+1;
 end
end
task command;input [7:0] c;input [15:0] sid;input [7:0] v;begin @(negedge clk);cmd={c,sid,v};cv=1;@(negedge clk);cv=0;end endtask
task tick;input integer n;integer j;begin for(j=0;j<n;j=j+1)begin @(negedge clk);ms=1;@(negedge clk);ms=0;end end endtask
task press;input [6:0] mask;begin
 @(negedge clk);down=0;trig=0;repeat(3)@(negedge clk);
 down=mask;trig=mask;@(negedge clk);trig=0;
end endtask
initial begin
 pitch[0]=0;pitch[1]=0;pitch[2]=2;pitch[3]=4;pitch[4]=6;pitch[5]=5;pitch[6]=1;
 repeat(5)@(negedge clk);command(8'h40,16'h1234,7);
 for(i=0;i<7;i=i+1)command(8'h41,16'h1234,(i<<3)|pitch[i]);
 command(8'h42,16'h1234,0);press(1);tick(70);repeat(3)@(negedge clk);
 if(tones!=7 || u.count!=0 || u.state!=u.INPUT)$fatal(1,"playback must ignore early input");
 down=1;repeat(20)@(negedge clk);if(u.count!=0)$fatal(1,"held key entered answer");
 press(3);repeat(3)@(negedge clk);if(u.count!=0)$fatal(1,"chord accepted");
 press(1);repeat(20)@(negedge clk);if(u.count!=1)$fatal(1,"fresh edge not counted once");
 press(1);press(4);repeat(4)@(negedge clk);if(u.count!=3)$fatal(1,"repeated note not accepted");
 command(8'h45,16'h1234,1);command(8'h45,16'h1234,2);command(8'h45,16'h1234,2);
 if(u.count!=1)$fatal(1,"undo click counting/idempotence");
 command(8'h44,16'h1234,0);tick(70);repeat(4)@(negedge clk);
 if(tones!=14 || u.count!=0 || u.state!=u.INPUT)$fatal(1,"replay did not clear inputs");
 for(i=0;i<7;i=i+1)press(7'b1<<pitch[i]);
 repeat(5)@(negedge clk);if(u.count!=7 || finals!=0)$fatal(1,"must wait for explicit submit");
 command(8'h45,16'h1234,3);if(u.count!=6)$fatal(1,"cannot undo seventh note");
 press(2);command(8'h46,16'h1234,0);repeat(20)@(negedge clk);
 if(finals!=1 || snapshots!=7)$fatal(1,"missing final snapshot");
 tick(310);if(active)$fatal(1,"tail never ends");
 command(8'h40,16'h2222,7);command(8'h42,16'h2222,0);if(active)$fatal(1,"incomplete chart accepted");
 command(8'h40,16'h3333,7);abort=1;@(negedge clk);abort=0;if(active)$fatal(1,"abort ignored");
 $display("PASS ear core: repeated random notes, playback input lock, held/chord rejection, real-time upload, multi-click undo/retry idempotence, replay reset, seventh-note undo, final snapshot, abort");$finish;
end
initial begin #10000000;$fatal(1,"timeout");end
endmodule
