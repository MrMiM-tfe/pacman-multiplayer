# Pacman Multiplayer Game

final project of advance computer science class (K. N. Toosi University of Technology)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [Running the Game](#running-the-game)
7. [Game Controls](#game-controls)
8. [Server API](#server-api)

---

## Project Overview

This is a **real-time multiplayer Pacman** game built with Python, Socket.IO, and Pygame. Two human players compete in a mirrored maze, collecting points while avoiding ghosts. Ghosts roam autonomously in designated map halves.
each player can enter other player section and become ghost and chase the player.

Key components:

-   **Server**: Manages game state, ghost, and synchronizes clients via Socket.IO.
-   **Client**: Renders the game in Pygame, handles user input, and displays real-time updates.

## Features

-   **Real-Time Multiplayer**: Two players connect and play simultaneously.
-   **Autonomous Ghosts**: Four ghosts (two per half) with random but region-constrained movement.
-   **Dynamic Map**: Maze is mirrored horizontally and supports point collection (`.`).
-   **Point Collection**: Players collect dots to score; clearing half the map wins the round.
-   **Collision Detection**: Players can be caught by ghosts or collide with each other to determine wins.
-   **Score Persistence**: Winning updates user scores in SqlLite.
-   **Online/Offline Modes**: Offline fake data mode for local testing.

## Architecture

```plaintext
+--------------+              +---------------+              +---------------+
|   Client 1   | <--Socket--> |    Server     | <--Socket--> |   Client 2    |
| (Pygame GUI) |              | (Socket.IO)   |              | (Pygame GUI)  |
+--------------+              +---------------+              +---------------+
                                   |
                                   v
                           +-------------------+
                           |   SqlLite DB      |
                           +-------------------+
```

### Server Flow

1. Client connects and authenticates.
2. Upon room creation or join, server pairs users and instantiates `Game`.
3. `Game.run()` starts threads:

    - **Main Loop**: Updates players and ghosts at 60 FPS.
    - **Broadcast**: Emits `game_state` each frame.

4. Clients receive state and render.
5. Collisions and wins update DB and emit `end_game`.

### Client Flow

1. Launch `MainApp`, choose offline or login mode.
2. Navigate pages (`Login`, `Main Menu`, `Room`, `Game`).
3. In `GamePage`, render maze, players, ghosts, and UI.
4. Send direction changes to server.
5. Handle `game_state` and `end_game` events.

## Tech Stack

-   **Python 3.10+**
-   **Pygame**: Game rendering and input.
-   **python-socketio**: Client/server communication.
-   **Threading**: Server game loop threads.
-   **SqlLite**: Persistent user scores.
-   **SQLAlchemy**: ORM for database interactions.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MrMiM-tfe/pacman-multiplayer.git
    cd pacman-multiplayer
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Unix
    venv\Scripts\activate    # Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

### Server

```bash
python dev_server.py # with host reload
python main.py
```

### Client

```bash
python main.py           # Online mode
python main.py --offline # Offline mode with fake data
```

## Game Controls

-   **Arrow Keys**: Move Up/Down/Left/Right

## Server API

#### `authenticate`

**Payload**: `{ "username": "...", "password": "..." }`
**Response**: `{ status: "success", data: { token, user_id, username } }`

#### Socket Events

-   `start_game` → `{ room_id }` start round.
-   `game_state` ← continuous state `{ game_id, p1, p2, map, ghosts }`.
-   `change_dir` → `{ game_id, user, direction }`.
-   `end_game` ← `{ winner: { user_id, username, score } }`.
