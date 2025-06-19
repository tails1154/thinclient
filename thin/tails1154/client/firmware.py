import pygame
import subprocess
import sys
import requests


# pygame setup
pygame.init()
global screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
global font
global ip
ip = "http://192.168.0.107"
font = pygame.font.SysFont('Arial', 48)
text_surface = font.render('Hello, Pygame!', True, (255, 255, 255))  # White text
# screen.blit(text_surface, (100, 100))  # Position at (100, 100)
pygame.display.flip()
def draw_to_screen(x, y, text):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#           running = False

    for event in pygame.event.get():
     if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_f:
       screen.fill("green")
       draw_to_screen(500, 500, "Updating")
       pygame.display.flip()
       cmd = f"curl -fsSL {ip}/tailsnet/update.sh | bash"
       subprocess.run(cmd, shell=True, check=True)
       open("counter.stop", "wt").write()
       sys.exit(0)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")


    #draw_to_screen(100, 100, "Getting ready...")
    #pygame.display.flip()


    #try:
    #    cmd = f'curl -fsSL {ip}/tailsnet/update.sh | bash'
    #    subprocess.run(cmd, shell=True, check=True)
    #    print("Update script was ran successfully!")
    #    screen.fill("black")
    #    draw_to_screen(100, 100, "Restarting")
    #    running = False
    #except subprocess.CalledProcessError:
    #    print("Download and execute update script failed!")
    #    screen.fill("red")
    #    draw_to_screen(100, 100, "Update Failed!")
    #    draw_to_screen(100, 200, "Try again Later")
   #3     pygame.display.flip()
   #     pygame.time.wait(10000)
   #     sys.exit(1)
#
    draw_to_screen(100, 100, "Cool Beans!")
    draw_to_screen(100, 300, "Press F to update firmware")
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
