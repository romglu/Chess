# Chess
A chess game with a simple AI implementation
<br><br>
<b>Versions</b>
<br><br>
There are two versions of the chess game. 
<br>
<ul>
  <li>The first, located in <b>Chess.py</b>, evaluates positions without looking ahead through various branches of the game tree.</li>
  <li>The second version, located in <b>AlphaBeta.py</b>, implements a Minimax algorithm with Alpha-Beta pruning in order to look ahead multiple moves. However, it is currently rather slow in comparison to the first version.</li>
</ul>
<br><br>
<b>Structure</b>
<br>
<ul>
  <li> The <b>Game</b> class is how to start a game against the AI. Instantiating it runs the play() method and sets up the initial board, prompting the user to choose a color and then you can play against the AI.<br>
  <li> The <b>Board</b> class is a representation of the 8x8 chess board. It keeps track of all the pieces on the board, whose turn it is, and there are a number of methods to check and modify properties of the board.<br>
  <li> The <b>Piece</b> class is a base class which the Pawn, Knight, Bishop, Rook, Queen, King classes all inherit from. It stores the properties of position, color, value, and board. The subclasses all contain a method to find all possible moves for the piece, and give their notation values.<br><br>
</ul>
<b>Instructions</b>
<br>
To play, see the instructions in the source code of Chess.py or AlphaBeta.py.
