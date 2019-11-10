import pygame


class WindowPage:
    def __init__(self,color=None):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Rescoding")
        
        self.bg_img = pygame.image.load('mainpage_bg.png')
        self.start = pygame.image.load('start_button.png')
        self.start_hover = pygame.image.load('start_button_hover.png')
        
        self.screen.blit(self.bg_img, (0,0))
        self.screen.blit(self.start, (350, 320))
        
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_hb = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 15, 15)        



if __name__ == '__main__':
    WindowPage()
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()