# Minesweeper Game (扫雷游戏)

A classic Minesweeper game built with Python and Pygame.

## Description
The objective of the game is to clear a rectangular board containing hidden "mines" without detonating any of them, with help from clues about the number of neighboring mines in each field.

## Features
- Classic Minesweeper gameplay
- Left-click to reveal cells
- Right-click to place flags
- Automatic expansion of empty areas
- Timer and mine counter
- Win/lose detection
- Restart functionality

## Requirements
- Python 3.6+
- Pygame library

## Installation
1. Clone this repository
2. Install dependencies: `pip install pygame`
3. Run the game: `python minesweeper.py`

## Controls
- Left Mouse Button: Reveal a cell
- Right Mouse Button: Place/remove flag
- R Key: Restart the game

## How to Play
- Left-click on a cell to reveal it
- Numbers indicate how many mines are adjacent to that cell
- Right-click to place a flag where you think a mine is located
- Avoid clicking on mines!
- Reveal all non-mine cells to win the game
- The timer starts after your first click

## Game Settings
- Grid size: 10x10
- Number of mines: 15
- First click is always safe (guaranteed to be empty)