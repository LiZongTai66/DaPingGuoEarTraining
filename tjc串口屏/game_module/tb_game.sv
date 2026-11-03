`timescale 1ns/1ps
module tb_game;
    reg clk=0;
    always #5 clk=~clk;
    reg ms_tick=0, rx_valid=0;
    reg [7:0] rx_data=0;
    reg [6:0] keys=0;
    wire [6:0] hit;
    wire [31:0] snapshot;
    wire enable;
    rhythm_game_core dut(clk,ms_tick,rx_valid,rx_data,keys,hit,snapshot,enable);
    integer checks=0;
    task command(input [7:0] value);
        @(negedge clk); rx_data=value; rx_valid=1;
        @(negedge clk); rx_valid=0;
    endtask
    task milliseconds(input integer count);
        integer m;
        for(m=0;m<count;m=m+1) begin
            @(negedge clk); ms_tick=1;
            @(negedge clk); ms_tick=0;
        end
    endtask
    task press(input [6:0] mask);
        @(negedge clk); keys=mask;
        @(negedge clk); keys=0;
    endtask
    task check(input integer score,combo,misses,judge,done);
        reg [31:0] expected;
        expected=score+(combo<<13)+(misses<<19)+(judge<<25)+(done<<28);
        checks=checks+1;
        if(snapshot!==expected) begin
            $display("FAIL snapshot actual=%d expected=%d",snapshot,expected);
            $fatal(1);
        end
    endtask
    task boundary(input integer age,judge,score);
        command('hC1); command('hD0); milliseconds(age); press(1);
        check(score,1,0,judge,0);
        if(hit!==7'd1) $fatal(1,"accepted hit did not make an audio pulse");
        @(negedge clk);
        if(hit!==7'd0) $fatal(1,"audio pulse lasted more than one cycle");
        press(1); check(score,1,0,judge,0);
    endtask

    // Independent sender with a deterministic byte-level UART handshake.
    reg tx_enable=0, tx_refresh=0, grant=1;
    reg [31:0] tx_snapshot=0;
    reg busy=0;
    wire owner,send;
    wire [7:0] data;
    rhythm_game_tx txdut(clk,ms_tick,tx_enable,tx_refresh,tx_snapshot,grant,busy,owner,send,data);
    integer busy_count=0, ff_count=0, frames=0, decoded=0, scan_result=0;
    integer received[0:127];
    reg [511:0] text_buffer=0;
    always @(posedge clk) begin
        if(busy) begin
            if(busy_count==0) busy<=0;
            else busy_count<=busy_count-1;
        end else if(send) begin
            if(!owner) $fatal(1,"byte sent without frame ownership");
            busy<=1; busy_count<=3;
            if(data==8'hFF) begin
                ff_count=ff_count+1;
                if(ff_count==3) begin
                    scan_result=$sscanf(text_buffer,"game.rx.val=%d",decoded);
                    if(scan_result!=1) $fatal(1,"malformed frame %s",text_buffer);
                    received[frames]=decoded;
                    frames=frames+1;
                    ff_count=0; text_buffer=0;
                end
            end else begin
                if(ff_count!=0) $fatal(1,"broken terminator sequence");
                text_buffer={text_buffer[503:0],data};
            end
        end
    end
    task settle;
        repeat(1500) @(negedge clk);
    endtask
    integer k,age,n,old_frames;
    reg [31:0] value;
    initial begin
        repeat(3) @(negedge clk);
        boundary(0,2,60); boundary(74,2,60); boundary(75,1,100);
        boundary(150,1,100); boundary(224,1,100);
        boundary(225,2,60); boundary(299,2,60);
        command('hC1); command('hD0); milliseconds(300);
        check(0,0,1,3,0); press(1); check(0,0,1,3,0);
        command('hC1); command('hD4); milliseconds(150); press(2);
        check(0,0,1,4,0);
        command('hD2); milliseconds(150); press(7'b0001100);
        check(0,0,2,4,0);
        command('hD0); command('hD1); check(0,0,3,3,0);
        command('hF0); check(0,0,4,3,1);
        command('hC1); check(0,0,0,0,0);
        command('hD0); command('hA0); milliseconds(500);
        if(enable!==0) $fatal(1,"A0 left telemetry enabled");
        check(0,0,0,0,0);
        for(n=0;n<7;n=n+1) begin
            command('hC1); command(8'hD0+n);
            milliseconds(150); press(7'd1<<n); check(100,1,0,1,0);
        end
        command('hC1);
        for(n=0;n<42;n=n+1) begin
            command(8'hD0+(n%7)); milliseconds(150); press(7'd1<<(n%7));
            check((n+1)*100,n+1,0,1,0);
            milliseconds(250);
        end
        command('hF0); check(4200,42,0,1,1);
        command('hC1);
        for(n=0;n<42;n=n+1) begin
            command(8'hD0+(n%7)); milliseconds(400);
        end
        command('hF0); check(0,0,42,3,1);

        // Real double-dabble RTL / framing tests, including the max unsigned
        // input even though screen gameplay values always stay below 2^31.
        tx_enable=1; tx_snapshot=0; settle;
        if(frames!=1 || received[0]!=0) $fatal(1,"zero encoding");
        for(k=0;k<12;k=k+1) begin
            case(k)
                0:value=1; 1:value=9; 2:value=10; 3:value=99;
                4:value=100; 5:value=8191; 6:value=4200+(42<<13)+(1<<25)+(1<<28);
                7:value=999999; 8:value=268435456; 9:value=999999999;
                10:value=2147483647; 11:value=32'hffffffff;
            endcase
            old_frames=frames; tx_snapshot=value; settle;
            if(frames!=old_frames+1 || received[frames-1]!==value)
                $fatal(1,"decimal encoding failed value=%d",value);
        end
        old_frames=frames;
        tx_snapshot=123;
        wait(owner); repeat(60) @(negedge clk); tx_snapshot=456;
        settle;
        if(frames!=old_frames+2 || received[old_frames]!=123 ||
           received[old_frames+1]!=456) $fatal(1,"snapshot tore mid-frame");
        grant=0; tx_snapshot=789; old_frames=frames; settle;
        if(frames!=old_frames || owner) $fatal(1,"sender ignored grant");
        grant=1; settle;
        if(received[frames-1]!=789) $fatal(1,"sender did not resume");
        tx_snapshot=987; wait(owner); tx_enable=0; settle;
        if(received[frames-1]!=987 || owner) $fatal(1,"mode exit truncated frame");
        $display("PASS: %0d judgement checks, %0d coherent telemetry frames",checks,frames);
        $finish;
    end
    initial begin #10000000; $fatal(1,"simulation timeout"); end
endmodule
