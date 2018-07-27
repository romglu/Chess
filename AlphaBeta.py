# TO PLAY: type "Game()" and follow directions
# for notation, use P,N,B,R,Q,K followed by square, i.e. "Pe4", "Rd5", even if capture
# en passant: "e.p.", castle: "oo", "o-o-o", promotion: "Pe8=Q", do NOT notate check/mate with + and #

import copy
import random
import sys
import math
#import pyomd
import numpy as np
#import fileinput
#import cProfile

class Piece():
    def __init__(self, color, pos, board):
        self.color = color
        self.position = pos
        self.x = pos[0]
        self.y = pos[1]
        self.board = board
        self.value = 0

    def getNotation(self):
        return self.notation

    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos
        self.x = pos[0]
        self.y = pos[1]

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self,y):
        self.y = y

    def getSquare(self, board):     #e.g. 'e5'
        for sq in board.squares:
            if self.position == sq[0]:
                return sq[1]

    #USE "t.findKing('w').getSquare(t)"

    def getColor(self):
        return self.color 
    
class Pawn(Piece):
    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.notation = "P"
        self.value = 1
        self.lastmovedtwo = 0

    def __repr__(self):
        if self.color == 'w':
            return "White Pawn" + chr(self.x+97)+str(self.y+1)
        elif self.color == 'b':
            return "Black Pawn" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        moves = []
        x = self.x
        y = self.y
        if self.color == 'w':
            #1 square up
            if y < 7:
                if not board.isOccupied((x,y+1)):
                    if self.y == 6: #promotion
                        moves.append((x, 7, 'Q'))
                        moves.append((x, 7, 'R'))
                        moves.append((x, 7, 'N'))
                        moves.append((x, 7, 'B'))
                    else:
                        moves.append((x,y+1))
                        if y == 1 and (not board.isOccupied((x,y+2))): #2 squares up
                            moves.append((x,y+2))
                #capturing
                if 0 < x and board.isOccupied((x-1,y+1)) and board.getPiece((x-1,y+1)).getColor() != self.color:
                    if y == 6:
                        moves.append((x-1, 7, 'Q'))
                        moves.append((x-1, 7, 'R'))
                        moves.append((x-1, 7, 'N'))
                        moves.append((x-1, 7, 'B'))
                    moves.append((x-1,y+1)) #possibly a problem
                if 0 <= x < 7 and 0 < y and board.isOccupied((x+1,y+1)) and board.getPiece((x+1,y+1)).getColor() != self.color:
                    if y == 6:
                        moves.append((x+1, 7, 'Q'))
                        moves.append((x+1, 7, 'R'))
                        moves.append((x+1, 7, 'N'))
                        moves.append((x+1, 7, 'B'))
                    moves.append((x+1,y+1)) #possibly a problem
                #en passant  
                if y == 4:
                    if board.isOccupied((x-1,y)): 
                        i1 = board.getPiece((x-1,y))
                        if type(i1) is Pawn and i1.lastmovedtwo == 1:
                            moves.append((x-1,y+1,'e','p'))
                    elif board.isOccupied((x+1, y)):
                        i2 = board.getPiece((x+1,y))
                        if type(i2) is Pawn and i2.lastmovedtwo == 1:
                            moves.append((x+1,y+1,'e','p'))
                
        elif self.color == 'b':
            #1 square up
            if y > 0:
                if not board.isOccupied((x,y-1)):
                    if self.y == 1:     #promotion
                        moves.append((x, 0, 'Q'))
                        moves.append((x, 0, 'R'))
                        moves.append((x, 0, 'N'))
                        moves.append((x, 0, 'B'))
                    else:
                        moves.append((x,y-1))
                        if y == 6 and (not board.isOccupied((x,y-2))):
                            moves.append((x,y-2))
                #capturing
                if 0 < x and board.isOccupied((x-1,y-1)) and board.getPiece((x-1,y-1)).getColor() != self.color:
                    if self.y == 1:
                        moves.append((x-1, 0, 'Q'))
                        moves.append((x-1, 0, 'R'))
                        moves.append((x-1, 0, 'N'))
                        moves.append((x-1, 0, 'B'))
                    moves.append((self.x-1,self.y-1))
                if 7 > x and board.isOccupied((x+1,y-1)) and board.getPiece((x+1,y-1)).getColor() != self.color:
                    if self.y == 1:
                        moves.append((x+1, 0, 'Q'))
                        moves.append((x+1, 0, 'R'))
                        moves.append((x+1, 0, 'N'))
                        moves.append((x+1, 0, 'B'))
                    moves.append((x+1,y-1))
                #en passant
                if y == 3:
                    if board.isOccupied((x-1,y)): 
                        i1 = board.getPiece((x-1,y))
                        if type(i1) is Pawn and i1.lastmovedtwo == 1:
                            moves.append((x-1,y-1,'e','p'))
                    elif board.isOccupied((x+1,y)):
                        i2 = board.getPiece((x+1,y))
                        if type(i2) is Pawn and i2.lastmovedtwo == 1:
                            moves.append((x+1,y-1,'e','p'))  
        return moves

        #USE "t.squares[1][2].listMoves(t)" to find list of moves for a given piece
    
class Knight(Piece):
    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.notation = "N"
        self.value = 3

    def __repr__(self):
        if self.color == 'w':
            return "White Knight" + chr(self.x+97)+str(self.y+1)
        else:
            return "Black Knight" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        i = 0
        moves = []
        x = self.x
        y = self.y
        moves.append((x-1,y+2))
        moves.append((x+1,y+2))
        moves.append((x-1,y-2))
        moves.append((x+1,y-2))
        moves.append((x-2,y+1))
        moves.append((x-2,y-1))
        moves.append((x+2,y+1))
        moves.append((x+2,y-1))

        while i < len(moves):
            mv = moves[i]
            if mv[0] < 0 or mv[0] > 7 or mv[1] < 0 or mv[1] > 7 or (board.isOccupied(mv) and board.getPiece(mv).getColor() == self.color):
                moves.remove(mv)
                i -= 1 
            i += 1
        return moves        

class Bishop(Piece):
    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.notation = "B"
        self.value = 3.25

    def __repr__(self):
        if self.color == 'w':
            return "White Bishop" + chr(self.x+97)+str(self.y+1)
        else:
            return "Black Bishop" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        moves = []
        x = self.x
        y = self.y
        i = 1
        while 0 <= x - i <= 7 and 0 <= y - i <= 7:
            if board.isOccupied((x-i,y-i)):
                if board.getPiece((x-i,y-i)).getColor() != self.color:
                    moves.append((x-i,y-i))
                i = 100
            else:
                moves.append((x-i,y-i))
                i += 1
        i = 1
        while 0 <= x - i <= 7 and 0 <= y + i <= 7:
            if board.isOccupied((x-i,y+i)):
                if board.getPiece((x-i,y+i)).getColor() != self.color:
                    moves.append((x-i,y+i))
                i = 100
            else:
                moves.append((x-i,y+i))
                i += 1
        i = 1      
        while 0 <= x + i <= 7 and 0 <= y - i <= 7:
            if board.isOccupied((x+i,y-i)):
                if board.getPiece((x+i,y-i)).getColor() != self.color:
                    moves.append((x+i,y-i))
                i = 100
            else:
                moves.append((x+i,y-i))
                i += 1
        i = 1        
        while 0 <= x + i <= 7 and 0 <= y + i <= 7:
            if board.isOccupied((x+i,y+i)):
                if board.getPiece((x+i,y+i)).getColor() != self.color:
                    moves.append((x+i,y+i))
                i = 100     
            else:
                moves.append((x+i,y+i))
                i += 1
                
        return moves

class Rook(Piece):
    def __init__(self, color, pos, board, hm = 0):
        super().__init__(color, pos, board)
        self.hasmoved = hm
        self.notation = "R"
        self.value = 5

    def __repr__(self):
        if self.color == 'w':
            return "White Rook" + chr(self.x+97)+str(self.y+1)
        else:
            return "Black Rook" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        moves = []
        i = 1
        x = self.x
        y = self.y
        while 0 <= x - i <= 7:
            if board.isOccupied((x-i,y)):
                if board.getPiece((x-i,y)).getColor() != self.color:
                    moves.append((x-i,y))
                i = 100
            else:
                moves.append((x-i,y))
                i += 1
        i = 1        
        while 0 <= x + i <= 7:
            if board.isOccupied((x+i,y)):
                if board.getPiece((x+i,y)).getColor() != self.color:
                    moves.append((x+i,y))
                i = 100
            else:
                moves.append((x+i,y))
                i += 1
        i = 1        
        while 0 <= y - i <= 7:
            if board.isOccupied((x,y-i)):
                if board.getPiece((x,y-i)).getColor() != self.color:
                    moves.append((x,y-i))
                i = 100
            else:
                moves.append((x,y-i))
                i += 1
        i = 1        
        while 0 <= y + i <= 7:
            if board.isOccupied((x,y+i)):
                if board.getPiece((x,y+i)).getColor() != self.color:
                    moves.append((x,y+i))
                i = 100
                
            else:
                moves.append((x,y+i))
                i += 1
                
        return moves

    def hasMoved(self, board):
        self.hasMoved = 1

class Queen(Piece):
    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.notation = "Q"
        self.value = 9

    def __repr__(self):
        if self.color == 'w':
            return "White Queen" + chr(self.x+97)+str(self.y+1)
        else:
            return "Black Queen" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        moves = []
        i = 1
        x = self.x
        y = self.y
        #rook moves
        while 0 <= x - i <= 7:
            if board.isOccupied((x-i,y)):
                if board.getPiece((x-i,y)).getColor() != self.color:
                    moves.append((x-i,y))
                i = 100
            else:
                moves.append((x-i,y))
                i += 1
        i = 1        
        while 0 <= x + i <= 7:
            if board.isOccupied((x+i,y)):
                if board.getPiece((x+i,y)).getColor() != self.color:
                    moves.append((x+i,y))
                i = 100
            else:
                moves.append((x+i,y))
                i += 1
        i = 1        
        while 0 <= y - i <= 7:
            if board.isOccupied((x,y-i)):
                if board.getPiece((x,y-i)).getColor() != self.color:
                    moves.append((x,y-i))
                i = 100
            else:
                moves.append((x,y-i))
                i += 1
        i = 1        
        while 0 <= y + i <= 7:
            if board.isOccupied((x,y+i)):
                if board.getPiece((x,y+i)).getColor() != self.color:
                    moves.append((x,y+i))
                i = 100
                
            else:
                moves.append((x,y+i))
                i += 1

        #bishop moves
        i = 1
        while 0 <= x - i <= 7 and 0 <= y - i <= 7:
            if board.isOccupied((x-i,y-i)):
                if board.getPiece((x-i,y-i)).getColor() != self.color:
                    moves.append((x-i,y-i))
                i = 100
            else:
                moves.append((x-i,y-i))
                i += 1
        i = 1        
        while 0 <= x - i <= 7 and 0 <= y + i <= 7:
            if board.isOccupied((x-i,y+i)):
                if board.getPiece((x-i,y+i)).getColor() != self.color:
                    moves.append((x-i,y+i))
                i = 100
            else:
                moves.append((x-i,y+i))
                i += 1
        i = 1        
        while 0 <= x + i <= 7 and 0 <= y - i <= 7:
            if board.isOccupied((x+i,y-i)):
                if board.getPiece((x+i,y-i)).getColor() != self.color:
                    moves.append((x+i,y-i))
                i = 100
            else:
                moves.append((x+i,y-i))
                i += 1
        i = 1        
        while 0 <= x + i <= 7 and 0 <= y + i <= 7:
            if board.isOccupied((x+i,y+i)):
                if board.getPiece((x+i,y+i)).getColor() != self.color:
                    moves.append((x+i,y+i))
                i = 100
                
            else:
                moves.append((x+i,y+i))
                i += 1
                
        return moves
        
class King(Piece):
    def __init__(self, color, pos, board, hm = 0):
        super().__init__(color, pos, board)
        self.hasmoved = hm
        self.notation = "K"
        self.value = 100

    def __repr__(self):
        if self.color == 'w':
            return "White King" + chr(self.x+97)+str(self.y+1)
        else:
            return "Black King" + chr(self.x+97)+str(self.y+1)
    
    def listMoves(self, board):
        i = 0
        x = self.x
        y = self.y
        if self.color == 'w':
            ocolor = 'b'
        else:
            ocolor = 'w'
            
        moves = []
        moves.append((x-1,y+1))
        moves.append((x+1,y+1))
        moves.append((x-1,y-1))
        moves.append((x+1,y-1))
        moves.append((x,y+1))
        moves.append((x,y-1))
        moves.append((x+1,y))
        moves.append((x-1,y))

        while i < len(moves): #takes away moves that leave the board
            mv = moves[i]
            if mv[0] < 0 or mv[0] > 7 or mv[1] < 0 or mv[1] > 7 or (board.isOccupied(mv) and board.getPiece(mv).getColor() == self.color):
                moves.remove(mv)
                i -= 1
            i += 1
        
        if self.hasmoved == 0 and not self.board.isAttacked(self.position,ocolor): #castling
            if type(board.getPiece((x+3,y))) is Rook and board.getPiece((x+3,y)).hasmoved == 0:
                if (not board.isOccupied((x+1, y))) and (not board.isOccupied((x+2, y))):
                    if (not board.isAttacked((x+1, y), ocolor)) and (not board.isAttacked((x+2,y), ocolor)):
                        moves.append(('O','O'))
            if type(board.getPiece((x-4,y))) is Rook and board.getPiece((x-4,y)).hasmoved == 0:                                                               
                if (not board.isOccupied((x-1, y))) and (not board.isOccupied((x-2, y))) and (not board.isOccupied((x-3, y))):
                    if (not board.isAttacked((x-1, y), ocolor)) and (not board.isAttacked((x-2, y), ocolor)) and (not board.isAttacked((x-3, y), ocolor)):
                        moves.append(('O','O','O'))
                                                                           
        return moves

    def hasMoved(self, board):
        self.hasmoved = 1
    
class Board():
    def __init__(self):
        self.squares = []
        self.pieces = []
        self.turn = 'player'
        self.captured = [] #represents pieces captured
        for file in range(8):
            for rank in range(8):
                self.squares.append([(file,rank),chr(file+97)+str(rank+1),None])
        for file in self.squares:
            sq = file[0]
            ntn = file[1]
            if sq[1] == 1:
                self.addPiece(Pawn('w',sq, self),sq)
            elif sq[1] == 6:
                self.addPiece(Pawn('b',sq, self),sq)
            elif ntn == 'a1' or ntn == 'h1':
                self.addPiece(Rook('w',sq, self),sq)
            elif ntn == 'a8' or ntn == 'h8':
                self.addPiece(Rook('b',sq, self),sq)
            elif ntn == 'b1' or ntn == 'g1':
                self.addPiece(Knight('w',sq, self),sq)
            elif ntn == 'b8' or ntn == 'g8':
                self.addPiece(Knight('b',sq, self),sq)
            elif ntn == 'c1' or ntn == 'f1':
                self.addPiece(Bishop('w',sq, self),sq)
            elif ntn == 'c8' or ntn == 'f8':
                self.addPiece(Bishop('b',sq, self),sq)
            elif ntn == 'd1':
                self.addPiece(Queen('w',sq, self), sq)
            elif ntn == 'd8':
                self.addPiece(Queen('b',sq, self), sq)
            elif ntn == 'e1':
                self.addPiece(King('w',sq, self), sq)
            elif ntn == 'e8':
                self.addPiece(King('b',sq, self), sq)
        self.setPieces()

    def setTurn(self, p):
        self.turn = p
        
    def getAllMoves(self, color):
        moves = []
        for piece in self.pieces:
            if piece.getColor() == color:
                for move in piece.listMoves(self):
                    if self.checkMove(piece,move): #ensures no checks
                        moves.append((piece,move))
        return moves

    def setPieces(self):
        self.pieces = []
        for sq in self.squares:
            #if sq[2] is not None:
            if isinstance(sq[2],Piece):
                if type(sq) is King:
                    self.pieces.insert(0,sq[2]) #to make findKing() a lot faster
                else:
                    self.pieces.append(sq[2])

    def setSquares(self, lst):
        self.squares = lst

    def getSquares(self):
        return self.squares
             
    def addPiece(self, piece, square = (-1,-1)):
        x = square[0]
        y = square[1]
        if type(square[0]) is int:
            self.squares[8*x+y][2] = piece
            piece.setPosition(square)
            piece.setX(x)
            piece.setY(y)
            self.setPieces()
        
    def removePiece(self, square = (-1,-1)):
        if square[0] in range(8) and square[1] in range(8):
            self.squares[8*square[0]+square[1]][2] = None
            self.setPieces()
                    
    def movePiece(self, piece, square, legality=1):
        if piece is not None:
            a = piece.position
            clr = piece.getColor()
            #if square not in piece.listMoves(self) and self.turn == 'player':
            #    print("Not a possible move. Try again!")
            #el
            if type(square[0]) is str: #castling
                x = piece.getX()
                y = piece.getY()
                if len(square) == 2:
                    rook = self.getPiece((x+3,y))
                    if rook is not None:
                        self.removePiece((x,y))
                        self.addPiece(piece,(x+2,y))
                        self.removePiece((x+3,y))
                        self.addPiece(rook,(x+1,y))
                else:
                    rook = self.getPiece((x-4,y))
                    if rook is not None:
                        self.removePiece((x,y))
                        self.addPiece(piece,(x-2,y))
                        #print("ROOK: ", rook)
                        self.removePiece((x-4,y))
                        self.addPiece(rook,(x-1,y))
            elif len(square) == 3: #promotion
                msq = (square[0],square[1])
                #print(msq)
                if not self.isOccupied(msq):
                    #self.movePiece(piece, msq)
                    self.removePiece(msq)
                    self.removePiece(a)
                    if square[2] == 'Q':
                        self.addPiece(Queen(clr, msq ,self),msq)
                    elif square[2] == 'N':
                        self.addPiece(Knight(clr, msq ,self),msq)
                    elif square[2] == 'R':
                        self.addPiece(Rook(clr, msq ,self),msq)
                    elif square[2] == 'B':
                        self.addPiece(Bishop(clr, msq ,self),msq)
                    if self.isChecked(clr) and legality==1:
                        self.removePiece(msq)
                        self.addPiece(piece, a)
                        if self.turn == 'player':
                            #print("Moved into check. Try again.")
                            return Error
                else:
                    self.captured.append(self.getPiece(msq))
                    self.removePiece(msq)
                    self.removePiece(a)
                    #self.movePiece(piece, msq)
                    #self.removePiece(msq)
                    if square[2] == 'Q':
                        self.addPiece(Queen(clr, msq, self), msq)
                    elif square[2] == 'N':
                        self.addPiece(Knight(clr, msq, self), msq)
                    elif square[2] == 'R':
                        self.addPiece(Rook(clr, msq, self), msq)
                    elif square[2] == 'B':
                        self.addPiece(Bishop(clr, msq, self), msq)
                    if self.isChecked(clr) and legality==1:
                        self.removePiece(msq)
                        self.addPiece(piece, a)
                        self.addPiece(self.captured[-1], square)
                        del self.captured[-1]
                        if self.turn == 'player':
                            #print("Captured into check. Try again..")
                            return Error
                            
            elif len(square) == 4: #en passant
                a = piece.getPosition()
                msq = (square[0],square[1])
                if piece.getColor() == 'w':
                    pawncapt = self.getPiece((msq[0],msq[1]-1))
                else:
                    pawncapt = self.getPiece((msq[0],msq[1]+1))
                loc = pawncapt.getPosition()
                self.captured.append(pawncapt)
                self.removePiece(loc)
                self.removePiece(a)
                self.addPiece(piece, msq)
                if self.isChecked(clr):
                    self.removePiece(msq)
                    self.addPiece(piece, a)
                    self.addPiece(self.captured[-1], loc)
                    del self.captured[-1]
                    if self.turn == 'player':
                        #print("En passanted into check. Try again..")
                        return Error
            else:
                if not self.isOccupied(square):
                    self.removePiece(a)
                    self.addPiece(piece, square)
                    if self.isChecked(clr) and legality == 1:
                        self.removePiece(square)
                        self.addPiece(piece, a)
                        if self.turn == 'player':
                            #print("Moved into check. Try again.")
                            return Error
                    else:
                        piece.position = square
                        piece.x = square[0]
                        piece.y = square[1]
                else:
                    self.captured.append(self.getPiece(square))
                    self.removePiece(square)
                    self.removePiece(piece.getPosition())
                    self.addPiece(piece, square)
                    if self.isChecked(clr) and legality == 1:
                        self.removePiece(square)
                        self.addPiece(piece, a)
                        self.addPiece(self.captured[-1], square)
                        del self.captured[-1]
                        if self.turn == 'player':
                            #print("Captured into check. Try again..")
                            return Error
                    else:
                        piece.setPosition(square)
                        piece.setX(square[0])
                        piece.setY(square[1])
                        
    def createBoard(self,pieces):
        self.clearBoard()
        for i in pieces:
            if i.getPosition() is not None:
                self.addPiece(i,i.getPosition())
        self.setPieces()

    def checkMove(self, piece, square):
        a = piece.getPosition()
        if square not in piece.listMoves(self) and self.turn == 'player':
            #print("Check - Not a possible move. Try again!")
            return False
        elif type(square[0]) is str: #castles
            pass
        else:
            if not self.isOccupied(square):
                self.removePiece(a)
                self.addPiece(piece, square)
                if self.isChecked(piece.getColor()):
                    self.removePiece(square)
                    self.addPiece(piece, a)
                    #if self.turn == 'player':
                    #    print("Check - Moved into check. Try again.")
                    return False
                self.removePiece(square)
                self.addPiece(piece, a)
                return True            
            else:
                self.captured.append(self.getPiece(square))
                self.removePiece(square)
                self.removePiece(a)
                self.addPiece(piece, square)
                if self.isChecked(piece.getColor()):
                    self.removePiece(square)
                    self.addPiece(piece, a)
                    self.addPiece(self.captured[-1], square)
                    del self.captured[-1]
                    #if self.turn == 'player':
                    #    print("Check - Captured into check. Try again..")
                    return False
                self.removePiece(square)
                self.addPiece(piece, a)
                self.addPiece(self.captured[-1], square)
                del self.captured[-1]
                return True
            
        return True                                 
        
    def isOccupied(self, pos):
        #print(self.squares[8*pos[0]+pos[1]][2])
        try:
            if type(pos[1]) is int and self.squares[8*pos[0]+pos[1]][2] == None:
                return False
            else:
                return True
        except IndexError:
            pass
            
    def findKing(self,color):
        for piece in self.pieces:
            if type(piece) is King and piece.getColor() == color:
                return piece
        return King(color, (-1,-1), Board())
    
    def isChecked(self, color):
        kingpos = self.findKing(color).getPosition()
        for piece in self.pieces:
            if piece.getColor() != color and type(piece) not in [King,Piece]:
                for move in piece.listMoves(self):
                    if move == kingpos:    
                        return True
        return False

    def isCheckmated(self, color):
        if len(self.getAllMoves(color)) == 0:
            if self.isChecked(color):
                return True
        return False
                
    def isAttacked(self, square, color, notpiece = Piece('g',(-1,-1),1)): #pc for defended
        #for piece in self.pieces:
        #    if (piece.getColor() == color) and (piece is not notpiece):
        #        if type(piece) is King and type(square[0]) is int:
        #            if abs(piece.x - square[0]) < 2 and abs(piece.y - square[1]) < 2:
        #                return True
        #        else:
        #            for move in piece.listMoves(self):
        #                if move == square:
        #                    return True
        #return False
        removed = False
        if self.isOccupied(square):
            self.captured.append(self.getPiece(square))
            self.removePiece(square)
            removed = True
        for piece in self.pieces:
            if (piece.getColor() == color) and (piece is not notpiece):
                x = piece.getX()
                y = piece.getY()
                if type(piece) is King and type(square[0]) is int:
                    if abs(x - square[0]) < 2 and abs(y - square[1]) < 2:
                        if removed:
                            self.addPiece(self.captured[-1],square)
                            del self.captured[-1]
                        return True
                elif type(piece) is Pawn:
                    if piece.getColor() == 'w':
                        if square == (x+1,y+1) or square == (x-1,y+1):
                            if removed:
                                self.addPiece(self.captured[-1],square)
                                del self.captured[-1]
                            return True
                    elif piece.getColor() == 'b':
                        if square == (x+1,y-1) or square == (x-1,y-1):
                            if removed:
                                self.addPiece(self.captured[-1],square)
                                del self.captured[-1]
                            return True
                else:
                    for move in piece.listMoves(self):
                        if move == square:
                            if removed:
                                self.addPiece(self.captured[-1],square)
                                del self.captured[-1]
                            return True
        if removed:
            self.addPiece(self.captured[-1],square)
            del self.captured[-1]
        return False
    
    def numPiecesDefended(self, color):
        count = 0
        for piece in self.pieces:
            count += (piece.getColor() == color and self.isAttacked(piece.getPosition(),color)) #if True, adds 1, else adds 0
            #if piece.getColor() == color and self.isAttacked(piece.getPosition(),color):
            #    count += 1
        #print(count)
        return count
    
    def getPiece(self, pos):
        if type(pos[0]) is int:
            try:
                return self.squares[8*pos[0]+pos[1]][2]
            except IndexError:
                pass #print('check out of range')
        elif type(pos) is str:
            try:
                tup = (ord(pos[0])-97,int(pos[1])-1)
                return self.squares[8*tup[0]+tup[1]][2]
            except IndexError:
                pass #print('check out of range')
        return Piece('grey', (-1,-1), self)
        
    def xDist(self,p1,p2):
        return p1.getX() - p2.getX()

    def yDist(self,p1,p2):
        return p1.getY() - p2.getY()
        
    def points(self,color):
        value = 0
        for i in self.pieces:
            if i.getColor() == color:
                value += i.value
        return value

    def setLastMovesTwo(self,turncolor):
        if turncolor == 'w':
            turncolor = 'b'
        else:
            turncolor = 'w'
        for i in self.pieces:
            if i.getColor() == turncolor and type(i) is Pawn:
                i.lastmovedtwo = 0

    def isThreateningCheckmate(self,color):
        if color == 'w':
            ocolor = 'b'
        else:
            ocolor = 'w'
        c = copy.deepcopy(self)
        mv = c.getAllMoves(color)
        for i in mv:
            #print(i)
            c.movePiece(i[0],i[1])
            if c.isCheckmated(ocolor):
                #print(self.pieces)
                #print((i[0], i[1]))
                c = copy.deepcopy(self)
                return True
            c = copy.deepcopy(self)
        
        return False

    def clearBoard(self):
        for i in self.squares:
            i[2] = None
        self.setPieces()
             
class Game():
    def __init__(self, color = 'w'):
        self.board = Board()
        self.cboard = Board()
        self.pcolor = 'w'
        self.ccolor = 'b'
        self.lastsquares = self.board.getSquares()
        self.pside = 0
        self.cside = 7
        self.cdir = -1
        self.turn = 'w'
        self.movenum = 1
        self.lastpawntwo = None
        self.wait = 0 #gets rid of lastpawntwo after one move
        self.notation = []
        #self.notation = ['pe3','pd5','d4','ph5','bd3','bg4','qd2','nf6','nc3','nc6','bb5','qd6','pg3','o-o-o','ph4','pe5','pe5','ne5','pf4','ng6','pb3','pa6','bf1','pd4','na4','ne4']
        self.play(color)

    def play(self, color = 'w'):
        self.pcolor = str(input('Choose a color (w or b): ')).lower()
        if self.pcolor == 'b':
            self.ccolor = 'w'
            self.cside = 7
            self.pside = 0
            self.cdir = 1
            self.board.setTurn('computer')
        
        #self.setPosition(['pe4', 'Pee6', 'pd4', 'Bfb4', 'nc3', 'Bbc3', 'pbc3', 'Nbc6', 'nf3', 'Ngf6', 'rg1', 'Rhg8', 'bd3', 'Nfg4', 'bf4', 'Ncb8', 'bb5', 'Pcc6', 'bc4', 'Pdd5', 'ped5', 'Nbd7', 'pde6', 'Ndf8', 'pef7', 'Kee7'])        

        while True:
            #game = ['Pee3', 'pe5', 'bb5', 'nc6', 'bf1', 'nf6', 'bb5', 'bc5', 'Bc4', 'ne4', 'pd4', 'ped4', 'ped4', 'nd4', 'bd5', 'qe7', 'kf1', 'qe5', 'Bc4', 'pg6', 'qg4', 'nc2', 'qe2', 'na1','bch6','rb8']
            #game2 = ['pe3','pe5','pg3','nc6','nc3','nf6','bc4','pd5','bb5','bd7','nf3','pe4','ng5','ph6','oo','bg4', 'qe2','be2','be2','pd4','na4','pde3','pde3','qd5','nh3','o-o-o','nf4','qa5','pb3','nb4','pa3','nc2', 'rb1','pg5','nb2','ba3','nc4','qc5','ba3','na3','ra1','nc2','ra2','nb4','raa1','pgf4','pef4','nc2','ra2','nb4','raa1','nc2','ra4','pb5','ra6','nd5','nb2','pe3','pfe3','nde3','pf5','nf1','kf1','qf5','kg1','qc5','kg2','rd2','pg4','re2','kg3','qe3','kh4','qg5','kh3','rhe8','nd1','ph5','pgh5','qh5','kg3','rg8']
            '''game3 = ['pb4', 'Pee6', 'bb2', 'Bfb4', 'bg7', 'Nbc6', 'bh8', 'Qdg5', 'pe4', 'Bbf8', 'nf3', 'Qga5', 'bc3', 'Qac5', 'pd4', 'Qch5', 'nbd2', 'Bfa3', 'nc4', 'Baf8', 'nce5', 'Nce5', 'ne5', 'Qhg5', 'bd2', 'Qgh4', 'qf3']
            for i in game3:
                self.move(i)
                self.lastsquares = self.board.getSquares()
                print(self.board.pieces)
                print(self.notation)'''
            print(self.notation)
            if self.turn == self.pcolor:
                try:
                    m = str(input('Enter a move (i.e. ph4): '))
                    self.move(m)
                    #m = self.randomMove()
                except Exception:
                    #m = str(input('Illegal Move. Try again. (i.e. ph4): '))
                    #self.move(m)
                    return Error

                if m != "undo":
                #random -- if True:
                    self.lastsquares = self.board.getSquares()
                    if self.board.isCheckmated(self.ccolor):
                        print("Good game! You win!")
                        print("Length of game: ", len(self.notation)//2)
                        return [self.notation, 0]
                    if len(self.board.getAllMoves(self.ccolor)) == 0 or len(self.notation) > 500:
                        print("Good game! It was a draw!")
                        print("Length of game: ", len(self.notation)//2)
                        return [self.notation, 0.5]
            else:
                #self.alphabeta(self.board, 3, -sys.maxsize, sys.maxsize)
                self.alphabeta(self.board,3,-sys.maxsize,sys.maxsize)
                if self.board.isCheckmated(self.pcolor):
                    print("Good game! I win!")
                    print("Length of game: ", len(self.notation)//2)

                    return [self.notation, 1]
                if len(self.board.getAllMoves(self.pcolor)) == 0 or len(self.notation) > 500:
                    print("Good game! It was a draw!")
                    print("Length of game: ", len(self.notation)//2)                    
                    return [self.notation, 0.5]

            #print(self.notation)

    def setPosition(self,notation = []):
        self.notation = notation
        if len(notation)>0:
            for mv in notation:
                self.move(mv)

    def move(self,notation):
        i = self.convertNotationtoMove(notation)
        pc = i[0]
        sq = i[1]
        if i == "undo":
            self.board = Board()
            self.cboard = Board()
            del self.notation[-2:]
            print(self.notation)
            if self.pcolor == 'b':
                self.turn = self.ccolor
                self.board.setTurn('computer')
            k = self.notation
            self.notation = []
            for j in k:
                #print(j)
                self.move(j)
        else:
            if i is not None:
                #checking en passant possibility
                '''if len(self.lastpawntwo) > 0:
                    if self.wait % 2 == 1: 
                        del self.lastpawntwo[-1]
                        self.board.setLastMovesTwo(self.turn)
                        self.cboard.setLastMovesTwo(self.turn)
                    self.wait += 1'''
                    
                if (type(pc) is Pawn) and (((self.turn == self.ccolor) and (sq == (pc.x,pc.y+2*self.cdir))) or ((self.turn == self.pcolor) and (sq == (pc.x,pc.y-2*self.cdir)))):
                    pc.lastmovedtwo = 1
                    self.lastpawntwo = pc
                else:
                    self.lastpawntwo = None
                    self.board.setLastMovesTwo(self.turn)
                    self.cboard.setLastMovesTwo(self.turn)

                self.board.movePiece(pc,sq)
                #self.cboard.movePiece(pc,sq)
                
                if type(pc) is King or type(pc) is Rook:
                   pc.hasmoved = 1

                self.notation.append(notation)
                #if i[1] == ('O','O') or i[1] == ('O','O','O'):
                #   if len(i[1]) == 2:
                #       self.notation.append("OO")
                #   else:
                #        self.notation.append("O-O-O")
                #else:
                #    self.notation.append(i[0].getNotation()+chr(i[1][0]+97)+str(i[1][1]+1))
            
                if self.turn == self.ccolor:
                    self.turn = self.pcolor
                    self.board.setTurn('player')
                else:
                    self.turn = self.ccolor
                    self.board.setTurn('computer')      

    def getLastMove(self):
        return self.notation[-1]

    def convertPostoSq(self, pos): #e4 -> (4,3)
        if len(pos)==2:
            return (ord(pos[0])-97,int(pos[1])-1)
        
    def convertSqtoPos(self,sq): #(4,3) -> e4
        if len(sq) == 2:
            return chr(sq[0]+97)+str(sq[1]+1)

    def convertNotationtoMove(self, notation):
        if notation == "undo" and len(self.notation)>1:
            return "undo"
        else:  
            piece = None
            sq1 = self.convertPostoSq(notation[1:])
            sq2 = self.convertPostoSq(notation[2:])
            
            if type(notation) is str:
                #normal move
                if len(notation) == 3:
                    for i in self.board.pieces:
                        if i.getColor() == self.turn and notation[0].upper() == i.getNotation() and sq1 in i.listMoves(self.board):
                            piece = i
                            break
                    square = self.convertPostoSq(notation[-2:])
                    
                #specified initial rank/file
                elif len(notation) == 4:
                    for i in self.board.pieces:
                        if i.getColor() == self.turn and notation[0].upper() == i.getNotation() and sq2 in i.listMoves(self.board):
                                if (chr(i.getX()+97) == notation[1] or i.getY() + 1 == ord(notation[1])-48):
                                    piece = i
                                    break
                    square = self.convertPostoSq(notation[-2:])
                    
                #en passant
                elif notation.lower() == 'ep':
                    done = False
                    for i in self.board.pieces:
                        if i.getColor() == self.turn and type(i) is Pawn:
                            for j in i.listMoves(self.board):
                                if len(j) == 4:
                                    piece = i
                                    square = j
                                    #print(square)
                                    done = True
                                    break
                        if done == True:
                            break
                        
                #promotion: e.g. pe8=Q
                elif '=' in notation:
                    sq3 = self.convertPostoSq(notation[1:-2])
                    for i in self.board.pieces:
                        if i.getColor() == self.turn and type(i) is Pawn and sq3 in i.listMoves(self.board):
                            piece = i
                            break
                    square = sq3 + (notation[-1],)
                else:
                    if notation.upper() == 'OO':
                        return (self.board.findKing(self.turn),('O','O'))
                    elif notation.upper() == 'O-O-O':
                        return (self.board.findKing(self.turn),('O','O','O'))

                #print((piece,square))
                return (piece, square)
            else:
                #castling
                if notation[1].upper() == 'OO':
                    piece = notation[0]
                    square = ('O','O')
                    return (piece, square)
                elif notation[1].upper() == 'O-O-O':
                    piece = notation[0]
                    square = ('O','O','O')
                    return (piece, square)
                else:
                    return notation

    def getScore(self, board, color, score = 0):
        b = copy.deepcopy(board)
        diff = b.points(self.ccolor) - b.points(self.pcolor)
        #defdiff = self.cboard.numPiecesDefended(self.ccolor) - self.cboard.numPiecesDefended(self.pcolor)
        allc = len(b.getAllMoves(self.ccolor))
        allp = len(b.getAllMoves(self.pcolor))
                 #point difference + c*(move difference) 
        score += diff + 0.01*(allc - allp)
        
        playercmed = b.isCheckmated(self.pcolor)
        numpmoves = len(b.getAllMoves(self.pcolor))
        if numpmoves == 0:
            if playercmed:
                score += 1000 #checkmate wins
            else:
                score = 0 #stalemate draws
        #1.06*diff + (0.20 * ((39+2*diff)/39) * ((((78-diff)/78)*allc)-1.11*(((78+1.5*diff)/78)*allp)))

        #+ .02*defdiff
        #if diff == 0, score == .16 * (allc - 1.12*allp)
        #oldformula --> (0.20 * (((139/pointsc)* allc) - ((139/pointsp) * allp))) + diff
        #(0.20 * ((1/39)*(39-diff)*(allc-allp))) + diff

        return score
                
    def alphabeta(self,board,depth,alpha,beta):
        self.cboard = copy.copy(self.board)
        move = self.alphamaxi(self.cboard,depth,alpha,beta)[0]
        bestpiece = move[0]
        bestsquare = move[1]
        if type(bestsquare[0]) is not str:
            if len(bestsquare) == 2:
                x = bestpiece.getNotation()+self.convertSqtoPos(bestpiece.getPosition())[0] + self.convertSqtoPos(bestsquare)
                #print(bestpiece,x)
                self.move(x)
            elif len(bestsquare) == 3:
                #print("promotion: ", bestpiece.getNotation()) 
                y = bestpiece.getNotation()+self.convertSqtoPos(bestsquare[0:2])+"="+bestsquare[2]
                #print(bestpiece,y)
                self.move(y)
        elif len(bestsquare) == 4:
            #print('ep')
            self.move('ep')
        else:
            #print(bestsquare)
            if bestsquare == ('O','O'):
                self.move((bestpiece,'OO'))
            else:
                self.move((bestpiece,'O-O-O'))

    def alphamaxi(self,board,depth,alpha,beta,move=None):
        if depth == 0:
            return self.getScore(board,self.ccolor)
        occ = False
        for i in board.getAllMoves(self.ccolor):
            piece = i[0]
            square = i[1]
            l = piece.getPosition()           
            #arr[0] = (piece, square)    
            #get a record of piece to be "captured"
            if self.cboard.isOccupied(square):
                occ = True
                p = self.cboard.getPiece(square)
            
            self.cboard.movePiece(piece,square)
            
            a = self.alphamini(board,depth-1,alpha,beta,move)
            if type(a) is tuple:
                score = a[1]
            else:
                score = a
            
            self.cboard.movePiece(piece, l,0)
            
            if occ:
                self.cboard.addPiece(p, square)
                occ = False
                
            if score >= beta:
                #j = (piece,square)
                return [(piece,square),beta]          
                
            if score > alpha:
                alpha = score
                move = (piece,square)
                
        return [move,score]
                
    def alphamini(self,board,depth,alpha,beta,move=None):
        if depth == 0:
            return self.getScore(board,self.pcolor)
        occ = False
        for i in board.getAllMoves(self.pcolor):
            piece = i[0]
            square = i[1]
            l = piece.getPosition()
            #arr[0] = (piece, square)
                
            #get a record of piece to be "captured"
            if self.cboard.isOccupied(square):
                occ = True
                p = self.cboard.getPiece(square)
            
            self.cboard.movePiece(piece,square)
            
            a = self.alphamaxi(board,depth-1,alpha,beta,move)
            if type(a)  in [tuple, list]:
                score = a[1]
            else:
                score = a
            
            self.cboard.movePiece(piece, l,0)
            
            if occ:
                self.cboard.addPiece(p, square)
                occ = False
                
            if score <= alpha:
                return alpha
                
            if score < beta:
                beta = score
                
        return beta
            
    def randomMove(self):
        if self.pcolor == 'b':
            self.ccolor = 'w'
            self.cside = 7
            self.pside = 0
            self.cdir = 1
            self.board.setTurn('computer')
        allMoves = self.board.getAllMoves(self.pcolor)
        num = len(allMoves)
        mv = allMoves[random.randint(0,num-1)]
        bestpiece = mv[0]
        bestsquare = mv[1]

        if type(bestsquare[0]) is not str:
            if len(bestsquare) == 2:
                x = bestpiece.getNotation()+self.convertSqtoPos(bestpiece.getPosition())[0] + self.convertSqtoPos(bestsquare)
                #print(bestpiece,x)
                self.move(x)
            elif len(bestsquare) == 3:
                #print("promotion: ", bestpiece.getNotation()) 
                y = bestpiece.getNotation()+self.convertSqtoPos(bestsquare[0:2])+"="+bestsquare[2]
                #print(bestpiece,y)
                self.move(y)
        elif len(bestsquare) == 4:
            #print('ep')
            self.move('ep')
        else:
            #print(bestsquare)
            if bestsquare == ('O','O'):
                self.move((bestpiece,'OO'))
            else:
                self.move((bestpiece,'O-O-O'))
        
    def getCColor(self):
        return self.ccolor
                    
