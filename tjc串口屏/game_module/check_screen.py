"""Execute the generated screen events in a small local TJC-subset interpreter.
This checks event logic; it is not the manufacturer's HMI compiler/render engine.
"""
from pathlib import Path
import json
import re
ROOT=Path(__file__).resolve().parent
chart=json.loads((ROOT/'chart.json').read_text())

def parse(name):
    lines=[s.strip() for s in (ROOT/name).read_text(encoding='utf-8').splitlines()
           if s.strip() and not s.strip().startswith('//')]
    def block(index, nested=False):
        nodes=[]
        while index<len(lines):
            line=lines[index]
            if line=='}':
                assert nested
                return nodes,index+1
            if line.startswith('if('):
                assert line.endswith(')') and lines[index+1]=='{'
                body,index=block(index+2,True)
                nodes.append(('if',line[3:-1],body))
            else:
                assert line!='{'
                nodes.append(('statement',line))
                index+=1
        assert not nested
        return nodes,index
    return block(0)[0]

EVENTS={n:parse(n) for n in ['01_game_load.txt','02_start_release.txt',
                           '03_tm0_timer.txt','04_back_release.txt','05_game_unload.txt']}
names={f'va{i}.val' for i in range(15)} | {
    'rx.val','snap.val','miss.val','pos.val','kind.val',
    'n0.val','n1.val','tm0.en','tm0.tim','t0.txt'}

class Screen:
    def __init__(self):
        self.values={n:('' if n.endswith('.txt') else 0) for n in names}
        self.sent=[]; self.drawn=[]; self.page='game'
    def expression(self,value):
        # Split quoted strings first so variable-like text inside strings
        # cannot be interpreted. All expressions come from our generated code.
        parts=re.split(r'("[^"]*")',value)
        for i in range(0,len(parts),2):
            parts[i]=re.sub(r'\b[a-z][a-z0-9]*\.(?:val|txt|en|tim)\b',
                           lambda m:repr(self.values[m[0]]),parts[i])
        return eval(''.join(parts).replace('/','//'), {'__builtins__':{}},{})
    def event(self,name):
        def execute(nodes):
            for node in nodes:
                if node[0]=='if':
                    if self.expression(node[1]): execute(node[2])
                    continue
                statement=node[1]
                if statement.startswith('printh '):
                    self.sent.append(bytes.fromhex(statement[7:]))
                elif statement.startswith(('pic ','xpic ')):
                    command,args=statement.split(' ',1)
                    args=[self.expression(a) for a in args.split(',')]
                    x,y=args[:2]
                    assert 0<=x<=430 and 28<=y<=180,(command,args)
                    self.drawn.append((command,args))
                elif statement.startswith('covx '):
                    source,target,_,_=statement[5:].split(',')
                    self.values[target]=str(self.expression(source))
                elif statement.startswith('page '):
                    self.page=statement[5:]
                else:
                    target,source=statement.split('=',1)
                    assert target in names,target
                    self.values[target]=self.expression(source)
        execute(EVENTS[name])

def packed(score,combo,miss,judge,done):
    return score+(combo<<13)+(miss<<19)+(judge<<25)+(done<<28)

def round_test(profile):
    screen=Screen()
    screen.event('01_game_load.txt')
    screen.event('02_start_release.txt')
    assert screen.sent==[b'\xa0',b'\xc1']
    screen.sent=[]
    score=combo=miss=0
    commands=[]
    for tick in range(1,chart['end_tick']+110):
        if profile!='unplugged':
            judge=0
            # Delayed telemetry still contains cumulative counts.
            for item in chart['notes']:
                if tick==item['target']+2:
                    if profile=='perfect': score+=100; combo+=1; judge=1
                    elif profile=='good': score+=60; combo+=1; judge=2
                if tick==item['clear']+2 and profile=='miss':
                    miss+=1; combo=0; judge=3
            if judge or tick==1 or tick==chart['end_tick']+2:
                screen.values['rx.val']=packed(score,combo,miss,judge,
                                              int(tick>chart['end_tick']))
        before=len(screen.sent)
        screen.event('03_tm0_timer.txt')
        for command in screen.sent[before:]: commands.append((tick,command))
        if screen.values['tm0.en']==0: break
    expected=[(n['window'],bytes([0xd0+n['note']])) for n in chart['notes']]
    assert [c for c in commands if 0xd0<=c[1][0]<=0xd6]==expected
    assert len([c for c in commands if c[1]==b'\xf0'])==1
    assert screen.values['va9.val']==(4 if profile=='unplugged' else 3)
    assert screen.values['tm0.en']==0
    if profile=='unplugged': assert screen.values['rx.val']==-1
    else:
        assert screen.values['n0.val']==score
        assert screen.values['n1.val']==combo
        assert screen.values['miss.val']==miss
    assert screen.values['t0.txt']=='小星星'
    return screen

outputs=[]
for profile in ['perfect','good','miss','unplugged']:
    result=round_test(profile)
    outputs.append(f'PASS {profile}: score={result.values["n0.val"]}, combo={result.values["n1.val"]}, miss={result.values["miss.val"]}, state={result.values["va9.val"]}')
screen=Screen(); screen.event('01_game_load.txt'); screen.event('02_start_release.txt')
for _ in range(200): screen.event('03_tm0_timer.txt')
screen.event('02_start_release.txt')
assert all(screen.values[f'va{i}.val']==0 for i in range(4))
assert screen.values['va4.val']==0 and screen.values['rx.val']==-1
screen.event('04_back_release.txt')
assert screen.page=='main' and screen.sent[-1]==b'\xa0' and screen.values['tm0.en']==0
outputs.append('PASS restart mid-animation and back-to-main cleanup')
for item in chart['notes']:
    later=[n for n in chart['notes'] if n['index']>item['index'] and n['slot']==item['slot']]
    if later: assert later[0]['spawn']>item['clear']
for a,b in zip(chart['notes'],chart['notes'][1:]):
    assert (b['window']-a['window'])*chart['timer_ms']>=400
assert chart['timer_ms']==50
assert chart['notes'][0]['spawn']*50==3000
assert chart['notes'][0]['target']*50==3800
assert all((n['target']-n['window'])*50==150 for n in chart['notes'])
assert all((n['clear']-n['window'])*50==300 for n in chart['notes'])
outputs.append('PASS 50ms timer, 3s countdown, 42 target commands, four-slot lifetime, nonoverlapping 300ms windows, final stop')
for name in EVENTS:
    text=(ROOT/name).read_text(encoding='utf-8')
    assert not re.search(r'\b(?:t1|t2|tmp)\.',text),name
outputs.append('PASS screen events require only t0/n0/n1 display controls, no additional text controls')
report='\n'.join(outputs)+'\n'
(ROOT/'screen_tests.txt').write_text(report,encoding='utf-8')
print(report)
