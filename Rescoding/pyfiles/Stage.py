import pygame, sys, json, gameSetting

class Stage:

    IMAGE_PATH = "images/"
    STAGE_PATH = "stages/"
    """
    @ param window: (pygame.Surface) main window
    @ param args: (int) stage number
    """
    def __init__(self, window, args):
        self.cell_size = 75
        self.window = window
        self.mapCanvas = pygame.Surface((600,600))
        self.commandCanvas = pygame.Surface((200, 600))
        self.programCanvas = pygame.Surface((200, 600))

        self.loadImage()
        self.readMapInfo(args)
        

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_map()

            pygame.display.update()
            clock.tick(gameSetting.FPS)

    
    def loadImage(self):
        # for map canvas
        self.bg_img = pygame.image.load(self.IMAGE_PATH+"grid_bg.png")
        self.grace_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"grace.png"), (75,75))
        self.animal_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"egg.png"), (75,75))
        self.stone_img = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"stone.png"), (75,75))
        self.arrow_u = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_u.png"), (75,25))
        self.arrow_d = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_d.png"), (75,25))
        self.arrow_l = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_l.png"), (25,75))
        self.arrow_r = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"arrow_r.png"), (25,75))
        self.sadface_tl = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_tl.png"), (75,75))
        self.sadface_tr = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_tr.png"), (75,75))
        self.sadface_bl = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_bl.png"), (75,75))
        self.sadface_br = pygame.transform.scale(pygame.image.load(self.IMAGE_PATH+"sadface_br.png"), (75,75))

        # for command list
        self.command_bg = pygame.image.load(self.IMAGE_PATH+"commandList_bg.png")


    def readMapInfo(self, stageNum):
        filename = self.STAGE_PATH + "stage%d.txt"%stageNum
        with open(filename, 'r') as file:
            data = json.load(file)
            self.map_size = tuple(data["size"])
            self.ch_pos = data["grace_position"]
            self.ch_direction = data["grace_direction"]
            animal = data["animal"]
            walls = data["walls"]
            rivers = data["rivers"]
            wolves = data["wolves"]
            self.command_list = data["command_list"]

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
        grace_pos = (self.ch_pos[0]*self.cell_size, self.ch_pos[1]*self.cell_size)
        self.draw_map_grace(grace_pos)
        self.draw_map_arrow(grace_pos)

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


    def draw_map_grace(self, pos):
        self.mapCanvas.blit(self.grace_img, pos)
    

    def draw_map_arrow(self, pos):
        if (self.ch_direction == "l"):
            self.mapCanvas.blit(self.arrow_l, (pos[0]-25, pos[1]))
        elif (self.ch_direction == "r"):
            self.mapCanvas.blit(self.arrow_r, (pos[0]+75, pos[1]))
        elif (self.ch_direction == "u"):
            self.mapCanvas.blit(self.arrow_u, (pos[0], pos[1]-20))
        else: #self.ch_direction == "d"
            self.mapCanvas.blit(self.arrow_d, (pos[0], pos[1]+75))
    
    
    # draw command part
    def draw_command(self):
        self.commandCanvas.blit(self.command_bg, (0,0))
        



    # draw program part
    def draw_program(self):
        pass