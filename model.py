"""
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4

class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other: "Vec") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other: "Vec") -> int:
        x = self.x + other.x
        y = self.y + other.y
        return Vec(x,y)
    
        


class Tile(GameElement):
    """A slidy numbered thing."""

    def __init__(self, pos: Vec, value: int):
        super().__init__()
        self.row = pos.x
        self.col = pos.y
        self.value = value
    
    def __repr__(self):
        """Not like constructor -- more useful for debugging"""
        return f"Tile[{self.row}, {self.col}]: {self.value}"

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other: "Tile"):
        return self.value == other.value

    def move_to(self, new_pos: Vec):
        self.row = new_pos.x
        self.col = new_pos.y
        self.notify_all(GameEvent(EventKind.tile_updated, self))

    def merge(self, other: "Tile"):
        self.value = self.value + other.value
        self.notify_all(GameEvent(EventKind.tile_updated, self))
        other.notify_all(GameEvent(EventKind.tile_removed, other))

    




class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    def __init__(self, rows=4, cols=4):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.tiles = []
        for row in range(rows):
            row_tiles = []
            for col in range(cols):
                row_tiles.append(None)
            self.tiles.append(row_tiles)
    
    def __getitem__(self, pos: Vec) -> Tile:
        return self.tiles[pos.x][pos.y]
    
    def __setitem__(self, pos: Vec, tile: Tile):
        self.tiles[pos.x][pos.y] = tile
    
    def _empty_positions(self) -> List[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces
        """
        empties = []
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                pos = Vec(row, col)
                if self[pos] is None:
                    empties.append(Vec(row, col))
        return empties

    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        if len(self._empty_positions()) > 0:
            return True
        return False

    def place_tile(self, value=None):
        """Place a tile on a randomly chosen empty square."""
        empties = self._empty_positions()
        assert len(empties) > 0
        choice = random.choice(empties)
        row, col = choice.x, choice.y
        if value is None:
            if random.random() < 0.1:
                value = 4
            else:
                value = 2
            new_tile = Tile(Vec(row, col), value)
            self.tiles[row][col] = new_tile
            self.notify_all(GameEvent(EventKind.tile_created, new_tile))

    def to_list(self) -> List[List[int]]:
        """Test scaffolding: represent each Tile by its
        integer value and empty positions as 0
        """
        result = []
        for row in self.tiles:
            row_values = []
            for col in row:
                if col is None:
                    row_values.append(0)
                else:
                    row_values.append(col.value)
            result.append(row_values)
        return result

    def from_list(self, values: List[List[int]]):
        """Test scaffolding: set board tiles to 
        give values, where 0 represents empty space"""
        
        for row in range(len(values)):
            for col in range(len(values[0])):
                if values[row][col] == 0:
                    newTile = None
                else:
                    newTile = Tile(Vec(row, col), values[row][col])
                self.tiles[row][col] = newTile       

    def in_bounds(self, pos: "Vec") -> bool:
        """Is position (pos.x, pos.y) a legal position on the board?"""
        return pos.x >= 0 and pos.x < self.rows and pos.y >= 0 and pos.y < self.cols

    def slide(self, pos: Vec, dir: Vec):
        """Slide tile at pos.x, pos.y (if any)
        in direction (dir.x, dir.y) until it bumps into
        another tile or the edge of the board.
        """

        if self[pos] is None:
            return
        while True:
            new_pos = pos + dir
            if not self.in_bounds(new_pos):
                break
            if self[new_pos] is None:
                self._move_tile(pos, new_pos)
            elif self[pos] == self[new_pos]:
                self[pos].merge(self[new_pos])
                self._move_tile(pos, new_pos)
                break
            else:
                break
            pos = new_pos
        
    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        """Move a tile to a different position"""
        self[old_pos].move_to(new_pos)
        self[new_pos] = self[old_pos]
        self[old_pos] = None

    def _move(self, startPos, slideVec, rowDir, colDir):
       # startPos: which tile to move first MAYBE NOT NEEDED
       # slideVec: what vector to add to each tile (how it moves)
       # rowDir: up or down? (1 is up, -1 is down) since changes from least to most affected
       # colDir: left or right? (1 is left, -1 is right) see above why
       
       # maybe use a while loop and repeatedly add direction to counter? for loops get tricky with reversing
       # and have too many ifs
    #    for row in range(self.rows):
    #         for col in range(self.cols):
    #             pos = Vec(row, col)
    #             self.slide(pos, slideVec)
        # add while loop below
        row = startPos(0)
        while row >= 0 and row < self.rows:
           # test here
           # add to columns first if going up or down. Add to rows first if going left or right
           
           # do code
           
           # how to loop
           
               

    def left(self):
        slideVec = Vec(0, -1)
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         pos = Vec(row, col)
        #         self.slide(pos, slideVec)
        startPos = Vec(0,0)
        rowDir = 0
        colDir = 1
        self._move(startPos, slideVec, rowDir, colDir)
    
    def right(self):
        slideVec = Vec(0, 1)
        # for row in reversed(range(self.rows)):
        #     for col in reversed(range(self.cols)):
        #         pos = Vec(row, col)
        #         self.slide(pos, slideVec)
        startPos = Vec(0,0)
        rowDir = 0
        colDir = -1
        self._move(startPos, slideVec, rowDir, colDir)

    def up(self):
        slideVec = Vec(-1, 0)
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         pos = Vec(row, col)
        #         self.slide(pos, slideVec)
        startPos = Vec(0,0)
        rowDir = 0
        colDir = 1
        self._move(startPos, slideVec, rowDir, colDir)

    def down(self):
        slideVec = Vec(1, 0)
        # for row in range(self.rows):
        #     for col in reversed(range(self.cols)):
        #         pos = Vec(row, col)
        #         self.slide(pos, slideVec)
        # maybe self.rows - 1?
        startPos = Vec(0,self.rows)
        rowDir = 0
        colDir = 1
        self._move(startPos, slideVec, rowDir, colDir)



    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        total = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.tiles[row][col] is not None:
                    total += self.tiles[row][col].value
        return total
