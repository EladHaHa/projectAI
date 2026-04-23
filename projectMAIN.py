# import streamlit as st

# tab1, tab2 = st.tabs(["Log In", "Home"])

# with tab1:
#   username = st.text_input("Username")
#   password = st.text_input("Password", type="password")
#   age = st.slider("Enter your age",0,100)
#   gender = st.radio("Gender", ["Male", "Female", "Else"])

  
#   test1, test2 = True, True
#   if st.button("Log In"):
#     if username == "" or password == "":
#       st.error("Please enter a username/password")
#       test1 = False
#     if len(password) > 0 and (len(password) < 2 or len(password) > 16):
#       st.warning("Password length must be between 2 and 16")
#       test1 = False
#     if age<16:
#       st.error("Age must be over 16")
#       test2 = False
#     elif test1 == True and test2 == True:  
#       st.success(f"{username} is logged in")
  
# with tab2:
#   st.subheader(f"Welcome, {username}", anchor = False)


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🐍 Snake Game", layout="centered")
st.title("🐍 Snake Game")
st.caption("חצים / WASD לתנועה • Space להשהיה • אסוף כוחות ושדרוגים!")

GAME_HTML = """
<!DOCTYPE html>
<html lang="he">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; font-family: 'Courier New', monospace; color: #e0e0e0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
  #wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 10px; }
  #hud { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
  .stat { display: flex; flex-direction: column; align-items: center; background: #111122; border: 1px solid #2a2a4a; border-radius: 6px; padding: 5px 12px; min-width: 65px; }
  .stat-label { font-size: 9px; color: #5566aa; text-transform: uppercase; letter-spacing: 1px; }
  .stat-value { font-size: 17px; font-weight: bold; color: #88aaff; }
  #coin-disp { color: #ffcc44; font-size: 17px; font-weight: bold; }
  canvas { border: 2px solid #2a2a4a; border-radius: 4px; background: #07070f; box-shadow: 0 0 30px #0044aa33; display: block; }
  #upgrade-panel { background: #0d0d22; border: 1px solid #2a2a5a; border-radius: 8px; padding: 10px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; justify-content: center; }
  .upg-btn { background: #111133; border: 1px solid #445588; color: #99aacc; padding: 5px 9px; border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 11px; text-align: center; transition: all 0.15s; min-width: 85px; }
  .upg-btn:hover:not(:disabled) { background: #1a1a44; border-color: #8899dd; color: #ccdeff; }
  .upg-btn:disabled { opacity: 0.35; cursor: default; }
  .cost { color: #ffcc55; font-size: 10px; }
  #overlay { position: fixed; inset: 0; background: #000000cc; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; z-index: 10; }
  #overlay h1 { font-size: 34px; color: #66aaff; text-shadow: 0 0 20px #3366ff; }
  #overlay p { color: #8888aa; font-size: 13px; text-align: center; }
  .btn { background: #1a1a3a; border: 1px solid #4455aa; color: #88aaff; padding: 10px 28px; border-radius: 6px; font-size: 15px; cursor: pointer; font-family: inherit; transition: all 0.15s; }
  .btn:hover { background: #2a2a5a; border-color: #7788dd; color: #aaccff; }
  #lu { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 9; pointer-events: none; }
  #lu span { font-size: 30px; color: #ffcc44; text-shadow: 0 0 20px #ffaa00; opacity: 0; transition: opacity 0.3s; }
  .hint { font-size: 11px; color: #444466; }
</style>
</head>
<body>
<div id="wrap">
  <div id="hud">
    <div class="stat"><span class="stat-label">ניקוד</span><span class="stat-value" id="score">0</span></div>
    <div class="stat"><span class="stat-label">שיא</span><span class="stat-value" id="hi">0</span></div>
    <div class="stat"><span class="stat-label">שלב</span><span class="stat-value" id="level">1</span></div>
    <div class="stat"><span class="stat-label">מטבעות</span><span id="coin-disp">0</span></div>
  </div>
  <canvas id="c" tabindex="0"></canvas>
  <div id="upgrade-panel">
    <span style="font-size:11px;color:#5566aa">שדרוגים:</span>
    <button class="upg-btn" id="upg-speed"  onclick="buy('speed')">🐇 מהירות<br><span class="cost">50🪙</span></button>
    <button class="upg-btn" id="upg-shield" onclick="buy('shield')">🛡️ מגן<br><span class="cost">80🪙</span></button>
    <button class="upg-btn" id="upg-magnet" onclick="buy('magnet')">🧲 מגנט<br><span class="cost">60🪙</span></button>
    <button class="upg-btn" id="upg-double" onclick="buy('double')">⭐ כפל נק׳<br><span class="cost">70🪙</span></button>
  </div>
  <p class="hint">חצים / WASD לתנועה &bull; Space להשהיה</p>
</div>
<div id="lu"><span id="lu-text"></span></div>
<div id="overlay">
  <h1>🐍 SNAKE</h1>
  <p>חצים / WASD לתנועה<br>אסוף כוחות מיוחדים ושדרג את הנחש!</p>
  <button class="btn" onclick="startGame()">התחל משחק ▶</button>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const GRID = 20, COLS = 24, ROWS = 24;
const CW = COLS * GRID, CH = ROWS * GRID;
canvas.width = CW; canvas.height = CH;

let snake, dir, nextDir, food, powerups, particles, coins, loop;
let score=0, hiScore=0, level=1, coinCount=0;
let paused=false, running=false;
let upgrades = {speed:0, shield:0, magnet:0, double:0};
let activePU = {};

const PU_TYPES = [
  {type:'speed',  emoji:'⚡', color:'#ffee44', dur:5000, msg:'מהיר!'},
  {type:'slow',   emoji:'🧊', color:'#44eeff', dur:6000, msg:'איטי...'},
  {type:'ghost',  emoji:'👻', color:'#cc88ff', dur:4000, msg:'רוח!'},
  {type:'score2x',emoji:'✨', color:'#ffaa22', dur:7000, msg:'x2 ניקוד!'},
  {type:'shrink', emoji:'✂️', color:'#ff8844', dur:0,    msg:'קצר!'},
  {type:'bigcoin',emoji:'🪙', color:'#ffd700', dur:0,    msg:'+20 מטבעות!'},
];
const FOOD_COLS = ['#ff4466','#ff6644','#44ffaa','#44aaff','#ff44cc','#aaff44'];
let fi=0;

const rnd = (a,b) => Math.floor(Math.random()*(b-a+1))+a;
const cell = () => ({x:rnd(1,COLS-2), y:rnd(1,ROWS-2)});
const free = p => !snake.some(s=>s.x===p.x&&s.y===p.y) && !(food&&food.x===p.x&&food.y===p.y);

function startGame(){
  document.getElementById('overlay').style.display='none';
  snake=[{x:12,y:12},{x:11,y:12},{x:10,y:12}];
  dir={x:1,y:0}; nextDir={x:1,y:0};
  food=mkFood(); powerups=[]; particles=[]; coins=[];
  score=0; level=1; coinCount=0; activePU={};
  running=true; paused=false;
  hud(); if(loop) clearInterval(loop); sched();
  canvas.focus();
}

function sched(){
  if(loop) clearInterval(loop);
  let spd = Math.max(50, 130 - upgrades.speed*15 - (activePU.speed?50:0) + (activePU.slow?60:0));
  loop = setInterval(tick, spd);
}

function mkFood(){
  let p; do{p=cell();}while(!free(p));
  fi=(fi+1)%FOOD_COLS.length;
  return {...p, color:FOOD_COLS[fi], pulse:0, val:rnd(1,3)};
}

function spawnPU(){
  if(powerups.length<2 && Math.random()<0.15){
    const t=PU_TYPES[rnd(0,PU_TYPES.length-1)];
    let p; do{p=cell();}while(!free(p));
    powerups.push({...p,...t,born:Date.now()});
  }
}

function spawnCoin(){
  if(coins.length<3 && Math.random()<0.08){
    let p; do{p=cell();}while(!free(p));
    coins.push({...p,born:Date.now(),ttl:8000});
  }
}

function tick(){
  if(paused||!running) return;
  dir={...nextDir};
  const h={x:(snake[0].x+dir.x+COLS)%COLS, y:(snake[0].y+dir.y+ROWS)%ROWS};

  if(!activePU.ghost && snake.some(s=>s.x===h.x&&s.y===h.y)){
    if(upgrades.shield>0&&!activePU.shieldUsed){
      activePU.shieldUsed=true; upgrades.shield--; flash('🛡️ מגן הופעל!');
    } else { die(); return; }
  }

  snake.unshift(h);
  const mag = upgrades.magnet>0 ? 4 : 0;

  if(h.x===food.x&&h.y===food.y){
    let pts = food.val * (activePU.score2x?2:1) * (upgrades.double>0?2:1);
    score+=pts; burst(food.x,food.y,food.color,8);
    food=mkFood(); spawnPU(); spawnCoin();
    if(score>=level*5){ level++; flash('LEVEL '+level+' 🚀'); sched(); }
  } else { snake.pop(); }

  powerups=powerups.filter(pu=>{
    let dx=h.x-pu.x, dy=h.y-pu.y;
    if((dx===0&&dy===0)||(mag&&Math.abs(dx)<=mag&&Math.abs(dy)<=mag)){
      applyPU(pu); burst(pu.x,pu.y,pu.color,12); flash(pu.msg); return false;
    }
    return Date.now()-pu.born<8000;
  });

  coins=coins.filter(c=>{
    let dx=h.x-c.x, dy=h.y-c.y;
    if((dx===0&&dy===0)||(mag&&Math.abs(dx)<=mag&&Math.abs(dy)<=mag)){
      coinCount+=5; hud(); burst(c.x,c.y,'#ffd700',6); return false;
    }
    return Date.now()-c.born<c.ttl;
  });

  let changed=false;
  for(let k of Object.keys(activePU)){
    if(typeof activePU[k]==='number'&&Date.now()>activePU[k]){delete activePU[k];changed=true;}
  }
  if(changed) sched();

  hud(); draw();
}

function applyPU(pu){
  if(pu.type==='speed')   activePU.speed   = Date.now()+pu.dur, sched();
  else if(pu.type==='slow')    activePU.slow    = Date.now()+pu.dur, sched();
  else if(pu.type==='ghost')   activePU.ghost   = Date.now()+pu.dur;
  else if(pu.type==='score2x') activePU.score2x = Date.now()+pu.dur;
  else if(pu.type==='shrink')  { for(let i=0;i<4&&snake.length>3;i++) snake.pop(); }
  else if(pu.type==='bigcoin') { coinCount+=20; }
}

function burst(gx,gy,color,n){
  for(let i=0;i<n;i++)
    particles.push({x:gx*GRID+GRID/2,y:gy*GRID+GRID/2,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*4,color,life:1,sz:rnd(2,5)});
}

function rrect(x,y,w,h,r){
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);
  ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
}

function draw(){
  ctx.clearRect(0,0,CW,CH);
  // grid
  ctx.strokeStyle='#0f0f1f'; ctx.lineWidth=0.5;
  for(let x=0;x<=COLS;x++){ctx.beginPath();ctx.moveTo(x*GRID,0);ctx.lineTo(x*GRID,CH);ctx.stroke();}
  for(let y=0;y<=ROWS;y++){ctx.beginPath();ctx.moveTo(0,y*GRID);ctx.lineTo(CW,y*GRID);ctx.stroke();}

  // food
  food.pulse=(food.pulse||0)+0.08;
  let r=GRID/2-1+Math.sin(food.pulse)*2;
  ctx.save(); ctx.shadowColor=food.color; ctx.shadowBlur=10; ctx.fillStyle=food.color;
  ctx.beginPath(); ctx.arc(food.x*GRID+GRID/2,food.y*GRID+GRID/2,r,0,Math.PI*2); ctx.fill();
  ctx.restore();
  if(food.val>1){
    ctx.fillStyle='#fff'; ctx.font='bold 9px Courier New';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(food.val+'x',food.x*GRID+GRID/2,food.y*GRID+GRID/2);
  }

  // coins
  let now=Date.now();
  coins.forEach(c=>{
    ctx.globalAlpha=Math.min(1,(c.ttl-(now-c.born))/1000);
    ctx.font='14px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('🪙',c.x*GRID+GRID/2,c.y*GRID+GRID/2);
    ctx.globalAlpha=1;
  });

  // powerups
  powerups.forEach(pu=>{
    let age=now-pu.born;
    ctx.globalAlpha=Math.max(0.3,Math.min(1,1-(age-6000)/2000));
    ctx.save(); ctx.shadowColor=pu.color; ctx.shadowBlur=12;
    ctx.fillStyle=pu.color+'33'; ctx.fillRect(pu.x*GRID+1,pu.y*GRID+1,GRID-2,GRID-2);
    ctx.restore();
    ctx.font='13px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(pu.emoji,pu.x*GRID+GRID/2,pu.y*GRID+GRID/2);
    ctx.globalAlpha=1;
  });

  // snake
  const ghost=!!activePU.ghost;
  snake.forEach((seg,i)=>{
    let t=i/snake.length;
    ctx.globalAlpha=ghost?0.45:1;
    if(i===0){
      ctx.save(); ctx.shadowColor=ghost?'#cc88ff':'#44ff88'; ctx.shadowBlur=ghost?14:8;
      ctx.fillStyle=ghost?'#bb66ee':'#22ee66';
      rrect(seg.x*GRID+1,seg.y*GRID+1,GRID-2,GRID-2,4); ctx.fill(); ctx.restore();
      // eyes
      ctx.fillStyle='#001100';
      let ex=dir.x,ey=dir.y;
      ctx.beginPath(); ctx.arc(seg.x*GRID+GRID/2+ex*4+ey*3,seg.y*GRID+GRID/2+ey*4-ex*3,2,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(seg.x*GRID+GRID/2+ex*4-ey*3,seg.y*GRID+GRID/2+ey*4+ex*3,2,0,Math.PI*2); ctx.fill();
    } else {
      let g=Math.floor(120+t*100), b=Math.floor(80+t*60);
      ctx.fillStyle=ghost?`rgba(170,100,220,${0.7-t*0.4})`:`rgb(20,${g},${b})`;
      let pd=1+t*1.5;
      rrect(seg.x*GRID+pd,seg.y*GRID+pd,GRID-pd*2,GRID-pd*2,3); ctx.fill();
    }
    ctx.globalAlpha=1;
  });

  // particles
  particles=particles.filter(p=>{
    p.x+=p.vx; p.y+=p.vy; p.life-=0.05; p.vy+=0.1;
    if(p.life<=0) return false;
    ctx.globalAlpha=p.life; ctx.fillStyle=p.color;
    ctx.fillRect(p.x-p.sz/2,p.y-p.sz/2,p.sz,p.sz);
    ctx.globalAlpha=1; return true;
  });

  // active PU timers on canvas
  let hx=4, hy=CH-4;
  for(let k of ['speed','slow','ghost','score2x']){
    if(activePU[k]&&activePU[k]>now){
      let rem=((activePU[k]-now)/1000).toFixed(1);
      let pu=PU_TYPES.find(p=>p.type===k);
      ctx.fillStyle='#ffffff22'; ctx.fillRect(hx,hy-20,50,20);
      ctx.fillStyle='#fff'; ctx.font='11px Courier New'; ctx.textAlign='left';
      ctx.fillText(pu.emoji+' '+rem+'s',hx+3,hy-6);
      hx+=56;
    }
  }
}

function die(){
  running=false; clearInterval(loop);
  if(score>hiScore) hiScore=score;
  burst(snake[0].x,snake[0].y,'#ff4444',20); draw();
  setTimeout(()=>{
    let ov=document.getElementById('overlay');
    ov.innerHTML=`<h1>💀 GAME OVER</h1><p>ניקוד: ${score}<br>שיא: ${hiScore}</p><button class="btn" onclick="startGame()">שחק שוב ↺</button>`;
    ov.style.display='flex';
  },600);
}

function flash(txt){
  let el=document.getElementById('lu-text');
  el.textContent=txt; el.style.opacity=1;
  setTimeout(()=>el.style.opacity=0,1300);
}

function hud(){
  document.getElementById('score').textContent=score;
  document.getElementById('hi').textContent=hiScore;
  document.getElementById('level').textContent=level;
  document.getElementById('coin-disp').textContent=coinCount;
  document.getElementById('upg-speed').disabled  = coinCount<50;
  document.getElementById('upg-shield').disabled = coinCount<80;
  document.getElementById('upg-magnet').disabled = coinCount<60;
  document.getElementById('upg-double').disabled = coinCount<70;
}

function buy(type){
  const cost={speed:50,shield:80,magnet:60,double:70};
  if(coinCount<cost[type]) return;
  coinCount-=cost[type]; upgrades[type]++;
  hud(); flash('✅ שדרוג הופעל!');
  if(type==='speed') sched();
}

document.addEventListener('keydown',e=>{
  const map={ArrowUp:{x:0,y:-1},ArrowDown:{x:0,y:1},ArrowLeft:{x:-1,y:0},ArrowRight:{x:1,y:0},
             w:{x:0,y:-1},s:{x:0,y:1},a:{x:-1,y:0},d:{x:1,y:0}};
  if(map[e.key]){
    e.preventDefault();
    let nd=map[e.key];
    if(nd.x!==-dir.x||nd.y!==-dir.y) nextDir=nd;
  }
  if(e.key===' '){ e.preventDefault(); if(running){paused=!paused; if(!paused)canvas.focus();} }
});

canvas.focus();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=700, scrolling=False)

