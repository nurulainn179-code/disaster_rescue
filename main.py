import pygame
import sys
from game_manager import GameManager

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Disaster Rescue - River Crossing")

    SCREEN_W = 800
    SCREEN_H = 600

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock  = pygame.time.Clock()
    manager = GameManager(screen, SCREEN_W, SCREEN_H)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manager.handle_event(event)

        manager.update()
        manager.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
