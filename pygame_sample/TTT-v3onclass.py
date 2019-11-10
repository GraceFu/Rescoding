# The X and Y player's take turns selecting empty tiles
# to fill on a 3x3 board. If a player selects three tiles
# in a row, a column or a diagonal, that player wins.
# If all the tiles are filled without a win, the game is
# a draw.
# This program requires two data files: cursorx.txt and
# cursoro.txt that contain string represenations of  two
# custom cursors used in the game.
from uagame import Window
import pygame, time
from pygame.locals import *
import math, random

def main():

   window = Window('Tic Tac Toe', 500, 400)
   window.set_auto_update(False)   
   game = Game(window)
   game.play()
   window.close()

class Game:
   def __init__(self, window):
      # - self is the Game to initialize
      self.window = window
      Tile.set_window(window)
      self.bg_color = 'black'
      self.font_color = 'white'
      self.pause_time = 0.01 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      self.player_1 = 'X'
      self.player_2 = 'O'
      self.cursor_x = Cursor('cursorx.txt')
      self.cursor_o = Cursor('cursoro.txt')
      self.cursor_x.activate()
      self.current_player = self.player_1
      self.number_of_occopied_tiles = 0
      self.board_size = 3
      self.flashers = []
      self.flasher_index = 0
      self.board = []
      self.create_board()
      
   def create_board(self):
      # - self is the Game whose board is created
      for row_index in range(0, self.board_size):
         row = self.create_row(row_index)
         self.board.append(row)
      
   def create_row(self, row_index):
      # - self is the Game whose board row is being created
      
      row = []
      width = self.window.get_width() // self.board_size
      height = self.window.get_height() // self.board_size
      y = row_index * height
      for col_index in range(0, self.board_size):
         x = col_index * width
         tile = Tile(x, y, width, height)
         row.append(tile)
      return row

   def play(self):
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_event()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         time.sleep(self.pause_time) # set game velocity by pausing

   def handle_event(self):
      # - self is the Game whose events will be handled

      event = pygame.event.poll()
      if event.type == QUIT:
         self.close_clicked = True
      elif event.type == MOUSEBUTTONUP and self.continue_game:
         self.handle_mouse_up(event)
         
   def handle_mouse_up(self, event):
      # - self is the Game where the mouse up occurred.
      # - event is the pygame.event.Event object to handle
      
      for row in self.board:
         for tile in row: # for every tile
            valid_move = tile.select(event.pos, self.current_player) # assign symbol to current player symbol for later display; return whether move valid for later telling
            if valid_move: # that's why we need to initialize (assign False to) valid_move
               self.change_turn()# through changing current player's symbol, and atitivate corresponding cursor
               self.number_of_occopied_tiles = self.number_of_occopied_tiles + 1 #cuz valid move, this instance varaible  plus itself by 1.
               
   def change_turn(self): #activate cursor in change turn method!! (purpose fuctions same as update method)
      if self.current_player == self.player_1:
         self.current_player = self.player_2
         self.cursor_o.activate() 
      else:
         self.current_player = self.player_1
         self.cursor_x.activate()

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.window.clear()
      self.select_flasher()# flash an element in the flasher list each time the while loop is processed.
      for row in self.board:
         for tile in row:
            tile.draw() #draw every tile
      self.window.update() #don't forget self.window.update!!!

   def select_flasher(self):
      if self.flashers != []: #only flash when there is tiles needed to be flashed.
         tile = self.flashers[self.flasher_index]#cuz this method is in the draw method in the while loop, thus, flash all elements in the flasher list,but each row flash together,nextround(while processision the next row)
         tile.flash()
         self.flasher_index = (self.flasher_index + 1) % len(self.flashers) # equals to seld add 1 but controll in the range and avoid index out of range and functions repetitively.
   

   def update(self):
      # Update the game objects.
      # - self is the Game to update
      pass
      
   def decide_continue(self):
      # - self is the Game to check
      
      if self.is_win() or self.is_tie():# if a player wins or all tiles are occupied, game stops
         self.continue_game = False
         self.pause_time = 0.03

   def is_tie(self):

      tie = False
      if self.number_of_occopied_tiles == self.board_size**2: # and not self.is_win(): <= is not necessary because of the lazy evlauation of self.is_win() or self.is_tie() in decide_continue
         tie = True
         for row in self.board:
               self.flashers.extend(row)#add all elements in each row into flash list so that in this case when tiles are all occupied flash one row each time. 
      return tie


   def is_win(self):
      is_row_win = self.is_row_win()
      is_column_win = self.is_column_win()
      is_diagonal_win = self.is_diagonal_win()# cannot omit those 3 lines cuz lazy evaluation (A or B or C, if A is true then B and C won't be evaluated and return True directly, but if force them to be assigned, then they are all evaluated.)
      return is_row_win or is_column_win or is_diagonal_win 
   

   def is_row_win(self):
      is_row_win = False #initialize 
      for row in self.board: 
         if self.is_list_win(row): 
            is_row_win = True # if any row wins, assign True
      return is_row_win
   
   def is_column_win(self):
      is_column_win = False # initialize
      for column_index in range(0, self.board_size):
         column = []# every column becomes a independent list
         for row_index in range(0, self.board_size):
            column.append(self.board[row_index][column_index])#coloumn index is fixed for each column, and row indexes are 0-(size-1) for each column
         if self.is_list_win(column): #judge each newly-created column list
            is_column_win = True


      return is_column_win

   def is_diagonal_win(self):
      diag_1 = []# no need to initialize within for loop like is_column_win cuz there is only 1 left and right daigonal. 
      diag_2 = []
      for index in range(0, self.board_size):
               diag_1.append(self.board[index][index])#rightdownward diagonal
               diag_2.append(self.board[index][self.board_size - (index + 1)])#sum of index of row and column is (size-1)
      is_diag_1_win = self.is_list_win(diag_1)
      is_diag_2_win = self.is_list_win(diag_2)
      return is_diag_1_win or is_diag_2_win 

   def is_list_win(self, tile_list): #1.decide whether the list wins 2.extend winning elements ready to be flashed
      # need a given list as argument
      tile_0 = tile_list[0]
      is_list_win = True #initialize as True cuz as long as one element not equal, we need to assign False.
      
      for tile in tile_list:# compare all Tile obj in the given list to the first Tile obj of that list
#         if not tile_0.is_equal(tile):
         if tile_0 != tile: # equivalent to not tile_0.__eq__(tile)
            # (tile == tile is True) means all instance attributes of those two Tile obj are the same
            is_list_win = False#as long as there is one Tile obj in the list is not the same, this list is not winning, thus, we initialize the is_list_win as True. 
            
            
      if is_list_win:
         # these tiles in tile_list have to be flashed  
         self.flashers.extend(tile_list)# flash all elemens(Tile objects) in the list
      return is_list_win
      


class Tile:
   # An object in this class represents a Rectangular tile
   # that contains a string. A new tile contains an empty
   # string. A tile can be selected if the tile contains a
   # position. If an empty tile is selected its string can
   # be changed. If a non-empty tile is selected it will flash
   # the next time it is drawn. A tile can also be set to
   # flash forever. Two tiles are equal if they contain the
   # same non-empty string.


   # initialize the class attributes that are common to all tiles.
   window = None 
   fg_color = pygame.Color('white') # border color
   border_width = 3  # the pixel width of the tile border
   font_size = 144 # for drawing the player symbol

   @classmethod
   def set_window(cls, window):
      cls.window = window

   def __init__(self, x, y, width, height):
      # Initialize a tile to contain a ' '
      # - x is the int x coord of the upper left corner
      # - y is the int y coord of the upper left corner
      self.rectangle = pygame.Rect(x, y, width, height)
      self.content = '' #every Tile obj has to have a content str
      self.flashing = False #every tile has to have a varaiable controls whether it is falshed or not

#   def is_equal(self, other_tile):
#      return self.content == other_tile.content and self.content != ''

   def __eq__(self, other_tile):
      return self.content == other_tile.content and self.content != ''
      
   def select(self, mouse_position, player_symbol): # organize content of clicked Tile for displaying
      # - self is the Tile
      # - position is the selected location (tuple)
      # - new_content is the new str contents of the tile
      
      valid_move = False #initialize valid_move
      if self.rectangle.collidepoint(mouse_position):
         if self.content == '':  # if the clicked tile is unoccupied
            self.content = player_symbol #assign the player's symbol to instance variable for displaying
            valid_move = True # cuz in this case a valid move is made, assign True to valid move
         else:
            self.flashing = True # if the clicked tile is occupied, flash once
            #assign True to self.flashing only flashes the Tile once, but append a tile into self.flashing list will flash it continuously cause the second method is written in the draw() in while loop. 
      return valid_move
   
   def draw(self):
      # Draw the tile on the surface
      # - self is the Tile
      
      if self.flashing:# falsh the tile that needed to be flashed
         pygame.draw.rect(Tile.window.get_surface(), Tile.fg_color, self.rectangle)
         self.flashing = False #if a tile is flashed in this round, show regular content in next round
      else:
         self.draw_content() #if no need to flash, draw regular cotent and black tile background
         
   def draw_content(self):#draw rect tiles and its content
         pygame.draw.rect(Tile.window.get_surface(), Tile.fg_color, self.rectangle, Tile.border_width)#if there appears borderwidth as argument, color argument becomes color of border, otherwise color is filled to whole tile.
         Tile.window.set_font_size(Tile.font_size)
         content_width = Tile.window.get_string_width(self.content)
         content_height = Tile.window.get_font_height()
         content_x = self.rectangle.left + (self.rectangle.width - content_width) // 2 
         content_y = self.rectangle.top + (self.rectangle.height - content_height) // 2
         Tile.window.draw_string(self.content, content_x, content_y) 


         
   def flash(self):
      self.flashing = True


class Cursor:
   
   def __init__(self, filename):
      
      cursor_string_list = self.read_cursor_data(filename)
      
      self.size = (len(cursor_string_list[0]), len(cursor_string_list))#size[width,height]
      self.hotspot = (self.size[0] // 2, self.size[1] // 2)
      compiled = pygame.cursors.compile(cursor_string_list, black='*', white='x')
      self.xormasks = compiled[0]
      self.andmasks = compiled[1]
   
   def activate(self):
      pygame.mouse.set_cursor(self.size, self.hotspot, self.xormasks, self.andmasks)
      
   def read_cursor_data(self, filename):
      file = open(filename, 'r')# open in reading mode
      string_list = []
      for line in file:
         string_list.append(line.strip('\n'))
      return string_list
   
   ''' 
   Alternative implementations of the read_cursor_data method:
   ===========================================================
   
   def read_cursor_data(self, filename):
      file = open(filename, 'r')
      strings = file.read().splitlines()
      file.close()
      return strings
      
   def read_cursor_data(self, filename):
      file = open(filename, 'r')
      strings = file.readlines()
      for i in range(len(strings)):
         strings[i] = strings[i].strip('\n')
      file.close()
      return strings

   '''
   
main()