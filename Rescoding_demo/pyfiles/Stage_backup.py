import pygame, sys, json, gameSetting
from pyfiles.Button import Button
from pyfiles.CommandBox import CommandBox
from pyfiles.MapSection import MapSection

class Stage:

    IMAGE_PATH = "images/"
    STAGE_PATH = "stages/"

    DELTA_SPEED = 5
    """
    @ param window: (pygame.Surface) main window
    @ param args: (int) stage number
    """
    def __init__(self, window, args):
        self.cell_size = 75
        self.window = window
        self.mapCanvas = pygame.Surface((600,600))
        self.rightCanvas = pygame.Surface((400, 600))
        self.programCanvas = pygame.Surface((200, 1200))

        self.loadImage()
        self.stageNum = args
        self.readMapInfo()
        

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if (self.currentDragging == -1):
                commandBox = None
                if self.comm_forward_static.isClicked():
                    commandBox = CommandBox(self.forward_imgPath, "f", scale=(150,50))
                    commandBox.setPosition((25, 10))
                elif self.comm_left_static.isClicked():
                    commandBox = CommandBox(self.left_imgPath, "l",scale=(150,50))
                    commandBox.setPosition((25, 70))
                elif self.comm_right_static.isClicked():
                    commandBox = CommandBox(self.right_imgPath, "r",scale=(150,50))
                    commandBox.setPosition((25, 130))
                
                if commandBox != None:
                    self.currentDragging = commandBox

            if self.comm_run_static.isClicked() and self.status == None:
                self.run_prog()

            if self.status == "running":
                self.running_update()

            self.draw_map()
            self.draw_rightSection()
            self.draw_currentDrag()

            if self.status == "win":
                self.win_update()
            elif self.status == "loss":
                self.loss_update()

            if (self.win_bool):
                return "choose level", 1

            pygame.display.update()
            clock.tick(gameSetting.FPS)



    def loadImage(self):
        # for map canvas
        self.bg_img = pygame.image.load(self.IMAGE_PATH+"grid_bg.png")
        self.grace_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"grace.png"), (75,75))
        self.animal_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"egg.png"), (75,75))
        self.huge_egg_img = pygame.transform.scale(self.animal_img, (150, 150))
        self.stone_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"stone.png"), (75,75))
        self.arrow_u = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_u.png"), (75,25))
        self.arrow_d = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_d.png"), (75,25))
        self.arrow_l = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_l.png"), (25,75))
        self.arrow_r = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_r.png"), (25,75))
        self.sad_face_tl = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_tl.png"), (75,75))
        self.sad_face_tr = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_tr.png"), (75,75))
        self.sad_face_bl = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_bl.png"), (75,75))
        self.sad_face_br = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_br.png"), (75,75))

        self.win_msg_box = pygame.image.load(self.IMAGE_PATH+"win_msg.png")
        self.win_cont_hover = pygame.image.load(self.IMAGE_PATH+"win_msg_cont_hover.png")

        # for command list and program part
        self.command_bg = pygame.image.load(self.IMAGE_PATH+"commandList_bg.png")
        self.program_bg = pygame.image.load(self.IMAGE_PATH+"program_bg.png")
        self.comm_forward_static = Button(self.window, self.IMAGE_PATH+"comm_forward.png", (625, 10), scale=(150, 50))
        self.comm_left_static = Button(self.window, self.IMAGE_PATH+"comm_left.png", (625, 70), scale=(150, 50))
        self.comm_right_static = Button(self.window, self.IMAGE_PATH+"comm_right.png", (625, 130), scale=(150, 50))
        self.comm_run_static = Button(self.window, self.IMAGE_PATH+"comm_run.png", (625, 500), scale=(150,50), onClick="smaller")
        self.prog_main = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"comm_main.png"), (150, 50))

        self.forward_imgPath = self.IMAGE_PATH + "comm_forward.png"
        self.left_imgPath = self.IMAGE_PATH + "comm_left.png"
        self.right_imgPath = self.IMAGE_PATH + "comm_right.png"

        self.commandBoxList = []
        self.currentDragging = -1
        self.program_y = 0
        
        self.status = None
        self.delta = -1
        self.currentCommand = None
        self.win_bool = False


    def readMapInfo(self):
        filename = self.STAGE_PATH + "stage%d.txt"%self.stageNum
        with open(filename, 'r') as file:
            data = json.load(file)
            self.map_size = tuple(data["size"])
            self.ch_pos = data["grace_position"]
            self.ch_direction = data["grace_direction"]
            animal = data["animal"]
            walls = data["walls"]
            rivers = data["rivers"]
            wolves = data["wolves"]
            # self.command_list = data["command_list"]

        self.grace_actual_pos = [self.ch_pos[0]*self.cell_size, self.ch_pos[1]*self.cell_size]

        # init all entry in self.env to 0
        self.env = []
        for i in range(self.map_size[0]):
            temp = []
            for j in range(self.map_size[1]):
                temp.append(0)
            self.env.append(temp)
        
        self.env[animal[0]][animal[1]] = 1
        
        for wall in walls:
            self.env[wall[0]][wall[1]] = 2
        
        for wolf in wolves:
            self.env[wolf[0]][wolf[1]] = 3

        for river in rivers:
            self.env[river[0]][river[1]] = 4


    # draw map part
    def draw_map(self):
        self.draw_map_env()
        if (self.status != "loss"):
            self.draw_map_grace()

        self.window.blit(self.mapCanvas, (0, 0))


    def draw_map_env(self):
        # draw map
        self.mapCanvas.blit(self.bg_img, (0, 0))
        for r in range(self.map_size[0]):
            for c in range(self.map_size[1]):
                pos = (r*self.cell_size, c*self.cell_size)
                if (self.env[r][c] == 1):
                    self.mapCanvas.blit(self.animal_img, pos)
                if (self.env[r][c] == 2):
                    self.mapCanvas.blit(self.stone_img, pos)


    def draw_map_grace(self, arrow=True):
        self.mapCanvas.blit(self.grace_img, self.grace_actual_pos)

        if (arrow):
            pos = self.grace_actual_pos
            if (self.ch_direction == "l"):
                self.mapCanvas.blit(self.arrow_l, (pos[0]-25, pos[1]))
            elif (self.ch_direction == "r"):
                self.mapCanvas.blit(self.arrow_r, (pos[0]+75, pos[1]))
            elif (self.ch_direction == "u"):
                self.mapCanvas.blit(self.arrow_u, (pos[0], pos[1]-20))
            else: #self.ch_direction == "d"
                self.mapCanvas.blit(self.arrow_d, (pos[0], pos[1]+75))
        

    # draw command part
    def deltaram(self):
        self.programCanvas.blit(self.program_bg, (0,0))
        self.programCanvas.blit(self.program_bg, (0,600))
        
        self.programCanvas.blit(self.prog_main, (25, 10))

        # display command boxes
        for i in range(len(self.commandBoxList)):
            self.commandBoxList[i].displayUpdate(self.programCanvas)

        self.rightCanvas.blit(self.programCanvas, (200, self.program_y))


    def run_prog(self):
        self.command_list = []
        for commandBox in self.commandBoxList:
            self.command_list.append(commandBox.getCommand())
        
        self.status = "running"
        self.delta = 301


    def running_update(self):
        if (self.delta > 300):
            print(self.command_list)
            self.command_list.pop(0)
            self.currentCommand = self.command_list[0]
            self.ch_update()
            self.delta = 0
        
        if (self.delta < 100):
            if self.currentCommand == "f":
                pos = [self.ch_pos[0]*75, self.ch_pos[1]*75]
                fwd = self.delta * 0.01 * 75
                if (self.ch_direction == "l"):
                    pos[0] -= fwd
                elif (self.ch_direction == "r"):
                    pos[0] += fwd
                elif (self.ch_direction == "u"):
                    pos[1] -= fwd
                else: # self.ch_direction == "d"
                    pos[1] += fwd
                self.grace_actual_pos = pos
            
        self.delta += self.DELTA_SPEED


    def ch_update(self):
        op = self.currentCommand
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
        
        # lose situation no.1
        if (len(self.command_list) == 0) :
            self.status = "loss"
            return

        # lose situation, collide on walls
        if (x >= self.map_size[0] or x < 0 or 
            y >= self.map_size[1] or y < 0 or
            (self.env[x][y] != 0 and self.env[x][y] != 1)):
            self.status = "loss"
            return

        # winning situation
        if (self.env[x][y] == 1):
            self.status = "win"
            return


    def win_update(self):
        self.window.blit(self.win_msg_box, (100, 150))
        self.window.blit(self.huge_egg_img, (227, 245))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_hb = pygame.Rect(mouse_pos[0], mouse_pos[1], 5, 5)
        button_hb = pygame.Rect(220, 402, 192, 46)

        if (self.win_bool):
            self.delta = 0
            return
        
        if mouse_hb.colliderect(button_hb):   # check if mouseover
            self.window.blit(self.win_cont_hover, (220, 402)) 
            if mouse_click == 1:   # if user clicks on button, go to menu
                self.win_bool = True


    def loss_update(self):
        if (self.delta > 600):
            self.delta = 0
            self.readMapInfo()
            self.status = None
            return

        self.draw_map()
        pos = [self.ch_pos[0]*75, self.ch_pos[1]*75]
        # blinking Grace
        if (self.delta < 200):
            if (self.delta % 80 < 40):
                self.draw_map_grace(False)
        
        # sad face
        else:
            self.draw_map_grace(False)
            if (self.ch_pos[0] == self.map_size[0]-1):
                if (self.ch_pos[1] == 0): # top right corner
                    self.window.blit(self.sad_face_tr, (pos[0]-60, pos[1]+60))
                else: # right side
                    self.window.blit(self.sad_face_br, (pos[0]-60, pos[1]+60))
            elif (self.ch_pos[1] == 0): # top side, without top right corner
                self.window.blit(self.sad_face_tl, (pos[0]+60, pos[1]+60))
            else:
                self.window.blit(self.sad_face_bl, (pos[0]+60, pos[1]-60))
        
        self.delta += self.DELTA_SPEED


    # draw the right section
    def draw_rightSection(self):
        # draw command list 
        self.rightCanvas.blit(self.command_bg, (0,0))
        

        self.checkCommandBoxes()

        self.deltaram()

        self.window.blit(self.rightCanvas, (600,0))

        self.comm_forward_static.displayUpdate()
        self.comm_left_static.displayUpdate()
        self.comm_right_static.displayUpdate()
        self.comm_run_static.displayUpdate()

    

    
    def checkCommandBoxes(self):
        destroyIndex = -1
        for i in range(len(self.commandBoxList)):
            if self.commandBoxList[i].isClicked()[1]:
                destroyIndex = i
                break
        if destroyIndex != -1:
            self.commandBoxList.pop(destroyIndex)
        else:
            destroyIndex = 0
        
        for i in range(destroyIndex, len(self.commandBoxList)):
            pos = (25, i*60 + 70)
            self.commandBoxList[i].setPosition(pos)

    
    def draw_currentDrag(self):
        if self.currentDragging == -1:
            return
        if not pygame.mouse.get_pressed()[0]:
            x = 825
            y = len(self.commandBoxList) * 60 + 70
            
            pos = self.currentDragging.pos
            if (pos[0] <= x+60 and pos[0] >= x-60 and pos[1] <= y+30 and pos[1] >= y-30):
                self.commandBoxList.append(self.currentDragging)
            self.currentDragging = -1
        
        else:
            self.currentDragging.displayUpdate(self.window, True)