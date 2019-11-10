import pygame
import time
from Stagebutton import Stagebutton


class WindowPage:
    def __init__(self,color=None):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Rescoding")


class Game:
    
    def __init__(self, window):
        
        self.clock = pygame.time.Clock()
        self.menu_open = False
        if self.menu_open == False:
            self.home_display()   # display home page
        else:
            self.menu_display()
  
        # Mouse: get position, define click, create nouse hitbox
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)
        
        # Start button
        if self.mouse_hb.colliderect(self.start_hb):   # check if mouseover
            self.start_hover = pygame.image.load('image/start_button_hover.png')
            window.screen.blit(self.start_hover, (350, 320)) 
            if self.click == 1:   # if user clicks on button, go to menu
                self.menu_open = True
                print("menu")
                

        
    def home_display(self):
        
        # background image display
        bg_img = pygame.image.load('image/mainpage_bg.png')
        window.screen.blit(bg_img, (0,0))
        
        # start button display
        start = pygame.image.load('image/start_button.png')
        self.start_hb = pygame.Rect(350, 320, 265, 110)
        window.screen.blit(start, (350, 320))
        
        # Mouse: get position, define click, create nouse hitbox
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)
        
        # Start button
        if self.mouse_hb.colliderect(self.start_hb):   # check if mouseover
            self.start_hover = pygame.image.load('image/start_button_hover.png')
            window.screen.blit(self.start_hover, (350, 320)) 
            if self.click == 1:   # if user clicks on button, go to menu
                self.menu_open = True
                print("menu")
                
        # Display menu        
        
    def menu_display(self):
        
        # background image display
        bg_img = pygame.image.load('image/menu_bg.png')
        window.screen.blit(bg_img, (0,0))
        
        # stage buttons display
        stage1 = Stagebutton(window, 1, (60,75))
        stage2 = Stagebutton(window, 2, (90,300))
        stage3 = Stagebutton(window, 3, (250,510))
        stage4 = Stagebutton(window, 4, (380,320))
        stage5 = Stagebutton(window, 5, (635,350))
        stage6 = Stagebutton(window, 6, (780,490))

        
        



if __name__ == '__main__':
    window = WindowPage()
    running = True
    homepage = True
    menupage = False
    
    game = Game(window)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        if homepage:
            game.home_display()
            if game.menu_open:
                menupage = True
                homepage = False
        
        if menupage:
            game.menu_display()
        
        pygame.display.update()
        game.clock.tick(60)        
      
        
         

                
    pygame.quit()