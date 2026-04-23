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

st.set_page_config(page_title="🎮 Arcade", layout="wide")

GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { margin:0; font-family:sans-serif; background:#eef; text-align:center;}
canvas { background:white; border:2px solid #999; margin-top:10px;}
button { margin:5px; padding:8px 16px; font-weight:bold; cursor:pointer;}
</style>
</head>
<body tabindex="0">

<h2>🎮 Arcade</h2>
<button onclick="setGame('snake')">Snake</button>
<button onclick="setGame('tetris')">Tetris</button>
<button onclick="setGame('breakout')">Breakout</button>
<button onclick="setGame('pong')">Pong</button>

<br>
<canvas id="game" width="400" height="400"></canvas>

<script>
let canvas = document.getElementById("game");
let ctx = canvas.getContext("2d");

let current = "snake";
document.body.focus();

/* ========= GLOBAL FIX ========= */
window.addEventListener("load", () => {
  document.body.focus();
});

window.addEventListener("keydown", (e) => {
  if(current === "snake") snakeKey(e);
  if(current === "tetris") tetrisKey(e);
  if(current === "breakout") breakoutKey(e);
  if(current === "pong") pongKey(e);
});

/* ========= SWITCH ========= */
function setGame(g){
  current = g;
  reset();
  document.body.focus();
}

/* ========= SNAKE ========= */
let snake, dir, food;

function snakeInit(){
  snake = [{x:10,y:10}];
  dir = {x:1,y:0};
  food = {x:5,y:5};
}

function snakeKey(e){
  if(e.key==="ArrowUp") dir={x:0,y:-1};
  if(e.key==="ArrowDown") dir={x:0,y:1};
  if(e.key==="ArrowLeft") dir={x:-1,y:0};
  if(e.key==="ArrowRight") dir={x:1,y:0};
}

function snakeUpdate(){
  let head = {x:snake[0].x+dir.x, y:snake[0].y+dir.y};
  snake.unshift(head);
  if(head.x===food.x && head.y===food.y){
    food={x:Math.floor(Math.random()*20),y:Math.floor(Math.random()*20)};
  } else snake.pop();
}

function snakeDraw(){
  ctx.clearRect(0,0,400,400);
  snake.forEach(s=>{
    ctx.fillRect(s.x*20,s.y*20,18,18);
  });
  ctx.fillStyle="red";
  ctx.fillRect(food.x*20,food.y*20,18,18);
  ctx.fillStyle="black";
}

/* ========= TETRIS ========= */
let tX=5;

function tetrisInit(){ tX=5; }

function tetrisKey(e){
  if(e.key==="ArrowLeft") tX--;
  if(e.key==="ArrowRight") tX++;
}

function tetrisUpdate(){}

function tetrisDraw(){
  ctx.clearRect(0,0,400,400);
  ctx.fillRect(tX*20,0,20,20);
}

/* ========= BREAKOUT ========= */
let paddle, ball;

function breakoutInit(){
  paddle = 150;
  ball = {x:200,y:200,vx:3,vy:3};
}

function breakoutKey(e){
  if(e.key==="ArrowLeft") paddle-=20;
  if(e.key==="ArrowRight") paddle+=20;
}

function breakoutUpdate(){
  ball.x+=ball.vx;
  ball.y+=ball.vy;

  if(ball.x<0||ball.x>400) ball.vx*=-1;
  if(ball.y<0) ball.vy*=-1;

  if(ball.y>380 && ball.x>paddle && ball.x<paddle+80){
    ball.vy*=-1;
  }
}

function breakoutDraw(){
  ctx.clearRect(0,0,400,400);
  ctx.fillRect(paddle,380,80,10);
  ctx.beginPath();
  ctx.arc(ball.x,ball.y,8,0,Math.PI*2);
  ctx.fill();
}

/* ========= PONG ========= */
let p1=150,p2=150,px=200,py=200,pvx=3,pvy=3;

function pongInit(){}

function pongKey(e){
  if(e.key==="w") p1-=20;
  if(e.key==="s") p1+=20;
  if(e.key==="ArrowUp") p2-=20;
  if(e.key==="ArrowDown") p2+=20;
}

function pongUpdate(){
  px+=pvx; py+=pvy;

  if(py<0||py>400) pvy*=-1;

  if(px<20 && py>p1 && py<p1+80) pvx*=-1;
  if(px>380 && py>p2 && py<p2+80) pvx*=-1;
}

function pongDraw(){
  ctx.clearRect(0,0,400,400);
  ctx.fillRect(10,p1,10,80);
  ctx.fillRect(380,p2,10,80);
  ctx.beginPath();
  ctx.arc(px,py,8,0,Math.PI*2);
  ctx.fill();
}

/* ========= LOOP ========= */
function reset(){
  if(current==="snake") snakeInit();
  if(current==="tetris") tetrisInit();
  if(current==="breakout") breakoutInit();
  if(current==="pong") pongInit();
}

function loop(){
  if(current==="snake"){ snakeUpdate(); snakeDraw(); }
  if(current==="tetris"){ tetrisUpdate(); tetrisDraw(); }
  if(current==="breakout"){ breakoutUpdate(); breakoutDraw(); }
  if(current==="pong"){ pongUpdate(); pongDraw(); }
  requestAnimationFrame(loop);
}

reset();
loop();

</script>
</body>
</html>
"""

components.html(GAME_HTML, height=600)
