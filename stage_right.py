import pygame
from MapSection import MapSection

# Define colors

class stageRight:
    PINK = (254, 223, 225)
    MINT = (186, 216, 185)

    STAGE_FOLDER_NAME = "stages"
    IMAGE_FOLDER_NAME = "image"

    def __init__(self, master, stage_level):
        pygame.init()
        self.SCREEN = master
        self.SCREEN.fill(pygame.Color('white'))
        self.close_clicked = False
        #self.back_clicked = False
        self.stage_end = False
        self.current_hb = None
        self.dragging = False
        self.f = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_forward.png')
        self.l = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_left.png')
        self.r = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_right.png')
        self.run = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_run.png')
        self.back_button = pygame.image.load(self.IMAGE_FOLDER_NAME+'/back_button.png')
        self.obj = []
        self.mapsection = MapSection(self.SCREEN, "stages/stage%d.txt"%stage_level)


    def motion(self):
        clock = pygame.time.Clock()
        while True:  # until player clicks close box play frame

            self.draw()
            self.handle_event()
            self.moving()
            if not self.stage_end and self.run_hb.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0] == 1:
                run_list = self.run_test()
                self.mapsection.move(run_list)
                #self.stage_end = True
            if self.mapsection.isLose():
                self.obj = []
            
            if self.mapsection.isWin(): # or self.back_clicked:
                return

            self.mapsection.display_update()
            pygame.display.update()

            clock.tick(60)




    def draw(self):

        # right side background
        pygame.draw.rect(self.SCREEN, self.PINK, (600, 0, 400, 140))
        pygame.draw.rect(self.SCREEN, self.MINT, (600, 140, 400, 460))

        # display action boxes and create action hitboxes
        self.forward_hb = pygame.Rect(730, 80, 150, 40)
        self.SCREEN.blit(self.f, (730, 80))
        self.left_hb = pygame.Rect(640, 20, 150, 50)
        self.SCREEN.blit(self.l, (640, 20))
        self.right_hb = pygame.Rect(820, 20, 150, 50)
        self.SCREEN.blit(self.r, (820, 20))
        self.run_hb = pygame.Rect(830, 530, 150, 50)
        self.SCREEN.blit(self.run, (830, 530))

        # display dropped boxed
        for item in self.obj:
            self.SCREEN.blit(item[0], (item[1] - 75, item[2] - 25))

        # back button display
        #self.SCREEN.blit(pygame.transform.scale(self.back_button, (50,50)), (930,80))
        #back_button_hb = pygame.Rect(935, 80, 45, 45)
        #if pygame.mouse.get_pressed()[0] == 1 and back_button_hb.collidepoint(pygame.mouse.get_pos()):
        #    self.back_clicked = True


    def moving(self):
        pos = pygame.mouse.get_pos()
        if self.dragging:
            self.SCREEN.blit(self.dragging_box, (pos[0] - 75, pos[1] - 25))

    def handle_event(self):
        event = pygame.event.poll()

        #for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.stage_end:
            self.current_hb = None
            pos = pygame.mouse.get_pos()

            if self.forward_hb.collidepoint(pos[0], pos[1]):
                self.dragging = True
                self.current_hb = self.forward_hb
                self.dragging_box = self.f
            elif self.left_hb.collidepoint(pos[0], pos[1]):
                self.dragging = True
                self.current_hb = self.left_hb
                self.dragging_box = self.l
            elif self.right_hb.collidepoint(pos[0], pos[1]):
                self.dragging = True
                self.current_hb = self.right_hb
                self.dragging_box = self.r

        elif event.type == pygame.MOUSEBUTTONUP and not self.stage_end:
            pos = pygame.mouse.get_pos()
            self.dragging = False
            if self.current_hb == self.forward_hb:
                self.obj.append((self.f, pos[0], pos[1], 'f'))
            elif self.current_hb == self.left_hb:
                self.obj.append((self.l, pos[0], pos[1], 'l'))
            elif self.current_hb == self.right_hb:
                self.obj.append((self.r, pos[0], pos[1], 'r'))


    def sorted_by_y_axis(self, obj):
        return obj[2]


    def run_test(self):
        self.obj.sort(key=self.sorted_by_y_axis)
        run_list = []
        for item in self.obj:
            run_list.append(item[-1])
        return run_list


