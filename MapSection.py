import pygame
from Map import Map

class MapSection:
    WINDOW_SIZE = (600, 600)
    SPEED = 2
    WAIT_TIME = 300
    CELL_SIZE = 75
    IMAGE_FOLDER = "image"

    """
    display: (pygame.Surface)
    size: (tuple of two int)
    map: (2d-list)
    ch_pos: (list of two int)
    ch_direction: (string) in ["l", "r", "u", "d"]
    """
    def __init__(self, display, filename):
        self.map = Map(filename)
        self.load_imgs()
        self.size = self.map.getSize()
        self.env = self.map.getEnv()
        self.ch_pos = self.map.ch_position
        self.ch_direction = self.map.ch_direction
        self.draw_prog = 0
        self.move_sequence = []

        height = self.size[0]
        width = self.size[1]
        self.display = pygame.Surface((height*75, width*75))

        
        self.master = display
        self.init()
        

    def load_imgs(self):
        self.stone_img = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/stone.png"), (75,75))
        self.grace_img = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/grace.png"), (75,75))
        self.animal_img = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/egg.png"), (75,75))
        self.bg_img = pygame.image.load(MapSection.IMAGE_FOLDER+"/grid_bg.png")
        self.arrow_u = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/arrow_u.png"), (75,25))
        self.arrow_d = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/arrow_d.png"), (75,25))
        self.arrow_l = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/arrow_l.png"), (25,75))
        self.arrow_r = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/arrow_r.png"), (25,75))
        self.sad_face_tl = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/sad_face_tl.png"), (75,75))
        self.sad_face_tr = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/sad_face_tr.png"), (75,75))
        self.sad_face_bl = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/sad_face_bl.png"), (75,75))
        self.sad_face_br = pygame.transform.scale(
                            pygame.image.load(MapSection.IMAGE_FOLDER+"/sad_face_br.png"), (75,75))



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


    def init(self):
        self.draw_map()

        # draw Grace
        self.display.blit(self.grace_img, (self.ch_pos[0]*75, self.ch_pos[1]*75))

        self.draw_on_master()


    def reach_egg(self):
        pass


    def collide(self):
        if (self.draw_prog > 600):
            self.draw_prog = 0
            self.move_sequence.pop()
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
                    self.display.blit(self.sad_face_tl, (pos[0]-60, pos[1]+60))
                else: # right side
                    self.display.blit(self.sad_face_br, (pos[0]-60, pos[1]+60))
            elif (self.ch_pos[1] == 0): # top side, without top right corner
                self.display.blit(self.sad_face_tr, (pos[0]+60, pos[1]+60))
            else:
                self.display.blit(self.sad_face_bl, (pos[0]+60, pos[1]-60))
        
        self.draw_prog += MapSection.SPEED
        self.draw_on_master()


    def display_update(self):
        if (len(self.move_sequence) == 0):
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

            # win situation
            if (self.env[x][y] == 1):
                self.move_sequence = ["win"]
                self.reach_egg()
                return

            # lose situation, collide on walls
            if (x >= self.size[0] or x < 0 or 
                y >= self.size[1] or y < 0 or
                self.env[x][y] != 0):
                self.move_sequence = ["lose"]
                self.collide()
                return
        
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
