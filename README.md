# Chess
A chess game with a simple AI implementation
<br><br>
<b>Structure</b>
<br>
<ul>
  <li> The <b>Game</b> class is how to start a game against the AI. Instantiating it runs the play() function and sets up the initial board, prompting the user to choose a color and then you can play against the AI.<br>
  <li> The <b>Board</b> class is a representation of the 8x8 chess board. It keeps track of all the pieces on the board, whose turn it is, and there are a number of functions to check and modify properties of the board.<br>
  <li> The <b>Piece</b> class is a base class which the Pawn, Knight, Bishop, Rook, Queen, King classes all inherit from. It stores the properties of position, color, value, and board. The subclasses all contain a function to find all possible moves for the piece, and give their notation values.<br><br>
</ul>
<b>Instructions</b>
<br>
To play, see the instructions in the source code of Chess.py.
