import pygame


class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

        image = pygame.image.load("player.png")

        while 1:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    return

            screen.fill((200, 200, 200))
            screen.blit(image, (screen.get_width()/2, screen.get_height()/2))
            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
