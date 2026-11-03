module donor_voice #(
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
    input wire [8:0] bend_level,
    input wire key_hold,
    output reg signed [23:0] audio_out = 24'sd0
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
    released ? released_step :
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
wire [34:0] bend_mult = active_inc[25:0] * bend_level;
wire [31:0] bend_full = {9'd0, bend_mult[34:12]};
wire [31:0] bend_inc  = note_guitar ? bend_full : 32'd0;
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
// Guitar waveform: two detuned strings + stronger upper harmonics
wire signed [15:0] guitar_wave =
    (s1 >>> 1) +
    (s2 >>> 1) +
    (h2 >>> 1) +
    (h3 >>> 2);
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
always @(posedge clk27m) audio_out <= audio_scaled[23:0];
endmodule