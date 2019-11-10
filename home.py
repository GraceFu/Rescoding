import pygame
import time


class WindowPage:
    def __init__(self,color=None):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Rescoding")


class Game:
    
    def __init__(self,window):
        
        self.home_display()   # display home page
        self.clock = pygame.time.Clock()

        # Mouse: get position, define click, create nouse hitbox
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)
        
        # Start button
        if self.mouse_hb.colliderect(self.start_hb):   # check if mouseover
            self.start_hover = pygame.image.load('start_button_hover.png')
            window.screen.blit(self.start_hover, (350, 320)) 
            if self.click == 1:   # if user clicks on button, go to manu
                print("Menu")
        
    def home_display(self):
        
        # background image display
        self.bg_img = pygame.image.load('mainpage_bg.png')
        window.screen.blit(self.bg_img, (0,0))
        
        # start button display
        self.start = pygame.image.load('start_button.png')
        self.start_hb = pygame.Rect(350, 320, 265, 110)
        window.screen.blit(self.start, (350, 320))
        

        



if __name__ == '__main__':
    window = WindowPage()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game = Game(window)
        pygame.display.update()
        game.clock.tick(60) 

                
    pygame.quit()