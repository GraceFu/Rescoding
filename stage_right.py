import pygame
from MapSection import MapSection

# Define colors
PINK = (254, 223, 225)
MINT = (186, 216, 185)


class stageRight:
    SCREEN = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Rescoding")
    SCREEN.fill(pygame.Color('white'))

    STAGE_FOLDER_NAME = "stages"
    IMAGE_FOLDER_NAME = "image"

    def __init__(self):
        pygame.init()
        self.close_clicked = False
        self.stage_end = False
        self.dragging = False
        self.f = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_forward.png')
        self.l = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_left.png')
        self.r = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_right.png')
        self.run = pygame.image.load(self.IMAGE_FOLDER_NAME+'/comm_run.png')
        self.obj = []
        self.mapsection = MapSection(self.SCREEN, "stages/stage1.txt")

    def motion(self):
        while not self.close_clicked:  # until player clicks close box play frame
            self.draw()
            self.handle_event()
            self.moving()
            if not self.stage_end and self.run_hb.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0] == 1:
                run_list = self.run_test()
                self.mapsection.move(run_list)
                #self.stage_end = True
            if self.mapsection.isLose():
                self.obj = []

            self.mapsection.display_update()
            pygame.display.update()
        pygame.quit()

    def draw(self):

        # right side background
        pygame.draw.rect(self.SCREEN, PINK, (600, 0, 400, 140))
        pygame.draw.rect(self.SCREEN, MINT, (600, 140, 400, 460))

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

    def moving(self):
        pos = pygame.mouse.get_pos()
        if self.dragging:
            self.SCREEN.blit(self.dragging_box, (pos[0] - 75, pos[1] - 25))

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.close_clicked = True
            self.continue_game = False

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


if __name__ == '__main__':
    sr = stageRight()
    sr.motion()
    clock = pygame.time.Clock()
    cont = True
    run = True
    click_time = 0
