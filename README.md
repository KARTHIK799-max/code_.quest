# 🎮 CodeQuest: Learn Programming Through Games

Welcome to **CodeQuest** — a modern, gamified coding education platform designed to help beginners and Computer Science students master programming fundamentals through an intuitive **Play → Code → Debug → Build** learning experience.

Created especially as a teaching architecture for 2nd-year B.Tech CSE-AI students stepping into full-stack software development!

---

## 🌟 Key Features

1. **Interactive Game: Escape the Lab**
   - Guide research robot **RX-7** out of a hazardous quarantined lab facility.
   - 6 progressively challenging levels:
     - **Level 1**: *First Steps* (Sequential Execution)
     - **Level 2**: *The Right Turn* (Directional Control)
     - **Level 3**: *The Zigzag Hallway* (Spatial Coordination & Turns)
     - **Level 4**: *Security Keycard* (Objective Satisfaction & Keys)
     - **Level 5**: *The Loop Corridor* (DRY Principle & For-Loops)
     - **Level 6**: *The Grand Escape* (Complex Maze & Reactor Core)
   - Visual 2D grid canvas with animated robot, glowing headlights, directional indicators, steel walls, and energy portals.
   - Run, Step-by-Step, Reset, Speed Control (1x, 2x, 4x), Progressive Hints, and Reference Solution viewer.

2. **100% Safe JavaScript Command Interpreter (No `eval()`)**
   - In real-world software engineering, `eval()` is a critical security vulnerability that can execute arbitrary malicious code or freeze browser tabs.
   - CodeQuest features a custom **Lexical Analyzer & AST Step Generator**:
     - Whitelist parser for `move()`, `turnRight()`, `turnLeft()`, `repeat(n)`, and `for(let i=0; i<n; i++)`.
     - Protection against infinite loops (halting problem safeguard: max 100 actions).
     - Beginner-friendly syntax error suggestions (e.g., catching case-sensitivity mistakes like `turnright` or missing parentheses `move`).

3. **Gamification & RPG Progression**
   - **XP Engine**: Mathematically modeled level formula: $\text{Level} = \lfloor\sqrt{\text{XP} / 50}\rfloor + 1$.
   - **Anti-Farming Protection**: XP is awarded only for the first victory per mission. Replaying allows practicing for 3-star ratings without artificially inflating scores.
   - **Daily Learning Streaks**: Tracks calendar activity to build consistent coding habits.
   - **9 Achievement Badges**: Unlockable milestones (e.g. *First Steps*, *Lab Escaper*, *Crash & Learn*, *Loop Luminary*, *Keymaster*, *Clean Coder*).
   - **Global Community Leaderboard**: Dynamic rankings alongside computing pioneers (Ada Lovelace, Alan Turing, Grace Hopper, Linus Torvalds).

4. **Structured B.Tech CSE Curriculum**
   - **Beginner Path**: Computational thinking, variables, memory, conditionals, loops, functions, and debugging.
   - **Intermediate Path**: Arrays, objects, searching (Linear vs Binary), and basic data structures (Stacks & Queues).
   - **Advanced Path**: Time & space complexity (Big-O analysis) and recursion.
   - Each module contains theory, code examples, interactive code challenges, and concept quizzes with instant feedback.

5. **Dual-Mode Persistence (Hybrid Offline/Online)**
   - Works **100% offline out-of-the-box** using browser `localStorage`.
   - Automatically syncs in the background with a high-performance **Python FastAPI + SQLite** backend when started!

---

## 🏗️ System Architecture (For CSE-AI Students)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                         │
│  - Tailwind CSS Dark Navy (#0B0F19) & Electric Indigo / Cyan Theme     │
│  - Interactive Grid Visualizer (2D Matrix Simulation)                  │
│  - Safe Command Interpreter (Lexer + AST Step Queue — Zero eval)       │
│  - Web Audio 8-bit Sound Synthesizer (Zero external audio files)       │
│  - Responsive Mobile / Desktop Layout & Confetti Win Celebrations      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST API (JSON)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND (Python FastAPI)                        │
│  - FastAPI REST Endpoints (/api/user, /api/progress, /api/leaderboard) │
│  - Anti-farming XP validator and achievement engine                    │
│  - CORS middleware enabled for local development                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQL
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         DATABASE (SQLite)                              │
│  - codequest.db (Users, Completed Missions, Achievements)              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Directory Structure

```
codequest/
├── backend/                         # Python FastAPI Backend
│   ├── main.py                     # API routes & app configuration
│   ├── database.py                 # SQLite tables & database initialization
│   ├── codequest.db                # Auto-generated SQLite database
│   ├── test_backend.py             # Database unit verification test
│   ├── test_api.py                 # FastAPI endpoints & anti-farming test
│   └── requirements.txt            # Python dependencies (fastapi, uvicorn)
│
├── frontend/                        # Modern React Frontend (Vite)
│   ├── index.html                  # HTML entry point with fonts & meta
│   ├── vite.config.js              # Vite server & build settings
│   ├── tailwind.config.js          # Custom colors, shadows & animations
│   ├── postcss.config.js           # PostCSS configuration
│   ├── package.json                # Node dependencies & scripts
│   └── src/
│       ├── main.jsx                # React root mount
│       ├── App.jsx                 # App shell, tab router, toast notifications
│       ├── index.css               # Tailwind directives & glassmorphic styles
│       ├── components/
│       │   ├── Navbar.jsx          # Top navigation, streak & XP indicators
│       │   ├── LandingPage.jsx     # Hero section with live interactive teaser
│       │   ├── Dashboard.jsx       # Student dashboard & recommended missions
│       │   ├── GamePlayground.jsx  # "Escape the Lab" core game container
│       │   ├── MazeCanvas.jsx      # 2D Grid visualizer with animated robot
│       │   ├── CodeEditor.jsx      # Beginner editor with quick snippets
│       │   ├── TerminalOutput.jsx  # Step-by-step console & debugger
│       │   ├── LearningPaths.jsx   # Beginner / Intermediate / Advanced tracks
│       │   ├── LessonModal.jsx     # Theory, challenge & quiz modal
│       │   ├── Challenges.jsx      # Algorithm problem solver
│       │   ├── Leaderboard.jsx     # Ranked leaderboard
│       │   └── Profile.jsx         # Profile stats, badges & progress reset
│       ├── game/
│       │   ├── interpreter.js      # Safe AST / Token command parser (No eval)
│       │   ├── levels.js           # 6 Escape the Lab progressive levels
│       │   └── test_interpreter.js # Automated unit tests for interpreter
│       ├── services/
│       │   ├── stateContext.jsx    # React Context for global state & XP
│       │   ├── storage.js          # LocalStorage + backend sync
│       │   └── sound.js            # 8-bit Web Audio synth sound generator
│       └── data/
│           ├── curriculum.js       # Complete CSE lesson database
│           └── achievements.js     # Badge definitions & unlock conditions
│
└── README.md                       # Comprehensive guide
```

---

## 🚀 How to Run in VS Code

### Prerequisites
Make sure you have installed on your machine:
- **Node.js** (v18 or newer)
- **Python** (v3.10 or newer)

---

### Step 1: Open the Project in VS Code
1. Launch VS Code.
2. Go to **File → Open Folder...** and select `c:\Users\karth\Desktop\codequest`.

---

### Step 2: Start the Frontend (Vite + React)
1. Open a new terminal in VS Code:
   - Shortcut: `` Ctrl + ` `` (Backtick) or **Terminal → New Terminal**.
2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
3. (Optional if already installed) Install dependencies:
   ```bash
   npm install
   ```
4. Start the local Vite development server:
   ```bash
   npm run dev
   ```
5. Open your web browser and go to:
   👉 **http://localhost:5173**

---

### Step 3: Start the Backend (FastAPI + SQLite)
*Note: The frontend is fully functional even without the backend running, but starting the backend enables multi-session SQLite persistence and live API endpoints!*

1. In VS Code, click the **`+`** icon in the terminal panel to open a **Second Terminal**.
2. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
3. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. You can view the interactive Swagger API documentation at:
   👉 **http://localhost:8000/docs**

---

## 🧪 Running Automated Tests

### 1. Test the Safe Command Interpreter (Node.js)
In the `frontend` folder:
```bash
cd frontend
node src/game/test_interpreter.js
```
*Verifies 13 test cases including sequential actions, loop unrolling, rejection of `eval()`, blocking DOM tampering, typo suggestions, and max-step execution limits.*

### 2. Test the SQLite Database & FastAPI Endpoints (Python)
In the `backend` folder:
```bash
cd backend
python test_backend.py
python test_api.py
```
*Verifies database initialization, health check, user profile fetch, leaderboard rankings, and anti-farming rules (ensuring 0 duplicate XP for replayed levels).*

### 3. Verify Production Frontend Build
In the `frontend` folder:
```bash
cd frontend
npm run build
```
*Verifies zero JSX errors, type safety, and optimal asset bundling.*

---

## 💡 How "Escape the Lab" Works

### Supported Commands
| Command | What it does | Example |
| :--- | :--- | :--- |
| `move()` | Moves the robot 1 tile in the direction it is currently facing | `move();` |
| `turnRight()` | Rotates the robot 90° clockwise without changing its tile position | `turnRight();` |
| `turnLeft()` | Rotates the robot 90° counter-clockwise | `turnLeft();` |
| `for (...)` | Repeats an action block $N$ times | `for (let i = 0; i < 4; i++) { move(); }` |

### Collision & Boundary Rules
- Moving into a wall tile (`■`) causes a **collision crash** with visual feedback, 8-bit sound effect, and informative console diagnostics.
- Attempting to step outside the grid perimeter triggers an **out-of-bounds warning**.
- Reaching the glowing Cyan exit portal (`🌀`) with all required keycards satisfies the mission win condition!

---

## 🔧 Troubleshooting Tips

1. **Port 5173 already in use**:
   - Vite will automatically prompt or switch to `http://localhost:5174`. Check the terminal output for the active URL.
2. **Backend "Uvicorn not found"**:
   - Ensure your Python Scripts folder is in your Windows `PATH`, or run via `python -m uvicorn main:app --reload --port 8000`.
3. **Sound not playing**:
   - Modern browsers require one user interaction (click) on the page before playing audio. Click anywhere on the screen or toggle the sound button in the navbar.
4. **Resetting your progress**:
   - Go to the **Profile** tab in the app and click **Reset Progress** to reset all completed missions, XP, and badges back to initial state.

---

## 🎓 Learning Takeaways for CSE-AI Students
- **State Management**: See how React Context (`useGameState`) centralizes user levels, XP math, and streak calculations cleanly across all components.
- **Lexical Analysis**: Understand how compilers and interpreters tokenize code safely instead of blindly evaluating raw user text.
- **Clean Architecture**: Notice how business logic (game simulation, level definitions, curriculum) is completely decoupled from the UI presentation components.
