import pygame

pygame.init()
pygame.font.get_fonts()

PINK = (254, 223, 225, 127)
MINT = (186, 216, 185, 127)
BLUE = (119, 150, 154)
PURPLE = (143, 119, 181)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("monospace", 20)
SCREEN = pygame.display.set_mode((1000, 600))
SCREEN.fill(pygame.Color('white'))
pygame.display.set_caption("game")

def gamePage():
    pygame.draw.rect(SCREEN, PINK, (600, 0, 395, 200))
    pygame.draw.rect(SCREEN, MINT, (600, 205, 395, 390))
    pygame.draw.rect(SCREEN, BLUE, (620, 20, 150, 40))
    pygame.draw.rect(SCREEN, BLUE, (620, 80, 150, 40))
    pygame.draw.rect(SCREEN, BLUE, (620, 140, 150, 40))
    pygame.draw.rect(SCREEN, PURPLE, (800, 20, 150, 40))

    text_forward = font.render("forward", False, BLACK)
    text_left = font.render("left", False, BLACK)
    text_right = font.render("right", False, BLACK)
    text_if = font.render("if", False, BLACK)
    SCREEN.blit(text_forward, (620+150//4, 20+40//4))
    SCREEN.blit(text_left, (620+150//4, 80+40//4))
    SCREEN.blit(text_right, (620+150//4, 140+40//4))
    SCREEN.blit(text_if, (800+150//4, 20+40//4))
    pygame.display.update()


def main():
    gamePage()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        click = pygame.mouse.get_pressed()[0]

        mx, my = pygame.mouse.get_pos()
        mouse_hb_x = (mx - 5)
        mouse_hb_y = (my - 5)
        mouse_hb = pygame.Rect(mouse_hb_x, mouse_hb_y, 15, 15)
        square_hb = pygame.Rect(320, 220, 60, 60)

        # Start menu
        if run == False:
            """
            SCREEN.fill(PINK)
            pygame.draw.rect(SCREEN, PINK [320, 220, 60, 60])
            #screen.blit(title, [150, 150])
            #screen.blit(start, [325, 240])
            pygame.draw.rect(screen, BLACK, [rect_x_1, rect_y_1, 100, 80])
            pygame.draw.rect(screen, BLACK, [rect_x_2, rect_y_2, 80, 100])
            pygame.draw.rect(screen, BLACK, [rect_x_3, rect_y_3, 60, 120])
            pygame.draw.rect(screen, BLACK, [rect_x_4, rect_y_4, 120, 60])
            if click == 1:
                if mouse_hb.colliderect(square_hb):
                    gamestart = True
            """
        else:
            pygame.draw.rect(SCREEN, MINT, [mx - 30, my - 30, 60, 60])
    pygame.quit()


main()