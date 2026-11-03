
`timescale 1ns / 1ps

// ============================================================
// Tang Primer 20K Pressure Piano V8
// 6 keys, 2 independent ADS1115, Piano / Guitar
//
// ADC1: SCL P8, SDA P9, ADDR GND
//        A0 Do, A1 Re, A2 Mi, A3 Fa
//
// ADC2: SCL A14, SDA A15, ADDR GND
//        A0 Sol, A1 La
//
// S0: active-low; 0 Piano, 1 Guitar
// Clock: 27MHz
// Audio: PT8211
//
// CST constraints are configured separately.
// ============================================================

module ads1115_pressure_test (
    input  wire clk27m,
    input  wire key_s0,

    inout  wire adc1_sda,
    inout  wire adc1_scl,

    inout  wire adc2_sda,
    inout  wire adc2_scl,

    output reg HP_DIN,
    output reg HP_WS,
    output reg HP_BCK,
    output wire PA_EN,

    // TJC UART
    input  wire uart_rx,
    output wire uart_tx,

    // Play mode LED
    output wire play_led
);

assign PA_EN = 1'b1;

// ============================================================
// TJC UART CONTROL
// FPGA clock: 27MHz
// UART: 9600 baud, 8N1
//
// 0xA1 : enter play mode, LED ON
// 0xA0 : leave play mode, LED OFF
// ============================================================

// TX is reserved for future FPGA -> TJC communication.
// UART idle level is HIGH.
// FPGA N8 -> TJC RX
reg        tjc_tx_send = 1'b0;
reg  [7:0] tjc_tx_data = 8'd0;
wire       tjc_tx_busy;
wire game_tx_owner;
wire game_tx_send;
wire [7:0] game_tx_data;
wire [6:0] game_hit_trigger;
wire [31:0] game_snapshot;
wire game_telemetry_enable;

tjc_uart_tx tjc_uart_sender (
    .clk  (clk27m),
    .send (game_tx_owner ? game_tx_send : tjc_tx_send),
    .data (game_tx_owner ? game_tx_data : tjc_tx_data),
    .tx   (uart_tx),
    .busy (tjc_tx_busy)
);


// UART receive result
wire [7:0] tjc_rx_data;
wire tjc_rx_valid;

// UART receiver instance
uart_rx_27m_9600 tjc_uart_receiver (
    .clk27m(clk27m),
    .rx(uart_rx),
    .data(tjc_rx_data),
    .valid(tjc_rx_valid)
);

// Current play-mode status
reg play_mode = 1'b0;

// 音游模式
reg game_mode = 1'b0;
// 当前音游目标音符
// 0 Do 1 Re 2 Mi 3 Fa 4 Sol 5 La 6 Si
reg [2:0] target_note = 3'd0;

// 示范模式
reg demo_mode = 1'b0;
reg [1:0] demo_song = 2'd0;
reg demo_restart = 1'b0;


    // 接收 TJC 指令
    always @(posedge clk27m) begin
        demo_restart <= 1'b0;

        if (tjc_rx_valid) begin
            case (tjc_rx_data)

                // A1：进入自由演奏模式
                8'hA1: begin
                    play_mode <= 1'b1;
                    demo_mode <= 1'b0;
                    game_mode <= 1'b0;
                end

                // A0：返回主页，退出所有模式
                8'hA0: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b0;
                    game_mode <= 1'b0;
                end

                // A2：进入示范模式选择页面
                8'hA2: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b0;
                    game_mode <= 1'b0;
                end

                // B1：示范小星星
                8'hB1: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b1;
                    game_mode <= 1'b0;
                    demo_song <= 2'd0;
                    demo_restart <= 1'b1;
                end

                // B2：示范两只老虎
                8'hB2: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b1;
                    game_mode <= 1'b0;
                    demo_song <= 2'd1;
                    demo_restart <= 1'b1;
                end

                // B3：示范欢乐颂
                8'hB3: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b1;
                    game_mode <= 1'b0;
                    demo_song <= 2'd2;
                    demo_restart <= 1'b1;
                end

                // B0：停止示范
                8'hB0: begin
                    demo_mode <= 1'b0;
                end

                // C1：开始音游
                8'hC1: begin
                    play_mode <= 1'b0;
                    demo_mode <= 1'b0;
                    game_mode <= 1'b1;
                end
                // F0: finish game, stop accepting pressure hits.
                8'hF0: begin
                    game_mode <= 1'b0;
                end
       // D0-D6：接收当前音符

8'hD0: begin
    target_note <= 3'd0;
end

8'hD1: begin
    target_note <= 3'd1;
end

8'hD2: begin
    target_note <= 3'd2;
end

8'hD3: begin
    target_note <= 3'd3;
end

8'hD4: begin
    target_note <= 3'd4;
end

8'hD5: begin
    target_note <= 3'd5;
end

8'hD6: begin
    target_note <= 3'd6;
end
                default: ;
            endcase
        end
    end

// LED output polarity
// 1: LED turns on at high level
// 0: LED turns on at low level
localparam LED_ACTIVE_HIGH = 1'b0;
assign play_led =
    LED_ACTIVE_HIGH ? (play_mode | game_mode)
                    : ~(play_mode | game_mode);
// ============================================================
// END TJC UART CONTROL
// ============================================================


// ============================================================
// S0 BUTTON - 20ms DEBOUNCE
// ============================================================

reg s0_meta   = 1'b1;
reg s0_sync   = 1'b1;
reg s0_stable = 1'b1;
reg [19:0] s0_count = 20'd0;

reg guitar_mode = 1'b0;

localparam [19:0] S0_DEBOUNCE = 20'd540000;

always @(posedge clk27m) begin
    s0_meta <= key_s0;
    s0_sync <= s0_meta;

    if (s0_sync == s0_stable) begin
        s0_count <= 20'd0;
    end
    else if (s0_count == S0_DEBOUNCE - 1'b1) begin
        s0_count <= 20'd0;
        s0_stable <= s0_sync;

        if (!s0_sync)
            guitar_mode <= ~guitar_mode;
    end
    else begin
        s0_count <= s0_count + 1'b1;
    end
end

// ============================================================
// AUDIO SAMPLE TICK: 46875 Hz
// ============================================================

reg [9:0] sample_div = 10'd0;
reg sample_tick = 1'b0;

always @(posedge clk27m) begin
    if (sample_div == 10'd575) begin
        sample_div <= 10'd0;
        sample_tick <= 1'b1;
    end
    else begin
        sample_div <= sample_div + 1'b1;
        sample_tick <= 1'b0;
    end
end

// ============================================================
// MILLISECOND TICK
// ============================================================

reg [14:0] ms_div = 15'd0;
reg ms_tick = 1'b0;

always @(posedge clk27m) begin
    if (ms_div == 15'd26999) begin
        ms_div <= 15'd0;
        ms_tick <= 1'b1;
    end
    else begin
        ms_div <= ms_div + 1'b1;
        ms_tick <= 1'b0;
    end
end

// ============================================================
// ADC1 DATA (DO RE MI FA)
// ============================================================

wire [15:0] adc1_ch0;
wire [15:0] adc1_ch1;
wire [15:0] adc1_ch2;
wire [15:0] adc1_ch3;

// ============================================================
// ADC2 DATA (SOL LA)
// ============================================================

wire [15:0] adc2_ch0;
wire [15:0] adc2_ch1;
wire [15:0] adc2_ch2;
// ============================================================
// TWO INDEPENDENT ADS1115 INSTANCES
// Both devices ADDR = GND, address = 0x48
// ============================================================

ads1115_reader #(
    .CHANNEL_COUNT(4)
) adc_reader_1 (
    .clk27m(clk27m),
    .sda(adc1_sda),
    .scl(adc1_scl),
    .adc_a0(adc1_ch0),
    .adc_a1(adc1_ch1),
    .adc_a2(adc1_ch2),
    .adc_a3(adc1_ch3)
);

ads1115_reader #(
    .CHANNEL_COUNT(3)
) adc_reader_2 (
    .clk27m(clk27m),
    .sda(adc2_sda),
    .scl(adc2_scl),
    .adc_a0(adc2_ch0),
    .adc_a1(adc2_ch1),
    .adc_a2(adc2_ch2),
    .adc_a3()
);

// ============================================================
// SIX PRESSURE VALUES
// Same scaling as the working V7
// ============================================================

wire [7:0] pressure_do =
    adc1_ch0[15] ? 8'd0 : adc1_ch0[14:7];

wire [7:0] pressure_re =
    adc1_ch1[15] ? 8'd0 : adc1_ch1[14:7];

wire [7:0] pressure_mi =
    adc1_ch2[15] ? 8'd0 : adc1_ch2[14:7];

wire [7:0] pressure_fa =
    adc1_ch3[15] ? 8'd0 : adc1_ch3[14:7];

wire [7:0] pressure_sol =
    adc2_ch0[15] ? 8'd0 : adc2_ch0[14:7];

wire [7:0] pressure_la =
    adc2_ch1[15] ? 8'd0 : adc2_ch1[14:7];
wire [7:0] pressure_si =
    adc2_ch2[15] ? 8'd0 : adc2_ch2[14:7];

// ============================================================
// SIX INDEPENDENT KEY TRIGGERS
// Same threshold / 1ms scan as V7
// ============================================================

localparam [7:0] KEY_ON_LEVEL  = 8'd3;
localparam [7:0] KEY_OFF_LEVEL = 8'd1;

reg [6:0] key_down = 7'b0000000;
reg [6:0] trigger  = 7'b0000000;

always @(posedge clk27m) begin
    trigger <= 7'b000000;

    if (ms_tick) begin

        // DO
        if (pressure_do <= KEY_OFF_LEVEL)
            key_down[0] <= 1'b0;
        else if (!key_down[0] &&
                 pressure_do >= KEY_ON_LEVEL) begin
            key_down[0] <= 1'b1;
            trigger[0] <= 1'b1;
        end

        // RE
        if (pressure_re <= KEY_OFF_LEVEL)
            key_down[1] <= 1'b0;
        else if (!key_down[1] &&
                 pressure_re >= KEY_ON_LEVEL) begin
            key_down[1] <= 1'b1;
            trigger[1] <= 1'b1;
        end

        // MI
        if (pressure_mi <= KEY_OFF_LEVEL)
            key_down[2] <= 1'b0;
        else if (!key_down[2] &&
                 pressure_mi >= KEY_ON_LEVEL) begin
            key_down[2] <= 1'b1;
            trigger[2] <= 1'b1;
        end

        // FA
        if (pressure_fa <= KEY_OFF_LEVEL)
            key_down[3] <= 1'b0;
        else if (!key_down[3] &&
                 pressure_fa >= KEY_ON_LEVEL) begin
            key_down[3] <= 1'b1;
            trigger[3] <= 1'b1;
        end

        // SOL
        if (pressure_sol <= KEY_OFF_LEVEL)
            key_down[4] <= 1'b0;
        else if (!key_down[4] &&
                 pressure_sol >= KEY_ON_LEVEL) begin
            key_down[4] <= 1'b1;
            trigger[4] <= 1'b1;
        end

        // LA
        if (pressure_la <= KEY_OFF_LEVEL)
            key_down[5] <= 1'b0;
        else if (!key_down[5] &&
                 pressure_la >= KEY_ON_LEVEL) begin
            key_down[5] <= 1'b1;
            trigger[5] <= 1'b1;
        end
      // SI
        if (pressure_si <= KEY_OFF_LEVEL)
                  key_down[6] <= 1'b0;
             else if (!key_down[6] &&
                   pressure_si >= KEY_ON_LEVEL) begin
             key_down[6] <= 1'b1;
              trigger[6] <= 1'b1;
        end
    end
end

// ============================================================
// ============================================================
// TJC 7-KEY IMAGE DISPLAY CONTROLLER
// p0..p6
// Pressed: 3,5,7,9,11,13,15
// Released: 4,6,8,10,12,14,16
// ============================================================

reg [6:0] tjc_sent_keys = 7'd0;
reg [6:0] tjc_valid_keys = 7'd0;

reg [2:0] tjc_key_index = 3'd0;
reg [2:0] tjc_active_key = 3'd0;
reg       tjc_active_pressed = 1'b0;

reg [4:0] tjc_picture = 5'd4;
reg [3:0] tjc_char_index = 4'd0;

reg [2:0] tjc_state = 3'd0;

localparam [2:0]
    TJC_SCAN      = 3'd0,
    TJC_SEND      = 3'd1,
    TJC_WAIT_BUSY = 3'd2,
    TJC_WAIT_DONE = 3'd3,
    TJC_NEXT      = 3'd4;

wire [4:0] tjc_target_picture =
    5'd4 + {tjc_key_index, 1'b0}
    - {4'd0, key_down[tjc_key_index]};

function [7:0] tjc_command_char;
    input [3:0] position;
    input [2:0] key_number;
    input [4:0] picture_number;

    begin
        case (position)
            4'd0: tjc_command_char = "p";
            4'd1: tjc_command_char = 8'h30 + {5'd0, key_number};
            4'd2: tjc_command_char = ".";
            4'd3: tjc_command_char = "p";
            4'd4: tjc_command_char = "i";
            4'd5: tjc_command_char = "c";
            4'd6: tjc_command_char = "=";

            4'd7: begin
                if (picture_number >= 10)
                    tjc_command_char = "1";
                else
                    tjc_command_char = 8'h30 + {3'd0, picture_number};
            end

            4'd8: begin
                if (picture_number >= 10)
                    tjc_command_char = 8'h30 +
                                       (picture_number - 5'd10);
                else
                    tjc_command_char = 8'hFF;
            end

            4'd9:  tjc_command_char = 8'hFF;
            4'd10: tjc_command_char = 8'hFF;
            4'd11: tjc_command_char = 8'hFF;

            default: tjc_command_char = 8'hFF;
        endcase
    end
endfunction

always @(posedge clk27m) begin
    tjc_tx_send <= 1'b0;

    if (!play_mode)
        tjc_valid_keys <= 7'd0;

    if (!game_tx_owner) begin
    case (tjc_state)

        TJC_SCAN: begin
            if (play_mode) begin
                if (!tjc_valid_keys[tjc_key_index] ||
                    tjc_sent_keys[tjc_key_index] !=
                    key_down[tjc_key_index]) begin

                    tjc_active_key <= tjc_key_index;
                    tjc_active_pressed <= key_down[tjc_key_index];
                    tjc_picture <= tjc_target_picture;
                    tjc_char_index <= 4'd0;
                    tjc_state <= TJC_SEND;

                end else begin
                    if (tjc_key_index == 3'd6)
                        tjc_key_index <= 3'd0;
                    else
                        tjc_key_index <= tjc_key_index + 1'b1;
                end
            end
        end

        TJC_SEND: begin
            if (!tjc_tx_busy) begin
                tjc_tx_data <= tjc_command_char(
                    tjc_char_index,
                    tjc_active_key,
                    tjc_picture
                );
                tjc_tx_send <= 1'b1;
                tjc_state <= TJC_WAIT_BUSY;
            end
        end

        TJC_WAIT_BUSY: begin
            if (tjc_tx_busy)
                tjc_state <= TJC_WAIT_DONE;
        end

        TJC_WAIT_DONE: begin
            if (!tjc_tx_busy)
                tjc_state <= TJC_NEXT;
        end

        TJC_NEXT: begin
           if ((tjc_picture < 10 &&
     tjc_char_index == 4'd10) ||
    (tjc_picture >= 10 &&
     tjc_char_index == 4'd11)) begin

                tjc_sent_keys[tjc_active_key]
                    <= tjc_active_pressed;

                if (play_mode)
                    tjc_valid_keys[tjc_active_key] <= 1'b1;

                if (tjc_active_key == 3'd6)
                    tjc_key_index <= 3'd0;
                else
                    tjc_key_index <= tjc_active_key + 1'b1;

                tjc_state <= TJC_SCAN;

            end else begin
                tjc_char_index <= tjc_char_index + 1'b1;
                tjc_state <= TJC_SEND;
            end
        end

        default: tjc_state <= TJC_SCAN;

    endcase
    end
end
// ============================================================
// DEMO SONG PLAYER
// 0=C4 1=D4 2=E4 3=F4 4=G4 5=A4 6=B4
// 7=REST
// Each duration unit = 350ms
// ============================================================

reg [6:0] demo_trigger = 7'd0;
reg [5:0] demo_index = 6'd0;
reg [12:0] demo_elapsed = 13'd0;
reg [12:0] demo_duration = 13'd0;

reg [6:0] demo_step;
reg [2:0] demo_note;

// 曲谱编码：高4位为节拍长度，低3位为音符
function [6:0] song_step;
    input [1:0] song;
    input [5:0] index;
    begin
        song_step = {4'd1, 3'd7};

        case (song)

            // 小星星
            2'd0: begin
                case (index)
                    0: song_step = {4'd1,3'd0};
                    1: song_step = {4'd1,3'd0};
                    2: song_step = {4'd1,3'd4};
                    3: song_step = {4'd1,3'd4};
                    4: song_step = {4'd1,3'd5};
                    5: song_step = {4'd1,3'd5};
                    6: song_step = {4'd2,3'd4};
                    7: song_step = {4'd1,3'd3};
                    8: song_step = {4'd1,3'd3};
                    9: song_step = {4'd1,3'd2};
                    10: song_step = {4'd1,3'd2};
                    11: song_step = {4'd1,3'd1};
                    12: song_step = {4'd1,3'd1};
                    13: song_step = {4'd2,3'd0};
                    default: song_step = {4'd1,3'd7};
                endcase
            end

            // 两只老虎（前两乐句）
            2'd1: begin
                case (index)
                    0: song_step = {4'd1,3'd0};
                    1: song_step = {4'd1,3'd1};
                    2: song_step = {4'd1,3'd2};
                    3: song_step = {4'd1,3'd0};
                    4: song_step = {4'd1,3'd0};
                    5: song_step = {4'd1,3'd1};
                    6: song_step = {4'd1,3'd2};
                    7: song_step = {4'd1,3'd0};
                    8: song_step = {4'd1,3'd2};
                    9: song_step = {4'd1,3'd3};
                    10: song_step = {4'd2,3'd4};
                    11: song_step = {4'd1,3'd2};
                    12: song_step = {4'd1,3'd3};
                    13: song_step = {4'd2,3'd4};
                    default: song_step = {4'd1,3'd7};
                endcase
            end

            // 欢乐颂（前两乐句）
            2'd2: begin
                case (index)
                    0: song_step = {4'd1,3'd2};
                    1: song_step = {4'd1,3'd2};
                    2: song_step = {4'd1,3'd3};
                    3: song_step = {4'd1,3'd4};
                    4: song_step = {4'd1,3'd4};
                    5: song_step = {4'd1,3'd3};
                    6: song_step = {4'd1,3'd2};
                    7: song_step = {4'd1,3'd1};
                    8: song_step = {4'd1,3'd0};
                    9: song_step = {4'd1,3'd0};
                    10: song_step = {4'd1,3'd1};
                    11: song_step = {4'd1,3'd2};
                    12: song_step = {4'd2,3'd2};
                    13: song_step = {4'd2,3'd1};
                    default: song_step = {4'd1,3'd7};
                endcase
            end

            default: song_step = {4'd1,3'd7};
        endcase
    end
endfunction


wire [5:0] demo_last_index = 6'd13;

// 当前曲谱音符
always @(*) begin
    demo_step = song_step(demo_song, demo_index);
    demo_note = demo_step[2:0];
end

// 示范歌曲自动播放控制器
always @(posedge clk27m) begin
    demo_trigger <= 7'd0;

    if (demo_restart || !demo_mode) begin
        demo_index    <= 6'd0;
        demo_elapsed  <= 13'd0;
        demo_duration <= 13'd0;
    end
    else if (ms_tick) begin

        // 尚未开始当前音符：读取曲谱并触发
        if (demo_duration == 13'd0) begin
            demo_elapsed <= 13'd0;
            demo_duration <=
                {9'd0, demo_step[6:3]} * 13'd350;

            if (demo_note < 3'd7)
                demo_trigger[demo_note] <= 1'b1;
        end

        // 当前音符持续时间结束
        else if (demo_elapsed >= demo_duration - 13'd1) begin
            demo_elapsed  <= 13'd0;
            demo_duration <= 13'd0;

            if (demo_index == demo_last_index)
                demo_index <= 6'd0;
            else
                demo_index <= demo_index + 6'd1;
        end

        // 当前音符继续计时
        else begin
            demo_elapsed <= demo_elapsed + 13'd1;
        end
    end
end

// DDS NOTE INCREMENTS (46875 Hz sample rate)
// ============================================================

localparam [31:0] INC_C4 = 32'd23977432;
localparam [31:0] INC_D4 = 32'd26909955;
localparam [31:0] INC_E4 = 32'd30205976;
localparam [31:0] INC_F4 = 32'd32001891;
localparam [31:0] INC_G4 = 32'd35931274;
localparam [31:0] INC_A4 = 32'd40354080;
localparam [31:0] INC_B4 = 32'd45294589;

// ============================================================
// SIX INDEPENDENT VOICES
// ============================================================

wire signed [23:0] audio_do;
wire signed [23:0] audio_re;
wire signed [23:0] audio_mi;
wire signed [23:0] audio_fa;
wire signed [23:0] audio_sol;
wire signed [23:0] audio_la;
wire signed [23:0] audio_si;
// Fresh, successfully judged hits are the only game audio triggers.
// Home / finished game is silent; free-play and demo keep their own triggers.
wire [6:0] voice_trigger =
    demo_mode ? demo_trigger :
    game_mode ? game_hit_trigger :
    play_mode ? trigger : 7'd0;

rhythm_game_core game_judge (
    .clk(clk27m), .ms_tick(ms_tick),
    .rx_valid(tjc_rx_valid), .rx_data(tjc_rx_data),
    .key_trigger(trigger), .hit_trigger(game_hit_trigger),
    .snapshot(game_snapshot), .telemetry_enable(game_telemetry_enable)
);
rhythm_game_tx game_feedback (
    .clk(clk27m), .ms_tick(ms_tick),
    .enable(game_telemetry_enable),
    .refresh(tjc_rx_valid && tjc_rx_data == 8'hC1),
    .snapshot(game_snapshot),
    .grant(tjc_state == TJC_SCAN && !tjc_tx_busy && !tjc_tx_send),
    .busy(tjc_tx_busy), .owner(game_tx_owner),
    .send(game_tx_send), .data(game_tx_data)
);

wire [7:0] demo_velocity = 8'd110;
piano_voice_v6 #(.NOTE_INC(INC_C4)) voice_do (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[0]),
.velocity(demo_mode ? demo_velocity : pressure_do),
    .guitar_mode(guitar_mode),
    .audio_out(audio_do)
);

piano_voice_v6 #(.NOTE_INC(INC_D4)) voice_re (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[1]),
    .velocity(demo_mode ? demo_velocity : pressure_re),
    .guitar_mode(guitar_mode),
    .audio_out(audio_re)
);

piano_voice_v6 #(.NOTE_INC(INC_E4)) voice_mi (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[2]),
    .velocity(demo_mode ? demo_velocity : pressure_mi),
    .guitar_mode(guitar_mode),
    .audio_out(audio_mi)
);

piano_voice_v6 #(.NOTE_INC(INC_F4)) voice_fa (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[3]),
.velocity(demo_mode ? demo_velocity : pressure_fa),
    .guitar_mode(guitar_mode),
    .audio_out(audio_fa)
);

piano_voice_v6 #(.NOTE_INC(INC_G4)) voice_sol (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
   .trigger(voice_trigger[4]),
.velocity(demo_mode ? demo_velocity : pressure_sol),
    .guitar_mode(guitar_mode),
    .audio_out(audio_sol)
);

piano_voice_v6 #(.NOTE_INC(INC_A4)) voice_la (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[5]),
.velocity(demo_mode ? demo_velocity : pressure_la),
    .guitar_mode(guitar_mode),
    .audio_out(audio_la)
);

piano_voice_v6 #(.NOTE_INC(INC_B4)) voice_si (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
   .trigger(voice_trigger[6]),
.velocity(demo_mode ? demo_velocity : pressure_si),
    .guitar_mode(guitar_mode),
    .audio_out(audio_si)
);
// ============================================================
// SIX-VOICE MIXER
// Sign extension before summation; clip to 16-bit range.
// ============================================================

// SEVEN-VOICE MIXER
wire signed [27:0] mix_sum =
    $signed({{4{audio_do[23]}},  audio_do})  +
    $signed({{4{audio_re[23]}},  audio_re})  +
    $signed({{4{audio_mi[23]}},  audio_mi})  +
    $signed({{4{audio_fa[23]}},  audio_fa})  +
    $signed({{4{audio_sol[23]}}, audio_sol}) +
    $signed({{4{audio_la[23]}},  audio_la})  +
    $signed({{4{audio_si[23]}},  audio_si});

wire signed [15:0] audio_sample =
    (mix_sum > 28'sd30000)
        ? 16'sd30000
    : (mix_sum < -28'sd30000)
        ? -16'sd30000
    : mix_sum[15:0];

// ============================================================
// PT8211 OUTPUT - KEEP V7 SERIALIZER
// ============================================================

reg [3:0] bck_div = 4'd0;
reg [5:0] bit_count = 6'd0;
reg signed [15:0] frame_sample = 16'sd0;

initial begin
    HP_DIN = 1'b0;
    HP_WS  = 1'b0;
    HP_BCK = 1'b0;
end

always @(posedge clk27m) begin

    if (bck_div == 4'd8) begin

        bck_div <= 4'd0;

        if (HP_BCK == 1'b0) begin
            HP_BCK <= 1'b1;
        end
        else begin

            HP_BCK <= 1'b0;

            if (bit_count == 6'd0) begin
                frame_sample <= audio_sample;
                HP_WS  <= 1'b0;
                HP_DIN <= audio_sample[15];
            end
            else if (bit_count < 6'd16) begin
                HP_WS  <= 1'b0;
                HP_DIN <= frame_sample[15-bit_count];
            end
            else if (bit_count == 6'd16) begin
                HP_WS  <= 1'b1;
                HP_DIN <= frame_sample[15];
            end
            else begin
                HP_WS  <= 1'b1;
                HP_DIN <= frame_sample[31-bit_count];
            end

            if (bit_count == 6'd31)
                bit_count <= 6'd0;
            else
                bit_count <= bit_count + 1'b1;
        end
    end
    else begin
        bck_div <= bck_div + 1'b1;
    end
end

endmodule

// ============================================================
// ADS1115 READER
//
// Two independent instances of the same module.
// ADDR = GND -> 7-bit I2C address 0x48
//
// CHANNEL_COUNT = 4: scan A0..A3
// CHANNEL_COUNT = 2: scan A0..A1
//
// Based on the working V7 scanner state machine.
// ============================================================

module ads1115_reader #(
    parameter integer CHANNEL_COUNT = 4
)(
    input  wire clk27m,
    inout  wire sda,
    inout  wire scl,

    output reg [15:0] adc_a0 = 16'd0,
    output reg [15:0] adc_a1 = 16'd0,
    output reg [15:0] adc_a2 = 16'd0,
    output reg [15:0] adc_a3 = 16'd0
);

// ============================================================
// I2C OPEN DRAIN
// 1 = pull low
// 0 = release line
// ============================================================

reg sda_low = 1'b0;
reg scl_low = 1'b0;

assign sda = sda_low ? 1'b0 : 1'bz;
assign scl = scl_low ? 1'b0 : 1'bz;

wire sda_in = sda;

// ============================================================
// I2C TICK - same divider as V7
// ============================================================

reg [7:0] i2c_div = 8'd0;
reg i2c_tick = 1'b0;

always @(posedge clk27m) begin
    if (i2c_div == 8'd134) begin
        i2c_div <= 8'd0;
        i2c_tick <= 1'b1;
    end
    else begin
        i2c_div <= i2c_div + 1'b1;
        i2c_tick <= 1'b0;
    end
end

// ============================================================
// ADS1115 REGISTERS
// ============================================================

reg [1:0] channel = 2'd0;

// Single-shot, A0/A1/A2/A3 input selection
wire [7:0] config_high =
    (channel == 2'd0) ? 8'hC3 :
    (channel == 2'd1) ? 8'hD3 :
    (channel == 2'd2) ? 8'hE3 :
                        8'hF3;

localparam [7:0] ADS_WRITE = 8'h90;
localparam [7:0] ADS_READ  = 8'h91;

reg [7:0] tx_byte  = 8'd0;
reg [7:0] rx_byte  = 8'd0;
reg [7:0] adc_high = 8'd0;

reg [2:0] bit_cnt = 3'd7;
reg [15:0] wait_count = 16'd0;
reg ack_ok = 1'b0;

// ============================================================
// I2C STATES
// ============================================================

localparam [7:0]
    ST_POWER_WAIT = 8'd0,

    ST_START_1 = 8'd1,
    ST_START_2 = 8'd2,
    ST_START_3 = 8'd3,

    ST_TX_SETUP = 8'd4,
    ST_TX_RISE  = 8'd5,
    ST_TX_HIGH  = 8'd6,
    ST_TX_FALL  = 8'd7,

    ST_ACK_RELEASE = 8'd8,
    ST_ACK_RISE    = 8'd9,
    ST_ACK_WAIT    = 8'd10,
    ST_ACK_SAMPLE  = 8'd11,
    ST_ACK_FALL    = 8'd12,

    ST_STOP_1 = 8'd13,
    ST_STOP_2 = 8'd14,
    ST_STOP_3 = 8'd15,

    ST_CFG_ADDR = 8'd20,
    ST_CFG_PTR  = 8'd21,
    ST_CFG_H    = 8'd22,
    ST_CFG_L    = 8'd23,
    ST_CFG_STOP = 8'd24,

    ST_ADC_WAIT = 8'd30,

    ST_PTR_START = 8'd31,
    ST_PTR_ADDR  = 8'd32,
    ST_PTR_STOP  = 8'd34,

    ST_READ_START = 8'd40,
    ST_READ_ADDR  = 8'd41,

    ST_RX_SETUP  = 8'd42,
    ST_RX_RISE   = 8'd43,
    ST_RX_SAMPLE = 8'd44,
    ST_RX_FALL   = 8'd45,

    ST_MASTER_ACK_1  = 8'd46,
    ST_MASTER_ACK_2  = 8'd47,
    ST_MASTER_ACK_3  = 8'd48,

    ST_MASTER_NACK_1 = 8'd49,
    ST_MASTER_NACK_2 = 8'd50,
    ST_MASTER_NACK_3 = 8'd51,

    ST_READ_STOP    = 8'd52,
    ST_NEXT_CHANNEL = 8'd53;

reg [7:0] state = ST_POWER_WAIT;
reg [7:0] return_state = ST_POWER_WAIT;
reg [7:0] rx_return_state = ST_POWER_WAIT;

// ============================================================
// ADS1115 I2C SCANNER
// ============================================================

always @(posedge clk27m) begin

    if (i2c_tick) begin

        case (state)

            // --------------------------------------------
            // Power-up delay
            // --------------------------------------------

            ST_POWER_WAIT: begin
                sda_low <= 1'b0;
                scl_low <= 1'b0;

                if (wait_count >= 16'd4000) begin
                    wait_count <= 16'd0;
                    state <= ST_CFG_ADDR;
                end
                else begin
                    wait_count <= wait_count + 1'b1;
                end
            end

            // --------------------------------------------
            // Configure ADS1115 conversion
            // --------------------------------------------

            ST_CFG_ADDR: begin
                tx_byte <= ADS_WRITE;
                return_state <= ST_CFG_PTR;
                state <= ST_START_1;
            end

            ST_CFG_PTR: begin
                tx_byte <= 8'h01;
                return_state <= ST_CFG_H;
                bit_cnt <= 3'd7;
                state <= ST_TX_SETUP;
            end

            ST_CFG_H: begin
                tx_byte <= config_high;
                return_state <= ST_CFG_L;
                bit_cnt <= 3'd7;
                state <= ST_TX_SETUP;
            end

            ST_CFG_L: begin
                tx_byte <= 8'hE3;
                return_state <= ST_CFG_STOP;
                bit_cnt <= 3'd7;
                state <= ST_TX_SETUP;
            end

            ST_CFG_STOP: begin
                return_state <= ST_ADC_WAIT;
                state <= ST_STOP_1;
            end

            // --------------------------------------------
            // I2C START
            // --------------------------------------------

            ST_START_1: begin
                sda_low <= 1'b0;
                scl_low <= 1'b0;
                state <= ST_START_2;
            end

            ST_START_2: begin
                sda_low <= 1'b1;
                scl_low <= 1'b0;
                state <= ST_START_3;
            end

            ST_START_3: begin
                scl_low <= 1'b1;
                bit_cnt <= 3'd7;
                state <= ST_TX_SETUP;
            end

            // --------------------------------------------
            // I2C TX BYTE
            // --------------------------------------------

            ST_TX_SETUP: begin
                scl_low <= 1'b1;
                sda_low <= ~tx_byte[bit_cnt];
                state <= ST_TX_RISE;
            end

            ST_TX_RISE: begin
                scl_low <= 1'b0;
                state <= ST_TX_HIGH;
            end

            ST_TX_HIGH: begin
                scl_low <= 1'b0;
                state <= ST_TX_FALL;
            end

            ST_TX_FALL: begin
                scl_low <= 1'b1;

                if (bit_cnt == 3'd0) begin
                    state <= ST_ACK_RELEASE;
                end
                else begin
                    bit_cnt <= bit_cnt - 1'b1;
                    state <= ST_TX_SETUP;
                end
            end

            // --------------------------------------------
            // SLAVE ACK
            // --------------------------------------------

            ST_ACK_RELEASE: begin
                scl_low <= 1'b1;
                sda_low <= 1'b0;
                state <= ST_ACK_RISE;
            end

            ST_ACK_RISE: begin
                scl_low <= 1'b0;
                state <= ST_ACK_WAIT;
            end

            ST_ACK_WAIT: begin
                scl_low <= 1'b0;
                state <= ST_ACK_SAMPLE;
            end

            ST_ACK_SAMPLE: begin
                ack_ok <= (sda_in == 1'b0);
                state <= ST_ACK_FALL;
            end

            ST_ACK_FALL: begin
                scl_low <= 1'b1;
                sda_low <= 1'b0;
                bit_cnt <= 3'd7;
                state <= return_state;
            end

            // --------------------------------------------
            // I2C STOP
            // --------------------------------------------

            ST_STOP_1: begin
                scl_low <= 1'b1;
                sda_low <= 1'b1;
                state <= ST_STOP_2;
            end

            ST_STOP_2: begin
                scl_low <= 1'b0;
                sda_low <= 1'b1;
                state <= ST_STOP_3;
            end

            ST_STOP_3: begin
                scl_low <= 1'b0;
                sda_low <= 1'b0;
                state <= return_state;
            end

            // --------------------------------------------
            // Wait for ADC conversion
            // --------------------------------------------

            ST_ADC_WAIT: begin
                sda_low <= 1'b0;
                scl_low <= 1'b0;

                if (wait_count >= 16'd1000) begin
                    wait_count <= 16'd0;
                    state <= ST_PTR_START;
                end
                else begin
                    wait_count <= wait_count + 1'b1;
                end
            end

            // --------------------------------------------
            // Set pointer to conversion register 0x00
            // --------------------------------------------

            ST_PTR_START: begin
                tx_byte <= ADS_WRITE;
                return_state <= ST_PTR_ADDR;
                state <= ST_START_1;
            end

            ST_PTR_ADDR: begin
                tx_byte <= 8'h00;
                return_state <= ST_PTR_STOP;
                bit_cnt <= 3'd7;
                state <= ST_TX_SETUP;
            end

            ST_PTR_STOP: begin
                return_state <= ST_READ_START;
                state <= ST_STOP_1;
            end

            // --------------------------------------------
            // Read conversion register
            // --------------------------------------------

            ST_READ_START: begin
                tx_byte <= ADS_READ;
                return_state <= ST_READ_ADDR;
                state <= ST_START_1;
            end

            ST_READ_ADDR: begin
                sda_low <= 1'b0;
                scl_low <= 1'b1;
                rx_byte <= 8'd0;
                bit_cnt <= 3'd7;
                rx_return_state <= ST_MASTER_ACK_1;
                state <= ST_RX_SETUP;
            end

            // --------------------------------------------
            // I2C RX BYTE
            // --------------------------------------------

            ST_RX_SETUP: begin
                scl_low <= 1'b1;
                sda_low <= 1'b0;
                state <= ST_RX_RISE;
            end

            ST_RX_RISE: begin
                scl_low <= 1'b0;
                state <= ST_RX_SAMPLE;
            end

            ST_RX_SAMPLE: begin
                scl_low <= 1'b0;
                rx_byte[bit_cnt] <= sda_in;
                state <= ST_RX_FALL;
            end

            ST_RX_FALL: begin
                scl_low <= 1'b1;

                if (bit_cnt == 3'd0) begin
                    state <= rx_return_state;
                end
                else begin
                    bit_cnt <= bit_cnt - 1'b1;
                    state <= ST_RX_SETUP;
                end
            end

            // --------------------------------------------
            // ACK after high byte
            // --------------------------------------------

            ST_MASTER_ACK_1: begin
                adc_high <= rx_byte;
                scl_low <= 1'b1;
                sda_low <= 1'b1;
                state <= ST_MASTER_ACK_2;
            end

            ST_MASTER_ACK_2: begin
                scl_low <= 1'b0;
                sda_low <= 1'b1;
                state <= ST_MASTER_ACK_3;
            end

            ST_MASTER_ACK_3: begin
                scl_low <= 1'b1;
                sda_low <= 1'b1;
                rx_byte <= 8'd0;
                bit_cnt <= 3'd7;
                rx_return_state <= ST_MASTER_NACK_1;
                state <= ST_RX_SETUP;
            end

            // --------------------------------------------
            // Save 16-bit conversion result
            // --------------------------------------------

            ST_MASTER_NACK_1: begin
                case (channel)
                    2'd0:
                        adc_a0 <= {adc_high, rx_byte};

                    2'd1:
                        adc_a1 <= {adc_high, rx_byte};

                    2'd2:
                        adc_a2 <= {adc_high, rx_byte};

                    2'd3:
                        adc_a3 <= {adc_high, rx_byte};
                endcase

                scl_low <= 1'b1;
                sda_low <= 1'b0;
                state <= ST_MASTER_NACK_2;
            end

            ST_MASTER_NACK_2: begin
                scl_low <= 1'b0;
                sda_low <= 1'b0;
                state <= ST_MASTER_NACK_3;
            end

            ST_MASTER_NACK_3: begin
                scl_low <= 1'b1;
                sda_low <= 1'b0;
                state <= ST_READ_STOP;
            end

            ST_READ_STOP: begin
                return_state <= ST_NEXT_CHANNEL;
                state <= ST_STOP_1;
            end

            // --------------------------------------------
            // Next channel
            // ADC1: 0,1,2,3
            // ADC2: 0,1
            // --------------------------------------------

            ST_NEXT_CHANNEL: begin

    if (channel == CHANNEL_COUNT - 1)
        channel <= 2'd0;
    else
        channel <= channel + 1'b1;

    state <= ST_CFG_ADDR;
       end

            default: begin
                sda_low <= 1'b0;
                scl_low <= 1'b0;
                wait_count <= 16'd0;
                state <= ST_POWER_WAIT;
            end

        endcase
    end
end

endmodule
// ============================================================
// INDEPENDENT PIANO / GUITAR VOICE V7
// Reused by all six keys in V8
// ============================================================
module piano_voice_v6 #(
    parameter [31:0] NOTE_INC = 32'd23977432
)(
    input wire clk27m,
    input wire ms_tick,
    input wire sample_tick,
    input wire trigger,
    input wire [7:0] velocity,
    input wire guitar_mode,
    output wire signed [23:0] audio_out
);
// ============================================================
// A. VELOCITY MAPPING
// ============================================================
function [15:0] velocity_to_peak;
    input [7:0] vel;
reg [16:0] temp;
    reg [16:0] delta;
begin
        temp = 0;
        delta = 0;
if (vel == 0) begin
            temp = 0;
end else if (vel < 8'd64) begin
            temp = ({9'd0, vel} << 7) +
                   ({9'd0, vel} << 5);
end else if (vel < 8'd128) begin
            delta = {9'd0, vel} - 17'd64;
            temp = 17'd10240 + (delta << 7);
end else begin
            delta = {9'd0, vel} - 17'd128;
temp = 17'd18432 +
                   (delta << 6) +
                   (delta << 5) +
                   (delta << 4);
        end
if (temp > 17'd32640)
            velocity_to_peak = 16'd32640;
        else
            velocity_to_peak = temp[15:0];
    end
endfunction
// ============================================================
// B. ENVELOPE
// ============================================================
localparam [1:0]
    ENV_IDLE   = 2'd0,
    ENV_ATTACK = 2'd1,
    ENV_DECAY  = 2'd2;
reg active = 0;
reg [1:0] env_state = ENV_IDLE;
reg [15:0] env_level = 0;
reg [15:0] env_peak = 0;
reg [7:0] key_velocity = 0;
reg [2:0] attack_count = 0;
// Latch timbre at note start
reg note_guitar = 0;
wire [15:0] piano_decay_step =
    (key_velocity < 8'd64)
        ? ((env_level >> 9) + 16'd1)
    : (key_velocity < 8'd160)
        ? ((env_level >> 10) + 16'd1)
        : ((env_level >> 11) + 16'd1);
// Faster decay for plucked guitar
wire [15:0] guitar_decay_step =
    (env_level >> 7) + 16'd2;
wire [15:0] decay_step =
    note_guitar ? guitar_decay_step : piano_decay_step;
always @(posedge clk27m) begin
    if (trigger) begin
        note_guitar <= guitar_mode;
active <= 1'b1;
        env_state <= ENV_ATTACK;
env_level <= 0;
        env_peak <= velocity_to_peak(velocity);
        key_velocity <= velocity;
        attack_count <= 0;
    end else if (ms_tick) begin
        case (env_state)
ENV_IDLE: begin
                env_level <= 0;
                active <= 0;
            end
            ENV_ATTACK: begin
if (attack_count <
                    (note_guitar ? 3'd0 : 3'd3)) begin
attack_count <= attack_count + 1'b1;
                    env_level <=
                        env_level + (env_peak >> 2);
end else begin
                    env_level <= env_peak;
                    env_state <= ENV_DECAY;
                end
            end
            ENV_DECAY: begin
if (env_level > decay_step)
                    env_level <= env_level - decay_step;
                else begin
                    env_level <= 0;
                    active <= 0;
                    env_state <= ENV_IDLE;
                end
            end
default: begin
                env_level <= 0;
                active <= 0;
                env_state <= ENV_IDLE;
            end
endcase
    end
end
// ============================================================
// C. TWO DETUNED STRINGS
// ============================================================
localparam [31:0] DETUNE = 32'd6568;
reg [31:0] phase1 = 0;
reg [31:0] phase2 = 0;
always @(posedge clk27m) begin
if (trigger) begin
        phase1 <= 0;
        phase2 <= 0;
    end else if (sample_tick) begin
if (active) begin
            phase1 <= phase1 + NOTE_INC;
            phase2 <= phase2 + NOTE_INC + DETUNE;
        end else begin
            phase1 <= 0;
            phase2 <= 0;
        end
end
end
// ============================================================
// D. SINE ROM
// ============================================================
function signed [8:0] sine64;
    input [5:0] addr;
begin
        case (addr)
0:sine64=0;
             1:sine64=12;
             2:sine64=25;
             3:sine64=37;
             4:sine64=49;
             5:sine64=60;
             6:sine64=71;
             7:sine64=81;
8:sine64=90;
             9:sine64=99;
            10:sine64=106;
            11:sine64=113;
            12:sine64=117;
            13:sine64=122;
            14:sine64=125;
            15:sine64=126;
            16:sine64=127;
17:sine64=126;
            18:sine64=125;
            19:sine64=122;
            20:sine64=117;
            21:sine64=113;
            22:sine64=106;
            23:sine64=99;
24:sine64=90;
            25:sine64=81;
            26:sine64=71;
            27:sine64=60;
            28:sine64=49;
            29:sine64=37;
            30:sine64=25;
            31:sine64=12;
            32:sine64=0;
33:sine64=-12;
            34:sine64=-25;
            35:sine64=-37;
            36:sine64=-49;
            37:sine64=-60;
            38:sine64=-71;
            39:sine64=-81;
40:sine64=-90;
            41:sine64=-99;
            42:sine64=-106;
            43:sine64=-113;
            44:sine64=-117;
            45:sine64=-122;
            46:sine64=-125;
            47:sine64=-126;
            48:sine64=-127;
49:sine64=-126;
            50:sine64=-125;
            51:sine64=-122;
            52:sine64=-117;
            53:sine64=-113;
            54:sine64=-106;
            55:sine64=-99;
56:sine64=-90;
            57:sine64=-81;
            58:sine64=-71;
            59:sine64=-60;
            60:sine64=-49;
            61:sine64=-37;
            62:sine64=-25;
            63:sine64=-12;
            default:sine64=0;
endcase
    end
endfunction
// ============================================================
// E. PIANO / GUITAR WAVEFORMS
// ============================================================
wire signed [8:0] sine1 =
    sine64(phase1[31:26]);
wire signed [8:0] sine2 =
    sine64(phase2[31:26]);
wire signed [8:0] harmonic2 =
    sine64(phase1[30:25]);
wire [31:0] phase3 =
    phase1 + (phase1 << 1);
wire signed [8:0] harmonic3 =
    sine64(phase3[31:26]);
wire signed [15:0] s1 =
    {{7{sine1[8]}}, sine1};
wire signed [15:0] s2 =
    {{7{sine2[8]}}, sine2};
wire signed [15:0] h2 =
    {{7{harmonic2[8]}}, harmonic2};
wire signed [15:0] h3 =
    {{7{harmonic3[8]}}, harmonic3};
// Original V6 piano waveform
wire signed [15:0] string_mix =
    (s1 >>> 1) + (s2 >>> 1);
wire signed [15:0] harmonic_mix =
    (h2 >>> 3) + (h3 >>> 5);
wire signed [32:0] harmonic_product =
    $signed(harmonic_mix) *
    $signed({1'b0, env_level});
wire signed [15:0] harmonic_dynamic =
    harmonic_product >>> 15;
wire signed [15:0] piano_wave =
    string_mix + harmonic_dynamic;
// Guitar waveform: stronger upper harmonics
wire signed [8:0] harmonic4 =
    sine64(phase1[29:24]);
wire signed [15:0] h4 =
    {{7{harmonic4[8]}}, harmonic4};
wire signed [15:0] guitar_wave =
    (s1 >>> 1) +
    (h2 >>> 2) +
    (h3 >>> 3) +
    (h4 >>> 4);
wire signed [15:0] selected_wave =
    note_guitar ? guitar_wave : piano_wave;
// ============================================================
// F. APPLY ENVELOPE
// ============================================================
wire signed [32:0] audio_product =
    $signed(selected_wave) *
    $signed({1'b0, env_level});
wire signed [32:0] audio_scaled =
    audio_product >>> 9;
assign audio_out = audio_scaled[23:0];
endmodule

// ============================================================
// UART RECEIVER
// 27MHz clock, 9600 baud, 8N1
//
// Output:
// data  - received byte
// valid - one clock pulse when byte is complete
// ============================================================

module uart_rx_27m_9600 (
    input  wire clk27m,
    input  wire rx,
    output reg [7:0] data = 8'd0,
    output reg valid = 1'b0
);

// 27,000,000 / 9600 = 2812.5
localparam [11:0] CLKS_PER_BIT = 12'd2813;
localparam [11:0] HALF_BIT     = 12'd1406;

localparam [1:0]
    RX_IDLE  = 2'd0,
    RX_START = 2'd1,
    RX_DATA  = 2'd2,
    RX_STOP  = 2'd3;

// Synchronize asynchronous RX input
reg rx_meta = 1'b1;
reg rx_sync = 1'b1;

always @(posedge clk27m) begin
    rx_meta <= rx;
    rx_sync <= rx_meta;
end

reg [1:0] state = RX_IDLE;
reg [11:0] clk_count = 12'd0;
reg [2:0] bit_index = 3'd0;
reg [7:0] rx_shift = 8'd0;

always @(posedge clk27m) begin

    // Default: valid pulses for one clock only
    valid <= 1'b0;

    case (state)

        // ----------------------------------------
        // Wait for start bit (LOW)
        // ----------------------------------------
        RX_IDLE: begin
            clk_count <= 12'd0;
            bit_index <= 3'd0;

            if (rx_sync == 1'b0)
                state <= RX_START;
        end

        // ----------------------------------------
        // Verify start bit at its center
        // ----------------------------------------
        RX_START: begin

            if (clk_count == HALF_BIT - 1'b1) begin
                clk_count <= 12'd0;

                if (rx_sync == 1'b0)
                    state <= RX_DATA;
                else
                    state <= RX_IDLE;
            end
            else begin
                clk_count <= clk_count + 1'b1;
            end
        end

        // ----------------------------------------
        // Receive 8 data bits, LSB first
        // ----------------------------------------
        RX_DATA: begin

            if (clk_count == CLKS_PER_BIT - 1'b1) begin
                clk_count <= 12'd0;

                rx_shift[bit_index] <= rx_sync;

                if (bit_index == 3'd7) begin
                    bit_index <= 3'd0;
                    state <= RX_STOP;
                end
                else begin
                    bit_index <= bit_index + 1'b1;
                end
            end
            else begin
                clk_count <= clk_count + 1'b1;
            end
        end

        // ----------------------------------------
        // Check stop bit and publish received byte
        // ----------------------------------------
        RX_STOP: begin

            if (clk_count == CLKS_PER_BIT - 1'b1) begin
                clk_count <= 12'd0;

                if (rx_sync == 1'b1) begin
                    data <= rx_shift;
                    valid <= 1'b1;
                end

                state <= RX_IDLE;
            end
            else begin
                clk_count <= clk_count + 1'b1;
            end
        end

        default: begin
            state <= RX_IDLE;
            clk_count <= 12'd0;
            bit_index <= 3'd0;
        end

    endcase
end

endmodule
module tjc_uart_tx (
    input  wire       clk,
    input  wire       send,
    input  wire [7:0] data,
    output reg        tx = 1'b1,
    output reg        busy = 1'b0
);

    localparam integer CLKS_PER_BIT = 2813;

    reg [12:0] clk_count = 0;
    reg [3:0]  bit_count = 0;
    reg [9:0]  shift_reg = 10'h3FF;

    always @(posedge clk) begin
        if (!busy) begin
            tx <= 1'b1;
            clk_count <= 0;
            bit_count <= 0;

            if (send) begin
                shift_reg <= {1'b1, data, 1'b0};
                busy <= 1'b1;
            end
        end else begin
            tx <= shift_reg[0];

            if (clk_count == CLKS_PER_BIT - 1) begin
                clk_count <= 0;
                shift_reg <= {1'b1, shift_reg[9:1]};

                if (bit_count == 9) begin
                    bit_count <= 0;
                    busy <= 1'b0;
                end else begin
                    bit_count <= bit_count + 1'b1;
                end
            end else begin
                clk_count <= clk_count + 1'b1;
            end
        end
    end
endmodule

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
