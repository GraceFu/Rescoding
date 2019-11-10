import pygame
import time
from stage_right import stageRight


class WindowPage:
    def __init__(self,color=None):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Rescoding")


class Game:
    
    def __init__(self, window):
        
        self.loadimage()
        self.menu_open = False
        if self.menu_open == False:
            self.home_display()   # display home page
        else:
            self.menu_display()


    def loadimage(self):
        self.start_hover = pygame.image.load('image/start_button_hover.png')
        self.home_bg_img = pygame.image.load('image/mainpage_bg.png')
        self.start_button = pygame.image.load('image/start_button.png')
        self.start_hover = pygame.image.load('image/start_button_hover.png')
        self.menu_bg_img = pygame.image.load('image/menu_bg.png')
        self.menu_back_button = pygame.image.load('image/back_button.png')
        self.stage1 = pygame.image.load('image/stages/stage1.png')
        self.stage2 = pygame.image.load('image/stages/stage2.png')
        self.stage3 = pygame.image.load('image/stages/stage3.png')
        self.stage4 = pygame.image.load('image/stages/stage4.png')
        self.stage5 = pygame.image.load('image/stages/stage5.png')
        self.stage6 = pygame.image.load('image/stages/stage6.png')


    def home_display(self):
        
        # background image display
        window.screen.blit(self.home_bg_img, (0,0))
        
        # start button display
        self.start_hb = pygame.Rect(350, 320, 265, 110)
        window.screen.blit(self.start_button, (350, 320))
        
        # Mouse: get position, define click, create nouse hitbox
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)
        
        # Start button
        if self.mouse_hb.colliderect(self.start_hb):   # check if mouseover
            window.screen.blit(self.start_hover, (350, 320)) 
            if self.click == 1:   # if user clicks on button, go to menu
                self.menu_open = True

        
    def menu_display(self):

        # background image display
        window.screen.blit(self.menu_bg_img, (0,0))

        # level buttons display
        self.level_button()

        # back button display
        window.screen.blit(pygame.transform.scale(self.menu_back_button, (50,50)), (930,30))
        back_button_hb = pygame.Rect(935, 35, 45, 45)
        if self.click == 1 and self.mouse_hb.colliderect(back_button_hb):
            self.menu_open = False

        # Mouse: get position, define click, create nouse hitbox
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)

    def level_button(self):

        size = (75,75)


        window.screen.blit(pygame.transform.scale(self.stage1, size), (60,75))
        stage1_hb = pygame.Rect(65, 80, 65, 65)
        self.stage1_clicked = self.mouse_hb.colliderect(stage1_hb) and self.click

        window.screen.blit(pygame.transform.scale(self.stage2, size), (90,300))
        stage2_hb = pygame.Rect(95, 305, 65, 65)
        self.stage2_clicked = self.mouse_hb.colliderect(stage2_hb) and self.click

        window.screen.blit(pygame.transform.scale(self.stage3, size), (250,510))
        stage3_hb = pygame.Rect(255, 515, 65, 65)
        self.stage3_clicked = self.mouse_hb.colliderect(stage3_hb) and self.click

        window.screen.blit(pygame.transform.scale(self.stage4, size), (380,320))
        stage4_hb = pygame.Rect(385, 325, 65, 65)
        self.stage4_clicked = self.mouse_hb.colliderect(stage4_hb) and self.click

        window.screen.blit(pygame.transform.scale(self.stage5, size), (635,350))
        stage5_hb = pygame.Rect(255, 515, 65, 65)
        self.stage5_clicked = self.mouse_hb.colliderect(stage5_hb) and self.click

        window.screen.blit(pygame.transform.scale(self.stage6, size), (780,490))
        stage6_hb = pygame.Rect(785, 495, 65, 65)
        self.stage6_clicked = self.mouse_hb.colliderect(stage6_hb) and self.click 


if __name__ == '__main__':
    window = WindowPage()
    homepage = True
    menupage = False
    stage1_run = False
    stage2_run = False

    
    game = Game(window)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if homepage:
            game.home_display()
            if game.menu_open:
                menupage = True
                homepage = False
        
        if menupage:
            game.menu_display()
            if not game.menu_open:
                menupage = False
                homepage = True
            if game.stage1_clicked:
                menupage = False
                stage1_run = True
                game.stage1_clicked = False
            elif game.stage2_clicked:
                menupage = False
                stage2_run = True
                game.stage2_clicked = False
            
        if stage1_run:
            stage = stageRight(window.screen, 1)
            stage.motion()
            menupage = True
            stage1_run = False
            game.click = False
        elif stage2_run:
            stage = stageRight(window.screen, 2)
            stage.motion()
            menupage = True
            stage2_run = False
            game.click = False
            


        pygame.display.update()
        clock.tick(60)
      

                
    pygame.quit()