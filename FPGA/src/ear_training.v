`timescale 1ns/1ps
// Seven-note listening exercise. Pitches are physical key indices C4..B4.
module ear_training #(parameter NOTE_MS=600, SOUND_MS=450, INPUT_MS=60000)(
 input clk,input ms_tick,input [31:0] command,input command_valid,input abort,
 input [6:0] key_trigger,input [6:0] key_down,
 output active,output reg tone_trigger=0,output reg [2:0] tone_note=0,
 output sound,output wire [47:0] event_frame,output reg event_valid=0);
 reg [31:0] event_payload=0;
 wire [7:0] checksum=~(event_payload[31:24]+event_payload[23:16]+event_payload[15:8]+event_payload[7:0]);
 assign event_frame={8'hAA,event_payload,checksum};
 localparam IDLE=0,LOAD=1,PLAY=2,INPUT=3,DRAIN=4,DONE=5,TAIL=6;
 reg [2:0] state=IDLE,index=0,count=0,drain=0;
 reg [15:0] session=0,age=0;reg [6:0] loaded=0;
 reg [2:0] notes[0:6],answers[0:6];reg armed=0;
 reg [9:0] sound_left=0;
 reg [7:0] last_undo=0;reg undo_seen=0;
 assign active=state!=IDLE && state!=DONE;
 assign sound=sound_left!=0;
 wire [7:0] cmd=command[31:24],value=command[7:0];
 wire matching=command[23:8]==session;
 wire one_key=key_trigger!=0 && (key_trigger & (key_trigger-1'b1))==0;
 function [2:0] key_number;input [6:0] mask;begin
  case(mask)1:key_number=0;2:key_number=1;4:key_number=2;8:key_number=3;
   16:key_number=4;32:key_number=5;64:key_number=6;default:key_number=0;endcase
 end endfunction
 function [31:0] packet;input [7:0] c;input [15:0] s;input [7:0] v;reg [7:0] check;
 begin check=~(c+s[15:8]+s[7:0]+v);packet={c,s,v};end endfunction
 always @(posedge clk)begin
  tone_trigger<=0;event_valid<=0;
  if(ms_tick && sound_left!=0)sound_left<=sound_left-1'b1;
  if(abort && active)begin
   state<=IDLE;sound_left<=0;armed<=0;
   event_valid<=1;event_payload<=packet(8'hB0,session,8'd4);
  end else if(command_valid && cmd==8'h40)begin
   session<=command[23:8];state<=LOAD;loaded<=0;age<=0;count<=0;armed<=0;sound_left<=0;undo_seen<=0;
   event_valid<=1;event_payload<=packet(8'hB0,command[23:8],8'd0);
  end else if(command_valid && matching && cmd>=8'h41 && cmd<=8'h46)begin
   if(cmd==8'h41 && state==LOAD && value[7:6]==0 && value[5:3]<7 && value[2:0]<7)begin
    notes[value[5:3]]<=value[2:0];loaded[value[5:3]]<=1;
   end else if((cmd==8'h42 && state==LOAD && loaded==7'h7F) || (cmd==8'h44 && state==INPUT))begin
    state<=PLAY;index<=0;age<=0;count<=0;armed<=0;undo_seen<=0;
    tone_note<=notes[0];tone_trigger<=1;sound_left<=SOUND_MS;
    event_valid<=1;event_payload<=packet(8'hB0,session,8'd1);
   end else if(cmd==8'h43)begin
    state<=IDLE;sound_left<=0;armed<=0;
    event_valid<=1;event_payload<=packet(8'hB0,session,8'd4);
   end else if(cmd==8'h45 && state==INPUT)begin
    if(!undo_seen || last_undo!=value)begin
     undo_seen<=1;last_undo<=value;
     if(count!=0)count<=count-1'b1;
     event_payload<=packet(8'hB5,session,count==0?8'd0:({5'd0,count}-8'd1));
    end else event_payload<=packet(8'hB5,session,{5'd0,count});
    event_valid<=1;armed<=0;
   end else if(cmd==8'h46 && state==INPUT && count==7)begin
    state<=DRAIN;drain<=0;
   end else if(cmd==8'h42)begin
    state<=IDLE;sound_left<=0;
    event_valid<=1;event_payload<=packet(8'hB0,session,8'd6);
   end
  end else case(state)
   LOAD:if(ms_tick)begin
    if(age==4999)begin state<=IDLE;event_valid<=1;event_payload<=packet(8'hB0,session,8'd5);end
    else age<=age+1'b1;
   end
   PLAY:if(ms_tick)begin
    if(age==NOTE_MS-1)begin
     age<=0;
     if(index==6)begin
      state<=INPUT;armed<=0;sound_left<=0;
      event_valid<=1;event_payload<=packet(8'hB0,session,8'd2);
     end else begin
      index<=index+1'b1;tone_note<=notes[index+1'b1];tone_trigger<=1;sound_left<=SOUND_MS;
     end
    end else age<=age+1'b1;
   end
   INPUT:begin
    if(ms_tick)age<=age+1'b1;
    if(ms_tick && age==INPUT_MS-1)begin
     state<=IDLE;sound_left<=0;event_valid<=1;event_payload<=packet(8'hB0,session,8'd5);
    end else if(!armed)begin if(key_down==0 && key_trigger==0)armed<=1;end
    else if(key_trigger!=0)begin
     armed<=0;
     if(one_key && count<7)begin
      answers[count]<=key_number(key_trigger);count<=count+1'b1;
      tone_note<=key_number(key_trigger);tone_trigger<=1;sound_left<=300;
      event_valid<=1;event_payload<=packet(8'hB1,session,{2'd0,count,key_number(key_trigger)});
     end else begin event_valid<=1;event_payload<=packet(8'hB4,session,8'd1);end
    end
   end
   DRAIN:begin
    event_valid<=1;
    if(drain<7)begin event_payload<=packet(8'hB6,session,{2'd0,drain,answers[drain]});drain<=drain+1'b1;end
    else begin event_payload<=packet(8'hB2,session,8'd7);state<=TAIL;end
   end
   TAIL:if(sound_left==0)state<=DONE;
   default:;
  endcase
 end
endmodule
