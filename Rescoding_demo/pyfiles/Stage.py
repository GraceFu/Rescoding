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

            self.scroll_program()

            self.mapSec.display_update()
            self.draw_rightSection()
            self.draw_currentDrag()

            if (self.mapSec.isWin()):
                return "choose level", 1
            elif(self.mapSec.isLose()):
                self.status = None

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
        self.mapSec = MapSection(self.window, filename)


    # draw command part
    def draw_program(self):
        self.programCanvas.blit(self.program_bg, (0,0))
        self.programCanvas.blit(self.program_bg, (0,600))
        
        self.programCanvas.blit(self.prog_main, (25, 10))

        # display command boxes
        for i in range(len(self.commandBoxList)):
            self.commandBoxList[i].displayUpdate(self.programCanvas)

        self.rightCanvas.blit(self.programCanvas, (200, self.program_y))


    def run_prog(self):
        command_list = []
        for commandBox in self.commandBoxList:
            command_list.append(commandBox.getCommand())
        self.status = "running"
        self.mapSec.move(command_list)


    # draw the right section
    def draw_rightSection(self):
        # draw command list 
        self.rightCanvas.blit(self.command_bg, (0,0))
        

        self.checkCommandBoxes()

        self.draw_program()

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
            y = len(self.commandBoxList) * 60 + 70 + self.program_y
            
            pos = self.currentDragging.pos
            if (pos[0] <= x+60 and pos[0] >= x-60 and pos[1] <= y+30 and pos[1] >= y-30):
                self.commandBoxList.append(self.currentDragging)
            self.currentDragging = -1
        
        else:
            self.currentDragging.displayUpdate(self.window, True)

    
    def scroll_program(self):
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] < 800):
            return
        if (mouse_pos[1] < 20):
            if (self.program_y <= -10):
                self.program_y += 10
        elif (mouse_pos[1] > 580):
            if (self.program_y >= -590):
                self.program_y -= 10