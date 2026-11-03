`timescale 1ns/1ps
module dpg_bridge(
 input clk,input ms_tick,input esp_rx,output esp_tx,
 input[47:0] game_frame,input game_valid,output game_ready,
 output[31:0] ear_command,output ear_command_valid,
 input ear_busy,input actual_voice,output[6:0] remote_held,
 input octave_down,input octave_up,output reg physical_mute=0,
 input[6:0] live_keys,input[55:0] pressures,
 output[223:0] physical_inc,output[223:0] remote_inc,output[55:0] remote_velocity,
 output reg[6:0] remote_trigger=0,output reg[6:0] remote_release=0,
 output reg mute_all=0,output reg mute_remote=0,
 output reg voice_set=0,output reg voice_value=0,output reg[15:0] gain_q15=32768
);
 wire[7:0] rxbyte;wire rxvalid;wire[31:0] command;wire command_valid;
 dpg_uart_rx rxu(clk,esp_rx,rxbyte,rxvalid);
 dpg_frame_rx rxp(clk,rxbyte,rxvalid,command,command_valid);
 wire[7:0] cmd=command[31:24],a0=command[23:16],a1=command[15:8],a2=command[7:0];
 reg[7:0] mapping[0:6];reg[7:0] held_note[0:6];
 reg[7:0] remote_note[0:6];reg[7:0] rvelocity[0:6];reg[31:0] rinc[0:6];reg[6:0] allocated=0;
 assign remote_held=allocated;
 // mode: 0 low, 1 normal, 2 high, 3 custom. Snapshots are immutable.
 reg[1:0] map_mode=1,button_pending=0,snapshot_mode=1;
 reg[7:0] map_revision=0,snapshot_revision=0;
 reg map_dirty=1;
 reg[3:0] map_phase=0;
 reg[7:0] map_snapshot[0:6];
 wire map_due=(map_phase!=0);
 wire[1:0] next_octave=(button_pending==1)?((map_mode==2)?1:0):((map_mode==0)?1:2);
 wire[7:0] octave_root=(next_octave==0)?8'd48:((next_octave==2)?8'd72:8'd60);
 reg sent_voice=0,voice_report=1;
 wire voice_due=voice_report || sent_voice!=actual_voice;
 reg[2:0] steal=0;integer i;integer chosen;
 initial begin
  mapping[0]=60;mapping[1]=62;mapping[2]=64;mapping[3]=65;mapping[4]=67;mapping[5]=69;mapping[6]=71;
  for(i=0;i<7;i=i+1)begin remote_note[i]=0;rvelocity[i]=0;rinc[i]=0;held_note[i]=0;end
 end
 genvar g;generate for(g=0;g<7;g=g+1)begin:pack
  assign physical_inc[g*32+:32]=midi_inc(mapping[g]);
  assign remote_inc[g*32+:32]=rinc[g];
  assign remote_velocity[g*8+:8]=rvelocity[g];
 end endgenerate
 function[31:0] midi_inc;input[7:0] n;begin case(n)
8'd21:midi_inc=32'd2519714;
8'd22:midi_inc=32'd2669544;
8'd23:midi_inc=32'd2828284;
8'd24:midi_inc=32'd2996462;
8'd25:midi_inc=32'd3174641;
8'd26:midi_inc=32'd3363415;
8'd27:midi_inc=32'd3563414;
8'd28:midi_inc=32'd3775306;
8'd29:midi_inc=32'd3999797;
8'd30:midi_inc=32'd4237637;
8'd31:midi_inc=32'd4489620;
8'd32:midi_inc=32'd4756587;
8'd33:midi_inc=32'd5039428;
8'd34:midi_inc=32'd5339088;
8'd35:midi_inc=32'd5656567;
8'd36:midi_inc=32'd5992924;
8'd37:midi_inc=32'd6349282;
8'd38:midi_inc=32'd6726830;
8'd39:midi_inc=32'd7126828;
8'd40:midi_inc=32'd7550611;
8'd41:midi_inc=32'd7999594;
8'd42:midi_inc=32'd8475274;
8'd43:midi_inc=32'd8979240;
8'd44:midi_inc=32'd9513174;
8'd45:midi_inc=32'd10078857;
8'd46:midi_inc=32'd10678177;
8'd47:midi_inc=32'd11313134;
8'd48:midi_inc=32'd11985848;
8'd49:midi_inc=32'd12698564;
8'd50:midi_inc=32'd13453659;
8'd51:midi_inc=32'd14253656;
8'd52:midi_inc=32'd15101222;
8'd53:midi_inc=32'd15999188;
8'd54:midi_inc=32'd16950549;
8'd55:midi_inc=32'd17958481;
8'd56:midi_inc=32'd19026348;
8'd57:midi_inc=32'd20157713;
8'd58:midi_inc=32'd21356353;
8'd59:midi_inc=32'd22626268;
8'd60:midi_inc=32'd23977432;
8'd61:midi_inc=32'd25397127;
8'd62:midi_inc=32'd26909955;
8'd63:midi_inc=32'd28507311;
8'd64:midi_inc=32'd30205976;
8'd65:midi_inc=32'd32001891;
8'd66:midi_inc=32'd33901097;
8'd67:midi_inc=32'd35931274;
8'd68:midi_inc=32'd38052695;
8'd69:midi_inc=32'd40354080;
8'd70:midi_inc=32'd42712706;
8'd71:midi_inc=32'd45294589;
8'd72:midi_inc=32'd47943392;
8'd73:midi_inc=32'd50794254;
8'd74:midi_inc=32'd53814638;
8'd75:midi_inc=32'd57014623;
8'd76:midi_inc=32'd60404889;
8'd77:midi_inc=32'd63996750;
8'd78:midi_inc=32'd67802195;
8'd79:midi_inc=32'd71833923;
8'd80:midi_inc=32'd76105391;
8'd81:midi_inc=32'd80630853;
8'd82:midi_inc=32'd85425413;
8'd83:midi_inc=32'd90505072;
8'd84:midi_inc=32'd95886784;
8'd85:midi_inc=32'd101588509;
8'd86:midi_inc=32'd107629276;
8'd87:midi_inc=32'd114029245;
8'd88:midi_inc=32'd120809777;
8'd89:midi_inc=32'd127993500;
8'd90:midi_inc=32'd135604390;
8'd91:midi_inc=32'd143667847;
8'd92:midi_inc=32'd152210781;
8'd93:midi_inc=32'd161261705;
8'd94:midi_inc=32'd170850825;
8'd95:midi_inc=32'd181010144;
8'd96:midi_inc=32'd191773567;
8'd97:midi_inc=32'd203177017;
8'd98:midi_inc=32'd215258551;
8'd99:midi_inc=32'd228058491;
8'd100:midi_inc=32'd241619554;
8'd101:midi_inc=32'd255987001;
8'd102:midi_inc=32'd271208780;
8'd103:midi_inc=32'd287335693;
8'd104:midi_inc=32'd304421563;
8'd105:midi_inc=32'd322523411;
8'd106:midi_inc=32'd341701651;
8'd107:midi_inc=32'd362020288;
8'd108:midi_inc=32'd383547135;
default:midi_inc=32'd0;endcase end endfunction

 function[15:0] gain;input[7:0] v;begin case(v)
8'd0:gain=16'd0;
8'd1:gain=16'd328;
8'd2:gain=16'd655;
8'd3:gain=16'd983;
8'd4:gain=16'd1311;
8'd5:gain=16'd1638;
8'd6:gain=16'd1966;
8'd7:gain=16'd2294;
8'd8:gain=16'd2621;
8'd9:gain=16'd2949;
8'd10:gain=16'd3277;
8'd11:gain=16'd3604;
8'd12:gain=16'd3932;
8'd13:gain=16'd4260;
8'd14:gain=16'd4588;
8'd15:gain=16'd4915;
8'd16:gain=16'd5243;
8'd17:gain=16'd5571;
8'd18:gain=16'd5898;
8'd19:gain=16'd6226;
8'd20:gain=16'd6554;
8'd21:gain=16'd6881;
8'd22:gain=16'd7209;
8'd23:gain=16'd7537;
8'd24:gain=16'd7864;
8'd25:gain=16'd8192;
8'd26:gain=16'd8520;
8'd27:gain=16'd8847;
8'd28:gain=16'd9175;
8'd29:gain=16'd9503;
8'd30:gain=16'd9830;
8'd31:gain=16'd10158;
8'd32:gain=16'd10486;
8'd33:gain=16'd10813;
8'd34:gain=16'd11141;
8'd35:gain=16'd11469;
8'd36:gain=16'd11796;
8'd37:gain=16'd12124;
8'd38:gain=16'd12452;
8'd39:gain=16'd12780;
8'd40:gain=16'd13107;
8'd41:gain=16'd13435;
8'd42:gain=16'd13763;
8'd43:gain=16'd14090;
8'd44:gain=16'd14418;
8'd45:gain=16'd14746;
8'd46:gain=16'd15073;
8'd47:gain=16'd15401;
8'd48:gain=16'd15729;
8'd49:gain=16'd16056;
8'd50:gain=16'd16384;
8'd51:gain=16'd16712;
8'd52:gain=16'd17039;
8'd53:gain=16'd17367;
8'd54:gain=16'd17695;
8'd55:gain=16'd18022;
8'd56:gain=16'd18350;
8'd57:gain=16'd18678;
8'd58:gain=16'd19005;
8'd59:gain=16'd19333;
8'd60:gain=16'd19661;
8'd61:gain=16'd19988;
8'd62:gain=16'd20316;
8'd63:gain=16'd20644;
8'd64:gain=16'd20972;
8'd65:gain=16'd21299;
8'd66:gain=16'd21627;
8'd67:gain=16'd21955;
8'd68:gain=16'd22282;
8'd69:gain=16'd22610;
8'd70:gain=16'd22938;
8'd71:gain=16'd23265;
8'd72:gain=16'd23593;
8'd73:gain=16'd23921;
8'd74:gain=16'd24248;
8'd75:gain=16'd24576;
8'd76:gain=16'd24904;
8'd77:gain=16'd25231;
8'd78:gain=16'd25559;
8'd79:gain=16'd25887;
8'd80:gain=16'd26214;
8'd81:gain=16'd26542;
8'd82:gain=16'd26870;
8'd83:gain=16'd27197;
8'd84:gain=16'd27525;
8'd85:gain=16'd27853;
8'd86:gain=16'd28180;
8'd87:gain=16'd28508;
8'd88:gain=16'd28836;
8'd89:gain=16'd29164;
8'd90:gain=16'd29491;
8'd91:gain=16'd29819;
8'd92:gain=16'd30147;
8'd93:gain=16'd30474;
8'd94:gain=16'd30802;
8'd95:gain=16'd31130;
8'd96:gain=16'd31457;
8'd97:gain=16'd31785;
8'd98:gain=16'd32113;
8'd99:gain=16'd32440;
8'd100:gain=16'd32768;
default:gain=16'd32768;endcase end endfunction

 function[47:0] packet;input[7:0] c,x,y,z;reg[7:0] check;begin check=~(c+x+y+z);packet={8'hAA,c,x,y,z,check};end endfunction
 reg[47:0] out_frame;reg out_valid;wire out_ready;
 dpg_frame_tx outq(clk,out_frame,out_valid,out_ready,esp_tx);
 assign game_ready=!command_valid && !overflow && out_ready;
 assign ear_command=command;
 assign ear_command_valid=command_valid && err==0 && (!out_valid || out_ready) &&
  (cmd>=8'h40 && cmd<=8'h46 || cmd==8'h03);
 reg[7:0] err;
 reg[2:0] scan=0;reg[6:0] last_keys=0;reg[2:0] subms=0;
 reg[31:0] now5=0,last5=0;wire[31:0] elapsed=now5-last5;
 wire changed=last_keys[scan]!=live_keys[scan];
 reg overflow=0;
 wire[7:0] pressure=pressures[scan*8+:8];
 wire[6:0] velocity=pressure>127?7'd127:pressure[6:0];
 // Keep all response generation combinational: queue and side effects see the same request.
 always @*begin
  err=0;
  case(cmd)
   8'h01,8'h02:if(ear_busy)err=6;else if(a0<21||a0>108||(cmd==1&&a1>127))err=4;
   8'h03,8'h20:;
   8'h40:if(a2!=7)err=4;
   8'h41:if(a2[7:6]!=0 || a2[5:3]>6 || a2[2:0]>6)err=4;
   8'h42,8'h43,8'h44,8'h46:if(a2!=0)err=4;
   8'h45:;
   8'h04:if(a0>1)err=4;
   8'h05:if(a0>100)err=4;
   8'h30:begin
    if(ear_busy)err=6;else if(a0>6||a1<21||a1>108)err=4;
    else if(live_keys[a0]||last_keys[a0])err=5;
   end
   default:err=2;
  endcase
  out_valid=0;out_frame=0;
  if(command_valid)begin
   if(err!=0)begin out_valid=1;out_frame=packet(8'h82,err,0,0);end
   else if(cmd==8'h20)begin out_valid=1;out_frame=packet(8'h83,a0,a1,a2);end
   else if(cmd!=1&&cmd!=2)begin out_valid=1;out_frame=packet(8'h81,cmd,a0,a1);end
  end else if(overflow)begin out_valid=1;out_frame=packet(8'h82,8,0,0);end
  else if(game_valid)begin out_valid=1;out_frame=game_frame;end
  else if(voice_due)begin out_valid=1;out_frame=packet(8'h86,{7'd0,actual_voice},8'd1,8'd0);end
  else if(map_due)begin
   out_valid=1;
   if(map_phase==1)out_frame=packet(8'h87,snapshot_revision,{6'd0,snapshot_mode},7);
   else if(map_phase==9)out_frame=packet(8'h89,snapshot_revision,{6'd0,snapshot_mode},7);
   else out_frame=packet(8'h88,snapshot_revision,{4'd0,map_phase}-8'd2,map_snapshot[map_phase-2]);
  end
  else if(elapsed>=255)begin out_valid=1;out_frame=packet(8'h90,255,0,0);end
  else if(changed)begin
   out_valid=1;
   out_frame=packet(8'h90,elapsed[7:0],live_keys[scan]?mapping[scan]:held_note[scan],live_keys[scan]?{1'b1,velocity}:8'd0);
  end
 end
 reg[13:0] link_age=0;reg link_seen=0;
 always @(posedge clk)begin
  remote_trigger<=0;remote_release<=0;mute_all<=0;mute_remote<=0;voice_set<=0;physical_mute<=0;
  if(ear_busy)button_pending<=0;
  else if(octave_down===1'b1 && octave_up===1'b1)button_pending<=0;
  else if(octave_down===1'b1)button_pending<=1;
  else if(octave_up===1'b1)button_pending<=2;
  if(map_phase==0 && map_dirty)begin
   for(i=0;i<7;i=i+1)map_snapshot[i]<=mapping[i];
   snapshot_revision<=map_revision;snapshot_mode<=map_mode;map_phase<=1;map_dirty<=0;
  end
  if(!command_valid && !ear_busy && button_pending!=0)begin
   button_pending<=0;
   if(map_mode!=next_octave)begin
   physical_mute<=1;map_mode<=next_octave;
   mapping[0]<=octave_root;mapping[1]<=octave_root+2;mapping[2]<=octave_root+4;
   mapping[3]<=octave_root+5;mapping[4]<=octave_root+7;mapping[5]<=octave_root+9;mapping[6]<=octave_root+11;
   map_revision<=map_revision+1'b1;map_dirty<=1;
   end
  end
  if(ms_tick)begin
   if(subms==4)begin subms<=0;now5<=now5+1'b1;end else subms<=subms+1'b1;
   if(link_seen&&link_age<10000)link_age<=link_age+1'b1;
   if(link_seen&&link_age==9999)begin allocated<=0;mute_remote<=1;link_seen<=0;end
  end
  if(command_valid)begin
   link_age<=0;link_seen<=1;
   if((!out_valid||out_ready)&&err==0)begin
    case(cmd)
     8'h01:begin
      if(a1==0)begin
       for(i=0;i<7;i=i+1)if(allocated[i]&&remote_note[i]==a0)begin allocated[i]<=0;remote_release[i]<=1;end
      end else begin
       chosen=-1;
       for(i=6;i>=0;i=i-1)if(!allocated[i])chosen=i;
       for(i=0;i<7;i=i+1)if(allocated[i]&&remote_note[i]==a0)chosen=i;
       if(chosen<0)begin chosen=steal;if(steal==6)steal<=0;else steal<=steal+1'b1;end
       allocated[chosen]<=1;remote_note[chosen]<=a0;rinc[chosen]<=midi_inc(a0);
       rvelocity[chosen]<={1'b0,a1[6:0]};remote_trigger[chosen]<=1;
      end
     end
     8'h02:for(i=0;i<7;i=i+1)if(allocated[i]&&remote_note[i]==a0)begin allocated[i]<=0;remote_release[i]<=1;end
     8'h03:begin allocated<=0;mute_all<=1;mute_remote<=1;end
     8'h04:begin voice_set<=1;voice_value<=a0[0];end
     8'h05:gain_q15<=gain(a0);
     8'h20:begin voice_report<=1;map_dirty<=1;end
     8'h30:begin mapping[a0]<=a1;map_mode<=3;map_revision<=map_revision+1'b1;map_dirty<=1;end
     8'h40:begin
      button_pending<=0;map_mode<=1;map_revision<=map_revision+1'b1;map_dirty<=1;
      allocated<=0;mute_remote<=1;mute_all<=1;
      mapping[0]<=60;mapping[1]<=62;mapping[2]<=64;mapping[3]<=65;
      mapping[4]<=67;mapping[5]<=69;mapping[6]<=71;
     end
     default:;
    endcase
   end
   if(out_valid&&!out_ready)overflow<=1;
  end else if(out_valid&&out_ready)begin
   if(overflow)overflow<=0;
   else if(game_valid)begin end
   else if(voice_due)begin sent_voice<=actual_voice;voice_report<=0;end
   else if(map_due)begin if(map_phase==9)map_phase<=0;else map_phase<=map_phase+1'b1;end
   else if(elapsed>=255)last5<=last5+255;
   else if(changed)begin
    last_keys[scan]<=live_keys[scan];if(live_keys[scan])held_note[scan]<=mapping[scan];last5<=now5;
   end
  end
  if(!command_valid&&!overflow&&!game_valid&&!voice_due&&!map_due&&elapsed<255)begin
   if(!changed||out_ready)begin if(scan==6)scan<=0;else scan<=scan+1'b1;end
   else overflow<=1;
  end
 end
endmodule

module game_event_queue(input clk,input [47:0] event_frame,input event_valid,
 output [47:0] frame,output valid,input ready);
 reg [47:0] fifo[0:15];reg [3:0] wp=0,rp=0;reg [4:0] count=0;
 reg overflow=0;
 wire pop=ready && count!=0;
 wire push=event_valid && (count<16 || pop);
 // AA AF 00 00 01 4F: record is incomplete, no inferred full-song advice.
 assign valid=count!=0 || overflow;
 assign frame=count!=0?fifo[rp]:48'hAAAF0000014F;
 always @(posedge clk)begin
  if(ready && count==0 && overflow)overflow<=0;
  if(event_valid && !push)overflow<=1;
  if(push)begin fifo[wp]<=event_frame;wp<=wp+1'b1;end
  if(pop)rp<=rp+1'b1;
  case({push,pop})2'b10:count<=count+1'b1;2'b01:count<=count-1'b1;default:;endcase
 end
endmodule
