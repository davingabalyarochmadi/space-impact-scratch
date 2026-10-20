import json, hashlib, zipfile, io, math, struct, random, os, base64, re
from pathlib import Path
D=Path(__file__).parent
A=D/'assets'; A.mkdir(exist_ok=True)

def asset(name, body, ext='svg'):
    data=body.encode('utf-8') if isinstance(body,str) else body
    md5=hashlib.md5(data).hexdigest(); filename=f'{md5}.{ext}'
    (A/filename).write_bytes(data)
    return {'name':name,'assetId':md5,'dataFormat':ext,'md5ext':filename},filename

def wrap(w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'

random.seed(31)
stars=''.join(f'<circle cx="{random.randint(8,472)}" cy="{random.randint(10,345)}" r="{random.choice([0.65,0.8,1,1.3])}" fill="{random.choice(["#9adfff","#c5baff","#fff","#5b90c3"])}" opacity="{random.uniform(.35,.9):.2f}"/>' for _ in range(95))
space=wrap(480,360,f'''<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#050820"/><stop offset=".55" stop-color="#111746"/><stop offset="1" stop-color="#060b28"/></linearGradient><radialGradient id="neb"><stop stop-color="#543d99" stop-opacity=".32"/><stop offset="1" stop-color="#543d99" stop-opacity="0"/></radialGradient></defs><rect width="480" height="360" fill="url(#bg)"/><ellipse cx="305" cy="100" rx="210" ry="120" fill="url(#neb)"/>{stars}<path d="M0 332 Q145 294 260 329 T480 312" stroke="#355fb1" stroke-opacity=".3" stroke-width="2" fill="none"/><g opacity=".3" stroke="#36598a"><path d="M0 45H480 M0 315H480"/></g>''')
menu=wrap(480,360,f'''<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#050820"/><stop offset="1" stop-color="#242064"/></linearGradient><linearGradient id="tx" x2="0" y2="1"><stop stop-color="#d8ffff"/><stop offset="1" stop-color="#27baff"/></linearGradient></defs><rect width="480" height="360" fill="url(#bg)"/>{stars}<circle cx="370" cy="105" r="58" fill="#6953b7" opacity=".18"/><text x="240" y="116" text-anchor="middle" fill="url(#tx)" font-size="51" font-family="Arial" font-weight="900" letter-spacing="3">SPACE</text><text x="240" y="161" text-anchor="middle" fill="#f8d671" font-size="50" font-family="Arial" font-weight="900" letter-spacing="4">IMPACT</text><path d="M102 181H378" stroke="#32cfff" stroke-width="2" opacity=".7"/><text x="240" y="222" fill="white" font-size="18" text-anchor="middle" font-family="Arial" font-weight="bold">TEKAN SPASI UNTUK MULAI</text><text x="240" y="254" fill="#b8ceec" font-size="13" text-anchor="middle" font-family="Arial">PANAH / WASD = GERAK</text><text x="240" y="278" fill="#b8ceec" font-size="13" text-anchor="middle" font-family="Arial">SPASI = TEMBAK &#160; | &#160; 3 GELOMBANG + BOS</text><text x="240" y="338" fill="#91a0c6" font-size="12" text-anchor="middle" font-family="Arial">Scratch Edition • dibuat untuk pembelajaran</text>''')
def end_screen(heading,subtitle,color):
 return wrap(480,360,f'''<rect width="480" height="360" fill="#080c25"/>{stars}<rect x="50" y="91" width="380" height="183" rx="16" fill="#171f45" stroke="{color}" stroke-width="3"/><text x="240" y="160" fill="{color}" text-anchor="middle" font-size="43" font-family="Arial" font-weight="900">{heading}</text><text x="240" y="205" fill="#e5f2ff" text-anchor="middle" font-size="18" font-family="Arial">{subtitle}</text><text x="240" y="246" fill="#aab7d9" text-anchor="middle" font-size="14" font-family="Arial">Klik bendera hijau untuk bermain lagi</text>''')
player=wrap(120,82,'''<defs><linearGradient id="h" x2="0" y2="1"><stop stop-color="#e0faff"/><stop offset="1" stop-color="#368fc2"/></linearGradient></defs><path d="M5 40 L37 26 L47 7 L67 23 L98 30 L116 41 L98 52 L67 60 L47 75 L37 56Z" fill="url(#h)" stroke="#0c3c74" stroke-width="4"/><path d="M38 30 L76 40 L38 51 Z" fill="#11718f"/><path d="M65 30 L84 40 L65 50 L50 40Z" fill="#052348" stroke="#37e8ff" stroke-width="2"/><path d="M11 40 L1 32 L1 48Z" fill="#f08a2c"/><path d="M91 36 L107 40 L91 44Z" fill="#f0e7a7"/><path d="M43 11 L57 25 L42 29Z M43 71 L57 57 L42 53Z" fill="#f9c250"/>''')
enemy1=wrap(110,80,'''<defs><linearGradient id="e" x2="0" y2="1"><stop stop-color="#ffb380"/><stop offset="1" stop-color="#cd4262"/></linearGradient></defs><path d="M6 40 L34 19 L66 10 L101 40 L66 70 L34 61Z" fill="url(#e)" stroke="#7d244e" stroke-width="5"/><path d="M14 40L61 27L82 40L61 53Z" fill="#612b67"/><circle cx="57" cy="40" r="12" fill="#f6ec81" stroke="#e74e45" stroke-width="4"/><path d="M70 10L59 28 L89 23 M70 70L59 52 L89 57" fill="none" stroke="#ffc75e" stroke-width="5"/>''')
enemy2=wrap(110,80,'''<path d="M6 40L32 16L64 25L86 10L105 40L86 70L64 55L32 64Z" fill="#ad5dd6" stroke="#4b267f" stroke-width="5"/><path d="M34 40L69 26L81 40L69 54Z" fill="#341e58"/><circle cx="62" cy="40" r="10" fill="#c8ff75"/><path d="M85 14L87 66" stroke="#fe93de" stroke-width="6"/>''')
laser=wrap(56,18,'''<defs><linearGradient id="l"><stop stop-color="#b5ffff"/><stop offset="1" stop-color="#2edaf6" stop-opacity="0"/></linearGradient></defs><ellipse cx="28" cy="9" rx="27" ry="7" fill="#24eefa" opacity=".32"/><path d="M0 5H39L55 9L39 13H0Z" fill="url(#l)"/><circle cx="10" cy="9" r="5" fill="#f9ffff"/>''')
boss=wrap(175,148,'''<defs><linearGradient id="b" x2="0" y2="1"><stop stop-color="#f64d94"/><stop offset="1" stop-color="#5f32a4"/></linearGradient></defs><path d="M3 25L51 30L89 6L123 30L170 25L147 74L171 121L123 118L89 143L51 118L3 121L29 74Z" fill="url(#b)" stroke="#361f74" stroke-width="6"/><path d="M23 76L84 39L147 76L84 109Z" fill="#341d68" stroke="#d066ff" stroke-width="5"/><circle cx="87" cy="73" r="30" fill="#ee739b"/><circle cx="87" cy="73" r="19" fill="#faec9f"/><circle cx="87" cy="73" r="11" fill="#fff"/><path d="M14 41L45 48M14 109L45 101M158 41L127 48M158 109L127 101" stroke="#ffca71" stroke-width="9" stroke-linecap="round"/>''')
plasma=wrap(36,36,'''<circle cx="18" cy="18" r="16" fill="#fc426b" opacity=".3"/><circle cx="18" cy="18" r="11" fill="#ff5687" stroke="#ffca75" stroke-width="3"/><circle cx="18" cy="18" r="5" fill="#fff9c0"/>''')

assets={}
for n,svg in [('menu',menu),('arena',space),('kalah',end_screen('GAME OVER','Pesawatmu hancur!','#ff6c91')),('menang',end_screen('MENANG!','Galaksi berhasil diselamatkan!','#6ffff4')),('player',player),('enemy-red',enemy1),('enemy-purple',enemy2),('laser',laser),('boss',boss),('plasma',plasma)]:
    a,_=asset(n,svg)
    # costume center appropriate
    sizes={'menu':(480,360),'arena':(480,360),'kalah':(480,360),'menang':(480,360),'player':(120,82),'enemy-red':(110,80),'enemy-purple':(110,80),'laser':(56,18),'boss':(175,148),'plasma':(36,36)}
    w,h=sizes[n]; a.update(rotationCenterX=w/2,rotationCenterY=h/2)
    assets[n]=a

# Sound: original synthetic retro arcade sfx, 11025 Hz mono 16bit WAV
def wavsound(name,fn,duration=.14):
    rate=11025; frames=int(duration*rate)
    payload=bytearray()
    for i in range(frames):
        t=i/rate
        val=max(-1,min(1,fn(t,duration)))
        payload.extend(struct.pack('<h',int(val*16000)))
    hdr=b'RIFF'+struct.pack('<I',36+len(payload))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,1,rate,rate*2,2,16)+b'data'+struct.pack('<I',len(payload))
    a,_=asset(name,hdr+payload,'wav'); a.update(rate=rate,sampleCount=frames); return a
sounds={
 'pew':wavsound('Pew',lambda t,d: math.sin(2*math.pi*(850*t-130*t*t))*((1-t/d)**1.7),.11),
 'boom':wavsound('Boom',lambda t,d: (math.sin(2*math.pi*(145*t-90*t*t))+math.sin(2*math.pi*67*t)*.4)*(1-t/d),.22),
 'hit':wavsound('Hit',lambda t,d: math.sin(2*math.pi*(360*t-160*t*t))*(1-t/d),.24),
 'boss':wavsound('Boss alarm',lambda t,d: math.sin(2*math.pi*(220*t+45*math.sin(2*math.pi*7*t)))*((1-t/d)**.5),.34)
}

V={'Skor':'v_score','Nyawa':'v_lives','Gelombang':'v_wave','HP Bos':'v_bosshp','Status':'v_state','Kebal':'v_invuln'}
B={'MULAI':'broadcast_start','BOS':'broadcast_boss','KENA':'broadcast_hit'}
class Graph:
 def __init__(self): self.blocks={}; self.idx=0
 def id(self): self.idx+=1; return f'b{self.idx:04d}'
 def make(self, op, fields=None, inputs=None, shadow=False, top=False,xy=None):
  id=self.id()
  b=dict(opcode=op,next=None,parent=None,inputs={},fields=fields or {},shadow=shadow,topLevel=top)
  if top: b.update(x=xy[0] if xy else 20,y=xy[1] if xy else 20)
  self.blocks[id]=b
  for k,val in (inputs or {}).items(): self.set_input(id,k,val)
  return id
 def set_input(self,id,k,value):
  if isinstance(value,str) and value in self.blocks:
   self.blocks[id]['inputs'][k]=[2,value]; self.blocks[value]['parent']=id
  elif isinstance(value,tuple) and value[0]=='shadow':
   val=value[1];self.blocks[id]['inputs'][k]=[1,val];self.blocks[val]['parent']=id
  else: self.blocks[id]['inputs'][k]=[1,value]
 def link(self,*ids):
  for p,c in zip(ids,ids[1:]): self.blocks[p]['next']=c;self.blocks[c]['parent']=p
  return ids[0] if ids else None
 def attach(self,block,*kids):
  for name,child in kids:
   if child: self.set_input(block,name,child)
  return block
 def sub(self,block,name,start):
  if start:self.set_input(block,name,start)
  else:self.blocks[block]['inputs'][name]=[2,None]
  return block
 def hat(self,kind,name=None,x=20,y=20):
  if kind=='flag':return self.make('event_whenflagclicked',top=True,xy=(x,y))
  if kind=='clone':return self.make('control_start_as_clone',top=True,xy=(x,y))
  if kind=='receive': return self.make('event_whenbroadcastreceived',fields={'BROADCAST_OPTION':[name,B[name]]},top=True,xy=(x,y))
 def num(self,n):return [4,str(n)]
 def string(self,s):return [10,s]
 def data(self,name):return self.make('data_variable',fields={'VARIABLE':[name,V[name]]})
 def unary(self,opcode,key,val):return self.make(opcode, inputs={key:val})
 def binary(self,op,a,b): return self.make(op,inputs={'OPERAND1':a,'OPERAND2':b})
 def gt(self,a,b):return self.binary('operator_gt',a,b)
 def lt(self,a,b):return self.binary('operator_lt',a,b)
 def eq(self,a,b):return self.binary('operator_equals',a,b)
 def and_(self,a,b):return self.binary('operator_and',a,b)
 def or_(self,a,b):return self.binary('operator_or',a,b)
 def not_(self,a):return self.unary('operator_not','OPERAND',a)
 def add(self,a,b):return self.binary('operator_add',a,b)
 def mul(self,a,b):return self.binary('operator_multiply',a,b)
 def random(self,a,b):return self.make('operator_random',inputs={'FROM':self.num(a),'TO':self.num(b)})
 def xpos(self):return self.make('motion_xposition')
 def ypos(self):return self.make('motion_yposition')
 def key(self,k):return self.make('sensing_keypressed',inputs={'KEY_OPTION':('shadow',self.make('sensing_keyoptions',fields={'KEY_OPTION':[k,None]},shadow=True))})
 def touching(self,s):return self.make('sensing_touchingobject',inputs={'TOUCHINGOBJECTMENU':('shadow',self.make('sensing_touchingobjectmenu',fields={'TOUCHINGOBJECTMENU':[s,None]},shadow=True))})
 def change(self,v,n):return self.make('data_changevariableby',fields={'VARIABLE':[v,V[v]]},inputs={'VALUE': n})
 def set(self,v,n):return self.make('data_setvariableto',fields={'VARIABLE':[v,V[v]]},inputs={'VALUE': n})
 def wait(self,n):return self.make('control_wait',inputs={'DURATION':self.num(n)})
 def until(self,cond):return self.make('control_wait_until',inputs={'CONDITION':cond})
 def loop(self,kind,cond=None,sub=None):
  b=self.make(kind,inputs={'CONDITION':cond} if cond else {})
  self.sub(b,'SUBSTACK',sub)
  return b
 def repeat(self,n,sub=None):
  b=self.make('control_repeat',inputs={'TIMES':self.num(n) if isinstance(n,(int,float)) else n})
  self.sub(b,'SUBSTACK',sub)
  return b
 def if_(self,cond,sub):
  b=self.make('control_if',inputs={'CONDITION':cond});self.sub(b,'SUBSTACK',sub);return b
 def ifelse(self,cond,sub,alt):
  b=self.make('control_if_else',inputs={'CONDITION':cond});self.sub(b,'SUBSTACK',sub);self.sub(b,'SUBSTACK2',alt);return b
 def simple(self,op):return self.make(op)
 def goto(self,s):return self.make('motion_goto',inputs={'TO':('shadow',self.make('motion_goto_menu',fields={'TO':[s,None]},shadow=True))})
 def towards(self,s):return self.make('motion_pointtowards',inputs={'TOWARDS':('shadow',self.make('motion_pointtowards_menu',fields={'TOWARDS':[s,None]},shadow=True))})
 def gotoxy(self,x,y):return self.make('motion_gotoxy',inputs={'X':self.num(x) if isinstance(x,(float,int)) else x,'Y':self.num(y) if isinstance(y,(float,int)) else y})
 def mx(self,v):return self.make('motion_changexby',inputs={'DX':self.num(v) if isinstance(v,(float,int)) else v})
 def my(self,v):return self.make('motion_changeyby',inputs={'DY':self.num(v) if isinstance(v,(float,int)) else v})
 def sx(self,v):return self.make('motion_setx',inputs={'X':self.num(v) if isinstance(v,(float,int)) else v})
 def sy(self,v):return self.make('motion_sety',inputs={'Y':self.num(v) if isinstance(v,(float,int)) else v})
 def move(self,v):return self.make('motion_movesteps',inputs={'STEPS':self.num(v) if isinstance(v,(int,float)) else v})
 def point(self,v):return self.make('motion_pointindirection',inputs={'DIRECTION':self.num(v)})
 def size(self,v):return self.make('looks_setsizeto',inputs={'SIZE':self.num(v)})
 def costume(self,name):return self.make('looks_switchcostumeto',inputs={'COSTUME':('shadow',self.make('looks_costume',fields={'COSTUME':[name,None]},shadow=True))})
 def backdrop(self,name):return self.make('looks_switchbackdropto',inputs={'BACKDROP':('shadow',self.make('looks_backdrops',fields={'BACKDROP':[name,None]},shadow=True))})
 def broadcast(self,name):return self.make('event_broadcast',inputs={'BROADCAST_INPUT':('shadow',self.make('event_broadcast_menu',fields={'BROADCAST_OPTION':[name,B[name]]},shadow=True))})
 def clone(self,which='_myself_'):return self.make('control_create_clone_of',inputs={'CLONE_OPTION':('shadow',self.make('control_create_clone_of_menu',fields={'CLONE_OPTION':[which,None]},shadow=True))})
 def sound(self,name):return self.make('sound_play',inputs={'SOUND_MENU':('shadow',self.make('sound_sounds_menu',fields={'SOUND_MENU':[name,None]},shadow=True))})
 def stop(self,option='this script'):return self.make('control_stop',fields={'STOP_OPTION':[option,None]})

# Scratch project game code
stage=Graph();hat=stage.hat('flag',x=30,y=40)
init=[stage.set('Skor',stage.num(0)),stage.set('Nyawa',stage.num(3)),stage.set('Gelombang',stage.num(1)),stage.set('HP Bos',stage.num(0)),stage.set('Status',stage.num(0)),stage.set('Kebal',stage.num(0)),stage.backdrop('menu'),stage.until(stage.key('space')),stage.set('Status',stage.num(1)),stage.backdrop('arena'),stage.broadcast('MULAI')]
check=stage.ifelse(stage.eq(stage.data('Status'),stage.num(2)),stage.link(stage.backdrop('menang'),stage.stop('this script')),stage.if_(stage.eq(stage.data('Status'),stage.num(3)),stage.link(stage.backdrop('kalah'),stage.stop('this script'))))
loop=stage.loop('control_forever',sub=stage.link(check,stage.wait(.08)))
stage.link(hat,*init,loop)

p=Graph();h=p.hat('flag',x=30,y=30);p.link(h,p.simple('looks_hide'))
h=p.hat('receive','MULAI',x=30,y=125)
start=[p.gotoxy(-175,0),p.point(90),p.size(80),p.simple('looks_show')]
up=p.if_(p.or_(p.key('up arrow'),p.key('w')),p.my(6))
down=p.if_(p.or_(p.key('down arrow'),p.key('s')),p.my(-6))
left=p.if_(p.or_(p.key('left arrow'),p.key('a')),p.mx(-6))
right=p.if_(p.or_(p.key('right arrow'),p.key('d')),p.mx(6))
clamps=[p.if_(p.gt(p.ypos(),p.num(145)),p.sy(145)),p.if_(p.lt(p.ypos(),p.num(-145)),p.sy(-145)),p.if_(p.gt(p.xpos(),p.num(-30)),p.sx(-30)),p.if_(p.lt(p.xpos(),p.num(-220)),p.sx(-220))]
body=p.link(up,down,left,right,*clamps,p.wait(.018))
live_loop=p.loop('control_repeat_until',cond=p.not_(p.eq(p.data('Status'),p.num(1))),sub=body)
p.link(h,*start,live_loop,p.simple('looks_hide'))
# fire auto repeat if key space remains held
h=p.hat('receive','MULAI',x=330,y=125)
fire=p.ifelse(p.key('space'),p.link(p.clone('Laser'),p.sound('Pew'),p.wait(.17)),p.wait(.025))
floop=p.loop('control_repeat_until',cond=p.not_(p.eq(p.data('Status'),p.num(1))),sub=fire)
p.link(h,floop)
# hit effect protection against overlapping broadcasts
h=p.hat('receive','KENA',x=670,y=125)
flash=p.repeat(4,p.link(p.simple('looks_hide'),p.wait(.095),p.simple('looks_show'),p.wait(.095)))
hitSeq=p.link(p.set('Kebal',p.num(1)),p.change('Nyawa',p.num(-1)),p.sound('Hit'),flash,p.if_(p.lt(p.data('Nyawa'),p.num(1)),p.set('Status',p.num(3))),p.set('Kebal',p.num(0)))
p.link(h,p.if_(p.and_(p.eq(p.data('Status'),p.num(1)),p.eq(p.data('Kebal'),p.num(0))),hitSeq))

l=Graph();h=l.hat('flag',x=20,y=30);l.link(h,l.simple('looks_hide'))
h=l.hat('clone',x=20,y=135)
laserStop=l.or_(l.or_(l.gt(l.xpos(),l.num(250)),l.touching('Enemy')),l.or_(l.touching('Boss'),l.not_(l.eq(l.data('Status'),l.num(1)))))
laserFly=l.loop('control_repeat_until',cond=laserStop,sub=l.link(l.mx(17),l.wait(.027)))
bossDamage=l.if_(l.and_(l.eq(l.data('Status'),l.num(1)),l.and_(l.gt(l.data('HP Bos'),l.num(0)),l.touching('Boss'))),l.link(l.change('HP Bos',l.num(-1)),l.change('Skor',l.num(5)),l.if_(l.lt(l.data('HP Bos'),l.num(1)),l.set('Status',l.num(2)))))
l.link(h,l.goto('Player'),l.mx(30),l.simple('looks_show'),laserFly,bossDamage,l.simple('control_delete_this_clone'))

e=Graph();h=e.hat('flag',x=20,y=30);e.link(h,e.simple('looks_hide'))
# Wave manager uses base enemy only, because enemy clones are spawned after START
h=e.hat('receive','MULAI',x=20,y=125)
wave_scripts=[]
for wave,num,delay in [(1,9,1.05),(2,13,.85),(3,17,.62)]:
 wave_scripts.append(e.set('Gelombang',e.num(wave)))
 spawn=e.if_(e.eq(e.data('Status'),e.num(1)),e.clone())
 wave_scripts.append(e.repeat(num,e.link(spawn,e.wait(delay))))
 wave_scripts.append(e.wait(.6))
wave_scripts.extend([e.wait(1.4),e.if_(e.eq(e.data('Status'),e.num(1)),e.link(e.set('HP Bos',e.num(28)),e.broadcast('BOS')))])
e.link(h,*wave_scripts)
h=e.hat('clone',x=460,y=125)
# Enemy random spawn, random costume, moving left
rand_costume=e.ifelse(e.lt(e.random(1,2),e.num(2)),e.costume('enemy-red'),e.costume('enemy-purple'))
spawn=[e.gotoxy(246,e.random(-138,138)),e.size(e.random(58,83)),rand_costume,e.simple('looks_show')]
# Enemies die on contact with laser, can hurt player if ship touches them
hitPlayer=e.if_(e.touching('Player'),e.link(e.broadcast('KENA'),e.simple('control_delete_this_clone')))
moveEnemy=e.link(e.mx(-7),hitPlayer,e.wait(.045))
stopEnemy=e.or_(e.or_(e.lt(e.xpos(),e.num(-254)),e.touching('Laser')),e.not_(e.eq(e.data('Status'),e.num(1))))
fly=e.loop('control_repeat_until',cond=stopEnemy,sub=moveEnemy)
addscore=e.if_(e.and_(e.eq(e.data('Status'),e.num(1)),e.touching('Laser')),e.link(e.change('Skor',e.num(10)),e.sound('Boom')))
e.link(h,*spawn,fly,addscore,e.simple('control_delete_this_clone'))

b=Graph();h=b.hat('flag',x=20,y=35);b.link(h,b.simple('looks_hide'))
# boss move vertically, with local variable 'Arah' 1/-1
h=b.hat('receive','BOS',x=20,y=120)
condition=b.or_(b.not_(b.eq(b.data('Status'),b.num(1))),b.lt(b.data('HP Bos'),b.num(1)))
moveBlock=b.link(b.my(b.mul(b.make('data_variable',fields={'VARIABLE':['Arah Bos','boss_dir']}),b.num(3))),b.if_(b.gt(b.ypos(),b.num(107)),b.make('data_setvariableto',fields={'VARIABLE':['Arah Bos','boss_dir']},inputs={'VALUE':b.num(-1)})),b.if_(b.lt(b.ypos(),b.num(-107)),b.make('data_setvariableto',fields={'VARIABLE':['Arah Bos','boss_dir']},inputs={'VALUE':b.num(1)})),b.wait(.035))
boss_loop=b.loop('control_repeat_until',cond=condition,sub=moveBlock)
b.link(h,b.gotoxy(175,0),b.make('data_setvariableto',fields={'VARIABLE':['Arah Bos','boss_dir']},inputs={'VALUE':b.num(1)}),b.size(95),b.simple('looks_show'),b.sound('Boss alarm'),boss_loop,b.simple('looks_hide'))
h=b.hat('receive','BOS',x=390,y=120)
bossShoot=b.loop('control_repeat_until',cond=b.or_(b.not_(b.eq(b.data('Status'),b.num(1))),b.lt(b.data('HP Bos'),b.num(1))),sub=b.link(b.clone('Plasma'),b.wait(.67)))
b.link(h,bossShoot)

pl=Graph();h=pl.hat('flag',x=20,y=30);pl.link(h,pl.simple('looks_hide'))
h=pl.hat('clone',x=20,y=125)
pl_stop=pl.or_(pl.touching('Player'),pl.or_(pl.not_(pl.eq(pl.data('Status'),pl.num(1))),pl.or_(pl.lt(pl.xpos(),pl.num(-245)),pl.or_(pl.gt(pl.ypos(),pl.num(174)),pl.lt(pl.ypos(),pl.num(-174))))))
pl_loop=pl.loop('control_repeat_until',cond=pl_stop,sub=pl.link(pl.move(10),pl.wait(.028)))
pl_hit=pl.if_(pl.and_(pl.eq(pl.data('Status'),pl.num(1)),pl.touching('Player')),pl.broadcast('KENA'))
pl.link(h,pl.goto('Boss'),pl.towards('Player'),pl.simple('looks_show'),pl_loop,pl_hit,pl.simple('control_delete_this_clone'))

def target(name,graph,costumes,soundslist=[],x=0,y=0,size=100,direction=90,visible=False,layer=1,variables=None,stageflag=False):
 t={'isStage':stageflag,'name':name,'variables':variables or {},'lists':{},'broadcasts':B if stageflag else {},'blocks':graph.blocks,'comments':{},'currentCostume':0,'costumes':costumes,'sounds':soundslist,'volume':80,'layerOrder':layer}
 if stageflag: t.update(tempo=60,videoTransparency=50,videoState='on',textToSpeechLanguage=None)
 else:t.update(visible=visible,x=x,y=y,size=size,direction=direction,draggable=False,rotationStyle="don't rotate")
 return t

stagevars={v:[n,0] for n,v in V.items()}
stagevars[V['Nyawa']]=['Nyawa',3]
stagevars[V['Gelombang']]=['Gelombang',1]
bs={'boss_dir':['Arah Bos',1]}
project={'targets':[
 target('Stage',stage,[assets[n] for n in ('menu','arena','kalah','menang')],layer=0,variables=stagevars,stageflag=True),
 target('Player',p,[assets['player']],[sounds['pew'],sounds['hit']],x=-175,visible=False,layer=1),
 target('Laser',l,[assets['laser']],layer=2),
 target('Enemy',e,[assets['enemy-red'],assets['enemy-purple']],[sounds['boom']],layer=3),
 target('Boss',b,[assets['boss']],[sounds['boss']],layer=4,variables=bs),
 target('Plasma',pl,[assets['plasma']],layer=5),
 ],'monitors':[
 {'id':V[n],'mode':'default','opcode':'data_variable','params':{'VARIABLE':n},'spriteName':None,'value':value,'width':0,'height':0,'x':8,'y':y,'visible':True,'sliderMin':0,'sliderMax':100,'isDiscrete':True} for n,value,y in [('Skor',0,5),('Nyawa',3,32),('Gelombang',1,59),('HP Bos',0,86)]
 ],'extensions':[],'meta':{'semver':'3.0.0','vm':'0.2.0','agent':'space-impact-scratch custom Scratch 3 project builder'}}
# Validate reference integrity and input encodings
for t in project['targets']:
 blocks=t['blocks']
 for id,node in blocks.items():
  for k in ('next','parent'):
   if node[k] is not None: assert node[k] in blocks, (t['name'],id,k,node[k])
  for nm,ip in node['inputs'].items():
   if isinstance(ip[1],str): assert ip[1] in blocks, (t['name'],id,nm,ip)
   if node['opcode']=='control_repeat_until' and nm=='CONDITION': assert ip[1] is not None
 for id,b0 in blocks.items():
  assert not b0['topLevel'] or b0['parent'] is None,('toplevel parent',t['name'],id)

raw=json.dumps(project,ensure_ascii=False,separators=(',',':')).encode()
(D/'project.json').write_bytes(raw)
out=D/'Space_Impact.sb3'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.writestr('project.json',raw)
 for path in sorted(A.iterdir()):z.write(path,path.name)

print('PROJECT',len(raw),'BYTES',out.stat().st_size,'BLOCKS',[(t['name'],len(t['blocks'])) for t in project['targets']],'ASSETS',len(list(A.iterdir())))
print('SB3 valid zip',zipfile.ZipFile(out).testzip())