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

st.set_page_config(page_title="🎮 Arcade Games", layout="wide")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="he">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap');
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:#f0f4ff;font-family:'Nunito',sans-serif;color:#1a1a2e;min-height:100vh;}
  #nav{display:flex;gap:8px;padding:12px 16px;background:#fff;border-bottom:2px solid #e8eaf6;justify-content:center;flex-wrap:wrap;}
  .nav-btn{padding:8px 22px;border-radius:50px;border:2px solid #c5cae9;background:#fff;font-family:inherit;font-size:14px;font-weight:700;cursor:pointer;transition:all .2s;color:#3949ab;}
  .nav-btn:hover{background:#e8eaf6;}
  .nav-btn.active{background:#3949ab;color:#fff;border-color:#3949ab;}
  .screen{display:none;flex-direction:column;align-items:center;padding:16px 8px;gap:10px;}
  .screen.show{display:flex;}
  .hud{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}
  .stat{background:#fff;border:2px solid #e8eaf6;border-radius:12px;padding:6px 16px;text-align:center;min-width:72px;}
  .stat-label{font-size:9px;color:#9fa8da;text-transform:uppercase;letter-spacing:1px;font-weight:700;}
  .stat-val{font-size:20px;font-weight:900;color:#3949ab;}
  .coin-val{color:#f9a825;}
  canvas{border-radius:12px;display:block;border:3px solid #c5cae9;background:#fff;}
  .upg-panel{background:#fff;border:2px solid #e8eaf6;border-radius:12px;padding:10px 14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;}
  .upg-btn{background:#f3f4ff;border:2px solid #c5cae9;color:#3949ab;padding:5px 10px;border-radius:8px;cursor:pointer;font-family:inherit;font-size:11px;font-weight:700;text-align:center;transition:all .15s;min-width:82px;}
  .upg-btn:hover:not(:disabled){background:#e8eaf6;border-color:#9fa8da;}
  .upg-btn:disabled{opacity:.35;cursor:default;}
  .cost{color:#f9a825;font-size:10px;}
  .overlay{position:fixed;inset:0;background:rgba(57,73,171,.85);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;z-index:20;}
  .overlay h1{font-size:38px;color:#fff;font-weight:900;}
  .overlay p{color:#c5cae9;font-size:14px;text-align:center;max-width:320px;line-height:1.6;}
  .start-btn{background:#fff;color:#3949ab;border:none;padding:12px 36px;border-radius:50px;font-size:16px;font-weight:900;font-family:inherit;cursor:pointer;transition:all .15s;}
  .start-btn:hover{background:#e8eaf6;transform:scale(1.04);}
  #flash{position:fixed;top:28%;left:50%;transform:translateX(-50%);font-size:26px;font-weight:900;color:#3949ab;pointer-events:none;opacity:0;transition:opacity .3s;z-index:30;background:#ffffffcc;padding:6px 18px;border-radius:50px;}
  #tetris-wrap{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;justify-content:center;}
  #tetris-side{background:#fff;border:2px solid #e8eaf6;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:10px;min-width:100px;}
  #next-label{font-size:11px;color:#9fa8da;font-weight:700;text-transform:uppercase;text-align:center;}
  .hint{font-size:11px;color:#9fa8da;font-weight:600;}
</style>
</head>
<body>

<div id="nav">
  <button class="nav-btn active" onclick="showGame('snake')">🐍 Snake</button>
  <button class="nav-btn" onclick="showGame('tetris')">🧩 Tetris</button>
  <button class="nav-btn" onclick="showGame('breakout')">🧱 Breakout</button>
</div>

<!-- SNAKE -->
<div id="screen-snake" class="screen show">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div class="stat-val" id="s-score">0</div></div>
    <div class="stat"><div class="stat-label">שיא</div><div class="stat-val" id="s-hi">0</div></div>
    <div class="stat"><div class="stat-label">שלב</div><div class="stat-val" id="s-level">1</div></div>
    <div class="stat"><div class="stat-label">מטבעות</div><div class="stat-val coin-val" id="s-coins">0</div></div>
  </div>
  <canvas id="snake-canvas" tabindex="0"></canvas>
  <div class="upg-panel">
    <span style="font-size:11px;color:#9fa8da;font-weight:700">שדרוגים:</span>
    <button class="upg-btn" id="su-speed"  onclick="snakeBuy('speed')">🐇 מהירות<br><span class="cost">50🪙</span></button>
    <button class="upg-btn" id="su-shield" onclick="snakeBuy('shield')">🛡️ מגן<br><span class="cost">80🪙</span></button>
    <button class="upg-btn" id="su-magnet" onclick="snakeBuy('magnet')">🧲 מגנט<br><span class="cost">60🪙</span></button>
    <button class="upg-btn" id="su-double" onclick="snakeBuy('double')">⭐ כפל<br><span class="cost">70🪙</span></button>
  </div>
  <p class="hint">חצים / WASD לתנועה • Space להשהיה</p>
</div>

<!-- TETRIS -->
<div id="screen-tetris" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div class="stat-val" id="t-score">0</div></div>
    <div class="stat"><div class="stat-label">שיא</div><div class="stat-val" id="t-hi">0</div></div>
    <div class="stat"><div class="stat-label">שלב</div><div class="stat-val" id="t-level">1</div></div>
    <div class="stat"><div class="stat-label">שורות</div><div class="stat-val" id="t-lines">0</div></div>
  </div>
  <div id="tetris-wrap">
    <canvas id="tetris-canvas" tabindex="0"></canvas>
    <div id="tetris-side">
      <div id="next-label">הבא</div>
      <canvas id="next-canvas" width="80" height="80"></canvas>
      <div style="font-size:11px;color:#9fa8da;font-weight:600;line-height:2;">
        ← → הזזה<br>↑ סיבוב<br>↓ מהיר<br>Space נפילה<br>P השהיה
      </div>
    </div>
  </div>
</div>

<!-- BREAKOUT -->
<div id="screen-breakout" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div class="stat-val" id="b-score">0</div></div>
    <div class="stat"><div class="stat-label">שיא</div><div class="stat-val" id="b-hi">0</div></div>
    <div class="stat"><div class="stat-label">שלב</div><div class="stat-val" id="b-level">1</div></div>
    <div class="stat"><div class="stat-label">חיים</div><div class="stat-val" id="b-lives">❤️❤️❤️</div></div>
  </div>
  <canvas id="breakout-canvas" tabindex="0"></canvas>
  <p class="hint">← → / A D להזזה • Space לשחרור הכדור • P השהיה</p>
</div>

<!-- OVERLAYS -->
<div class="overlay" id="ov-snake">
  <h1>🐍 SNAKE</h1>
  <p>חצים / WASD לתנועה<br>אסוף כוחות מיוחדים ושדרג את הנחש!</p>
  <button class="start-btn" onclick="snakeStart()">התחל משחק ▶</button>
</div>
<div class="overlay" id="ov-tetris" style="display:none">
  <h1>🧩 TETRIS</h1>
  <p>חצים לתנועה וסיבוב<br>Space לנפילה מיידית • P להשהיה</p>
  <button class="start-btn" onclick="tetrisStart()">התחל משחק ▶</button>
</div>
<div class="overlay" id="ov-breakout" style="display:none">
  <h1>🧱 BREAKOUT</h1>
  <p>← → להזזת המחבט<br>Space לשחרור הכדור<br>שבור את כל הלבנים!</p>
  <button class="start-btn" onclick="breakoutStart()">התחל משחק ▶</button>
</div>

<div id="flash"></div>

<script>
let currentGame='snake';

function showGame(g){
  ['snake','tetris','breakout'].forEach((n,i)=>{
    document.getElementById('screen-'+n).classList.toggle('show',n===g);
    const ov=document.getElementById('ov-'+n);
    if(n===g && ov._hidden) { ov.style.display='flex'; ov._hidden=false; }
    if(n!==g) { ov.style.display='none'; }
    document.querySelectorAll('.nav-btn')[i].classList.toggle('active',n===g);
  });
  currentGame=g;
}

function flash(txt,color){
  const el=document.getElementById('flash');
  el.textContent=txt; el.style.color=color||'#3949ab'; el.style.opacity=1;
  clearTimeout(el._t); el._t=setTimeout(()=>el.style.opacity=0,1300);
}

/* ═══════ SNAKE ═══════ */
(function(){
  const C=document.getElementById('snake-canvas');
  const ctx=C.getContext('2d');
  const GRID=20,COLS=24,ROWS=24;
  C.width=COLS*GRID; C.height=ROWS*GRID;
  const CW=C.width,CH=C.height;

  let snake,prevSnake,dir,nextDir,food,powerups,particles,coins;
  let score=0,hi=0,level=1,coinCount=0;
  let paused=false,running=false;
  let upgrades={speed:0,shield:0,magnet:0,double:0};
  let activePU={};
  const BASE_TICK=105;
  let tickInterval=BASE_TICK,lastTick=0,rafId=null,lerpT=0;

  const PU=[
    {type:'speed',  e:'⚡',c:'#ff9800',dur:5000,msg:'מהיר! ⚡'},
    {type:'slow',   e:'🧊',c:'#29b6f6',dur:6000,msg:'איטי... 🧊'},
    {type:'ghost',  e:'👻',c:'#ab47bc',dur:4000,msg:'רוח! 👻'},
    {type:'score2x',e:'✨',c:'#fdd835',dur:7000,msg:'x2 ניקוד! ✨'},
    {type:'shrink', e:'✂️',c:'#ef5350',dur:0,   msg:'קצר! ✂️'},
    {type:'bigcoin',e:'🪙',c:'#ffd700',dur:0,   msg:'+20 מטבעות!'},
  ];
  const FC=['#e53935','#fb8c00','#43a047','#1e88e5','#8e24aa','#00acc1'];
  let fi=0;

  const rnd=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
  const cell=()=>({x:rnd(1,COLS-2),y:rnd(1,ROWS-2)});
  const free=p=>!snake.some(s=>s.x===p.x&&s.y===p.y)&&!(food&&food.x===p.x&&food.y===p.y);
  const lerp=(a,b,t)=>a+(b-a)*t;

  function sched(){
    tickInterval=Math.max(55, BASE_TICK-upgrades.speed*12-(activePU.speed?40:0)+(activePU.slow?55:0));
  }
  function mkFood(){
    let p; do{p=cell();}while(!free(p));
    fi=(fi+1)%FC.length;
    return {...p,color:FC[fi],pulse:0,val:rnd(1,3)};
  }

  window.snakeStart=function(){
    document.getElementById('ov-snake').style.display='none';
    document.getElementById('ov-snake')._hidden=true;
    snake=[{x:12,y:12},{x:11,y:12},{x:10,y:12}];
    prevSnake=snake.map(s=>({...s}));
    dir={x:1,y:0}; nextDir={x:1,y:0};
    food=mkFood(); powerups=[];particles=[];coins=[];
    score=0;level=1;coinCount=0;activePU={};
    running=true;paused=false;lerpT=0;
    sched(); hudS();
    if(rafId) cancelAnimationFrame(rafId);
    lastTick=performance.now();
    rafId=requestAnimationFrame(loop);
    C.focus();
  };

  function loop(now){
    rafId=requestAnimationFrame(loop);
    if(paused||!running) return;
    let dt=now-lastTick;
    lerpT=Math.min(1,dt/tickInterval);
    if(dt>=tickInterval){lastTick=now;lerpT=0;tick();}
    draw(lerpT);
  }

  function tick(){
    dir={...nextDir};
    prevSnake=snake.map(s=>({...s}));
    const h={x:(snake[0].x+dir.x+COLS)%COLS,y:(snake[0].y+dir.y+ROWS)%ROWS};
    if(!activePU.ghost&&snake.some(s=>s.x===h.x&&s.y===h.y)){
      if(upgrades.shield>0&&!activePU.shieldUsed){
        activePU.shieldUsed=true;upgrades.shield--;flash('🛡️ מגן הופעל!');
      } else {die();return;}
    }
    snake.unshift(h);
    const mag=upgrades.magnet>0?4:0;
    if(h.x===food.x&&h.y===food.y){
      let pts=food.val*(activePU.score2x?2:1)*(upgrades.double>0?2:1);
      score+=pts; burst(food.x,food.y,food.color,8);
      food=mkFood(); spawnPU(); spawnCoin();
      if(score>=level*8){level++;flash('LEVEL '+level+' 🚀','#e53935');sched();}
    } else {snake.pop();prevSnake.pop();}

    powerups=powerups.filter(pu=>{
      let dx=h.x-pu.x,dy=h.y-pu.y;
      if((dx===0&&dy===0)||(mag&&Math.abs(dx)<=mag&&Math.abs(dy)<=mag)){
        applyPU(pu);burst(pu.x,pu.y,pu.c||'#ff0',12);flash(pu.msg);return false;
      }
      return Date.now()-pu.born<8000;
    });
    coins=coins.filter(c=>{
      let dx=h.x-c.x,dy=h.y-c.y;
      if((dx===0&&dy===0)||(mag&&Math.abs(dx)<=mag&&Math.abs(dy)<=mag)){
        coinCount+=5;hudS();burst(c.x,c.y,'#ffd700',6);return false;
      }
      return Date.now()-c.born<c.ttl;
    });
    let changed=false;
    for(let k of Object.keys(activePU)){
      if(typeof activePU[k]==='number'&&Date.now()>activePU[k]){delete activePU[k];changed=true;}
    }
    if(changed) sched();
    hudS();
  }

  function applyPU(pu){
    if(pu.type==='speed'){activePU.speed=Date.now()+pu.dur;sched();}
    else if(pu.type==='slow'){activePU.slow=Date.now()+pu.dur;sched();}
    else if(pu.type==='ghost') activePU.ghost=Date.now()+pu.dur;
    else if(pu.type==='score2x') activePU.score2x=Date.now()+pu.dur;
    else if(pu.type==='shrink'){for(let i=0;i<4&&snake.length>3;i++){snake.pop();prevSnake.pop();}}
    else if(pu.type==='bigcoin') coinCount+=20;
  }

  function spawnPU(){
    if(powerups.length<2&&Math.random()<0.18){
      const t=PU[rnd(0,PU.length-1)];
      let p; do{p=cell();}while(!free(p));
      powerups.push({...p,...t,born:Date.now()});
    }
  }
  function spawnCoin(){
    if(coins.length<3&&Math.random()<0.1){
      let p; do{p=cell();}while(!free(p));
      coins.push({...p,born:Date.now(),ttl:7000});
    }
  }
  function burst(gx,gy,color,n){
    for(let i=0;i<n;i++)
      particles.push({x:gx*GRID+GRID/2,y:gy*GRID+GRID/2,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,color,life:1,sz:rnd(2,5)});
  }

  function rrect(ctx,x,y,w,h,r){
    ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
    ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);
    ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
  }

  function draw(t){
    ctx.clearRect(0,0,CW,CH);
    ctx.fillStyle='#f8f9ff'; ctx.fillRect(0,0,CW,CH);
    ctx.strokeStyle='#eef0fb'; ctx.lineWidth=1;
    for(let x=0;x<=COLS;x++){ctx.beginPath();ctx.moveTo(x*GRID,0);ctx.lineTo(x*GRID,CH);ctx.stroke();}
    for(let y=0;y<=ROWS;y++){ctx.beginPath();ctx.moveTo(0,y*GRID);ctx.lineTo(CW,y*GRID);ctx.stroke();}

    food.pulse=(food.pulse||0)+0.09;
    let fr=GRID/2-2+Math.sin(food.pulse)*2;
    ctx.save();ctx.shadowColor=food.color;ctx.shadowBlur=12;ctx.fillStyle=food.color;
    ctx.beginPath();ctx.arc(food.x*GRID+GRID/2,food.y*GRID+GRID/2,fr,0,Math.PI*2);ctx.fill();
    ctx.restore();
    if(food.val>1){
      ctx.fillStyle='#fff';ctx.font='bold 9px Nunito';
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(food.val+'x',food.x*GRID+GRID/2,food.y*GRID+GRID/2);
    }

    let now=Date.now();
    coins.forEach(c=>{
      ctx.globalAlpha=Math.min(1,(c.ttl-(now-c.born))/800);
      ctx.font='14px serif';ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText('🪙',c.x*GRID+GRID/2,c.y*GRID+GRID/2);
      ctx.globalAlpha=1;
    });
    powerups.forEach(pu=>{
      let age=now-pu.born;
      ctx.globalAlpha=Math.max(0.4,1-(age-6000)/2000);
      ctx.fillStyle=(pu.c||'#aaa')+'33';
      ctx.fillRect(pu.x*GRID+1,pu.y*GRID+1,GRID-2,GRID-2);
      ctx.font='13px serif';ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pu.e||'?',pu.x*GRID+GRID/2,pu.y*GRID+GRID/2);
      ctx.globalAlpha=1;
    });

    const ghost=!!(activePU.ghost&&activePU.ghost>now);
    snake.forEach((seg,i)=>{
      const prev=prevSnake[i]||seg;
      const px=lerp(prev.x,seg.x,t)*GRID;
      const py=lerp(prev.y,seg.y,t)*GRID;
      let ratio=i/Math.max(snake.length-1,1);
      ctx.globalAlpha=ghost?0.4:1;
      if(i===0){
        ctx.save();
        ctx.shadowColor=ghost?'#ab47bc':'#43a047';ctx.shadowBlur=ghost?14:10;
        ctx.fillStyle=ghost?'#ba68c8':'#43a047';
        rrect(ctx,px+1,py+1,GRID-2,GRID-2,5);ctx.fill();ctx.restore();
        ctx.fillStyle='#fff';
        let ex=dir.x,ey=dir.y;
        ctx.beginPath();ctx.arc(px+GRID/2+ex*5+ey*4,py+GRID/2+ey*5-ex*4,2.5,0,Math.PI*2);ctx.fill();
        ctx.beginPath();ctx.arc(px+GRID/2+ex*5-ey*4,py+GRID/2+ey*5+ex*4,2.5,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#1a2e1a';
        ctx.beginPath();ctx.arc(px+GRID/2+ex*6+ey*4,py+GRID/2+ey*6-ex*4,1.2,0,Math.PI*2);ctx.fill();
        ctx.beginPath();ctx.arc(px+GRID/2+ex*6-ey*4,py+GRID/2+ey*6+ex*4,1.2,0,Math.PI*2);ctx.fill();
      } else {
        let r=Math.floor(67+ratio*20),g=Math.floor(160-ratio*40),b=Math.floor(71+ratio*50);
        ctx.fillStyle=ghost?`rgba(186,104,200,${0.7-ratio*0.4})`:`rgb(${r},${g},${b})`;
        let pd=1+ratio*2;
        rrect(ctx,px+pd,py+pd,GRID-pd*2,GRID-pd*2,3);ctx.fill();
      }
      ctx.globalAlpha=1;
    });

    particles=particles.filter(p=>{
      p.x+=p.vx;p.y+=p.vy;p.life-=0.045;p.vy+=0.12;
      if(p.life<=0) return false;
      ctx.globalAlpha=p.life;ctx.fillStyle=p.color;
      ctx.beginPath();ctx.arc(p.x,p.y,p.sz/2,0,Math.PI*2);ctx.fill();
      ctx.globalAlpha=1;return true;
    });

    let hx=6,hy=CH-6;
    for(let k of ['speed','slow','ghost','score2x']){
      if(activePU[k]&&activePU[k]>now){
        let rem=((activePU[k]-now)/1000).toFixed(1);
        let pu=PU.find(p=>p.type===k);
        ctx.fillStyle='rgba(57,73,171,.12)';
        rrect(ctx,hx,hy-22,58,22,6);ctx.fill();
        ctx.fillStyle='#3949ab';ctx.font='bold 11px Nunito';ctx.textAlign='left';
        ctx.fillText((pu?pu.e:'?')+' '+rem+'s',hx+5,hy-7);
        hx+=64;
      }
    }
  }

  function die(){
    running=false;
    if(score>hi){hi=score;document.getElementById('s-hi').textContent=hi;}
    burst(snake[0].x,snake[0].y,'#e53935',24);
    setTimeout(()=>{
      let ov=document.getElementById('ov-snake');
      ov.innerHTML=`<h1>💀 GAME OVER</h1><p>ניקוד: ${score}<br>שיא: ${hi}</p><button class="start-btn" onclick="snakeStart()">שחק שוב ↺</button>`;
      ov.style.display='flex';
    },700);
  }

  function hudS(){
    document.getElementById('s-score').textContent=score;
    document.getElementById('s-hi').textContent=hi;
    document.getElementById('s-level').textContent=level;
    document.getElementById('s-coins').textContent=coinCount;
    document.getElementById('su-speed').disabled=coinCount<50;
    document.getElementById('su-shield').disabled=coinCount<80;
    document.getElementById('su-magnet').disabled=coinCount<60;
    document.getElementById('su-double').disabled=coinCount<70;
  }

  window.snakeBuy=function(type){
    const cost={speed:50,shield:80,magnet:60,double:70};
    if(coinCount<cost[type]) return;
    coinCount-=cost[type];upgrades[type]++;hudS();
    flash('✅ שדרוג!');if(type==='speed') sched();
  };

  document.addEventListener('keydown',e=>{
    if(currentGame!=='snake') return;
    const map={ArrowUp:{x:0,y:-1},ArrowDown:{x:0,y:1},ArrowLeft:{x:-1,y:0},ArrowRight:{x:1,y:0},
               w:{x:0,y:-1},s:{x:0,y:1},a:{x:-1,y:0},d:{x:1,y:0}};
    if(map[e.key]){
      e.preventDefault();
      let nd=map[e.key];
      if(running&&(nd.x!==-(dir.x)||nd.y!==-(dir.y))) nextDir=nd;
    }
    if(e.key===' '&&running){e.preventDefault();paused=!paused;if(!paused)C.focus();}
  });
})();

/* ═══════ TETRIS ═══════ */
(function(){
  const C=document.getElementById('tetris-canvas');
  const ctx=C.getContext('2d');
  const NC=document.getElementById('next-canvas');
  const nctx=NC.getContext('2d');
  const COLS=10,ROWS=20,SZ=28;
  C.width=COLS*SZ; C.height=ROWS*SZ;

  const COLORS=['#e53935','#fb8c00','#fdd835','#43a047','#1e88e5','#8e24aa','#00acc1'];
  const PIECES=[
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[1,0],[1,0],[1,1]],
    [[0,1],[0,1],[1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]],
  ];

  let board,piece,nextPiece,score=0,hi=0,level=1,lines=0,paused=false,running=false,rafId=null,dropT=0,lastT=0;

  function mkPiece(){
    const idx=Math.floor(Math.random()*PIECES.length);
    const shape=PIECES[idx].map(r=>[...r]);
    return {shape,color:COLORS[idx],x:Math.floor((COLS-shape[0].length)/2),y:0};
  }

  window.tetrisStart=function(){
    document.getElementById('ov-tetris').style.display='none';
    board=Array.from({length:ROWS},()=>Array(COLS).fill(null));
    piece=mkPiece();nextPiece=mkPiece();
    score=0;level=1;lines=0;paused=false;running=true;dropT=0;
    hudT();
    if(rafId) cancelAnimationFrame(rafId);
    lastT=performance.now();
    rafId=requestAnimationFrame(tLoop);
    C.focus();
  };

  const dropInt=()=>Math.max(80,600-level*50);

  function tLoop(now){
    rafId=requestAnimationFrame(tLoop);
    if(paused||!running) return;
    let dt=now-lastT;lastT=now;dropT+=dt;
    if(dropT>=dropInt()){dropT=0;tDrop();}
    tDraw();
  }

  const rotate=m=>m[0].map((_,i)=>m.map(r=>r[i]).reverse());
  const valid=(p,b)=>p.shape.every((row,dy)=>row.every((v,dx)=>{
    if(!v) return true;
    let nx=p.x+dx,ny=p.y+dy;
    return nx>=0&&nx<COLS&&ny<ROWS&&!(ny>=0&&b[ny][nx]);
  }));

  function tDrop(){
    let np={...piece,y:piece.y+1};
    if(valid(np,board)) piece=np; else place();
  }

  function place(){
    piece.shape.forEach((row,dy)=>row.forEach((v,dx)=>{
      if(v&&piece.y+dy>=0) board[piece.y+dy][piece.x+dx]=piece.color;
    }));
    let cleared=0;
    for(let y=ROWS-1;y>=0;){
      if(board[y].every(c=>c)){board.splice(y,1);board.unshift(Array(COLS).fill(null));cleared++;}
      else y--;
    }
    if(cleared){
      lines+=cleared;score+=cleared*100*level;level=Math.floor(lines/10)+1;
      hudT();flash(cleared===4?'TETRIS! 🎉':'+'+(cleared*100*level),'#43a047');
    }
    piece=nextPiece;nextPiece=mkPiece();
    if(!valid(piece,board)) tGameOver();
  }

  function tGameOver(){
    running=false;
    if(score>hi) hi=score;
    let ov=document.getElementById('ov-tetris');
    ov.innerHTML=`<h1>🧩 GAME OVER</h1><p>ניקוד: ${score}<br>שיא: ${hi}</p><button class="start-btn" onclick="tetrisStart()">שחק שוב ↺</button>`;
    ov.style.display='flex';
  }

  function hudT(){
    document.getElementById('t-score').textContent=score;
    document.getElementById('t-hi').textContent=hi;
    document.getElementById('t-level').textContent=level;
    document.getElementById('t-lines').textContent=lines;
  }

  function drawBlock(ctx,x,y,color,sz){
    ctx.fillStyle=color;
    ctx.fillRect(x*sz+1,y*sz+1,sz-2,sz-2);
    ctx.fillStyle='rgba(255,255,255,.3)';
    ctx.fillRect(x*sz+2,y*sz+2,sz-4,4);
    ctx.fillStyle='rgba(0,0,0,.12)';
    ctx.fillRect(x*sz+2,y*sz+sz-5,sz-4,3);
  }

  function tDraw(){
    ctx.clearRect(0,0,C.width,C.height);
    ctx.fillStyle='#f8f9ff';ctx.fillRect(0,0,C.width,C.height);
    ctx.strokeStyle='#eef0fb';ctx.lineWidth=1;
    for(let x=0;x<=COLS;x++){ctx.beginPath();ctx.moveTo(x*SZ,0);ctx.lineTo(x*SZ,C.height);ctx.stroke();}
    for(let y=0;y<=ROWS;y++){ctx.beginPath();ctx.moveTo(0,y*SZ);ctx.lineTo(C.width,y*SZ);ctx.stroke();}
    board.forEach((row,y)=>row.forEach((c,x)=>{if(c) drawBlock(ctx,x,y,c,SZ);}));
    // ghost
    let ghost={...piece};
    while(valid({...ghost,y:ghost.y+1},board)) ghost.y++;
    ghost.shape.forEach((row,dy)=>row.forEach((v,dx)=>{
      if(v){ctx.fillStyle='rgba(57,73,171,.12)';ctx.fillRect((ghost.x+dx)*SZ+1,(ghost.y+dy)*SZ+1,SZ-2,SZ-2);}
    }));
    piece.shape.forEach((row,dy)=>row.forEach((v,dx)=>{if(v) drawBlock(ctx,piece.x+dx,piece.y+dy,piece.color,SZ);}));
    nctx.clearRect(0,0,80,80);
    nctx.fillStyle='#f8f9ff';nctx.fillRect(0,0,80,80);
    let off=Math.floor((4-nextPiece.shape[0].length)/2);
    nextPiece.shape.forEach((row,dy)=>row.forEach((v,dx)=>{if(v) drawBlock(nctx,dx+off,dy+1,nextPiece.color,18);}));
  }

  document.addEventListener('keydown',e=>{
    if(currentGame!=='tetris'||!running||paused) return;
    if(e.key==='ArrowLeft'||e.key==='a'){e.preventDefault();let np={...piece,x:piece.x-1};if(valid(np,board)) piece=np;}
    if(e.key==='ArrowRight'||e.key==='d'){e.preventDefault();let np={...piece,x:piece.x+1};if(valid(np,board)) piece=np;}
    if(e.key==='ArrowDown'||e.key==='s'){e.preventDefault();dropT+=80;}
    if(e.key==='ArrowUp'||e.key==='w'){e.preventDefault();let rp={...piece,shape:rotate(piece.shape)};if(valid(rp,board)) piece=rp;}
    if(e.key===' '){e.preventDefault();while(valid({...piece,y:piece.y+1},board)) piece={...piece,y:piece.y+1};tDrop();}
    if(e.key==='p'||e.key==='P') paused=!paused;
  });
})();

/* ═══════ BREAKOUT ═══════ */
(function(){
  const C=document.getElementById('breakout-canvas');
  const ctx=C.getContext('2d');
  C.width=480; C.height=500;
  const W=C.width,H=C.height;
  const PAD_W=80,PAD_H=12,BALL_R=8;
  const BCOLS=10,BROWS=6,BW=42,BH=18,BPAD=4;
  const BCOLORS=['#e53935','#fb8c00','#fdd835','#43a047','#1e88e5','#8e24aa'];

  let pad,ball,bricks,score=0,hi=0,level=1,lives=3,running=false,paused=false,rafId=null,keys={};

  function makeBricks(){
    let arr=[];
    for(let r=0;r<BROWS;r++)
      for(let c=0;c<BCOLS;c++){
        let x=c*(BW+BPAD)+20, y=r*(BH+BPAD)+50;
        let hp=(BROWS-r<=2)?2:1;
        arr.push({x,y,w:BW,h:BH,color:BCOLORS[r%BCOLORS.length],alive:true,hp,maxHp:hp});
      }
    return arr;
  }

  function resetBall(){
    ball={x:W/2,y:H-80,vx:3+level*0.3,vy:-(3.5+level*0.35),r:BALL_R,attached:true};
  }

  window.breakoutStart=function(){
    document.getElementById('ov-breakout').style.display='none';
    pad={x:W/2-PAD_W/2,y:H-30,w:PAD_W,h:PAD_H};
    bricks=makeBricks();score=0;level=1;lives=3;
    resetBall();running=true;paused=false;
    hudB();
    if(rafId) cancelAnimationFrame(rafId);
    rafId=requestAnimationFrame(bLoop);
    C.focus();
  };

  function bLoop(){
    rafId=requestAnimationFrame(bLoop);
    if(paused||!running) return;
    update();bDraw();
  }

  function update(){
    const spd=6;
    if((keys['ArrowLeft']||keys['a'])&&pad.x>0) pad.x-=spd;
    if((keys['ArrowRight']||keys['d'])&&pad.x+pad.w<W) pad.x+=spd;
    if(ball.attached){ball.x=pad.x+pad.w/2;return;}
    ball.x+=ball.vx; ball.y+=ball.vy;
    if(ball.x-ball.r<0){ball.x=ball.r;ball.vx*=-1;}
    if(ball.x+ball.r>W){ball.x=W-ball.r;ball.vx*=-1;}
    if(ball.y-ball.r<0){ball.y=ball.r;ball.vy*=-1;}
    if(ball.y+ball.r>pad.y&&ball.y-ball.r<pad.y+pad.h&&ball.x>pad.x&&ball.x<pad.x+pad.w){
      ball.vy=-Math.abs(ball.vy);
      let rel=(ball.x-(pad.x+pad.w/2))/(pad.w/2);
      ball.vx=rel*5.5;
      let spd2=Math.sqrt(ball.vx**2+ball.vy**2);
      let mx=3.5+level*0.4;if(spd2>mx){ball.vx*=mx/spd2;ball.vy*=mx/spd2;}
    }
    if(ball.y-ball.r>H){
      lives--;
      if(lives<=0){bGameOver(false);return;}
      resetBall();hudB();
    }
    let allDead=true;
    for(let b of bricks){
      if(!b.alive) continue; allDead=false;
      if(ball.x+ball.r>b.x&&ball.x-ball.r<b.x+b.w&&ball.y+ball.r>b.y&&ball.y-ball.r<b.y+b.h){
        b.hp--;if(b.hp<=0){b.alive=false;score+=10*BROWS;}
        let overlapL=ball.x+ball.r-b.x, overlapR=b.x+b.w-ball.x+ball.r;
        let overlapT=ball.y+ball.r-b.y, overlapB=b.y+b.h-ball.y+ball.r;
        let minOv=Math.min(overlapL,overlapR,overlapT,overlapB);
        if(minOv===overlapT||minOv===overlapB) ball.vy*=-1; else ball.vx*=-1;
        hudB(); break;
      }
    }
    if(allDead){level++;bricks=makeBricks();resetBall();flash('LEVEL '+level+' 🎉','#43a047');hudB();}
  }

  function bGameOver(win){
    running=false;
    if(score>hi) hi=score;
    let ov=document.getElementById('ov-breakout');
    ov.innerHTML=`<h1>${!win?'💥 GAME OVER':'🏆 ניצחת!'}</h1><p>ניקוד: ${score}<br>שיא: ${hi}</p><button class="start-btn" onclick="breakoutStart()">שחק שוב ↺</button>`;
    ov.style.display='flex';
  }

  function hudB(){
    document.getElementById('b-score').textContent=score;
    document.getElementById('b-hi').textContent=hi;
    document.getElementById('b-level').textContent=level;
    document.getElementById('b-lives').textContent='❤️'.repeat(Math.max(0,lives));
  }

  function bDraw(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#f8f9ff';ctx.fillRect(0,0,W,H);
    ctx.strokeStyle='#eef0fb';ctx.lineWidth=1;
    for(let x=0;x<W;x+=20){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
    for(let y=0;y<H;y+=20){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}

    bricks.forEach(b=>{
      if(!b.alive) return;
      ctx.fillStyle=b.hp<b.maxHp?b.color+'99':b.color;
      ctx.beginPath();
      if(ctx.roundRect) ctx.roundRect(b.x,b.y,b.w,b.h,4); else ctx.rect(b.x,b.y,b.w,b.h);
      ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.3)';ctx.fillRect(b.x+2,b.y+2,b.w-4,5);
    });

    ctx.fillStyle='#3949ab';
    ctx.beginPath();
    if(ctx.roundRect) ctx.roundRect(pad.x,pad.y,pad.w,pad.h,6); else ctx.rect(pad.x,pad.y,pad.w,pad.h);
    ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.3)';ctx.fillRect(pad.x+4,pad.y+2,pad.w-8,4);

    ctx.save();ctx.shadowColor='#3949ab';ctx.shadowBlur=12;
    ctx.fillStyle='#3949ab';
    ctx.beginPath();ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);ctx.fill();
    ctx.restore();

    if(ball.attached){
      ctx.fillStyle='rgba(57,73,171,.5)';ctx.font='700 12px Nunito';ctx.textAlign='center';
      ctx.fillText('Space לשחרור',W/2,H-52);
    }
  }

  document.addEventListener('keydown',e=>{
    if(currentGame!=='breakout') return;
    keys[e.key]=true;
    if(e.key===' '){e.preventDefault();if(ball&&ball.attached) ball.attached=false;}
    if(['ArrowLeft','ArrowRight','a','d'].includes(e.key)) e.preventDefault();
    if(e.key==='p') paused=!paused;
  });
  document.addEventListener('keyup',e=>{keys[e.key]=false;});
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=760, scrolling=False)


