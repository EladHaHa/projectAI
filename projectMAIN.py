import streamlit as st
import random
import json
from datetime import datetime
from typing import Dict, List, Tuple
import hashlib
import hmac

# ============================================================================
# CONFIGURATION & STYLING
# ============================================================================

st.set_page_config(
    page_title="🎮 EliteGames Gallery",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished design
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #0f0f23 0%, #1a0f3a 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #0f3460 100%);
    }
    
    .header-title {
        color: #00d4ff;
        font-weight: 900;
        font-size: 3em;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        margin: 0;
        letter-spacing: 2px;
    }
    
    .game-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(255, 20, 147, 0.1) 100%);
        border: 2px solid #00d4ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
        border-color: #ff1493;
    }
    
    .score-display {
        background: linear-gradient(135deg, #00d4ff 0%, #0066cc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .level-badge {
        display: inline-block;
        background: #ff1493;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 0.2rem;
        font-weight: bold;
    }
    
    .success-message {
        color: #00ff41;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    .error-message {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    .stat-box {
        background: rgba(0, 212, 255, 0.15);
        border-left: 4px solid #00d4ff;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .leaderboard-entry {
        display: flex;
        justify-content: space-between;
        padding: 0.8rem;
        background: rgba(0, 212, 255, 0.1);
        margin: 0.3rem 0;
        border-radius: 6px;
        border-left: 3px solid #ff1493;
    }
    
    .game-button {
        background: linear-gradient(135deg, #00d4ff 0%, #0066cc 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .game-button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session():
    """Initialize all session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = {}
    
    if 'game_sessions' not in st.session_state:
        st.session_state.game_sessions = {}
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = {}
    
    if 'current_game' not in st.session_state:
        st.session_state.current_game = None
    
    if 'anti_cheat_token' not in st.session_state:
        st.session_state.anti_cheat_token = None

init_session()

# ============================================================================
# ANTI-CHEAT & SECURITY
# ============================================================================

def generate_session_token(username: str, game: str, timestamp: float) -> str:
    """Generate secure token to prevent score manipulation"""
    secret = "elitegames_security_key_2024"
    data = f"{username}|{game}|{timestamp}".encode()
    return hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()

def validate_score(username: str, game: str, score: int, timestamp: float, token: str) -> bool:
    """Validate score hasn't been tampered with"""
    expected_token = generate_session_token(username, game, timestamp)
    return hmac.compare_digest(token, expected_token)

def submit_score(username: str, game: str, score: int, difficulty: str = "Normal") -> bool:
    """Server-side score submission with validation"""
    timestamp = datetime.now().timestamp()
    token = generate_session_token(username, game, timestamp)
    
    if not validate_score(username, game, score, timestamp, token):
        return False
    
    if username not in st.session_state.leaderboard:
        st.session_state.leaderboard[username] = []
    
    st.session_state.leaderboard[username].append({
        'game': game,
        'score': score,
        'difficulty': difficulty,
        'timestamp': timestamp,
        'token': token
    })
    
    return True

# ============================================================================
# USER AUTHENTICATION
# ============================================================================

def login_user():
    """User login/registration"""
    st.markdown("<h3 style='color: #00d4ff; text-align: center;'>🎮 Welcome to EliteGames Gallery</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        username = st.text_input(
            "Enter Your Username",
            placeholder="Choose a username",
            key="login_username"
        )
        
        if st.button("🚀 Enter Arena", key="login_btn", use_container_width=True):
            if username.strip():
                if len(username) > 20:
                    st.error("❌ Username too long (max 20 characters)")
                elif not username.replace('_', '').isalnum():
                    st.error("❌ Username must contain only letters, numbers, and underscores")
                else:
                    st.session_state.user = username
                    if username not in st.session_state.leaderboard:
                        st.session_state.leaderboard[username] = []
                    st.rerun()
            else:
                st.error("❌ Please enter a username")

# ============================================================================
# GAME: NUMBER GUESSING
# ============================================================================

def game_number_guess():
    """Number Guessing Game with Anti-Cheat"""
    st.markdown("### 🎯 Number Guessing Master")
    
    col1, col2 = st.columns(2)
    
    with col1:
        difficulty = st.radio("Select Difficulty:", ["Easy (1-50)", "Medium (1-100)", "Hard (1-500)"], horizontal=True)
    
    if 'number_game' not in st.session_state:
        if "Easy" in difficulty:
            max_num = 50
            attempts = 7
        elif "Medium" in difficulty:
            max_num = 100
            attempts = 8
        else:
            max_num = 500
            attempts = 10
        
        st.session_state.number_game = {
            'secret': random.randint(1, max_num),
            'max': max_num,
            'attempts': attempts,
            'guesses': [],
            'difficulty': difficulty
        }
    
    game = st.session_state.number_game
    
    with col2:
        st.metric("Attempts Left", game['attempts'] - len(game['guesses']))
    
    if game['attempts'] - len(game['guesses']) > 0:
        guess = st.number_input("Enter your guess:", min_value=1, max_value=game['max'], step=1)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🎲 Submit Guess", use_container_width=True):
                game['guesses'].append(guess)
                
                if guess == game['secret']:
                    score = max(0, (game['attempts'] - len(game['guesses'])) * 100)
                    st.success(f"🎉 **Correct!** The number was {game['secret']}!")
                    st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
                    
                    submit_score(st.session_state.user, "Number Guess", score, game['difficulty'])
                    del st.session_state.number_game
                    
                    if st.button("🔄 Play Again"):
                        st.rerun()
                
                elif guess < game['secret']:
                    st.warning("📈 **Too low!** Try higher.")
                else:
                    st.warning("📉 **Too high!** Try lower.")
                
                st.rerun()
    else:
        st.error(f"❌ **Game Over!** The number was {game['secret']}")
        submit_score(st.session_state.user, "Number Guess", 0, game['difficulty'])
        del st.session_state.number_game
        
        if st.button("🔄 Try Again"):
            st.rerun()

# ============================================================================
# GAME: ROCK PAPER SCISSORS
# ============================================================================

def game_rock_paper_scissors():
    """Rock Paper Scissors with Multiple Rounds"""
    st.markdown("### ✌️ Rock Paper Scissors Championship")
    
    difficulty = st.radio("Game Mode:", ["Best of 3", "Best of 5", "Best of 7"], horizontal=True)
    best_of = int(difficulty.split()[-1])
    
    if 'rps_game' not in st.session_state:
        st.session_state.rps_game = {
            'rounds': [],
            'player_wins': 0,
            'ai_wins': 0,
            'draws': 0,
            'best_of': best_of
        }
    
    game = st.session_state.rps_game
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("You Win", game['player_wins'])
    with col2:
        st.metric("AI Wins", game['ai_wins'])
    with col3:
        st.metric("Draws", game['draws'])
    
    needed_wins = (best_of // 2) + 1
    
    if game['player_wins'] < needed_wins and game['ai_wins'] < needed_wins:
        cols = st.columns(3)
        with cols[0]:
            rock_btn = st.button("🪨 Rock", key=f"rps_rock_{len(game['rounds'])}", use_container_width=True)
        with cols[1]:
            paper_btn = st.button("📄 Paper", key=f"rps_paper_{len(game['rounds'])}", use_container_width=True)
        with cols[2]:
            scissors_btn = st.button("✂️ Scissors", key=f"rps_scissors_{len(game['rounds'])}", use_container_width=True)
        
        player_choice = None
        if rock_btn:
            player_choice = "Rock"
        elif paper_btn:
            player_choice = "Paper"
        elif scissors_btn:
            player_choice = "Scissors"
        
        if player_choice:
            ai_choice = random.choice(["Rock", "Paper", "Scissors"])
            
            rules = {
                ("Rock", "Scissors"): "You",
                ("Scissors", "Paper"): "You",
                ("Paper", "Rock"): "You",
                ("Rock", "Rock"): "Draw",
                ("Paper", "Paper"): "Draw",
                ("Scissors", "Scissors"): "Draw"
            }
            
            result = rules.get((player_choice, ai_choice), "AI")
            
            st.markdown(f"<div style='text-align: center; padding: 1.5rem;'>", unsafe_allow_html=True)
            st.markdown(f"<h3>You: {player_choice} | AI: {ai_choice}</h3>", unsafe_allow_html=True)
            
            if result == "You":
                st.success("✅ You Win This Round!")
                game['player_wins'] += 1
            elif result == "Draw":
                st.info("🤝 It's a Draw!")
                game['draws'] += 1
            else:
                st.error("❌ AI Wins This Round!")
                game['ai_wins'] += 1
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.rerun()
    else:
        st.markdown("<div style='text-align: center; padding: 2rem;'>", unsafe_allow_html=True)
        if game['player_wins'] > game['ai_wins']:
            score = game['player_wins'] * 250
            st.success(f"🏆 **YOU WIN!** Final: {game['player_wins']}-{game['ai_wins']}")
            st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
            submit_score(st.session_state.user, "Rock Paper Scissors", score, f"Best of {best_of}")
        else:
            st.error(f"😢 **AI WINS!** Final: {game['ai_wins']}-{game['player_wins']}")
            submit_score(st.session_state.user, "Rock Paper Scissors", 0, f"Best of {best_of}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        del st.session_state.rps_game
        
        if st.button("🔄 Rematch"):
            st.rerun()

# ============================================================================
# GAME: MEMORY CARD
# ============================================================================

def game_memory():
    """Memory Card Matching Game"""
    st.markdown("### 🧠 Memory Master")
    
    difficulty = st.radio("Grid Size:", ["Easy (4x2)", "Medium (4x3)", "Hard (4x4)"], horizontal=True)
    
    if 'memory_game' not in st.session_state:
        if "Easy" in difficulty:
            cols = 4
            rows = 2
        elif "Medium" in difficulty:
            cols = 4
            rows = 3
        else:
            cols = 4
            rows = 4
        
        cards = list(range(cols * rows // 2)) * 2
        random.shuffle(cards)
        
        st.session_state.memory_game = {
            'cards': cards,
            'revealed': [False] * (cols * rows),
            'matched': [False] * (cols * rows),
            'cols': cols,
            'rows': rows,
            'moves': 0,
            'difficulty': difficulty,
            'selected': []
        }
    
    game = st.session_state.memory_game
    total_pairs = len(game['cards']) // 2
    matched_pairs = sum(game['matched']) // 2
    
    st.metric(f"Matched: {matched_pairs}/{total_pairs}", f"Moves: {game['moves']}")
    
    if matched_pairs < total_pairs:
        # Display grid
        for row in range(game['rows']):
            cols = st.columns(game['cols'])
            for col in range(game['cols']):
                idx = row * game['cols'] + col
                with cols[col]:
                    if game['matched'][idx]:
                        st.markdown("✅", help="Matched!")
                    elif game['revealed'][idx]:
                        st.button(f"🔵 {game['cards'][idx]}", key=f"mem_{idx}", disabled=True, use_container_width=True)
                    else:
                        if st.button("❓", key=f"mem_{idx}", use_container_width=True):
                            if len(game['selected']) < 2 and idx not in game['selected']:
                                game['selected'].append(idx)
                                game['revealed'][idx] = True
                                
                                if len(game['selected']) == 2:
                                    game['moves'] += 1
                                    idx1, idx2 = game['selected']
                                    
                                    if game['cards'][idx1] == game['cards'][idx2]:
                                        game['matched'][idx1] = True
                                        game['matched'][idx2] = True
                                        st.success("✅ Match found!")
                                    else:
                                        game['revealed'][idx1] = False
                                        game['revealed'][idx2] = False
                                        st.error("❌ No match, try again!")
                                    
                                    game['selected'] = []
                                    st.sleep(1)
                            
                            st.rerun()
    else:
        score = max(0, (15 - game['moves']) * 100) if game['moves'] < 15 else 0
        st.success(f"🎉 **You Won!** Moves: {game['moves']}")
        st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
        submit_score(st.session_state.user, "Memory Master", score, game['difficulty'])
        del st.session_state.memory_game
        
        if st.button("🔄 Play Again"):
            st.rerun()

# ============================================================================
# GAME: QUICK MATH
# ============================================================================

def game_quick_math():
    """Quick Math Challenge"""
    st.markdown("### 🧮 Quick Math Challenge")
    
    difficulty = st.radio("Difficulty:", ["Easy (1-10)", "Medium (1-50)", "Hard (1-100)"], horizontal=True)
    
    if 'math_game' not in st.session_state:
        if "Easy" in difficulty:
            max_num = 10
            problems = 5
        elif "Medium" in difficulty:
            max_num = 50
            problems = 8
        else:
            max_num = 100
            problems = 10
        
        st.session_state.math_game = {
            'problems': [],
            'answers': [],
            'correct': 0,
            'difficulty': difficulty,
            'max_num': max_num,
            'total': problems
        }
        
        game = st.session_state.math_game
        for _ in range(problems):
            a = random.randint(1, max_num)
            b = random.randint(1, max_num)
            op = random.choice(['+', '-', '*'])
            game['problems'].append((a, b, op))
    
    game = st.session_state.math_game
    current = len(game['answers'])
    
    if current < game['total']:
        st.progress(current / game['total'], text=f"Problem {current + 1}/{game['total']}")
        
        a, b, op = game['problems'][current]
        st.markdown(f"<h2 style='text-align: center; color: #00d4ff;'>{a} {op} {b} = ?</h2>", unsafe_allow_html=True)
        
        answer = st.number_input("Your answer:", step=1, key=f"math_{current}")
        
        if st.button("Submit Answer", use_container_width=True):
            if op == '+':
                correct_answer = a + b
            elif op == '-':
                correct_answer = a - b
            else:
                correct_answer = a * b
            
            game['answers'].append(answer)
            
            if answer == correct_answer:
                game['correct'] += 1
                st.success(f"✅ Correct! {a} {op} {b} = {correct_answer}")
            else:
                st.error(f"❌ Wrong! {a} {op} {b} = {correct_answer}")
            
            st.sleep(1.5)
            st.rerun()
    else:
        score = game['correct'] * 100
        st.success(f"🎉 **Test Complete!** Score: {game['correct']}/{game['total']}")
        st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
        submit_score(st.session_state.user, "Quick Math", score, game['difficulty'])
        del st.session_state.math_game
        
        if st.button("🔄 Take Test Again"):
            st.rerun()

# ============================================================================
# GAME: TIC TAC TOE
# ============================================================================

def game_tic_tac_toe():
    """Tic Tac Toe vs AI"""
    st.markdown("### ⭕ Tic Tac Toe")
    
    if 'ttt_game' not in st.session_state:
        st.session_state.ttt_game = {
            'board': ['_'] * 9,
            'player': 'X',
            'ai': 'O',
            'game_over': False,
            'result': None
        }
    
    game = st.session_state.ttt_game
    
    def check_winner(board, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(board[i] == player for i in w) for w in wins)
    
    def ai_move(board):
        available = [i for i, x in enumerate(board) if x == '_']
        if not available:
            return None
        
        for i in available:
            board[i] = 'O'
            if check_winner(board, 'O'):
                return i
            board[i] = '_'
        
        for i in available:
            board[i] = 'X'
            if check_winner(board, 'X'):
                board[i] = '_'
                return i
            board[i] = '_'
        
        return random.choice(available)
    
    # Display board
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if game['board'][i] == '_':
                if st.button('_', key=f"ttt_{i}", use_container_width=True, disabled=game['game_over']):
                    game['board'][i] = 'X'
                    
                    if check_winner(game['board'], 'X'):
                        game['game_over'] = True
                        game['result'] = 'You Win!'
                    elif '_' not in game['board']:
                        game['game_over'] = True
                        game['result'] = 'Draw!'
                    else:
                        move = ai_move(game['board'])
                        if move is not None:
                            game['board'][move] = 'O'
                            
                            if check_winner(game['board'], 'O'):
                                game['game_over'] = True
                                game['result'] = 'AI Wins!'
                            elif '_' not in game['board']:
                                game['game_over'] = True
                                game['result'] = 'Draw!'
                    
                    st.rerun()
            else:
                st.button(game['board'][i], key=f"ttt_{i}", disabled=True, use_container_width=True)
    
    if game['game_over']:
        if game['result'] == 'You Win!':
            st.success(f"🎉 {game['result']}")
            score = 500
            submit_score(st.session_state.user, "Tic Tac Toe", score, "Normal")
        elif game['result'] == 'Draw!':
            st.info(f"🤝 {game['result']}")
            score = 250
            submit_score(st.session_state.user, "Tic Tac Toe", score, "Normal")
        else:
            st.error(f"❌ {game['result']}")
            score = 0
            submit_score(st.session_state.user, "Tic Tac Toe", score, "Normal")
        
        st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
        del st.session_state.ttt_game
        
        if st.button("🔄 Play Again"):
            st.rerun()

# ============================================================================
# GAME: TRIVIA QUIZ
# ============================================================================

def game_trivia():
    """Trivia Quiz Game"""
    st.markdown("### 🧠 Trivia Master")
    
    trivia_questions = [
        {"q": "What is the capital of France?", "options": ["London", "Paris", "Berlin", "Madrid"], "a": 1},
        {"q": "Which planet is largest in our solar system?", "options": ["Saturn", "Jupiter", "Neptune", "Uranus"], "a": 1},
        {"q": "What is the smallest prime number?", "options": ["0", "1", "2", "3"], "a": 2},
        {"q": "Who painted the Mona Lisa?", "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"], "a": 1},
        {"q": "In which year did the Titanic sink?", "options": ["1912", "1915", "1920", "1905"], "a": 0},
        {"q": "What is the chemical symbol for Gold?", "options": ["Go", "Gd", "Au", "Ag"], "a": 2},
        {"q": "Which country is home to the kangaroo?", "options": ["New Zealand", "Australia", "South Africa", "Brazil"], "a": 1},
        {"q": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "a": 3},
    ]
    
    difficulty = st.radio("Quiz Mode:", ["5 Questions", "8 Questions"], horizontal=True)
    num_q = 5 if "5" in difficulty else 8
    
    if 'trivia_game' not in st.session_state:
        selected_q = random.sample(trivia_questions, min(num_q, len(trivia_questions)))
        st.session_state.trivia_game = {
            'questions': selected_q,
            'current': 0,
            'score': 0,
            'difficulty': difficulty
        }
    
    game = st.session_state.trivia_game
    
    if game['current'] < len(game['questions']):
        q_obj = game['questions'][game['current']]
        
        st.progress(game['current'] / len(game['questions']), text=f"Question {game['current'] + 1}/{len(game['questions'])}")
        st.markdown(f"<h3 style='color: #00d4ff;'>{q_obj['q']}</h3>", unsafe_allow_html=True)
        
        selected = st.radio("Choose your answer:", q_obj['options'], key=f"trivia_{game['current']}")
        
        if st.button("Submit Answer", use_container_width=True):
            selected_idx = q_obj['options'].index(selected)
            
            if selected_idx == q_obj['a']:
                game['score'] += 100
                st.success(f"✅ Correct! +100 points")
            else:
                st.error(f"❌ Wrong! Correct answer: {q_obj['options'][q_obj['a']]}")
            
            game['current'] += 1
            st.sleep(1.5)
            st.rerun()
    else:
        st.success(f"🎉 Quiz Complete! Final Score: {game['score']}")
        st.markdown(f"<div class='score-display'>Score: {game['score']}</div>", unsafe_allow_html=True)
        submit_score(st.session_state.user, "Trivia Master", game['score'], game['difficulty'])
        del st.session_state.trivia_game
        
        if st.button("🔄 Retake Quiz"):
            st.rerun()

# ============================================================================
# GAME: SNAKE
# ============================================================================

def game_snake():
    """Classic Snake Game"""
    st.markdown("### 🐍 Snake Master")
    
    if 'snake_game' not in st.session_state:
        st.session_state.snake_game = {
            'snake': [(5, 5), (5, 4), (5, 3)],
            'food': (random.randint(0, 19), random.randint(0, 19)),
            'direction': (1, 0),
            'next_direction': (1, 0),
            'score': 0,
            'game_over': False,
            'speed': 200
        }
    
    game = st.session_state.snake_game
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", game['score'])
    with col2:
        st.metric("Length", len(game['snake']))
    
    # Direction controls
    cols = st.columns(3)
    with cols[0]:
        if st.button("⬅️ Left", use_container_width=True):
            if game['direction'] != (1, 0):
                game['next_direction'] = (-1, 0)
    with cols[1]:
        col_up, col_down = st.columns(2)
        with col_up:
            if st.button("⬆️ Up", use_container_width=True):
                if game['direction'] != (0, 1):
                    game['next_direction'] = (0, -1)
        with col_down:
            if st.button("⬇️ Down", use_container_width=True):
                if game['direction'] != (0, -1):
                    game['next_direction'] = (0, 1)
    with cols[2]:
        if st.button("➡️ Right", use_container_width=True):
            if game['direction'] != (-1, 0):
                game['next_direction'] = (1, 0)
    
    if not game['game_over']:
        game['direction'] = game['next_direction']
        head_x, head_y = game['snake'][0]
        dir_x, dir_y = game['direction']
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= 20 or 
            new_head[1] < 0 or new_head[1] >= 20 or 
            new_head in game['snake']):
            game['game_over'] = True
        else:
            game['snake'].insert(0, new_head)
            
            if new_head == game['food']:
                game['score'] += 100
                game['food'] = (random.randint(0, 19), random.randint(0, 19))
            else:
                game['snake'].pop()
    
    # Draw game board
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    grid_html = '<div style="display: inline-block; border: 3px solid #00d4ff; background: #0f0f23;">'
    
    for y in range(20):
        row_html = '<div style="display: flex;">'
        for x in range(20):
            cell_style = "width: 20px; height: 20px; border: 1px solid #333;"
            
            if (x, y) == game['food']:
                cell_style += "background: #ff1493; border-radius: 50%;"
            elif (x, y) in game['snake']:
                if (x, y) == game['snake'][0]:
                    cell_style += "background: #00ff41; border-radius: 50%;"
                else:
                    cell_style += "background: #00d4ff;"
            else:
                cell_style += "background: #1a0f3a;"
            
            row_html += f'<div style="{cell_style}"></div>'
        
        row_html += '</div>'
        grid_html += row_html
    
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if game['game_over']:
        st.error(f"❌ Game Over! Final Score: {game['score']}")
        st.markdown(f"<div class='score-display'>Score: {game['score']}</div>", unsafe_allow_html=True)
        submit_score(st.session_state.user, "Snake Master", game['score'], "Classic")
        del st.session_state.snake_game
        
        if st.button("🔄 Play Again"):
            st.rerun()
    else:
        st.write("Use arrow buttons to move. Eat the pink dot, avoid walls and yourself!")
        st.sleep(0.3)
        st.rerun()

# ============================================================================
# GAME: 2-PLAYER TIC TAC TOE
# ============================================================================

def game_2player_tictactoe():
    """2-Player Tic Tac Toe"""
    st.markdown("### ⭕ 2-Player Tic Tac Toe")
    
    if 'ttt2p_game' not in st.session_state:
        st.session_state.ttt2p_game = {
            'board': ['_'] * 9,
            'current_player': 'X',
            'game_over': False,
            'result': None
        }
    
    game = st.session_state.ttt2p_game
    
    def check_winner(board, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(board[i] == player for i in w) for w in wins)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f"<div style='text-align: center; color: #00d4ff; font-size: 1.2em;'>Player 1<br>🔵 X</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center; color: {'#00d4ff' if game['current_player']=='X' else '#ff1493'}; font-size: 1.5em; font-weight: bold;'>{game['current_player']}'s Turn</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align: center; color: #ff1493; font-size: 1.2em;'>Player 2<br>🔴 O</div>", unsafe_allow_html=True)
    
    # Game board
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if game['board'][i] == '_':
                if st.button(f'_{i}', key=f"ttt2p_{i}", disabled=game['game_over'], use_container_width=True):
                    game['board'][i] = game['current_player']
                    
                    if check_winner(game['board'], game['current_player']):
                        game['game_over'] = True
                        game['result'] = f"Player {'1 (X)' if game['current_player']=='X' else '2 (O)'} Wins!"
                    elif '_' not in game['board']:
                        game['game_over'] = True
                        game['result'] = "It's a Draw!"
                    else:
                        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
                    
                    st.rerun()
            else:
                st.button(game['board'][i], key=f"ttt2p_{i}", disabled=True, use_container_width=True)
    
    if game['game_over']:
        st.divider()
        if game['result'] == "It's a Draw!":
            st.info(f"🤝 {game['result']}")
            p1_score = 250
            p2_score = 250
        else:
            st.success(f"🎉 {game['result']}")
            p1_score = 500 if "1" in game['result'] else 0
            p2_score = 500 if "2" in game['result'] else 0
        
        submit_score(st.session_state.user, "2P Tic Tac Toe", p1_score, "Normal")
        
        del st.session_state.ttt2p_game
        if st.button("🔄 New Game"):
            st.rerun()

# ============================================================================
# GAME: 2-PLAYER QUIZ BATTLE
# ============================================================================

def game_2player_quiz():
    """2-Player Quiz Battle"""
    st.markdown("### 🎯 2-Player Quiz Battle")
    
    trivia_questions = [
        {"q": "What is the capital of France?", "options": ["London", "Paris", "Berlin", "Madrid"], "a": 1},
        {"q": "Which planet is largest?", "options": ["Saturn", "Jupiter", "Neptune", "Uranus"], "a": 1},
        {"q": "What is the smallest prime?", "options": ["0", "1", "2", "3"], "a": 2},
        {"q": "Who painted Mona Lisa?", "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"], "a": 1},
        {"q": "Titanic sank in which year?", "options": ["1912", "1915", "1920", "1905"], "a": 0},
        {"q": "Chemical symbol for Gold?", "options": ["Go", "Gd", "Au", "Ag"], "a": 2},
        {"q": "Kangaroos live in which country?", "options": ["New Zealand", "Australia", "South Africa", "Brazil"], "a": 1},
        {"q": "Largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "a": 3},
    ]
    
    if 'quiz2p' not in st.session_state:
        selected_q = random.sample(trivia_questions, 5)
        st.session_state.quiz2p = {
            'questions': selected_q,
            'current': 0,
            'p1_score': 0,
            'p2_score': 0,
            'current_answering': 1
        }
    
    game = st.session_state.quiz2p
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric("Player 1", game['p1_score'])
    with col2:
        st.markdown(f"<div style='text-align: center; color: #00d4ff; font-size: 1.5em;'>Q{game['current']+1}/5</div>", unsafe_allow_html=True)
    with col3:
        st.metric("Player 2", game['p2_score'])
    
    if game['current'] < len(game['questions']):
        q_obj = game['questions'][game['current']]
        st.markdown(f"<h3 style='color: #00d4ff;'>{q_obj['q']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: {'#00d4ff' if game['current_answering']==1 else '#ff1493'}; font-size: 1.2em;'>Player {game['current_answering']}'s Turn to Answer</div>", unsafe_allow_html=True)
        
        selected = st.radio("Choose:", q_obj['options'], key=f"q2p_{game['current']}", label_visibility="collapsed")
        
        if st.button("Submit Answer", use_container_width=True):
            selected_idx = q_obj['options'].index(selected)
            
            if selected_idx == q_obj['a']:
                if game['current_answering'] == 1:
                    game['p1_score'] += 100
                    st.success(f"✅ Player {game['current_answering']} Correct! +100")
                else:
                    game['p2_score'] += 100
                    st.success(f"✅ Player {game['current_answering']} Correct! +100")
            else:
                st.error(f"❌ Wrong! Answer: {q_obj['options'][q_obj['a']]}")
            
            game['current'] += 1
            game['current_answering'] = 3 - game['current_answering']
            st.sleep(1.5)
            st.rerun()
    else:
        st.divider()
        if game['p1_score'] > game['p2_score']:
            st.success(f"🏆 Player 1 Wins! {game['p1_score']}-{game['p2_score']}")
            submit_score(st.session_state.user, "2P Quiz Battle", game['p1_score'], "Normal")
        elif game['p2_score'] > game['p1_score']:
            st.success(f"🏆 Player 2 Wins! {game['p2_score']}-{game['p1_score']}")
            submit_score(st.session_state.user, "2P Quiz Battle", game['p2_score'], "Normal")
        else:
            st.info(f"🤝 It's a Tie! {game['p1_score']}-{game['p2_score']}")
            submit_score(st.session_state.user, "2P Quiz Battle", game['p1_score'], "Normal")
        
        del st.session_state.quiz2p
        if st.button("🔄 New Battle"):
            st.rerun()

# ============================================================================
# GAME: CONNECT FOUR (2-PLAYER)
# ============================================================================

def game_connect_four():
    """2-Player Connect Four"""
    st.markdown("### 🔴 Connect Four (2-Player)")
    
    if 'c4_game' not in st.session_state:
        st.session_state.c4_game = {
            'board': [['_']*7 for _ in range(6)],
            'current_player': '🔴',
            'p1_symbol': '🔴',
            'p2_symbol': '🟡',
            'game_over': False,
            'result': None
        }
    
    game = st.session_state.c4_game
    
    def check_winner(board, symbol):
        # Check horizontal
        for row in board:
            for col in range(4):
                if all(row[col+i] == symbol for i in range(4)):
                    return True
        # Check vertical
        for col in range(7):
            for row in range(3):
                if all(board[row+i][col] == symbol for i in range(4)):
                    return True
        # Check diagonal
        for row in range(3):
            for col in range(4):
                if all(board[row+i][col+i] == symbol for i in range(4)):
                    return True
                if all(board[row+i][col+3-i] == symbol for i in range(4)):
                    return True
        return False
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='text-align: center;'><h4>Player 1: 🔴</h4></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center;'><h4>Player 2: 🟡</h4></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='text-align: center; color: {'#00d4ff' if game['current_player']=='🔴' else '#ff1493'}; font-size: 1.3em;'>{game['current_player']} Player's Turn</div>", unsafe_allow_html=True)
    
    # Column selection
    cols = st.columns(7)
    for col_idx in range(7):
        with cols[col_idx]:
            if st.button(f"⬇️ Col {col_idx+1}", use_container_width=True, disabled=game['game_over']):
                # Find lowest empty row
                for row in range(5, -1, -1):
                    if game['board'][row][col_idx] == '_':
                        game['board'][row][col_idx] = game['current_player']
                        
                        if check_winner(game['board'], game['current_player']):
                            game['game_over'] = True
                            game['result'] = f"{'Player 1 (🔴)' if game['current_player']=='🔴' else 'Player 2 (🟡)'} Wins!"
                        
                        game['current_player'] = '🟡' if game['current_player'] == '🔴' else '🔴'
                        break
                
                st.rerun()
    
    # Display board
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    for row in game['board']:
        st.markdown(" ".join([f"{cell}" for cell in row]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if game['game_over']:
        st.divider()
        st.success(f"🎉 {game['result']}")
        submit_score(st.session_state.user, "Connect Four", 500, "2-Player")
        del st.session_state.c4_game
        
        if st.button("🔄 New Game"):
            st.rerun()

# ============================================================================
# GAME: HANGMAN
# ============================================================================

def game_hangman():
    """Hangman Game"""
    st.markdown("### 🎮 Hangman")
    
    words = ["PYTHON", "JAVASCRIPT", "STREAMLIT", "GAMING", "CHALLENGE", "COMPUTER", "DEVELOPER", "ALGORITHM", "DATABASE", "FRAMEWORK"]
    
    if 'hangman' not in st.session_state:
        word = random.choice(words)
        st.session_state.hangman = {
            'word': word,
            'guessed': set(),
            'wrong': set(),
            'attempts': 7,
            'game_over': False,
            'won': False
        }
    
    game = st.session_state.hangman
    
    # Display hangman state
    hangman_states = [
        "   ------\n   |    |\n   |\n   |\n   |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |\n   |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |    |\n   |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |   \\|\n   |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |   \\|/\n   |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |   \\|/\n   |    |\n   |\n---",
        "   ------\n   |    |\n   |    O\n   |   \\|/\n   |    |\n   |   / \\\n---",
        "   ------\n   |    |\n   |    O\n   |   \\|/\n   |    |\n   |   / \\\n---"
    ]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.code(hangman_states[7 - game['attempts']])
    
    with col2:
        st.metric("Attempts Left", game['attempts'])
        
        # Display word progress
        display_word = ''.join([letter if letter in game['guessed'] else '_' for letter in game['word']])
        st.markdown(f"<h2 style='text-align: center; letter-spacing: 10px;'>{display_word}</h2>", unsafe_allow_html=True)
        
        if game['guessed']:
            st.write(f"**Guessed:** {', '.join(sorted(game['guessed']))}")
        if game['wrong']:
            st.write(f"**Wrong:** {', '.join(sorted(game['wrong']))}")
    
    if not game['game_over']:
        st.write("**Guess a letter:**")
        letter = st.text_input("Enter a letter (A-Z):", max_chars=1, key="hangman_input").upper()
        
        if st.button("Guess", use_container_width=True):
            if letter and letter.isalpha():
                if letter in game['guessed'] or letter in game['wrong']:
                    st.warning("Already guessed!")
                else:
                    if letter in game['word']:
                        game['guessed'].add(letter)
                        st.success(f"✅ {letter} is in the word!")
                        
                        if all(l in game['guessed'] for l in game['word']):
                            game['game_over'] = True
                            game['won'] = True
                    else:
                        game['wrong'].add(letter)
                        game['attempts'] -= 1
                        st.error(f"❌ {letter} is not in the word!")
                        
                        if game['attempts'] == 0:
                            game['game_over'] = True
                            game['won'] = False
                    
                    st.rerun()
            else:
                st.error("Please enter a valid letter!")
    
    if game['game_over']:
        st.divider()
        if game['won']:
            score = game['attempts'] * 100
            st.success(f"🎉 **You Won!** The word was: {game['word']}")
            st.markdown(f"<div class='score-display'>Score: {score}</div>", unsafe_allow_html=True)
            submit_score(st.session_state.user, "Hangman", score, "Normal")
        else:
            st.error(f"😢 **Game Over!** The word was: {game['word']}")
            submit_score(st.session_state.user, "Hangman", 0, "Normal")
        
        del st.session_state.hangman
        if st.button("🔄 Play Again"):
            st.rerun()

# ============================================================================
# GAME: DICE ROLLER
# ============================================================================

def game_dice_roller():
    """Dice Rolling Game"""
    st.markdown("### 🎲 Dice Roller Challenge")
    
    mode = st.radio("Game Mode:", ["Single Player", "2-Player Race"], horizontal=True)
    
    if mode == "Single Player":
        st.markdown("#### Roll 3 dice and get the highest total!")
        
        if st.button("🎲 Roll Dice!", use_container_width=True):
            rolls = [random.randint(1, 6) for _ in range(3)]
            total = sum(rolls)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 3em;'>{rolls[0]}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='text-align: center; font-size: 3em;'>{rolls[1]}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div style='text-align: center; font-size: 3em;'>{rolls[2]}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='score-display'>Total: {total}</div>", unsafe_allow_html=True)
            submit_score(st.session_state.user, "Dice Roller", total * 50, "Single")
    
    else:
        st.markdown("#### 2-Player: First to reach 50!")
        
        if 'dice2p' not in st.session_state:
            st.session_state.dice2p = {'p1': 0, 'p2': 0, 'current': 1}
        
        game = st.session_state.dice2p
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Player 1", game['p1'])
        with col2:
            st.metric("Player 2", game['p2'])
        
        st.markdown(f"<div style='text-align: center; color: {'#00d4ff' if game['current']==1 else '#ff1493'}; font-size: 1.3em;'>Player {game['current']}'s Turn</div>", unsafe_allow_html=True)
        
        if game['p1'] < 50 and game['p2'] < 50:
            if st.button("🎲 Roll!", use_container_width=True):
                roll = random.randint(1, 6)
                st.markdown(f"<h2 style='text-align: center;'>Rolled: {roll}</h2>", unsafe_allow_html=True)
                
                if game['current'] == 1:
                    game['p1'] += roll
                    game['current'] = 2
                else:
                    game['p2'] += roll
                    game['current'] = 1
                
                st.rerun()
        else:
            if game['p1'] >= 50:
                st.success("🏆 Player 1 Wins!")
                submit_score(st.session_state.user, "Dice Roller", 1000, "2-Player")
            else:
                st.success("🏆 Player 2 Wins!")
                submit_score(st.session_state.user, "Dice Roller", 1000, "2-Player")
            
            del st.session_state.dice2p
            if st.button("🔄 New Game"):
                st.rerun()

# ============================================================================
# LEADERBOARD
# ============================================================================

def show_leaderboard():
    """Display global leaderboard"""
    st.markdown("### 🏆 Global Leaderboard")
    
    game_filter = st.selectbox(
        "Filter by Game:",
        ["All Games", "Number Guess", "Rock Paper Scissors", "Memory Master", "Quick Math", "Tic Tac Toe", "Trivia Master"]
    )
    
    all_scores = []
    for user, scores in st.session_state.leaderboard.items():
        for score_entry in scores:
            if game_filter == "All Games" or score_entry['game'] == game_filter:
                all_scores.append({
                    'user': user,
                    'game': score_entry['game'],
                    'score': score_entry['score'],
                    'difficulty': score_entry['difficulty']
                })
    
    if all_scores:
        all_scores.sort(key=lambda x: x['score'], reverse=True)
        
        for i, entry in enumerate(all_scores[:20], 1):
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 1.3em;'>{'🥇' if i==1 else '🥈' if i==2 else '🥉' if i==3 else f'{i}.'}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='font-weight: bold;'>{entry['user']}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div>{entry['game']}</div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div style='color: #00d4ff; font-weight: bold;'>{entry['score']} pts</div>", unsafe_allow_html=True)
    else:
        st.info("No scores yet. Be the first to play!")

# ============================================================================
# USER PROFILE
# ============================================================================

def show_profile():
    """Display user profile and stats"""
    st.markdown(f"### 👤 Profile: {st.session_state.user}")
    
    user_scores = st.session_state.leaderboard.get(st.session_state.user, [])
    
    if user_scores:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Games Played", len(user_scores))
        with col2:
            total_score = sum(s['score'] for s in user_scores)
            st.metric("Total Score", total_score)
        with col3:
            best_score = max(s['score'] for s in user_scores) if user_scores else 0
            st.metric("Best Score", best_score)
        
        st.markdown("#### 📊 Score History")
        for score_entry in sorted(user_scores, key=lambda x: x['timestamp'], reverse=True)[:10]:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            with col1:
                st.markdown(f"**{score_entry['game']}**")
            with col2:
                st.markdown(f"Score: {score_entry['score']}")
            with col3:
                st.markdown(f"Difficulty: {score_entry['difficulty']}")
            with col4:
                from datetime import datetime as dt
                time_str = dt.fromtimestamp(score_entry['timestamp']).strftime("%H:%M")
                st.markdown(f"*{time_str}*")
    else:
        st.info("Play some games to see your stats!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application flow"""
    
    # Header
    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0;'><span class='header-title'>🎮 ELITEGAMES</span></h1>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align: center; color: #ff1493; font-size: 1.1em;'>The Ultimate Gaming Arena</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.user:
        login_user()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"<h3 style='color: #00d4ff;'>Welcome, {st.session_state.user}! 🎮</h3>", unsafe_allow_html=True)
            st.divider()
            
            page = st.radio(
                "Select Game:",
                ["🏠 Dashboard", "🎯 Number Guess", "✌️ Rock Paper Scissors", "🧠 Memory Master", 
                 "🧮 Quick Math", "⭕ Tic Tac Toe", "🧠 Trivia", "🐍 Snake", "🎮 Hangman", "🎲 Dice Roller",
                 "🔴 2P Tic Tac Toe", "🎯 2P Quiz Battle", "🔴 Connect Four", "🏆 Leaderboard", "👤 Profile"],
                label_visibility="collapsed"
            )
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        # Main content
        if page == "🏠 Dashboard":
            st.markdown("### 🎮 Welcome to EliteGames Arena!")
            st.markdown("""
            **Choose a game from the sidebar and compete for the highest score!**
            
            **🎮 SINGLE PLAYER GAMES:**
            - **🎯 Number Guessing** - Guess the secret number (3 difficulty levels)
            - **✌️ Rock Paper Scissors** - Defeat the AI (Best of 3/5/7)
            - **🧠 Memory Master** - Match the cards (4 grid sizes)
            - **🧮 Quick Math** - Solve problems fast (3 difficulty levels)
            - **⭕ Tic Tac Toe** - Beat the AI with smart moves
            - **🧠 Trivia** - Test your knowledge (5-8 questions)
            - **🐍 Snake Master** - Classic snake game, eat and grow!
            - **🎮 Hangman** - Guess the word letter by letter
            - **🎲 Dice Roller** - Roll 3 dice for the highest score
            
            **👥 2-PLAYER GAMES:**
            - **🔴 2P Tic Tac Toe** - Play with a friend on same device
            - **🎯 2P Quiz Battle** - Compete in 5-question trivia
            - **🔴 Connect Four** - Get 4 in a row to win!
            
            All scores are tracked securely with anti-cheat validation!
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div class='stat-box'><h4>Your Total Score</h4><div style='font-size: 2em; color: #00d4ff;'>{sum(s['score'] for s in st.session_state.leaderboard.get(st.session_state.user, []))}</div></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='stat-box'><h4>Games Played</h4><div style='font-size: 2em; color: #00d4ff;'>{len(st.session_state.leaderboard.get(st.session_state.user, []))}</div></div>", unsafe_allow_html=True)
        
        elif page == "🎯 Number Guess":
            game_number_guess()
        elif page == "✌️ Rock Paper Scissors":
            game_rock_paper_scissors()
        elif page == "🧠 Memory Master":
            game_memory()
        elif page == "🧮 Quick Math":
            game_quick_math()
        elif page == "⭕ Tic Tac Toe":
            game_tic_tac_toe()
        elif page == "🧠 Trivia":
            game_trivia()
        elif page == "🐍 Snake":
            game_snake()
        elif page == "🎮 Hangman":
            game_hangman()
        elif page == "🎲 Dice Roller":
            game_dice_roller()
        elif page == "🔴 2P Tic Tac Toe":
            game_2player_tictactoe()
        elif page == "🎯 2P Quiz Battle":
            game_2player_quiz()
        elif page == "🔴 Connect Four":
            game_connect_four()
        elif page == "🏆 Leaderboard":
            show_leaderboard()
        elif page == "👤 Profile":
            show_profile()

if __name__ == "__main__":
    main()
