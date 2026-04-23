import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🎮 Arcade Games Ultimate", layout="wide")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#f0f4ff; font-family:'Nunito', sans-serif; color:#1a1a2e; overflow:hidden; }
  
  /* Navigation */
  #nav { display:flex; gap:10px; padding:15px; background:#fff; border-bottom:2px solid #e8eaf6; justify-content:center; flex-wrap:wrap; }
  .nav-btn { padding:10px 20px; border-radius:12px; border:2px solid #c5cae9; background:#fff; font-family:inherit; font-size:14px; font-weight:700; cursor:pointer; transition:all .2s; color:#3949ab; }
  .nav-btn:hover { background:#e8eaf6; }
  .nav-btn.active { background:#3949ab; color:#fff; border-color:#3949ab; box-shadow: 0 4px 10px rgba(57,73,171,0.3); }

  /* Screens */
  .screen { display:none; flex-direction:column; align-items:center; padding:20px; gap:15px; height: calc(100vh - 80px); }
  .screen.show { display:flex; }
  
  /* Stats & HUD */
  .hud { display:flex; gap:15px; margin-bottom:10px; }
  .stat { background:#fff; border:2px solid #e8eaf6; border-radius:12px; padding:8px 20px; text-align:center; min-width:90px; }
  .stat-label { font-size:10px; color:#9fa8da; text-transform:uppercase; font-weight:700; }
  .stat-val { font-size:22px; font-weight:900; color:#3949ab; }
  .coin-val { color:#f9a825; }

  canvas { border-radius:12px; display:block; border:4px solid #fff; background:#fff; box-shadow: 0 10px 30px rgba(0,0,0,0.1); touch-action: none; }
  
  /* Overlays */
  .overlay { position:absolute; top:80px; left:0; right:0; bottom:0; background:rgba(240,244,255,0.95); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; z-index:100; text-align:center; }
  .overlay h1 { font-size:48px; color:#3949ab; font-weight:900; }
  .overlay p { font-size:18px; max-width:400px; color:#5c6bc0; }
  .start-btn { background:#3949ab; color:#fff; border:none; padding:15px 40px; border-radius:50px; font-size:20px; font-weight:900; cursor:pointer; transition:0.2s; }
  .start-btn:hover { transform:scale(1.05); background:#303f9f; }

  /* Upgrades */
  .upg-panel { display:flex; gap:10px; background:#fff; padding:10px; border-radius:15px; border:2px solid #e8eaf6; }
  .upg-btn { padding:8px; border-radius:8px; border:1px solid #c5cae9; background:#f8f9ff; cursor:pointer; font-size:12px; font-weight:700; }
  .upg-btn:disabled { opacity:0.5; cursor:not-allowed; }

  #flash { position:fixed; top:120px; left:50%; transform:translateX(-50%); font-size:24px; font-weight:900; pointer-events:none; opacity:0; transition:0.3s; z-index:200; background:rgba(255,255,255,0.9); padding:10px 30px; border-radius:50px; }
</style>
</head>
<body>

<div id="nav">
  <button class="nav-btn active" onclick="switchGame('snake')">🐍 נחש</button>
  <button class="nav-btn" onclick="switchGame('tetris')">🧩 טטריס</button>
  <button class="nav-btn" onclick="switchGame('breakout')">🧱 לבנים</button>
  <button class="nav-btn" onclick="switchGame('flappy')">🐦 ציפור</button>
  <button class="nav-btn" onclick="switchGame('invaders')">👾 פולשים</button>
</div>

<div id="flash"></div>

<div id="screen-snake" class="screen show">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div id="s-score" class="stat-val">0</div></div>
    <div class="stat"><div class="stat-label">מטבעות</div><div id="s-coins" class="stat-val coin-val">0</div></div>
  </div>
  <canvas id="snake-canvas"></canvas>
  <div class="upg-panel">
    <button class="upg-btn" id="su-speed" onclick="snakeBuy('speed')">מהירות (50🪙)</button>
    <button class="upg-btn" id="su-magnet" onclick="snakeBuy('magnet')">מגנט (60🪙)</button>
  </div>
  <div class="overlay" id="ov-snake">
    <h1>SNAKE</h1>
    <p>השתמש בחצים כדי לאכול ולגדול. אל תתנגש בקירות או בעצמך!</p>
    <button class="start-btn" onclick="snakeStart()">שחק עכשיו</button>
  </div>
</div>

<div id="screen-tetris" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div id="t-score" class="stat-val">0</div></div>
    <div class="stat"><div class="stat-label">שורות</div><div id="t-lines" class="stat-val">0</div></div>
  </div>
  <canvas id="tetris-canvas"></canvas>
  <div class="overlay" id="ov-tetris">
    <h1>TETRIS</h1>
    <p>סדר את הבלוקים בשורות מלאות כדי להעלים אותן.</p>
    <button class="start-btn" onclick="tetrisStart()">שחק עכשיו</button>
  </div>
</div>

<div id="screen-breakout" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div id="b-score" class="stat-val">0</div></div>
    <div class="stat"><div class="stat-label">חיים</div><div id="b-lives" class="stat-val">❤️❤️❤️</div></div>
  </div>
  <canvas id="breakout-canvas"></canvas>
  <div class="overlay" id="ov-breakout">
    <h1>BREAKOUT</h1>
    <p>השתמש במחבט כדי להקפיץ את הכדור ולשבור את כל הלבנים.</p>
    <button class="start-btn" onclick="breakoutStart()">שחק עכשיו</button>
  </div>
</div>

<div id="screen-flappy" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div id="f-score" class="stat-val">0</div></div>
    <div class="stat"><div class="stat-label">שיא</div><div id="f-hi" class="stat-val">0</div></div>
  </div>
  <canvas id="flappy-canvas"></canvas>
  <div class="overlay" id="ov-flappy">
    <h1>FLAPPY BIRD</h1>
    <p>לחץ על רווח או על המסך כדי לעוף בין הצינורות.</p>
    <button class="start-btn" onclick="flappyStart()">שחק עכשיו</button>
  </div>
</div>

<div id="screen-invaders" class="screen">
  <div class="hud">
    <div class="stat"><div class="stat-label">ניקוד</div><div id="i-score" class="stat-val">0</div></div>
    <div class="stat"><div class="stat-label">גל</div><div id="i-wave" class="stat-val">1</div></div>
  </div>
  <canvas id="invaders-canvas"></canvas>
  <div class="overlay" id="ov-invaders">
    <h1>INVADERS</h1>
    <p>השמד את הפולשים לפני שהם יגיעו לכדור הארץ!</p>
    <button class="start-btn" onclick="invadersStart()">שחק עכשיו</button>
  </div>
</div>

<script>
/* UTILS */
let currentGame = 'snake';
function flash(m, c='#3949ab') {
  const e = document.getElementById('flash');
  e.textContent = m; e.style.color = c; e.style.opacity = 1;
  setTimeout(() => e.style.opacity = 0, 1500);
}

function switchGame(g) {
  stopAllGames();
  currentGame = g;
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('show'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('screen-'+g).classList.add('show');
  document.querySelector(`button[onclick*="${g}"]`).classList.add('active');
  document.getElementById('ov-'+g).style.display = 'flex';
}

function stopAllGames() {
  running = false; // Global flag check
  if (window.snakeRaf) cancelAnimationFrame(window.snakeRaf);
  if (window.tetrisRaf) cancelAnimationFrame(window.tetrisRaf);
  if (window.breakoutRaf) cancelAnimationFrame(window.breakoutRaf);
  if (window.flappyRaf) cancelAnimationFrame(window.flappyRaf);
  if (window.invadersRaf) cancelAnimationFrame(window.invadersRaf);
}

/* --- SNAKE --- */
(function() {
  const canvas = document.getElementById('snake-canvas');
  const ctx = canvas.getContext('2d');
  const grid = 20;
  canvas.width = 400; canvas.height = 400;
  let snake, dir, food, score, coins, speedUpg, magnetUpg, running = false;

  window.snakeStart = () => {
    document.getElementById('ov-snake').style.display = 'none';
    snake = [{x:10, y:10}]; dir = {x:1, y:0}; score = 0; coins = 0;
    speedUpg = 0; magnetUpg = 0;
    spawnFood(); running = true; updateHUD(); loop();
  };

  function spawnFood() { food = {x: Math.floor(Math.random()*20), y: Math.floor(Math.random()*20)}; }
  function updateHUD() {
    document.getElementById('s-score').textContent = score;
    document.getElementById('s-coins').textContent = coins;
  }

  function loop() {
    if (!running || currentGame !== 'snake') return;
    ctx.clearRect(0,0,400,400);
    
    const head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};
    if (head.x<0||head.x>=20||head.y<0||head.y>=20||snake.some(s=>s.x===head.x&&s.y===head.y)) {
      running = false; flash("נפסלת!", "red"); return;
    }
    
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
      score += 10; coins += 5; spawnFood(); updateHUD();
    } else { snake.pop(); }

    ctx.fillStyle = "red"; ctx.fillRect(food.x*grid, food.y*grid, grid-2, grid-2);
    ctx.fillStyle = "#3949ab";
    snake.forEach(s => ctx.fillRect(s.x*grid, s.y*grid, grid-2, grid-2));
    
    window.snakeRaf = setTimeout(() => requestAnimationFrame(loop), 100 - (speedUpg*10));
  }

  window.addEventListener('keydown', e => {
    if (currentGame!=='snake') return;
    if (e.key==='ArrowUp' && dir.y===0) dir = {x:0, y:-1};
    if (e.key==='ArrowDown' && dir.y===0) dir = {x:0, y:1};
    if (e.key==='ArrowLeft' && dir.x===0) dir = {x:-1, y:0};
    if (e.key==='ArrowRight' && dir.x===0) dir = {x:1, y:0};
  });
})();

/* --- TETRIS --- */
(function() {
  const canvas = document.getElementById('tetris-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 240; canvas.height = 400;
  const scale = 20;
  let board, player, score, lines, running = false;

  const SHAPES = [
    [[1,1,1,1]], [[1,1],[1,1]], [[0,1,0],[1,1,1]], [[1,0],[1,0],[1,1]], [[0,1],[0,1],[1,1]]
  ];

  window.tetrisStart = () => {
    document.getElementById('ov-tetris').style.display = 'none';
    board = Array.from({length: 20}, () => Array(12).fill(0));
    player = { pos: {x: 4, y: 0}, matrix: SHAPES[Math.floor(Math.random()*SHAPES.length)] };
    score = 0; lines = 0; running = true;
    lastTime = 0; dropCounter = 0;
    updateHUD(); loop();
  };

  function updateHUD() {
    document.getElementById('t-score').textContent = score;
    document.getElementById('t-lines').textContent = lines;
  }

  function collide(b, p) {
    const [m, o] = [p.matrix, p.pos];
    for (let y=0; y<m.length; ++y) {
      for (let x=0; x<m[y].length; ++x) {
        if (m[y][x] !== 0 && (b[y+o.y] && b[y+o.y][x+o.x]) !== 0) return true;
      }
    }
    return false;
  }

  function merge(b, p) {
    p.matrix.forEach((row, y) => {
      row.forEach((value, x) => {
        if (value !== 0) b[y+p.pos.y][x+p.pos.x] = value;
      });
    });
  }

  function playerDrop() {
    player.pos.y++;
    if (collide(board, player)) {
      player.pos.y--;
      merge(board, player);
      playerReset();
      arenaSweep();
      updateHUD();
    }
    dropCounter = 0;
  }

  function playerReset() {
    player.matrix = SHAPES[Math.floor(Math.random()*SHAPES.length)];
    player.pos.y = 0;
    player.pos.x = 4;
    if (collide(board, player)) {
      running = false; flash("Game Over!", "red");
    }
  }

  function arenaSweep() {
    outer: for (let y = board.length - 1; y > 0; --y) {
      for (let x = 0; x < board[y].length; ++x) {
        if (board[y][x] === 0) continue outer;
      }
      const row = board.splice(y, 1)[0].fill(0);
      board.unshift(row);
      ++y; score += 10; lines++;
    }
  }

  let dropCounter = 0, lastTime = 0;
  function loop(time = 0) {
    if (!running || currentGame !== 'tetris') return;
    const deltaTime = time - lastTime;
    lastTime = time;
    dropCounter += deltaTime;
    if (dropCounter > 1000) playerDrop();

    ctx.fillStyle = '#fff'; ctx.fillRect(0,0,canvas.width,canvas.height);
    board.forEach((row, y) => row.forEach((val, x) => {
      if (val) { ctx.fillStyle = 'blue'; ctx.fillRect(x*scale, y*scale, scale-1, scale-1); }
    }));
    player.matrix.forEach((row, y) => row.forEach((val, x) => {
      if (val) { ctx.fillStyle = 'red'; ctx.fillRect((x+player.pos.x)*scale, (y+player.pos.y)*scale, scale-1, scale-1); }
    }));
    window.tetrisRaf = requestAnimationFrame(loop);
  }

  window.addEventListener('keydown', e => {
    if (currentGame !== 'tetris') return;
    if (e.key === 'ArrowLeft') { player.pos.x--; if (collide(board, player)) player.pos.x++; }
    if (e.key === 'ArrowRight') { player.pos.x++; if (collide(board, player)) player.pos.x--; }
    if (e.key === 'ArrowDown') playerDrop();
  });
})();

/* --- BREAKOUT --- */
(function() {
  const canvas = document.getElementById('breakout-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 400; canvas.height = 400;
  let ball, paddle, bricks, score, lives, running = false;

  window.breakoutStart = () => {
    document.getElementById('ov-breakout').style.display = 'none';
    ball = { x: 200, y: 350, dx: 2, dy: -2, r: 8 };
    paddle = { x: 160, w: 80, h: 10 };
    score = 0; lives = 3;
    bricks = [];
    for(let i=0; i<5; i++) for(let j=0; j<8; j++) bricks.push({x: j*50+5, y: i*20+30, w: 40, h: 15, active: true});
    running = true; updateHUD(); loop();
  };

  function updateHUD() {
    document.getElementById('b-score').textContent = score;
    document.getElementById('b-lives').textContent = "❤️".repeat(lives);
  }

  function loop() {
    if (!running || currentGame !== 'breakout') return;
    ctx.clearRect(0,0,400,400);
    
    ball.x += ball.dx; ball.y += ball.dy;
    if (ball.x<0 || ball.x>400) ball.dx *= -1;
    if (ball.y<0) ball.dy *= -1;
    if (ball.y>400) { 
       lives--; updateHUD(); 
       if(lives<=0) { running=false; flash("הפסדת!"); return; }
       ball.x = 200; ball.y = 350; ball.dy = -2;
    }
    
    if (ball.y > 380 && ball.x > paddle.x && ball.x < paddle.x + paddle.w) ball.dy *= -1;
    
    bricks.forEach(b => {
      if (b.active && ball.x > b.x && ball.x < b.x+b.w && ball.y > b.y && ball.y < b.y+b.h) {
        b.active = false; ball.dy *= -1; score += 10; updateHUD();
      }
      if (b.active) { ctx.fillStyle = "orange"; ctx.fillRect(b.x, b.y, b.w, b.h); }
    });

    ctx.fillStyle = "blue"; ctx.fillRect(paddle.x, 385, paddle.w, paddle.h);
    ctx.fillStyle = "green"; ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2); ctx.fill();
    
    window.breakoutRaf = requestAnimationFrame(loop);
  }

  window.addEventListener('mousemove', e => {
    if (currentGame === 'breakout') {
      const rect = canvas.getBoundingClientRect();
      paddle.x = e.clientX - rect.left - paddle.w/2;
    }
  });
})();

/* --- FLAPPY BIRD --- */
(function() {
  const canvas = document.getElementById('flappy-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 320; canvas.height = 480;
  let bird, pipes, score, hi=0, running = false;

  window.flappyStart = () => {
    document.getElementById('ov-flappy').style.display = 'none';
    bird = { y: 240, v: 0, g: 0.25 };
    pipes = []; score = 0; running = true; loop();
  };

  function loop() {
    if (!running || currentGame !== 'flappy') return;
    ctx.fillStyle = '#70c5ce'; ctx.fillRect(0,0,320,480);
    
    bird.v += bird.g; bird.y += bird.v;
    if (bird.y > 480 || bird.y < 0) { endGame(); return; }

    if (pipes.length === 0 || pipes[pipes.length-1].x < 150) {
      pipes.push({ x: 320, h: Math.random()*200+50 });
    }

    pipes.forEach((p, i) => {
      p.x -= 2;
      ctx.fillStyle = '#74bf2e';
      ctx.fillRect(p.x, 0, 40, p.h);
      ctx.fillRect(p.x, p.h+100, 40, 480);
      
      if (p.x === 50) { score++; document.getElementById('f-score').textContent = score; }
      if (50 > p.x && 50 < p.x+40 && (bird.y < p.h || bird.y > p.h+100)) { endGame(); }
    });

    pipes = pipes.filter(p => p.x > -40);

    ctx.fillStyle = 'yellow'; ctx.beginPath(); ctx.arc(50, bird.y, 12, 0, Math.PI*2); ctx.fill();
    window.flappyRaf = requestAnimationFrame(loop);
  }

  function endGame() {
    running = false; if(score>hi) hi=score;
    document.getElementById('f-hi').textContent = hi;
    flash("בום!");
  }

  const flap = () => { if(currentGame==='flappy' && running) bird.v = -5; };
  window.addEventListener('keydown', e => { if(e.code==='Space') flap(); });
  canvas.addEventListener('mousedown', flap);
})();

/* --- SPACE INVADERS --- */
(function() {
  const canvas = document.getElementById('invaders-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 400; canvas.height = 400;
  let ship, bullets, aliens, direction, score, wave, running = false;

  window.invadersStart = () => {
    document.getElementById('ov-invaders').style.display = 'none';
    ship = { x: 180, w: 40 }; bullets = []; aliens = [];
    direction = 1; score = 0; wave = 1;
    for(let i=0; i<3; i++) for(let j=0; j<6; j++) aliens.push({x: j*50+50, y: i*40+50, r: 15});
    running = true; loop();
  };

  function loop() {
    if (!running || currentGame !== 'invaders') return;
    ctx.fillStyle = 'black'; ctx.fillRect(0,0,400,400);
    
    ctx.fillStyle = 'white'; ctx.fillRect(ship.x, 370, ship.w, 20);

    let edge = false;
    aliens.forEach(a => {
      a.x += direction * wave;
      if (a.x > 380 || a.x < 20) edge = true;
      ctx.fillStyle = 'lime'; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI*2); ctx.fill();
      if (a.y > 350) { running = false; flash("הפולשים הגיעו!"); }
    });

    if (edge) { direction *= -1; aliens.forEach(a => a.y += 20); }

    bullets.forEach((b, bi) => {
      b.y -= 5; ctx.fillStyle = 'yellow'; ctx.fillRect(b.x, b.y, 4, 10);
      aliens.forEach((a, ai) => {
        if (Math.hypot(b.x-a.x, b.y-a.y) < a.r) {
          aliens.splice(ai, 1); bullets.splice(bi, 1);
          score += 20; document.getElementById('i-score').textContent = score;
        }
      });
    });

    if (aliens.length === 0) { wave++; invadersStart(); flash("גל " + wave); }

    window.invadersRaf = requestAnimationFrame(loop);
  }

  window.addEventListener('keydown', e => {
    if (currentGame !== 'invaders') return;
    if (e.key === 'ArrowLeft' && ship.x > 0) ship.x -= 20;
    if (e.key === 'ArrowRight' && ship.x < 360) ship.x += 20;
    if (e.key === ' ') bullets.push({x: ship.x + 18, y: 370});
  });
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=650, scrolling=False)
