`timescale 1ns / 1ps
// Screen is the chart master. D0..D6 opens one 300 ms judgement window.
// Target time is 150 ms after receipt; Perfect: [75,225), Good: otherwise.
// One window produces exactly one Perfect / Good / Miss / Bad outcome.
module rhythm_game_core (
    input wire clk,
    input wire ms_tick,
    input wire rx_valid,
    input wire [7:0] rx_data,
    input wire [6:0] key_trigger,
    output reg [6:0] hit_trigger = 7'd0,
    output wire [31:0] snapshot,
    output wire telemetry_enable
);
    reg active = 1'b0;
    reg done = 1'b0;
    reg armed = 1'b0;
    reg [2:0] note = 3'd0;
    reg [8:0] age_ms = 9'd0;
    reg [12:0] score = 13'd0;
    reg [5:0] combo = 6'd0;
    reg [5:0] misses = 6'd0;
    reg [2:0] judgement = 3'd0;
    wire [6:0] target_mask = 7'b0000001 << note;
    wire leave_mode = rx_valid &&
        ((rx_data == 8'hA0) || (rx_data == 8'hA1) ||
         (rx_data == 8'hA2) || (rx_data == 8'hB1) ||
         (rx_data == 8'hB2) || (rx_data == 8'hB3));
    assign telemetry_enable = active | done;
    // bits: score[12:0], combo[18:13], misses[24:19],
    // judgement[27:25] (0 ready,1 perfect,2 good,3 miss,4 bad), done[28].
    assign snapshot = {3'd0, done, judgement, misses, combo, score};

    always @(posedge clk) begin
        hit_trigger <= 7'd0;
        if (rx_valid && rx_data == 8'hC1) begin
            active <= 1'b1;
            done <= 1'b0;
            armed <= 1'b0;
            note <= 3'd0;
            age_ms <= 9'd0;
            score <= 13'd0;
            combo <= 6'd0;
            misses <= 6'd0;
            judgement <= 3'd0;
        end else if (leave_mode) begin
            active <= 1'b0;
            done <= 1'b0;
            armed <= 1'b0;
        end else if (rx_valid && rx_data == 8'hF0) begin
            // F0 ends a round; a pending target is consumed as a miss.
            if (active) begin
                if (armed) begin
                    if (misses != 6'd63) misses <= misses + 1'b1;
                    combo <= 6'd0;
                    judgement <= 3'd3;
                end
                active <= 1'b0;
                done <= 1'b1;
                armed <= 1'b0;
            end
        end else if (active && rx_valid &&
                     rx_data >= 8'hD0 && rx_data <= 8'hD6) begin
            // Chart guarantees >=400ms between targets; do not silently
            // lose an unfinished target if a malformed chart replaces it.
            if (armed) begin
                if (misses != 6'd63) misses <= misses + 1'b1;
                combo <= 6'd0;
                judgement <= 3'd3;
            end
            note <= rx_data[2:0];
            age_ms <= 9'd0;
            armed <= 1'b1;
        end else if (active && armed) begin
            if (ms_tick && age_ms == 9'd299) begin
                armed <= 1'b0;
                combo <= 6'd0;
                if (misses != 6'd63) misses <= misses + 1'b1;
                judgement <= 3'd3;
            end else if (key_trigger != 7'd0) begin
                // Only a fresh pressure edge counts. Holding cannot farm
                // points. A chord containing any wrong key is Bad.
                armed <= 1'b0;
                if (key_trigger == target_mask) begin
                    hit_trigger <= target_mask;
                    if (combo != 6'd63) combo <= combo + 1'b1;
                    if (age_ms >= 9'd75 && age_ms < 9'd225) begin
                        if (score <= 13'd8091) score <= score + 13'd100;
                        judgement <= 3'd1;
                    end else begin
                        if (score <= 13'd8131) score <= score + 13'd60;
                        judgement <= 3'd2;
                    end
                end else begin
                    combo <= 6'd0;
                    if (misses != 6'd63) misses <= misses + 1'b1;
                    judgement <= 3'd4;
                end
            end else if (ms_tick) begin
                age_ms <= age_ms + 1'b1;
            end
        end
    end
endmodule

// Sends a coherent, cumulative snapshot: game.rx.val=<decimal> FF FF FF.
// Double-dabble conversion avoids expensive variable decimal divisions.
// Ownership covers the WHOLE instruction, including its three terminators.
module rhythm_game_tx (
    input wire clk,
    input wire ms_tick,
    input wire enable,
    input wire refresh,
    input wire [31:0] snapshot,
    input wire grant,
    input wire busy,
    output reg owner = 1'b0,
    output reg send = 1'b0,
    output reg [7:0] data = 8'd0
);
    localparam [2:0] IDLE=0, CONVERT=1, TRIM=2, SEND=3,
                     WAIT_BUSY=4, WAIT_DONE=5, ADVANCE=6;
    reg [2:0] state = IDLE;
    reg [31:0] last_snapshot = 32'd0;
    reg last_valid = 1'b0;
    reg [8:0] heartbeat_ms = 9'd250;
    reg [31:0] binary_value = 32'd0;
    reg [39:0] bcd = 40'd0;
    reg [39:0] adjusted;
    reg [5:0] convert_count = 6'd0;
    reg [3:0] prefix_index = 4'd0;
    reg [3:0] digit_index = 4'd9;
    reg [1:0] part = 2'd0;
    reg [1:0] suffix_index = 2'd0;
    integer i;
    function [7:0] prefix_char;
        input [3:0] index;
        begin
            case (index)
                0:prefix_char="g"; 1:prefix_char="a";
                2:prefix_char="m"; 3:prefix_char="e";
                4:prefix_char="."; 5:prefix_char="r";
                6:prefix_char="x"; 7:prefix_char=".";
                8:prefix_char="v"; 9:prefix_char="a";
                10:prefix_char="l"; 11:prefix_char="=";
                default:prefix_char=8'hFF;
            endcase
        end
    endfunction
    always @* begin
        adjusted = bcd;
        for (i=0; i<10; i=i+1)
            if (bcd[i*4 +: 4] >= 4'd5)
                adjusted[i*4 +: 4] = bcd[i*4 +: 4] + 4'd3;
    end
    always @(posedge clk) begin
        send <= 1'b0;
        if (refresh || !enable) last_valid <= 1'b0;
        if (ms_tick && heartbeat_ms < 9'd250)
            heartbeat_ms <= heartbeat_ms + 1'b1;
        case (state)
            IDLE: begin
                owner <= 1'b0;
                if (enable && !refresh && grant &&
                    (!last_valid || snapshot != last_snapshot ||
                     heartbeat_ms == 9'd250)) begin
                    owner <= 1'b1;
                    binary_value <= snapshot;
                    last_snapshot <= snapshot;
                    last_valid <= 1'b1;
                    heartbeat_ms <= 9'd0;
                    bcd <= 40'd0;
                    convert_count <= 6'd0;
                    prefix_index <= 4'd0;
                    digit_index <= 4'd9;
                    part <= 2'd0;
                    suffix_index <= 2'd0;
                    state <= CONVERT;
                end
            end
            CONVERT: begin
                bcd <= {adjusted[38:0],binary_value[31]};
                binary_value <= {binary_value[30:0],1'b0};
                if (convert_count == 6'd31) state <= TRIM;
                else convert_count <= convert_count + 1'b1;
            end
            TRIM: begin
                if (digit_index != 4'd0 && bcd[digit_index*4 +: 4] == 4'd0)
                    digit_index <= digit_index - 1'b1;
                else state <= SEND;
            end
            SEND: if (!busy) begin
                if (part == 2'd0) data <= prefix_char(prefix_index);
                else if (part == 2'd1)
                    data <= 8'h30 + {4'd0,bcd[digit_index*4 +: 4]};
                else data <= 8'hFF;
                send <= 1'b1;
                state <= WAIT_BUSY;
            end
            WAIT_BUSY: if (busy) state <= WAIT_DONE;
            WAIT_DONE: if (!busy) state <= ADVANCE;
            ADVANCE: begin
                if (part == 2'd0) begin
                    if (prefix_index == 4'd11) part <= 2'd1;
                    else prefix_index <= prefix_index + 1'b1;
                    state <= SEND;
                end else if (part == 2'd1) begin
                    if (digit_index == 4'd0) part <= 2'd2;
                    else digit_index <= digit_index - 1'b1;
                    state <= SEND;
                end else if (suffix_index == 2'd2) begin
                    owner <= 1'b0;
                    state <= IDLE;
                end else begin
                    suffix_index <= suffix_index + 1'b1;
                    state <= SEND;
                end
            end
            default: begin owner <= 1'b0; state <= IDLE; end
        endcase
    end
endmodule
