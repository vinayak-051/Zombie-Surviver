# 🧟‍♂️ Zombie Surviver

A grid-based Pygame simulation where a human must reach a safe zone while zombies chase using **A\*** pathfinding.  
The human uses **danger-aware A\*** to avoid zombies, while the map, obstacles, zombies, and safe zone are **randomized each run** and guaranteed to be solvable.

This project provides a clean architecture, real-time visualization, and deterministic pathfinding logic suitable for AI/pathfinding coursework or game-AI experimentation.

---

## Table of Contents

- [Key Features](#key-features)  
- [Project Structure](#project-structure)  
- [Simulation Overview](#simulation-overview)  
- [Environment Generation & Logic](#environment-generation--logic)  
- [Local Setup](#local-setup)  
- [How to Use the Simulation](#how-to-use-the-simulation)  
  - [Controls](#Controls)  
  - [Game Flow](#Game-Flow)  
  - [Tips](#Tips)   
- [File Descriptions](#file-descriptions)  
- [Assets](#assets)  
- [Troubleshooting](#troubleshooting)  
---

## Key Features

- Fully randomized:
  - Human starting position  
  - Safe zone  
  - Obstacles  
  - Zombie locations  
- Human uses **A\* pathfinding + danger cost** to avoid zombies  
- Zombies use **A\*** to chase the human  
- **Thin black line** drawn along the shortest human path  
- **Solvable-map guarantee** using connectivity checks  
- Sprite-based rendering with fallback shapes if assets are missing  
- **Game Over screen** with a “New Game” button  
- Modular architecture for easy experimentation with AI/pathfinding logic  

---

## Project Structure
```
ZombieSurviver/
│
├── assets/
│ ├── brick.png
│ ├── home.jpeg
│ ├── human.png
│ └── zombie.jpeg
│
├── agent.py
├── environment.py
├── game.py
├── main.py
├── visualization.py
└── README.md
```
---

## Simulation Overview

The simulation runs on a **grid-based world**, where:

- The **human** attempts to reach the **safe zone**
- **Zombies** attempt to catch the human
- Both use **A\***, but with different heuristics:
  - Human avoids zombies via **danger-weighted nodes**
  - Zombies use pure shortest-path A\*

A turn manager updates entity movement, path recalculation, game state, and rendering at each frame.

---

## Environment Generation & Logic

- The grid is generated with **random obstacles**.
- Human, zombies, and safe zone are placed **randomly**, but only after checking that:
  - The map is **fully solvable**
  - A human → safe zone path **exists**
- Manhattan distance is used for heuristic calculations.
- A tile-claiming mechanism prevents zombies from overlapping during movement.

---
## Local Setup
### Install Dependencies 

   Install Pygame

### Run the Simulation

pip install pygame

---
## How to Use the Simulation

### Controls

- **Arrow Keys** or **W A S D** — Move the human manually
- **SPACE** — Toggle auto mode (human uses A* pathfinding)
- **ESC** or close window — Quit simulation

### Game Flow

1. **Start:** Human, zombies, obstacles, and safe zone are randomly placed.
2. **Movement:**
   - Human moves first (either manual or auto).
   - Zombies recalculate paths using A* and move toward the human.
3. **Path Visualization:** 
   - The human’s **shortest safe path** is drawn as a thin black line.
4. **Win/Loss Conditions:**
   - **Win:** Human reaches the safe zone.
   - **Loss:** A zombie catches the human.
5. **New Game:** 
   - After game over, click **“New Game”** to generate a new random environment.

### Tips

- Use **auto mode** to see the human plan paths avoiding danger.
- Observe how zombies **avoid overlapping** using the claimed-tile system.
- Maps are **always solvable**, so every game has a path from human to safe zone.
---
---

## File Descriptions

- **main.py**  
  Entry point of the simulation. Sets constants, generates a solvable map, spawns the human, zombies, obstacles, and safe zone, then starts the Pygame loop.

- **agent.py**  
  Contains the **Human** and **Zombie** classes. Handles movement, A* pathfinding, danger avoidance for humans, and tile claiming for zombies.

- **environment.py**  
  Implements the **Grid** class, obstacles, safe zone, random placement functions, and heuristic calculations like Manhattan distance. Checks map connectivity to ensure solvability.

- **game.py**  
  Manages turn-based logic: updating human and zombie positions, win/loss detection, and converting captured humans into zombies.

- **visualization.py**  
  Handles all Pygame rendering: grid, sprites, human path line, safe zone, and UI elements like New Game or Game Over screens. Loads assets with fallback shapes.

- **assets/**  
  Folder containing images for the simulation.

- **README.md**  
  This file containing project documentation.

---

## Assets

Place the following images inside the `assets/` folder:

- `brick.png` — used for obstacles
- `home.jpeg` — used for the safe zone
- `human.png` — human sprite
- `zombie.jpeg` — zombie sprite

> **Note:** If any image is missing, the program will use basic drawn shapes instead.
---
## Troubleshooting

- **Pygame window does not open**
  - Ensure Pygame is installed: `pip install pygame`
  - Verify you are using Python 3.10+  

- **Images not showing**
  - Place the required images in the `assets/` folder:
    - `brick.png`
    - `home.jpeg`
    - `human.png`
    - `zombie.jpeg`
  - If missing, the simulation will use fallback shapes.  

- **Game crashes or freezes**
  - Make sure all dependencies are installed.
  - Check that the grid size and number of zombies/obstacles are reasonable.
  - Ensure no other program is blocking Pygame from rendering.  

- **Paths not updating**
  - Auto mode must be enabled for the human to use A* pathfinding.
  - Zombies recalculate paths each turn; ensure no errors in `environment.py` or `agent.py`.  

- **Human or zombie spawn issues**
  - Map generation ensures solvable paths; if the simulation repeatedly fails, reduce obstacles or grid size.

