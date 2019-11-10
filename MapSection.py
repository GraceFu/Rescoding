import pygame
import json

"""
INTERFACES:

To import this file
use: from MapSection import MapSection

@ methods (of MapSection):
    self.move(move_sequence): (list) arbitrary length with, value = "f", "l", "r"
    self.display_update(): single loop function
    self.isWin(): return True if usr wins, False otherwise
    self.isLose(): return True only if usr loses
"""


"""
@attributes:
    self.size: list of two int, (height, width)
    self.ch_position: list of two int, e.g. [3, 2]
    self.ch_direction: string of 1 char, l -> left, r -> right, u -> up, d -> down
    self.env: 2d-list of int, int representation:
        0 -> None
        1 -> animal
        2 -> walls
        3 -> wolves
        4 -> rivers
    self.command_list: list of string, values:
        "forward", "turn left", "turn right"
"""
class Map:
    
    def __init__(self, filename):
        self.env = []
        self.readfile(filename)
        
    
    def readfile(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.size = tuple(data["size"])
            self.ch_position = data["grace_position"]
            self.ch_direction = data["grace_direction"]
            animal = data["animal"]
            walls = data["walls"]
            rivers = data["rivers"]
            wolves = data["wolves"]
            self.command_list = data["command_list"]
        
        # init all entry in self.env to 0
        for i in range(self.size[0]):
            temp = []
            for j in range(self.size[1]):
                temp.append(0)
            self.env.append(temp)
        
        self.env[animal[0]][animal[1]] = 1
        
        for wall in walls:
            self.env[wall[0]][wall[1]] = 2
        
        for wolf in wolves:
            self.env[wolf[0]][wolf[1]] = 3

        for river in rivers:
            self.env[river[0]][river[1]] = 4


    def getSize(self):
        return self.size

    def getEnv(self):
        return self.env


"""
@ methods:
    self.move(move_sequence): (list) arbitrary length with, value = "f", "l", "r"
    self.display_update(): single loop function
"""
class MapSection:
    WINDOW_SIZE = (600, 600)
    SPEED = 5
    WAIT_TIME = 300
    CELL_SIZE = 75

    FOLDER_NAME = "image"

    """
    display: (pygame.Surface) where to draw
    filename: (string) filename of map
    """
    def __init__(self, display, filename):
        self.map = Map(filename)
        self.load_imgs()
        self.size = self.map.getSize()
        self.env = self.map.getEnv()
        self.ch_pos = self.map.ch_position[:]
        self.ch_direction = self.map.ch_direction
        self.draw_prog = 0
        self.move_sequence = []
        self.win_bool = False
        self.loss_bool = False

        height = self.size[0]
        width = self.size[1]
        self.display = pygame.Surface((height*75, width*75))

        self.master = display
        self.init()
        

    def load_imgs(self):
        self.stone_img = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/stone.png"), (75,75))
        self.grace_img = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/grace.png"), (75,75))
        self.animal_img = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/egg.png"), (75,75))
        self.bg_img = pygame.image.load(MapSection.FOLDER_NAME+"/grid_bg.png")
        self.arrow_u = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/arrow_u.png"), (75,25))
        self.arrow_d = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/arrow_d.png"), (75,25))
        self.arrow_l = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/arrow_l.png"), (25,75))
        self.arrow_r = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/arrow_r.png"), (25,75))
        self.sad_face_tl = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/sad_face_tl.png"), (75,75))
        self.sad_face_tr = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/sad_face_tr.png"), (75,75))
        self.sad_face_bl = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/sad_face_bl.png"), (75,75))
        self.sad_face_br = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/sad_face_br.png"), (75,75))
        self.win_msg_box = pygame.image.load(MapSection.FOLDER_NAME+"/win_msg.png")
        self.win_cont_hover = pygame.image.load(MapSection.FOLDER_NAME+"/win_msg_cont_hover.png")
        self.huge_egg_img = pygame.transform.scale(
                            pygame.image.load(MapSection.FOLDER_NAME+"/animal.png"), (150,150))


    def draw_map(self):
        # draw map
        self.display.blit(self.bg_img, (0, 0))
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                pos = (r*75, c*75)
                if (self.env[r][c] == 1):
                    self.display.blit(self.animal_img, pos)
                if (self.env[r][c] == 2):
                    self.display.blit(self.stone_img, pos)


    def basic_update(self):
        self.draw_map()

        # draw Grace
        self.display.blit(self.grace_img, (self.ch_pos[0]*75, self.ch_pos[1]*75))

        self.draw_on_master()


    def init(self):
        self.ch_direction = self.map.ch_direction
        self.ch_pos = self.map.ch_position[:]
        self.loss_bool = False
        self.draw()


    def isWin(self):
        return self.win_bool


    def isLose(self):
        return self.loss_bool


    def reach_egg(self):
        self.display.blit(self.win_msg_box, (100, 150))
        self.display.blit(self.huge_egg_img, (227, 245))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_hb = pygame.Rect(mouse_pos[0], mouse_pos[1], 5, 5)
        button_hb = pygame.Rect(220, 402, 192, 46)

        if (self.win_bool):
            self.draw_prog = 0
            self.move_sequence.pop()
            return
        
        if mouse_hb.colliderect(button_hb):   # check if mouseover
            self.display.blit(self.win_cont_hover, (220, 402)) 
            if mouse_click == 1:   # if user clicks on button, go to menu
                self.win_bool = True

        self.draw_on_master()


    def collide(self):
        if (self.draw_prog > 600):
            self.draw_prog = 0
            self.move_sequence.pop()
            self.init()
            return

        self.draw_map()
        pos = [self.ch_pos[0]*75, self.ch_pos[1]*75]
        # blinking Grace
        if (self.draw_prog < 200):
            if (self.draw_prog % 80 < 40):
                # draw Grace
                self.display.blit(self.grace_img, pos)
        
        # sad face
        else:
            # draw Grace
            self.display.blit(self.grace_img, pos)
            if (self.ch_pos[0] == self.size[0]-1):
                if (self.ch_pos[1] == 0): # top right corner
                    self.display.blit(self.sad_face_tr, (pos[0]-60, pos[1]+60))
                else: # right side
                    self.display.blit(self.sad_face_br, (pos[0]-60, pos[1]+60))
            elif (self.ch_pos[1] == 0): # top side, without top right corner
                self.display.blit(self.sad_face_tl, (pos[0]+60, pos[1]+60))
            else:
                self.display.blit(self.sad_face_bl, (pos[0]+60, pos[1]-60))
        
        self.draw_prog += MapSection.SPEED
        self.draw_on_master()


    def display_update(self):
        if (len(self.move_sequence) == 0):
            self.draw()
            return
        
        if (self.move_sequence[0] == "win"):
            self.reach_egg()
            return

        if (self.move_sequence[0] == "lose"):
            self.collide()
            return

        if (self.draw_prog > MapSection.WAIT_TIME):
            self.draw_prog = 0
            self.ch_update(self.move_sequence.pop(0))
            return
                    
        if (self.draw_prog < 100):
            self.draw()
        
        self.draw_prog += MapSection.SPEED
        return


    def draw_on_master(self):
        self.master.blit(pygame.transform.scale(self.display, MapSection.WINDOW_SIZE),(0,0))


    def draw(self):
        self.draw_map()
        csize = MapSection.CELL_SIZE
        pos = [self.ch_pos[0]*csize, self.ch_pos[1]*csize]

        if (len(self.move_sequence) != 0):
            if (self.move_sequence[0] == "f"):
                fwd = self.draw_prog * 0.01 * MapSection.CELL_SIZE
                if (self.ch_direction == "l"):
                    pos[0] -= fwd
                elif (self.ch_direction == "r"):
                    pos[0] += fwd
                elif (self.ch_direction == "u"):
                    pos[1] -= fwd
                else: # self.ch_direction == "d"
                    pos[1] += fwd

        if (self.ch_direction == "l"):
            self.display.blit(self.arrow_l, (pos[0]-25, pos[1]))
        elif (self.ch_direction == "r"):
            self.display.blit(self.arrow_r, (pos[0]+75, pos[1]))
        elif (self.ch_direction == "u"):
            self.display.blit(self.arrow_u, (pos[0], pos[1]-20))
        else: #self.ch_direction == "d"
            self.display.blit(self.arrow_d, (pos[0], pos[1]+75))

        self.display.blit(self.grace_img, tuple(pos))
        self.draw_on_master()


    def move(self, move_list):
        self.move_sequence = move_list

    
    # op: (string) in ["f", "l", "r"]
    def ch_update(self, op):
        if (op == "f"):
            if (self.ch_direction == "l"):
                self.ch_pos[0] -= 1
            elif (self.ch_direction == "r"):
                self.ch_pos[0] += 1
            elif (self.ch_direction == "u"):
                self.ch_pos[1] -= 1
            else: # self.ch_direction == "d"
                self.ch_pos[1] += 1
        
        elif (op == "l"):
            if (self.ch_direction == "l"):
                self.ch_direction = "d"
            elif (self.ch_direction == "r"):
                self.ch_direction = "u"
            elif (self.ch_direction == "u"):
                self.ch_direction = "l"
            else: # self.ch_direction == "d"
                self.ch_direction = "r"
        
        else: # op == "r"
            if (self.ch_direction == "l"):
                self.ch_direction = "u"
            elif (self.ch_direction == "r"):
                self.ch_direction = "d"
            elif (self.ch_direction == "u"):
                self.ch_direction = "r"
            else: # self.ch_direction == "d"
                self.ch_direction = "l"
        
        # win/loss detection
        x = self.ch_pos[0]  # x coord
        y = self.ch_pos[1]  # y coord

        if (self.ch_direction == "l"):
            x -= 1
        elif (self.ch_direction == "r"):
            x += 1
        elif (self.ch_direction == "u"):
            y -= 1
        else: # self.ch_direction == "d"
            y += 1

        # lose situation no.1
        if (len(self.move_sequence) == 0) :
            self.loss_bool = True
            self.move_sequence = ["lose"]
            self.collide()
            return 
            
        if (self.move_sequence[0] != "f"):
            return

        # lose situation, collide on walls
        if (x >= self.size[0] or x < 0 or 
            y >= self.size[1] or y < 0 or
            (self.env[x][y] != 0 and self.env[x][y] != 1)):
            self.loss_bool = True
            self.move_sequence = ["lose"]
            self.collide()
            return

        # winning situation
        if (self.env[x][y] == 1):
            self.move_sequence = ["win"]
            self.reach_egg()
            return
