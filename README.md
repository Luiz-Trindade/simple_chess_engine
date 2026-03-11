# Simple Chess Engine

A lightweight chess engine with a graphical interface built using Python and Tkinter.

## Features

- Interactive chessboard GUI (8x8 grid)
- Click-based piece movement
- Move validation system
- Visual selection highlighting

## Requirements

- Python 3.x
- Tkinter
- Custom utilities module

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

### How to Play

1. Click on a square to select a piece (highlighted in green)
2. Click on a destination square to move the piece
3. The engine validates the move based on chess rules

## Project Structure

```
simple_chess_engine/
├── main.py          # GUI and game logic
├── utils.py         # Utility functions (verify_move, etc.)
└── README.md        # This file
```

## Current Implementation

- Basic piece selection and movement
- Move validation for pieces (currently supports rook)
- Tkinter-based visual interface

## Future Enhancements

- Full chess rule implementation
- All piece types and movement patterns
- Game state management
- Move history and undo functionality
# simple_chess_engine
