
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
// Audio: external PCM5102, standard I2S, A11/B11/D11
//
// CST constraints are configured separately.
// ============================================================

module ads1115_pressure_test (
    input  wire clk27m,
    input  wire key_s0,
    input wire key_bend,
    input wire key_oct_down,
    input wire key_oct_up,
    input wire esp_rx,
    output wire esp_tx,
    inout wire oled_scl,
    inout wire oled_sda,

    inout  wire adc1_sda,
    inout  wire adc1_scl,

    inout  wire adc2_sda,
    inout  wire adc2_scl,

    output wire HP_DIN,
    output wire HP_WS,
    output wire HP_BCK,
    output wire DAC_BCK,
    output wire DAC_DIN,
    output wire DAC_LRCK,
    output wire PA_EN,

    // TJC UART
    input  wire uart_rx,
    output wire uart_tx,

    // Play mode LED
    output wire play_led,
    output wire note_do_out,
    output wire note_re_out,
    output wire note_mi_out,
    output wire note_fa_out,
    output wire note_sol_out,
    output wire note_la_out,
    output wire note_si_out
);

assign PA_EN = 1'b0; // Board amplifier disabled; use external PCM5102 line output.

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
wire [31:0] ear_command;wire ear_command_valid;
wire ear_active,ear_trigger,ear_sound;wire [2:0] ear_note;
wire [47:0] ear_event,ear_frame;wire ear_event_valid,ear_valid,ear_ready;
wire ear_prepare=ear_command_valid && ear_command[31:24]==8'h40;
reg ear_prepare_last=0;
always @(posedge clk27m)ear_prepare_last<=ear_prepare;
wire ear_screen_abort=tjc_rx_valid && ((tjc_rx_data>=8'hA0 && tjc_rx_data<=8'hA2) ||
 (tjc_rx_data>=8'hB1 && tjc_rx_data<=8'hB3) || tjc_rx_data==8'hC1);
ear_training ear_core(.clk(clk27m),.ms_tick(ms_tick),.command(ear_command),.command_valid(ear_command_valid),
 .abort((app_mute_remote && !ear_prepare_last) || ear_screen_abort || (ear_command_valid && ear_command[31:24]==8'h03)),.key_trigger(trigger),.key_down(key_down),
 .active(ear_active),.tone_trigger(ear_trigger),.tone_note(ear_note),.sound(ear_sound),
 .event_frame(ear_event),.event_valid(ear_event_valid));
game_event_queue ear_events(.clk(clk27m),.event_frame(ear_event),.event_valid(ear_event_valid),
 .frame(ear_frame),.valid(ear_valid),.ready(ear_ready));
wire [47:0] merged_frame=game_frame_valid?game_frame:ear_frame;
wire merged_ready;
assign game_frame_ready=merged_ready;
assign ear_ready=merged_ready && !game_frame_valid;
wire [47:0] game_event;
wire game_event_valid;
wire [47:0] game_frame;
wire game_frame_valid,game_frame_ready;
game_event_queue game_events(.clk(clk27m),.event_frame(game_event),.event_valid(game_event_valid),
 .frame(game_frame),.valid(game_frame_valid),.ready(game_frame_ready));

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
reg play_mode = 1'b1;

// 音游模式
reg game_mode = 1'b0;
// 当前音游目标音符
// 0 Do 1 Re 2 Mi 3 Fa 4 Sol 5 La 6 Si
reg [2:0] target_note = 3'd0;
// TJC屏幕虚拟琴键状态
reg [6:0] touch_key_down = 7'd0;

// TJC虚拟琴键按下触发脉冲
reg [6:0] touch_trigger = 7'd0;
// 示范模式
reg demo_mode = 1'b0;
reg [1:0] demo_song = 2'd0;
reg demo_restart = 1'b0;
// The screen page does not disable the physical instrument.
// Demonstration and rhythm-game modes retain exclusive local sound control.
wire physical_play_enable = !demo_mode && !game_mode && !ear_active;


    // 接收 TJC 指令
  always @(posedge clk27m) begin
    demo_restart <= 1'b0;
    touch_trigger <= 7'd0;
    if(ear_prepare)begin demo_mode<=0;game_mode<=0;touch_key_down<=0;end

    // 离开自由演奏模式后清除虚拟琴键状态
    if (!play_mode)
        touch_key_down <= 7'd0;
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
// =======================================
// TJC虚拟琴键按下：E0~E6
// =======================================
8'hE0, 8'hE1, 8'hE2, 8'hE3,
8'hE4, 8'hE5, 8'hE6: begin

    if (play_mode) begin

        touch_key_down[tjc_rx_data[2:0]] <= 1'b1;

        // 只在刚按下时发声一次
        if (!touch_key_down[tjc_rx_data[2:0]])
            touch_trigger[tjc_rx_data[2:0]] <= 1'b1;

    end
end

// =======================================
// TJC虚拟琴键弹起：E8~EE
// =======================================
8'hE8, 8'hE9, 8'hEA, 8'hEB,
8'hEC, 8'hED, 8'hEE: begin

    touch_key_down[tjc_rx_data[2:0]] <= 1'b0;

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
    if(app_voice_set) guitar_mode <= app_voice_value;
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

wire [6:0] display_key_down =
    key_down | touch_key_down;

wire [4:0] tjc_target_picture =
    5'd4 + {tjc_key_index, 1'b0}
    - {4'd0, display_key_down[tjc_key_index]};

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
            display_key_down[tjc_key_index]) begin

            tjc_active_key <= tjc_key_index;

            tjc_active_pressed <=
                display_key_down[tjc_key_index];

            tjc_picture <= tjc_target_picture;

            tjc_char_index <= 4'd0;

            tjc_state <= TJC_SEND;

        end
        else begin

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
// Duration unit = 175ms: eighth note=1, quarter note=2, half note=4
// ============================================================

reg [6:0] demo_trigger = 7'd0;
reg [5:0] demo_index = 6'd0;
reg [12:0] demo_elapsed = 13'd0;
reg [12:0] demo_duration = 13'd0;

wire [7:0] demo_step;
wire [2:0] demo_note;

// [7]: octave down, [6:3]: duration in 175ms units, [2:0]: pitch class.
function [7:0] song_step;
    input [1:0] song; input [5:0] index;
    begin
        song_step = {1'b0,4'd2,3'd7};
        case (song)
            2'd0: begin // Twinkle, 42 notes
                case (index)
                    0: song_step = {1'b0,4'd2,3'd0}; // C4
                    1: song_step = {1'b0,4'd2,3'd0}; // C4
                    2: song_step = {1'b0,4'd2,3'd4}; // G4
                    3: song_step = {1'b0,4'd2,3'd4}; // G4
                    4: song_step = {1'b0,4'd2,3'd5}; // A4
                    5: song_step = {1'b0,4'd2,3'd5}; // A4
                    6: song_step = {1'b0,4'd4,3'd4}; // G4
                    7: song_step = {1'b0,4'd2,3'd3}; // F4
                    8: song_step = {1'b0,4'd2,3'd3}; // F4
                    9: song_step = {1'b0,4'd2,3'd2}; // E4
                    10: song_step = {1'b0,4'd2,3'd2}; // E4
                    11: song_step = {1'b0,4'd2,3'd1}; // D4
                    12: song_step = {1'b0,4'd2,3'd1}; // D4
                    13: song_step = {1'b0,4'd4,3'd0}; // C4
                    14: song_step = {1'b0,4'd2,3'd4}; // G4
                    15: song_step = {1'b0,4'd2,3'd4}; // G4
                    16: song_step = {1'b0,4'd2,3'd3}; // F4
                    17: song_step = {1'b0,4'd2,3'd3}; // F4
                    18: song_step = {1'b0,4'd2,3'd2}; // E4
                    19: song_step = {1'b0,4'd2,3'd2}; // E4
                    20: song_step = {1'b0,4'd4,3'd1}; // D4
                    21: song_step = {1'b0,4'd2,3'd4}; // G4
                    22: song_step = {1'b0,4'd2,3'd4}; // G4
                    23: song_step = {1'b0,4'd2,3'd3}; // F4
                    24: song_step = {1'b0,4'd2,3'd3}; // F4
                    25: song_step = {1'b0,4'd2,3'd2}; // E4
                    26: song_step = {1'b0,4'd2,3'd2}; // E4
                    27: song_step = {1'b0,4'd4,3'd1}; // D4
                    28: song_step = {1'b0,4'd2,3'd0}; // C4
                    29: song_step = {1'b0,4'd2,3'd0}; // C4
                    30: song_step = {1'b0,4'd2,3'd4}; // G4
                    31: song_step = {1'b0,4'd2,3'd4}; // G4
                    32: song_step = {1'b0,4'd2,3'd5}; // A4
                    33: song_step = {1'b0,4'd2,3'd5}; // A4
                    34: song_step = {1'b0,4'd4,3'd4}; // G4
                    35: song_step = {1'b0,4'd2,3'd3}; // F4
                    36: song_step = {1'b0,4'd2,3'd3}; // F4
                    37: song_step = {1'b0,4'd2,3'd2}; // E4
                    38: song_step = {1'b0,4'd2,3'd2}; // E4
                    39: song_step = {1'b0,4'd2,3'd1}; // D4
                    40: song_step = {1'b0,4'd2,3'd1}; // D4
                    41: song_step = {1'b0,4'd4,3'd0}; // C4
                    default: song_step = {1'b0,4'd2,3'd7};
                endcase
            end
            2'd1: begin // Frere Jacques, 32 notes
                case (index)
                    0: song_step = {1'b0,4'd2,3'd0}; // C4
                    1: song_step = {1'b0,4'd2,3'd1}; // D4
                    2: song_step = {1'b0,4'd2,3'd2}; // E4
                    3: song_step = {1'b0,4'd2,3'd0}; // C4
                    4: song_step = {1'b0,4'd2,3'd0}; // C4
                    5: song_step = {1'b0,4'd2,3'd1}; // D4
                    6: song_step = {1'b0,4'd2,3'd2}; // E4
                    7: song_step = {1'b0,4'd2,3'd0}; // C4
                    8: song_step = {1'b0,4'd2,3'd2}; // E4
                    9: song_step = {1'b0,4'd2,3'd3}; // F4
                    10: song_step = {1'b0,4'd4,3'd4}; // G4
                    11: song_step = {1'b0,4'd2,3'd2}; // E4
                    12: song_step = {1'b0,4'd2,3'd3}; // F4
                    13: song_step = {1'b0,4'd4,3'd4}; // G4
                    14: song_step = {1'b0,4'd1,3'd4}; // G4
                    15: song_step = {1'b0,4'd1,3'd5}; // A4
                    16: song_step = {1'b0,4'd1,3'd4}; // G4
                    17: song_step = {1'b0,4'd1,3'd3}; // F4
                    18: song_step = {1'b0,4'd2,3'd2}; // E4
                    19: song_step = {1'b0,4'd2,3'd0}; // C4
                    20: song_step = {1'b0,4'd1,3'd4}; // G4
                    21: song_step = {1'b0,4'd1,3'd5}; // A4
                    22: song_step = {1'b0,4'd1,3'd4}; // G4
                    23: song_step = {1'b0,4'd1,3'd3}; // F4
                    24: song_step = {1'b0,4'd2,3'd2}; // E4
                    25: song_step = {1'b0,4'd2,3'd0}; // C4
                    26: song_step = {1'b0,4'd2,3'd0}; // C4
                    27: song_step = {1'b1,4'd2,3'd4}; // G3
                    28: song_step = {1'b0,4'd4,3'd0}; // C4
                    29: song_step = {1'b0,4'd2,3'd0}; // C4
                    30: song_step = {1'b1,4'd2,3'd4}; // G3
                    31: song_step = {1'b0,4'd4,3'd0}; // C4
                    default: song_step = {1'b0,4'd2,3'd7};
                endcase
            end
            2'd2: begin // Ode to Joy, 62 notes
                case (index)
                    0: song_step = {1'b0,4'd2,3'd2}; // E4
                    1: song_step = {1'b0,4'd2,3'd2}; // E4
                    2: song_step = {1'b0,4'd2,3'd3}; // F4
                    3: song_step = {1'b0,4'd2,3'd4}; // G4
                    4: song_step = {1'b0,4'd2,3'd4}; // G4
                    5: song_step = {1'b0,4'd2,3'd3}; // F4
                    6: song_step = {1'b0,4'd2,3'd2}; // E4
                    7: song_step = {1'b0,4'd2,3'd1}; // D4
                    8: song_step = {1'b0,4'd2,3'd0}; // C4
                    9: song_step = {1'b0,4'd2,3'd0}; // C4
                    10: song_step = {1'b0,4'd2,3'd1}; // D4
                    11: song_step = {1'b0,4'd2,3'd2}; // E4
                    12: song_step = {1'b0,4'd3,3'd2}; // E4
                    13: song_step = {1'b0,4'd1,3'd1}; // D4
                    14: song_step = {1'b0,4'd4,3'd1}; // D4
                    15: song_step = {1'b0,4'd2,3'd2}; // E4
                    16: song_step = {1'b0,4'd2,3'd2}; // E4
                    17: song_step = {1'b0,4'd2,3'd3}; // F4
                    18: song_step = {1'b0,4'd2,3'd4}; // G4
                    19: song_step = {1'b0,4'd2,3'd4}; // G4
                    20: song_step = {1'b0,4'd2,3'd3}; // F4
                    21: song_step = {1'b0,4'd2,3'd2}; // E4
                    22: song_step = {1'b0,4'd2,3'd1}; // D4
                    23: song_step = {1'b0,4'd2,3'd0}; // C4
                    24: song_step = {1'b0,4'd2,3'd0}; // C4
                    25: song_step = {1'b0,4'd2,3'd1}; // D4
                    26: song_step = {1'b0,4'd2,3'd2}; // E4
                    27: song_step = {1'b0,4'd3,3'd1}; // D4
                    28: song_step = {1'b0,4'd1,3'd0}; // C4
                    29: song_step = {1'b0,4'd4,3'd0}; // C4
                    30: song_step = {1'b0,4'd2,3'd1}; // D4
                    31: song_step = {1'b0,4'd2,3'd1}; // D4
                    32: song_step = {1'b0,4'd2,3'd2}; // E4
                    33: song_step = {1'b0,4'd2,3'd0}; // C4
                    34: song_step = {1'b0,4'd2,3'd1}; // D4
                    35: song_step = {1'b0,4'd1,3'd2}; // E4
                    36: song_step = {1'b0,4'd1,3'd3}; // F4
                    37: song_step = {1'b0,4'd2,3'd2}; // E4
                    38: song_step = {1'b0,4'd2,3'd0}; // C4
                    39: song_step = {1'b0,4'd2,3'd1}; // D4
                    40: song_step = {1'b0,4'd1,3'd2}; // E4
                    41: song_step = {1'b0,4'd1,3'd3}; // F4
                    42: song_step = {1'b0,4'd2,3'd2}; // E4
                    43: song_step = {1'b0,4'd2,3'd1}; // D4
                    44: song_step = {1'b0,4'd2,3'd0}; // C4
                    45: song_step = {1'b0,4'd2,3'd1}; // D4
                    46: song_step = {1'b0,4'd4,3'd4}; // G4
                    47: song_step = {1'b0,4'd2,3'd2}; // E4
                    48: song_step = {1'b0,4'd2,3'd2}; // E4
                    49: song_step = {1'b0,4'd2,3'd3}; // F4
                    50: song_step = {1'b0,4'd2,3'd4}; // G4
                    51: song_step = {1'b0,4'd2,3'd4}; // G4
                    52: song_step = {1'b0,4'd2,3'd3}; // F4
                    53: song_step = {1'b0,4'd2,3'd2}; // E4
                    54: song_step = {1'b0,4'd2,3'd1}; // D4
                    55: song_step = {1'b0,4'd2,3'd0}; // C4
                    56: song_step = {1'b0,4'd2,3'd0}; // C4
                    57: song_step = {1'b0,4'd2,3'd1}; // D4
                    58: song_step = {1'b0,4'd2,3'd2}; // E4
                    59: song_step = {1'b0,4'd3,3'd1}; // D4
                    60: song_step = {1'b0,4'd1,3'd0}; // C4
                    61: song_step = {1'b0,4'd4,3'd0}; // C4
                    default: song_step = {1'b0,4'd2,3'd7};
                endcase
            end
            default: song_step = {1'b0,4'd2,3'd7};
        endcase
    end
endfunction



wire [5:0] demo_last_index =
    (demo_song == 2'd0) ? 6'd41 :
    (demo_song == 2'd1) ? 6'd31 : 6'd61;

// 当前曲谱音符
assign demo_step = song_step(demo_song, demo_index);
assign demo_note = demo_step[2:0];

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
                {9'd0, demo_step[6:3]} * 13'd175;

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
assign audio_do=synth_active[8] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[8*24+:24]) : 24'sd0;

wire signed [23:0] audio_re;
assign audio_re=synth_active[9] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[9*24+:24]) : 24'sd0;

wire signed [23:0] audio_mi;
assign audio_mi=synth_active[10] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[10*24+:24]) : 24'sd0;

wire signed [23:0] audio_fa;
assign audio_fa=synth_active[11] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[11*24+:24]) : 24'sd0;

wire signed [23:0] audio_sol;
assign audio_sol=synth_active[12] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[12*24+:24]) : 24'sd0;

wire signed [23:0] audio_la;
assign audio_la=synth_active[13] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[13*24+:24]) : 24'sd0;

wire signed [23:0] audio_si;
assign audio_si=synth_active[14] && !(app_mute_all | demo_mode | game_mode) ? $signed(synth_audio[14*24+:24]) : 24'sd0;

// Game audio accepts judged hits only; physical playing also works at home.
// Demonstration audio uses the dedicated demo_voice below.
wire [6:0] voice_trigger =
    demo_mode ? 7'd0 :
    game_mode ? 7'd0 :
    physical_play_enable ? (trigger | touch_trigger) : 7'd0;

rhythm_game_core game_judge (
    .clk(clk27m), .ms_tick(ms_tick),
    .rx_valid(tjc_rx_valid || ear_prepare), .rx_data(ear_prepare ? 8'hA0 : tjc_rx_data),
    .key_trigger(trigger), .hit_trigger(game_hit_trigger),
    .snapshot(game_snapshot), .telemetry_enable(game_telemetry_enable),
    .event_frame(game_event),.event_valid(game_event_valid)
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


// Dedicated App channel. TJC uart_rx/uart_tx above are unchanged.
wire [223:0] app_physical_inc, app_remote_inc;
wire [55:0] app_remote_velocity;
wire [6:0] app_remote_trigger, app_remote_release, app_remote_held;
wire app_mute_all, app_mute_remote, app_voice_set, app_voice_value;
wire [15:0] app_gain;
reg [6:0] app_record_keys = 7'd0;
always @(posedge clk27m) begin
 if(!physical_play_enable || app_mute_all || octave_mute_physical) app_record_keys <= 7'd0;
 else app_record_keys <= (app_record_keys | trigger | touch_trigger) & (key_down | touch_key_down);
end
wire [6:0] app_live_keys = app_record_keys;
wire [55:0] app_pressures = {
 touch_key_down[6]?8'd110:pressure_si, touch_key_down[5]?8'd110:pressure_la,
 touch_key_down[4]?8'd110:pressure_sol,touch_key_down[3]?8'd110:pressure_fa,
 touch_key_down[2]?8'd110:pressure_mi,touch_key_down[1]?8'd110:pressure_re,
 touch_key_down[0]?8'd110:pressure_do};
wire octave_down_pulse,octave_up_pulse,octave_mute_physical;
octave_buttons octave_keys(.clk(clk27m),.ms_tick(ms_tick),
 .key_down_n(key_oct_down),.key_up_n(key_oct_up),
 .down_pulse(octave_down_pulse),.up_pulse(octave_up_pulse));
dpg_bridge app_bridge (
 .clk(clk27m),.ms_tick(ms_tick),.esp_rx(esp_rx),.esp_tx(esp_tx),
 .game_frame(merged_frame),.game_valid(game_frame_valid || ear_valid),.game_ready(merged_ready),
 .ear_command(ear_command),.ear_command_valid(ear_command_valid),
 .ear_busy(ear_active),.actual_voice(guitar_mode),.remote_held(app_remote_held),
 .octave_down(octave_down_pulse),.octave_up(octave_up_pulse),.physical_mute(octave_mute_physical),
 .live_keys(app_live_keys),.pressures(app_pressures),.physical_inc(app_physical_inc),
 .remote_inc(app_remote_inc),.remote_velocity(app_remote_velocity),
 .remote_trigger(app_remote_trigger),.remote_release(app_remote_release),
 .mute_all(app_mute_all),.mute_remote(app_mute_remote),
 .voice_set(app_voice_set),.voice_value(app_voice_value),.gain_q15(app_gain));
// 15 envelopes/phase states, one shared 4-lane / 32-partial synthesizer.
wire [479:0] synth_phase,synth_phase2,synth_inc,synth_base_inc;
// key_bend 消抖（5ms）
reg bend_meta   = 1'b1;
reg bend_sync   = 1'b1;
reg bend_stable = 1'b1;
reg [17:0] bend_count = 18'd0;
localparam [17:0] BEND_DEBOUNCE = 18'd135000;

always @(posedge clk27m) begin
    bend_meta <= key_bend;
    bend_sync <= bend_meta;
    if (bend_sync == bend_stable)
        bend_count <= 18'd0;
    else if (bend_count == BEND_DEBOUNCE - 1'b1) begin
        bend_count  <= 18'd0;
        bend_stable <= bend_sync;
    end
    else
        bend_count <= bend_count + 1'b1;
end

// 推弦深度斜坡计数器（0~511）
localparam [8:0] BEND_MAX       = 9'd511;
localparam [3:0] BEND_UP_STEP   = 4'd4;
localparam [3:0] BEND_DOWN_STEP = 4'd8;

reg [8:0] bend_level = 9'd0;

always @(posedge clk27m) begin
    if (ms_tick) begin
        if (!bend_stable) begin
            if (bend_level < BEND_MAX - BEND_UP_STEP)
                bend_level <= bend_level + BEND_UP_STEP;
            else
                bend_level <= BEND_MAX;
        end
        else begin
            if (bend_level > BEND_DOWN_STEP)
                bend_level <= bend_level - BEND_DOWN_STEP;
            else
                bend_level <= 9'd0;
        end
    end
end

// 记录最后按下的音（Si 优先）
reg [2:0] last_key = 3'd0;

always @(posedge clk27m) begin
    if      (trigger[6]) last_key <= 3'd7;
    else if (trigger[5]) last_key <= 3'd6;
    else if (trigger[4]) last_key <= 3'd5;
    else if (trigger[3]) last_key <= 3'd4;
    else if (trigger[2]) last_key <= 3'd3;
    else if (trigger[1]) last_key <= 3'd2;
    else if (trigger[0]) last_key <= 3'd1;
end

// One shared, full-width bend multiplier, evaluated continuously.
// Unlike the donor's [25:0] truncation this also handles remapped high notes.
reg [31:0] bend_base=0;
always @* begin
 case(last_key)
  1:bend_base=synth_base_inc[8*32+:32];2:bend_base=synth_base_inc[9*32+:32];
  3:bend_base=synth_base_inc[10*32+:32];4:bend_base=synth_base_inc[11*32+:32];
  5:bend_base=synth_base_inc[12*32+:32];6:bend_base=synth_base_inc[13*32+:32];
  7:bend_base=synth_base_inc[14*32+:32];default:bend_base=0;
 endcase
end
reg [40:0] bend_product=0;
always @(posedge clk27m)bend_product<=bend_base*bend_level;
wire [31:0] bend_delta={3'd0,bend_product[40:12]};

wire [239:0] synth_env;
wire [14:0] synth_guitar,synth_active;
wire [359:0] synth_audio;
wire synth_busy,synth_overrun,synth_done;
additive32_bank bank32(.clk(clk27m),.sample_tick(sample_tick),
 .phase_bus(synth_phase),.phase2_bus(synth_phase2),.inc_bus(synth_inc),.env_bus(synth_env),
 .guitar_bus(synth_guitar),.active_bus(synth_active),.audio_bus(synth_audio),
 .busy(synth_busy),.overrun(synth_overrun),.frame_done(synth_done));

wire signed [23:0] app_audio[0:6];
genvar av;
generate for(av=0;av<7;av=av+1)begin:app_voices
 additive32_voice voice (
 .clk27m(clk27m),.ms_tick(ms_tick),.sample_tick(sample_tick),
 .trigger(app_remote_trigger[av]),.velocity(app_remote_velocity[av*8+:8]),
 .guitar_mode(guitar_mode),.note_inc(app_remote_inc[av*32+:32]),
 .note_release(app_remote_release[av]),.mute(app_mute_all|app_mute_remote),.bend_offset(32'd0),.key_hold(app_remote_held[av]),.phase_out(synth_phase[(av)*32+:32]),.phase2_out(synth_phase2[(av)*32+:32]),.base_inc_out(synth_base_inc[(av)*32+:32]),.inc_out(synth_inc[(av)*32+:32]),.env_out(synth_env[(av)*16+:16]),.guitar_out(synth_guitar[av]),.active_out(synth_active[av]));
assign app_audio[av]=synth_active[av] && !(app_mute_all|app_mute_remote) ? $signed(synth_audio[av*24+:24]) : 24'sd0;
end endgenerate

// An independent monophonic demonstration voice: old notes cannot accumulate
// across the seven physical voices. The next note restarts a short attack.
function [31:0] demo_note_increment;
    input [2:0] note;
    begin
        case(note)
            0:demo_note_increment=INC_C4; 1:demo_note_increment=INC_D4;
            2:demo_note_increment=INC_E4; 3:demo_note_increment=INC_F4;
            4:demo_note_increment=INC_G4; 5:demo_note_increment=INC_A4;
            6:demo_note_increment=INC_B4; default:demo_note_increment=0;
        endcase
    end
endfunction
wire [31:0] demo_pitch = demo_step[7] ?
    (demo_note_increment(demo_note) >> 1) : demo_note_increment(demo_note);
wire signed [23:0] audio_demo;
assign audio_demo=synth_active[7] && !shared_voice_mute ? $signed(synth_audio[7*24+:24]) : 24'sd0;

// Shared monophonic demo/game voice: the exact score-producing hit pulse
// directly triggers the voice, with no dependency on the duplicated game_mode.
wire game_hit_audio = |game_hit_trigger;
reg [2:0] game_audio_note;
always @* begin
 case(game_hit_trigger)
  7'b0000001:game_audio_note=0;7'b0000010:game_audio_note=1;
  7'b0000100:game_audio_note=2;7'b0001000:game_audio_note=3;
  7'b0010000:game_audio_note=4;7'b0100000:game_audio_note=5;
  7'b1000000:game_audio_note=6;default:game_audio_note=0;
 endcase
end
wire game_audio_reset = tjc_rx_valid &&
 ((tjc_rx_data==8'hC1)||(tjc_rx_data==8'hF0)||
  (tjc_rx_data==8'hA0)||(tjc_rx_data==8'hA1)||(tjc_rx_data==8'hA2)||
  (tjc_rx_data==8'hB1)||(tjc_rx_data==8'hB2)||(tjc_rx_data==8'hB3));
wire shared_voice_mute = ear_active ? !ear_sound : game_mode ? game_audio_reset :
 (app_mute_all | !demo_mode | demo_restart | game_audio_reset);
additive32_voice demo_voice (
 .clk27m(clk27m),.ms_tick(ms_tick),.sample_tick(sample_tick),
 .trigger(ear_trigger | (!ear_active && (game_hit_audio | (demo_mode && (|demo_trigger))))),.velocity(8'd110),
 .guitar_mode(guitar_mode),
 .note_inc(ear_active ? demo_note_increment(ear_note) : (game_hit_audio ? demo_note_increment(game_audio_note) : demo_pitch)),
 .note_release(1'b0),.mute(shared_voice_mute),.bend_offset(32'd0),.key_hold(1'b0),.phase_out(synth_phase[(7)*32+:32]),.phase2_out(synth_phase2[(7)*32+:32]),.base_inc_out(synth_base_inc[(7)*32+:32]),.inc_out(synth_inc[(7)*32+:32]),.env_out(synth_env[(7)*16+:16]),.guitar_out(synth_guitar[7]),.active_out(synth_active[7])
);

wire [7:0] demo_velocity = 8'd110;
additive32_voice #(.NOTE_INC(INC_C4)) voice_do (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[0]),
.velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[0] ? 8'd110 : pressure_do)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_C4:app_physical_inc[0+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd1)?bend_delta:32'd0),.key_hold(key_down[0]),.phase_out(synth_phase[(8)*32+:32]),.phase2_out(synth_phase2[(8)*32+:32]),.base_inc_out(synth_base_inc[(8)*32+:32]),.inc_out(synth_inc[(8)*32+:32]),.env_out(synth_env[(8)*16+:16]),.guitar_out(synth_guitar[8]),.active_out(synth_active[8])
);

additive32_voice #(.NOTE_INC(INC_D4)) voice_re (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[1]),
    .velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[1] ? 8'd110 : pressure_re)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_D4:app_physical_inc[32+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd2)?bend_delta:32'd0),.key_hold(key_down[1]),.phase_out(synth_phase[(9)*32+:32]),.phase2_out(synth_phase2[(9)*32+:32]),.base_inc_out(synth_base_inc[(9)*32+:32]),.inc_out(synth_inc[(9)*32+:32]),.env_out(synth_env[(9)*16+:16]),.guitar_out(synth_guitar[9]),.active_out(synth_active[9])
);

additive32_voice #(.NOTE_INC(INC_E4)) voice_mi (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[2]),
    .velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[2] ? 8'd110 : pressure_mi)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_E4:app_physical_inc[64+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd3)?bend_delta:32'd0),.key_hold(key_down[2]),.phase_out(synth_phase[(10)*32+:32]),.phase2_out(synth_phase2[(10)*32+:32]),.base_inc_out(synth_base_inc[(10)*32+:32]),.inc_out(synth_inc[(10)*32+:32]),.env_out(synth_env[(10)*16+:16]),.guitar_out(synth_guitar[10]),.active_out(synth_active[10])
);

additive32_voice #(.NOTE_INC(INC_F4)) voice_fa (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[3]),
.velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[3] ? 8'd110 : pressure_fa)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_F4:app_physical_inc[96+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd4)?bend_delta:32'd0),.key_hold(key_down[3]),.phase_out(synth_phase[(11)*32+:32]),.phase2_out(synth_phase2[(11)*32+:32]),.base_inc_out(synth_base_inc[(11)*32+:32]),.inc_out(synth_inc[(11)*32+:32]),.env_out(synth_env[(11)*16+:16]),.guitar_out(synth_guitar[11]),.active_out(synth_active[11])
);

additive32_voice #(.NOTE_INC(INC_G4)) voice_sol (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
   .trigger(voice_trigger[4]),
.velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[4] ? 8'd110 : pressure_sol)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_G4:app_physical_inc[128+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd5)?bend_delta:32'd0),.key_hold(key_down[4]),.phase_out(synth_phase[(12)*32+:32]),.phase2_out(synth_phase2[(12)*32+:32]),.base_inc_out(synth_base_inc[(12)*32+:32]),.inc_out(synth_inc[(12)*32+:32]),.env_out(synth_env[(12)*16+:16]),.guitar_out(synth_guitar[12]),.active_out(synth_active[12])
);

additive32_voice #(.NOTE_INC(INC_A4)) voice_la (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
    .trigger(voice_trigger[5]),
.velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[5] ? 8'd110 : pressure_la)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_A4:app_physical_inc[160+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd6)?bend_delta:32'd0),.key_hold(key_down[5]),.phase_out(synth_phase[(13)*32+:32]),.phase2_out(synth_phase2[(13)*32+:32]),.base_inc_out(synth_base_inc[(13)*32+:32]),.inc_out(synth_inc[(13)*32+:32]),.env_out(synth_env[(13)*16+:16]),.guitar_out(synth_guitar[13]),.active_out(synth_active[13])
);

additive32_voice #(.NOTE_INC(INC_B4)) voice_si (
    .clk27m(clk27m),
    .ms_tick(ms_tick),
    .sample_tick(sample_tick),
   .trigger(voice_trigger[6]),
.velocity((demo_mode || game_mode) ? demo_velocity : (touch_trigger[6] ? 8'd110 : pressure_si)),
    .guitar_mode(guitar_mode),
    .note_inc((demo_mode|game_mode)?INC_B4:app_physical_inc[192+:32]),
    .note_release(1'b0),.mute(app_mute_all | demo_mode | game_mode | octave_mute_physical),
    .bend_offset((last_key==3'd7)?bend_delta:32'd0),.key_hold(key_down[6]),.phase_out(synth_phase[(14)*32+:32]),.phase2_out(synth_phase2[(14)*32+:32]),.base_inc_out(synth_base_inc[(14)*32+:32]),.inc_out(synth_inc[(14)*32+:32]),.env_out(synth_env[(14)*16+:16]),.guitar_out(synth_guitar[14]),.active_out(synth_active[14])
);
// ============================================================
// SIX-VOICE MIXER
// Sign extension before summation; clip to 16-bit range.
// ============================================================

// SEVEN-VOICE MIXER
wire signed [27:0] mix_raw =
    $signed({{4{audio_do[23]}},  audio_do})  +
    $signed({{4{audio_re[23]}},  audio_re})  +
    $signed({{4{audio_mi[23]}},  audio_mi})  +
    $signed({{4{audio_fa[23]}},  audio_fa})  +
    $signed({{4{audio_sol[23]}}, audio_sol}) +
    $signed({{4{audio_la[23]}},  audio_la})  +
    $signed({{4{audio_si[23]}},  audio_si}) +
    $signed({{4{audio_demo[23]}}, audio_demo}) +
    $signed({{4{app_audio[0][23]}},app_audio[0]}) +
    $signed({{4{app_audio[1][23]}},app_audio[1]}) +
    $signed({{4{app_audio[2][23]}},app_audio[2]}) +
    $signed({{4{app_audio[3][23]}},app_audio[3]}) +
    $signed({{4{app_audio[4][23]}},app_audio[4]}) +
    $signed({{4{app_audio[5][23]}},app_audio[5]}) +
    $signed({{4{app_audio[6][23]}},app_audio[6]});

reg signed [27:0] mix_sum = 28'sd0;
always @(posedge clk27m) mix_sum <= mix_raw;
wire [15:0] effective_gain = game_mode ? 16'd32768 : app_gain;
wire signed [44:0] app_scaled_mix = $signed(mix_sum) * $signed({1'b0,effective_gain});
wire signed [27:0] app_volume_mix = app_scaled_mix >>> 15;
wire signed [15:0] audio_sample =
    (app_volume_mix > 28'sd30000)
        ? 16'sd30000
    : (app_volume_mix < -28'sd30000)
        ? -16'sd30000
    : app_volume_mix[15:0];

// ============================================================
// OLED reads the final 16-bit PCM stream; it never gates the audio path.
// Default: SSD1306 128x64, 7-bit address 0x3C. SH1106 panels: set SH1106 to 1.
oled_audio_scope #(.I2C_ADDR(7'h3c), .SH1106(0)) oled_scope (
    .clk(clk27m), .sample_tick(sample_tick), .pcm(audio_sample),
    .oled_scl(oled_scl), .oled_sda(oled_sda), .online(), .frames()
);

// External PCM5102: 16-bit PCM in 32-bit I2S channel words (zero low bits).
// 27MHz / 9 = 3MHz BCK; 64 BCK per stereo frame = 46875Hz, unchanged synth rate.
// Legacy board DAC pins are held low and the old amplifier is disabled.
assign HP_DIN=1'b0;
assign HP_WS=1'b0;
assign HP_BCK=1'b0;
pcm5102_i2s_tx external_dac(
 .clk(clk27m),.pcm_left(audio_sample),.pcm_right(audio_sample),
 .bck(DAC_BCK),.din(DAC_DIN),.lrck(DAC_LRCK)
);
// Seven note-class outputs. Bits 0..6 = Do Re Mi Fa Sol La Si.
// Serialized scan shares one pitch decoder across the existing 15 voices.
// Use base_inc, not bend-modified inc: bends keep the original note class.
// Fold octave by retaining the leading 12 bits of the base DDS increment.
// These 15 mantissas cover every natural note in the existing MIDI21..108 ROM,
// including the C4..B4 tuning constants and low-octave demonstration aliases.
// Sharps/flats in that ROM do not match. Pitch bends use the original base note.
function [6:0] note_out_decode;
 input [31:0] phase_inc;
 reg [11:0] mantissa;
 begin
  if(|phase_inc[31:29])mantissa=0;
  else if(phase_inc[28])mantissa=phase_inc[28:17];
  else if(phase_inc[27])mantissa=phase_inc[27:16];
  else if(phase_inc[26])mantissa=phase_inc[26:15];
  else if(phase_inc[25])mantissa=phase_inc[25:14];
  else if(phase_inc[24])mantissa=phase_inc[24:13];
  else if(phase_inc[23])mantissa=phase_inc[23:12];
  else if(phase_inc[22])mantissa=phase_inc[22:11];
  else if(phase_inc[21])mantissa=phase_inc[21:10];
  else mantissa=0;
  case(mantissa)
   12'd2926:note_out_decode=7'b0000001;
   12'd3284:note_out_decode=7'b0000010;
   12'd3686,12'd3687:note_out_decode=7'b0000100;
   12'd3906:note_out_decode=7'b0001000;
   12'd2192,12'd2193:note_out_decode=7'b0010000;
   12'd2460,12'd2461,12'd2462,12'd2463:note_out_decode=7'b0100000;
   12'd2761,12'd2762,12'd2763,12'd2764:note_out_decode=7'b1000000;
   default:note_out_decode=7'd0;
  endcase
 end
endfunction

reg [3:0] note_out_index = 4'd0;
reg [6:0] note_out_accum = 7'd0;
reg [6:0] note_out_state = 7'd0;
wire [31:0] note_out_pitch = synth_base_inc[note_out_index*32 +: 32];
wire [14:0] note_out_env_present;
genvar note_env_index;
generate for(note_env_index=0;note_env_index<15;note_env_index=note_env_index+1)begin:note_env_presence
 assign note_out_env_present[note_env_index]=|synth_env[note_env_index*16 +: 16];
end endgenerate
wire note_out_env=note_out_env_present[note_out_index];

// Match the mute conditions used by the actual audio mixer.
wire note_out_path_enabled =
    (note_out_index < 4'd7) ? !(app_mute_all | app_mute_remote) :
    (note_out_index == 4'd7) ? !shared_voice_mute :
                             !(app_mute_all | demo_mode | game_mode);
wire [6:0] note_out_current =
    (synth_active[note_out_index] && note_out_env &&
     note_out_path_enabled) ? note_out_decode(note_out_pitch) : 7'd0;

always @(posedge clk27m) begin
    if (note_out_index == 4'd14) begin
        note_out_state <= note_out_accum | note_out_current;
        note_out_accum <= 7'd0;
        note_out_index <= 4'd0;
    end else begin
        note_out_accum <= note_out_accum | note_out_current;
        note_out_index <= note_out_index + 1'b1;
    end
end

// Global volume zero forces every output low immediately.
assign {note_si_out, note_la_out, note_sol_out, note_fa_out,
        note_mi_out, note_re_out, note_do_out} =
       (effective_gain != 16'd0) ? note_out_state : 7'd0;

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
module additive32_voice #(
    parameter [31:0] NOTE_INC = 32'd23977432
)(
    input wire clk27m,
    input wire ms_tick,
    input wire sample_tick,
    input wire trigger,
    input wire [7:0] velocity,
    input wire guitar_mode,
    input wire [31:0] note_inc,
    input wire note_release,
    input wire mute,
    input wire [31:0] bend_offset,
    input wire key_hold,
    output wire [31:0] phase_out, phase2_out, inc_out, base_inc_out,
    output wire [15:0] env_out,
    output wire guitar_out, active_out
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
localparam [2:0]
    ENV_IDLE    = 3'd0,
    ENV_ATTACK  = 3'd1,
    ENV_DECAY   = 3'd2,
    ENV_SUSTAIN = 3'd3,
    ENV_RELEASE = 3'd4;
reg active = 0;
reg [2:0] env_state = ENV_IDLE;
reg [15:0] env_level = 0;
reg [15:0] env_peak = 0;
reg [7:0] key_velocity = 0;
reg [2:0] attack_count = 0;
// Latch timbre at note start
reg note_guitar = 0;
reg released = 0;
reg [31:0] active_inc = NOTE_INC;
always @(posedge clk27m) if(trigger) active_inc <= note_inc;

// 钢琴衰减步长（保留原有分档）
wire [15:0] piano_decay_step =
    (key_velocity < 8'd64)
        ? ((env_level >> 9) + 16'd1)
    : (key_velocity < 8'd160)
        ? ((env_level >> 10) + 16'd1)
        : ((env_level >> 11) + 16'd1);
// 吉他弹拨衰减步长（更快）
wire [15:0] guitar_tail_step =
    (env_level >> 7) + 16'd2;
// 松开后缓慢衰减，保留尾音（app/非按住路径复用）
wire [15:0] released_step =
    (env_level >> 8) + 16'd4;
wire [15:0] decay_step =
    (released && !note_guitar) ? released_step :
    (note_guitar ? guitar_tail_step : piano_decay_step);

// 吉他按住保持：衰减到 sustain 电平后维持
wire [15:0] guitar_sustain =
    env_peak - (env_peak >> 1) - (env_peak >> 4);
wire [15:0] guitar_decay_step =
    (env_peak >> 4) + 16'd1;
wire [15:0] guitar_release_step =
    (env_level >> 7) + 16'd2;
always @(posedge clk27m) begin
    if (mute) begin
        active <= 0;
        env_state <= ENV_IDLE;
        env_level <= 0;
        released <= 0;
    end
    else if (note_release) begin
        released <= 1'b1;
    end
    else if (trigger) begin
        released <= 0;
        note_guitar <= guitar_mode;
        active <= 1'b1;
        env_state <= ENV_ATTACK;
        env_level <= 0;
        env_peak <= velocity_to_peak(velocity);
        key_velocity <= velocity;
        attack_count <= 0;
    end
    else if (ms_tick) begin
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
                // 吉他按住：衰减到 sustain 电平后进入保持
                if (note_guitar && key_hold) begin
                    if (env_level > guitar_sustain + guitar_decay_step)
                        env_level <= env_level - guitar_decay_step;
                    else begin
                        env_level <= guitar_sustain;
                        env_state <= ENV_SUSTAIN;
                    end
                end
                else if (env_level > decay_step)
                    env_level <= env_level - decay_step;
                else begin
                    env_level <= 0;
                    active <= 0;
                    env_state <= ENV_IDLE;
                end
            end
            ENV_SUSTAIN: begin
                // 松开或收到 release 才进入释放
                if (!key_hold || released)
                    env_state <= ENV_RELEASE;
            end
            ENV_RELEASE: begin
                if (env_level > guitar_release_step)
                    env_level <= env_level - guitar_release_step;
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
localparam [31:0] DETUNE_PIANO  = 32'd6568;
localparam [31:0] DETUNE_GUITAR = 32'd150000;
reg [31:0] phase1 = 0;
reg [31:0] phase2 = 0;
// 推弦偏移：bend_level 满偏(511)时 ≈ active_inc/8（推高约1全音）
wire [31:0] bend_inc=note_guitar?bend_offset:32'd0;
always @(posedge clk27m) begin
if (trigger) begin
        phase1 <= 0;
        phase2 <= 0;
    end else if (sample_tick) begin
if (active) begin
            phase1 <= phase1 + active_inc + bend_inc;
            phase2 <= phase2 + active_inc + (note_guitar ? DETUNE_GUITAR : DETUNE_PIANO) + bend_inc;
        end else begin
            phase1 <= 0;
            phase2 <= 0;
        end
end
end

assign phase_out=phase1;assign phase2_out=phase2;
assign base_inc_out=active_inc;assign inc_out=active_inc+bend_inc;
assign env_out=env_level;assign guitar_out=note_guitar;assign active_out=active;
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
    output wire telemetry_enable,
    output reg [47:0] event_frame=0,
    output reg event_valid=0
);
    reg [15:0] event_index=0,session_id=0;
    reg finish_pending=0;
    reg [7:0] finish_status=0;
    function [47:0] game_packet;
      input [7:0] c;input [15:0] index;input [7:0] value;
      reg [7:0] check;
      begin check=~(c+index[15:8]+index[7:0]+value);
        game_packet={8'hAA,c,index,value,check};end
    endfunction
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
        event_valid<=0;
        if(finish_pending)begin
          event_valid<=1;event_frame<=game_packet(8'hA5,event_index,finish_status);
          finish_pending<=0;
        end
        if (rx_valid && rx_data == 8'hC1) begin
            event_index<=0;session_id<=session_id+1'b1;finish_pending<=0;
            event_valid<=1;event_frame<=game_packet(8'hA0,session_id+16'd1,8'd1);
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
            if(active)begin
              if(armed)begin
                event_valid<=1;event_frame<=game_packet(8'hA3,event_index,8'hFF);
                finish_pending<=1;finish_status<=1;
              end else begin event_valid<=1;event_frame<=game_packet(8'hA5,event_index,8'd1);end
            end
            active <= 1'b0;
            done <= 1'b0;
            armed <= 1'b0;
        end else if (rx_valid && rx_data == 8'hF0) begin
            // F0 ends a round; a pending target is consumed as a miss.
            if (active) begin
                if (armed) begin
                    event_valid<=1;event_frame<=game_packet(8'hA3,event_index,8'hFF);
                    finish_pending<=1;finish_status<=0;
                    if (misses != 6'd63) misses <= misses + 1'b1;
                    combo <= 6'd0;
                    judgement <= 3'd3;
                end
                if(!armed)begin event_valid<=1;event_frame<=game_packet(8'hA5,event_index,8'd0);end
                active <= 1'b0;
                done <= 1'b1;
                armed <= 1'b0;
            end
        end else if (active && rx_valid &&
                     rx_data >= 8'hD0 && rx_data <= 8'hD6) begin
            // Chart guarantees >=400ms between targets; do not silently
            // lose an unfinished target if a malformed chart replaces it.
            event_index<=event_index+1'b1;
            if(event_index==16'hFFFF)begin event_valid<=1;event_frame<=game_packet(8'hAF,0,1);end
            if (armed) begin
                event_valid<=1;event_frame<=game_packet(8'hA3,event_index,8'hFF);
                if (misses != 6'd63) misses <= misses + 1'b1;
                combo <= 6'd0;
                judgement <= 3'd3;
            end
            note <= rx_data[2:0];
            age_ms <= 9'd0;
            armed <= 1'b1;
        end else if (active && armed) begin
            if (ms_tick && age_ms == 9'd299) begin
                event_valid<=1;event_frame<=game_packet(8'hA3,event_index,8'hFF);
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
                    event_valid<=1;
                    event_frame<=game_packet((age_ms>=75 && age_ms<225)?8'hA1:8'hA2,event_index,age_ms[8:1]);
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
                    event_valid<=1;event_frame<=game_packet(8'hA4,event_index,age_ms[8:1]);
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


// Two active-low buttons, two-flop synchronizer, 20 real millisecond debounce.
module octave_buttons(input clk,input ms_tick,input key_down_n,input key_up_n,
 output reg down_pulse=0,output reg up_pulse=0);
 reg[1:0] meta=2'b11,sync=2'b11,stable=2'b11;
 reg[4:0] count_down=0,count_up=0;
 always @(posedge clk)begin
  meta<={key_up_n,key_down_n};sync<=meta;down_pulse<=0;up_pulse<=0;
  if(ms_tick)begin
   if(sync[0]===stable[0])count_down<=0;
   else if(count_down==19)begin count_down<=0;stable[0]<=sync[0];if(sync[0]===1'b0)down_pulse<=1;end
   else count_down<=count_down+1'b1;
   if(sync[1]===stable[1])count_up<=0;
   else if(count_up==19)begin count_up<=0;stable[1]<=sync[1];if(sync[1]===1'b0)up_pulse<=1;end
   else count_up<=count_up+1'b1;
  end
 end
endmodule
