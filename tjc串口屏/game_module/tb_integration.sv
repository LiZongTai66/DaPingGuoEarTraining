`timescale 1ns/1ps
module tb_integration;
    reg clk=0;
    always #5 clk=~clk;
    tri1 a,b,c,d;
    wire tx,led,din,ws,bck,pa;
    ads1115_pressure_test top(clk,1'b1,a,b,c,d,din,ws,bck,pa,1'b1,tx,led);
    reg inject_valid=0, fast_ms=0;
    reg [7:0] inject_data=0;
    reg [6:0] inject_keys=0;
    wire [7:0] decoded;
    wire valid;
    uart_rx_27m_9600 serial_check(clk,tx,decoded,valid);
    integer frame_count=0, ff_count=0, play_frames=0, game_frames=0;
    integer result=0, picture=0, scanned=0;
    reg [511:0] frame=0;
    always @(posedge clk) if(valid) begin
        if(decoded==8'hFF) begin
            ff_count=ff_count+1;
            if(ff_count==3) begin
                scanned=$sscanf(frame,"game.rx.val=%d",result);
                if(scanned==1) game_frames=game_frames+1;
                else begin
                    scanned=$sscanf(frame,"p%d.pic=%d",result,picture);
                    if(scanned!=2) $fatal(1,"interleaved UART frame: %s",frame);
                    play_frames=play_frames+1;
                end
                frame_count=frame_count+1;
                ff_count=0; frame=0;
            end
        end else begin
            if(ff_count!=0) $fatal(1,"UART frame terminators interrupted");
            frame={frame[503:0],decoded};
        end
    end
    task command(input [7:0] value);
        @(negedge clk); inject_data=value; inject_valid=1;
        @(negedge clk); inject_valid=0;
    endtask
    integer m;
    initial begin
        force top.tjc_rx_data=inject_data;
        force top.tjc_rx_valid=inject_valid;
        force top.ms_tick=fast_ms;
        force top.trigger=inject_keys;
        repeat(5) @(negedge clk);
        command('hA1);
        wait(top.tjc_char_index==4'd2);
        command('hC1);
        wait(top.game_tx_owner);
        command('hD4);
        for(m=0;m<150;m=m+1) begin
            @(negedge clk); fast_ms=1;
            @(negedge clk); fast_ms=0;
        end
        @(negedge clk); inject_keys=7'b0010000;
        @(negedge clk); inject_keys=0;
        wait(game_frames>=2);
        if(top.game_snapshot!==32'd33562724) $fatal(1,"integration score mismatch");
        command('hF0);
        // Wait for the NEW final snapshot to be latched, rather than the
        // tail of the previous frame still owning the port.
        wait(top.game_feedback.last_snapshot==32'd301998180);
        wait(top.game_tx_owner);
        command('hA1);
        wait(game_frames>=3 && play_frames>=2);
        if(ff_count!=0) wait(ff_count==0);
        $display("PASS integration: %0d real UART frames (%0d play / %0d game), no interleaving",frame_count,play_frames,game_frames);
        $finish;
    end
    initial begin
        #40000000;
        $display("frames=%0d play=%0d game=%0d owner=%0d last=%0d state=%0d",frame_count,play_frames,game_frames,top.game_tx_owner,top.game_feedback.last_snapshot,top.tjc_state);
        $fatal(1,"integration timeout");
    end
endmodule
