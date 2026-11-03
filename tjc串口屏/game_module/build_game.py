from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\Users\Lenovo\.codex\attachments\fa1aeada-63ff-495f-bbf7-efee85b825a3\已粘贴的文本.txt')

def write(name, content):
    (ROOT / name).write_text(content.rstrip() + '\n', encoding='utf-8')

original = SOURCE.read_text(encoding='utf-8-sig')
write('original_gowin.v', original)
src = original

def replace_once(old, new):
    global src
    assert src.count(old) == 1, (old[:80], src.count(old))
    src = src.replace(old, new)

replace_once('.send (tjc_tx_send),\n    .data (tjc_tx_data),',
             '.send (game_tx_owner ? game_tx_send : tjc_tx_send),\n    .data (game_tx_owner ? game_tx_data : tjc_tx_data),')
replace_once('wire       tjc_tx_busy;', '''wire       tjc_tx_busy;
wire game_tx_owner;
wire game_tx_send;
wire [7:0] game_tx_data;
wire [6:0] game_hit_trigger;
wire [31:0] game_snapshot;
wire game_telemetry_enable;''')
replace_once('       // D0-D6：接收当前音符', '''                // F0: finish game, stop accepting pressure hits.
                8'hF0: begin
                    game_mode <= 1'b0;
                end
       // D0-D6：接收当前音符''')
# Freeze the play-image FSM for the entire game telemetry instruction.
replace_once('    case (tjc_state)', '    if (!game_tx_owner) begin\n    case (tjc_state)')
replace_once('        default: tjc_state <= TJC_SCAN;\n\n    endcase\nend',
             '        default: tjc_state <= TJC_SCAN;\n\n    endcase\n    end\nend')
start = src.index('wire [6:0] game_trigger =')
end = src.index('wire [7:0] demo_velocity', start)
src = src[:start] + '''// Fresh, successfully judged hits are the only game audio triggers.
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

''' + src[end:]
# Single file, no risk of forgetting to add a second RTL file in Gowin.
write('piano_game_complete.v', src + '\n' + (ROOT/'rhythm_game_core.v').read_text(encoding='utf-8'))

# Full Twinkle Twinkle Little Star: A B A, 42 notes / 48 quarter beats.
A = [(0,1),(0,1),(4,1),(4,1),(5,1),(5,1),(4,2),
     (3,1),(3,1),(2,1),(2,1),(1,1),(1,1),(0,2)]
B = [(4,1),(4,1),(3,1),(3,1),(2,1),(2,1),(1,2)] * 2
song = A+B+A
chart = []
tick = 60
for index,(note,duration) in enumerate(song):
    chart.append(dict(index=index, note=note, duration=duration,
                      spawn=tick, slot=index % 4, target=tick+16,
                      window=tick+13, clear=tick+19))
    tick += duration*8
end_tick = tick+20
write('chart.json', json.dumps(dict(timer_ms=50, beat_ms=400, end_tick=end_tick,
                                  notes=chart), ensure_ascii=False, indent=2))

# Existing names reused: va0..3=slot ages, va4=clock, va5..8=x,
# va9=state, va10=end timeout. Added va11..14=note for each slot.
load = '''// game: page initialization event
tm0.en=0
va0.val=0
va1.val=0
va2.val=0
va3.val=0
va4.val=0
va9.val=0
va10.val=0
rx.val=-1
snap.val=0
n0.val=0
n1.val=0
miss.val=0
t0.txt="小星星"
printh A0
'''
write('01_game_load.txt', load)
start_code = ['// m1: touch release event (start / restart)', 'tm0.en=0']
for i in range(4):
    start_code += [f'if(va{i}.val>0)', '{', f'  pos.val=va{i}.val-1',
                   '  pos.val=pos.val*10', '  pos.val=pos.val+28',
                   '  if(pos.val>180)', '  {', '    pos.val=180', '  }',
                   f'  xpic va{i+5}.val,pos.val,50,14,va{i+5}.val,pos.val,18', '}']
for i in range(15):
    start_code += [f'va{i}.val=0']
start_code += ['rx.val=-1','snap.val=0','miss.val=0','n0.val=0','n1.val=0',
               'va9.val=1','tm0.tim=50',
               'printh C1','tm0.en=1']
write('02_start_release.txt', '\n'.join(start_code))

timer = ['// tm0: timer event, tim=50ms. No local variable declarations.',
         '// Four ring slots. Ages 1..19; y clamps at the judgement line.',
         'if(va9.val==1)', '{', '  va4.val=va4.val+1']
for i in range(4):
    timer += [f'  if(va{i}.val>0)', '  {', f'    pos.val=va{i}.val-1',
              '    pos.val=pos.val*10', '    pos.val=pos.val+28',
              '    if(pos.val>180)', '    {', '      pos.val=180', '    }',
              f'    xpic va{i+5}.val,pos.val,50,14,va{i+5}.val,pos.val,18',
              f'    va{i}.val=va{i}.val+1', f'    if(va{i}.val==14)', '    {']
    for note in range(7):
        timer += [f'      if(va{i+11}.val=={note})', '      {',
                  f'        printh D{note}', '      }']
    timer += ['    }', f'    if(va{i}.val>=20)', '    {',
              f'      va{i}.val=0', '    }', '  }']
timer += ['  // Launch chart AFTER advancing old slots: new age is exactly 1.']
for item in chart:
    s = item['slot']
    timer += [f"  if(va4.val=={item['spawn']})", '  {', f'    va{s}.val=1',
              f"    va{s+5}.val={57+53*item['note']}",
              f"    va{s+11}.val={item['note']}", '  }']
for i in range(4):
    timer += [f'  if(va{i}.val>0)', '  {', f'    pos.val=va{i}.val-1',
              '    pos.val=pos.val*10', '    pos.val=pos.val+28',
              '    if(pos.val>180)', '    {', '      pos.val=180', '    }',
              f'    pic va{i+5}.val,pos.val,19', '  }']
timer += [f'  if(va4.val>={end_tick})', '  {', '    printh F0',
          '    va9.val=2', '    va10.val=0', '  }', '}']
# Atomic screen-side read: RX interrupt can update rx between instructions.
# Copy once, then decode only the copy. Avoid multiple-operator expressions.
timer += ['if(rx.val>=0)', '{', '  if(rx.val!=snap.val)', '  {', '  snap.val=rx.val',
          '  n0.val=snap.val%8192', '  n1.val=snap.val/8192',
          '  n1.val=n1.val%64', '  miss.val=snap.val/524288',
          '  miss.val=miss.val%64', '  }', '}']
timer += ['if(va9.val==2)', '{',
          '  va10.val=va10.val+1', '  if(rx.val>=0)', '  {',
          '    kind.val=snap.val/268435456', '    if(kind.val==1)', '    {',
          '      va9.val=3', '      tm0.en=0', '    }', '  }',
          '  if(va9.val==2)', '  {', '    if(va10.val>=40)', '    {',
          '      va9.val=4', '      tm0.en=0', '    }', '  }', '}']
write('03_tm0_timer.txt', '\n'.join(timer))
write('04_back_release.txt', '''// m0: touch release event (back)
tm0.en=0
va9.val=0
printh A0
page main
''')
write('05_game_unload.txt', '''// game: page unload event
tm0.en=0
va9.val=0
printh A0
''')
print(f'Generated {len(song)} notes, {sum(d for _,d in song)} beats, {end_tick*50/1000:.2f}s round, {len(timer)} timer lines.')
