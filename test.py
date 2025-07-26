import pygame

pygame.init()

def create_window(resizable=True):
    flags = pygame.RESIZABLE if resizable else 0
    return pygame.display.set_mode((400, 400), flags)

# Initially resizable
resizable = True
screen = create_window(resizable)

pygame.display.set_caption('Toggle Resizable')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle resizable on SPACE key
                resizable = not resizable
                screen = create_window(resizable)
                print("Resizable:", resizable)

    screen.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()
