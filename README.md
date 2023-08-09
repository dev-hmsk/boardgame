# Checkers Game
Checkers Game is a console-based implementation of the classic board game Checkers (also known as Draughts). The game allows two players to take turns and play against each other. The game is played on an 8x8 board with alternating dark and light squares. Players move their pieces diagonally on the board, capturing the opponent's pieces by jumping over them.

### Getting Started
To play the game, follow these steps:

Make sure you have Python 3.x installed on your system.
Clone or download this repository to your local machine.
Open a terminal or command prompt and navigate to the downloaded repository's directory.
How to Play
Run the main.py script to start the game.

```python main.py```

### Turn Order
- The game will alternate between the white and black players' turns.

- During your turn, you'll be prompted to select a piece to move.
  - You can use the 'q' and 'e' keys to cycle through your available pieces and 's' to select a piece.

- After selecting a piece, you'll see the available moves for that piece.
  - If there are captures available, you must make a capture move. Otherwise, you can make a regular move.

- Enter the move you want to make based on the available options presented.

- The game will display the updated board and provide information about the current state of the game.

- The game continues alternating turns until one player wins or there are no valid moves left for both players.

### Game Logic and Implementation
The game is implemented using Python and object-oriented programming principles. 

The game logic is divided into several classes:

- Game_Piece and Checkers_Game_Piece Classes:
  - These classes represent the game pieces, including regular pieces and kings.
  - They have attributes to store the piece's position, team, and available moves.

- Board and Checkers_Board Classes:
  - These classes represent the game board.
  - The Board class provides a general structure for the game board
  - The Checkers_Board class adds Checkers-specific functionality, such as piece placement and capturing.

- main.py Script: This script contains the main game loop and orchestrates the game. It handles player turns, piece selection, and the game's overall flow.

### Game Features
- Players can cycle through their available pieces and select the one they want to move.
- Capturing opponent pieces is mandatory when possible.
- The game displays a visual representation of the board after each move.
 The game checks for victory conditions (no valid moves or all pieces captured) after each turn.

### Future Improvements
While the current implementation provides the basic functionality of the Checkers game, there are several areas for potential improvement:

- Enhance the user interface for a more user-friendly experience.
- Implement an AI opponent for single-player mode.
- Add options for players to restart or exit the game.
- Implement more advanced victory conditions, such as a time limit or a set number of turns.
- Implement logging and error handling to improve the robustness of the game.

### Contributions
Contributions to the project are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository.

License
This project is licensed under the MIT License. You can find the full license text in the LICENSE file.
