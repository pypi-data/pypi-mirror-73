import pygame
import sys

def main():
    
    pygame.init()

    screen = pygame.display.set_mode([600,600])
    pygame.display.set_caption("Star")
    test_list = pygame.Color(0,255,255,50)
    test_list2 = test_list.cmy

    print(test_list2)

    while True: #While program running
        for evt in pygame.event.get(): #For event in events basically
            if evt.type == pygame.QUIT: #If the window says quit
                pygame.quit()
                sys.exit()
        screen.fill(test_list2)
        surface = pygame.Surface((200,200), pygame.SRCALPHA)
        pygame.draw.circle(surface, [0,0,255,50], (100,100), 50)
        pygame.draw.polygon(screen, [0,100,0, 50], [[100,100],[100,50],
                                            [150,100], [200,100], [150,175],
                                            [150,200], [125,175],
                                            [50,100], [25,40]])
        screen.blit(surface, (0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
