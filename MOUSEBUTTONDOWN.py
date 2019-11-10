import pygame
import time

pygame.init()
pygame.font.get_fonts()

WHITE = (255, 255, 255)
PINK = (254, 223, 225, 127)
MINT = (186, 216, 185, 127)
BLUE = (119, 150, 154)
PURPLE = (143, 119, 181)
BLACK = (0, 0, 0)
TRANS = (119, 150, 154, 127)

font = pygame.font.SysFont("monospace", 20)
SCREEN = pygame.display.set_mode((1000, 600))
SCREEN.fill(pygame.Color('white'))
pygame.display.set_caption("game")


def gamePage():
    pygame.draw.rect(SCREEN, PINK, (600, 0, 395, 200))
    pygame.draw.rect(SCREEN, MINT, (600, 205, 395, 390))
    f = pygame.draw.rect(SCREEN, BLUE, (620, 20, 150, 40))  # forward
    l = pygame.draw.rect(SCREEN, BLUE, (620, 80, 150, 40))  # left
    r = pygame.draw.rect(SCREEN, BLUE, (620, 140, 150, 40))  # right
    i = pygame.draw.rect(SCREEN, PURPLE, (800, 20, 150, 40))  # if

    text_forward = font.render("forward", False, BLACK)
    text_left = font.render("left", False, BLACK)
    text_right = font.render("right", False, BLACK)
    text_if = font.render("if", False, BLACK)
    SCREEN.blit(text_forward, (620 + 150 // 4, 20 + 40 // 4))
    SCREEN.blit(text_left, (620 + 150 // 4, 80 + 40 // 4))
    SCREEN.blit(text_right, (620 + 150 // 4, 140 + 40 // 4))
    SCREEN.blit(text_if, (800 + 150 // 4, 20 + 40 // 4))
    pygame.display.update()

def handle_button_down(event):

    mx = event.pos[0]
    my = event.pos[1]
    pygame.draw.rect(SCREEN, color, [mx - 30, my - 30, 60, 60])
    text_forward = font.render("forward", False, BLACK)
    text_left = font.render("left", False, BLACK)
    text_right = font.render("right", False, BLACK)
    text_if = font.render("if", False, BLACK)
    pygame.draw.rect(SCREEN, PINK, (600, 0, 395, 200))
    pygame.draw.rect(SCREEN, MINT, (600, 205, 395, 390))
    pygame.draw.rect(SCREEN, BLUE, (620, 20, 150, 40))  # forward
    pygame.draw.rect(SCREEN, BLUE, (620, 80, 150, 40))  # left
    pygame.draw.rect(SCREEN, BLUE, (620, 140, 150, 40))  # right
    pygame.draw.rect(SCREEN, PURPLE, (800, 20, 150, 40))  # if
    SCREEN.blit(text_forward, (620 + 150 // 4, 20 + 40 // 4))
    SCREEN.blit(text_left, (620 + 150 // 4, 80 + 40 // 4))
    SCREEN.blit(text_right, (620 + 150 // 4, 140 + 40 // 4))
    SCREEN.blit(text_if, (800 + 150 // 4, 20 + 40 // 4))




def main():
    gamePage()
    clock = pygame.time.Clock()
    color = TRANS
    cont = True
    run = True
    click_time = 0

    while run:
        for event in pygame.event.poll():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == MOUSEBUTTONDOWN:
                handle_button_down(event)

        '''click = pygame.mouse.get_pressed()[0]
        mx, my = pygame.mouse.get_pos()
        if click == 1 and click_time == 0:
            click_time += 1
            if 620 < mx < 770:
                if 20 < my < 60:
                    color = PINK
                elif 80 < my < 120:
                    color = MINT
                elif 140 < my < 180:
                    color = PURPLE
                
            elif 800 < mx < 950 and 20 < my < 60:
                color = BLUE
        elif click == 1 and click_time == 1:
            click_time += 1
            mx, my = pygame.mouse.get_pos()
            #cont = False
            #break'''


        '''if cont:

            # SCREEN.fill(WHITE)
            mx, my = pygame.mouse.get_pos()
            text_forward = font.render("forward", False, BLACK)
            text_left = font.render("left", False, BLACK)
            text_right = font.render("right", False, BLACK)
            text_if = font.render("if", False, BLACK)
            pygame.draw.rect(SCREEN, PINK, (600, 0, 395, 200))
            pygame.draw.rect(SCREEN, MINT, (600, 205, 395, 390))
            pygame.draw.rect(SCREEN, BLUE, (620, 20, 150, 40))  # forward
            pygame.draw.rect(SCREEN, BLUE, (620, 80, 150, 40))  # left
            pygame.draw.rect(SCREEN, BLUE, (620, 140, 150, 40))  # right
            pygame.draw.rect(SCREEN, PURPLE, (800, 20, 150, 40))  # if
            SCREEN.blit(text_forward, (620 + 150 // 4, 20 + 40 // 4))
            SCREEN.blit(text_left, (620 + 150 // 4, 80 + 40 // 4))
            SCREEN.blit(text_right, (620 + 150 // 4, 140 + 40 // 4))
            SCREEN.blit(text_if, (800 + 150 // 4, 20 + 40 // 4))
            if click_time == 2:
                pygame.draw.rect(SCREEN, color, [mx - 30, my - 30, 60, 60])'''  # pygame.display.update()

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()


main()



