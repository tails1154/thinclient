import os
import socket
import pygame
from Xlib import display

SOCKET_PATH = "/tmp/indicator_socket"
WIDTH, HEIGHT = 200, 50

# Cleanup any existing socket
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

# Setup Pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Indicators")
clock = pygame.time.Clock()

# Indicator states
indicators = {
    "power": False,
    "warning": False,
}

# Move to bottom-left
def move_window():
    d = display.Display()
    root = d.screen().root
    window_id = pygame.display.get_wm_info()['window']
    window = d.create_resource_object('window', window_id)
    height = root.get_geometry().height
    window.configure(x=0, y=height - HEIGHT)
    d.sync()

move_window()

# Socket setup
server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind(SOCKET_PATH)

def handle_command(cmd):
    parts = cmd.strip().split()
    if len(parts) != 2:
        return
    name, state = parts
    if name in indicators and state in {"on", "off"}:
        indicators[name] = (state == "on")

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    # Draw power (green/red)
    power_color = (0, 255, 0) if indicators["power"] else (100, 0, 0)
    pygame.draw.circle(screen, power_color, (30, HEIGHT // 2), 15)

    # Draw warning (yellow/gray)
    warning_color = (255, 255, 0) if indicators["warning"] else (80, 80, 0)
    pygame.draw.circle(screen, warning_color, (90, HEIGHT // 2), 15)

    pygame.display.flip()
    clock.tick(30)

    # Handle socket messages
    try:
        server.settimeout(0.01)
        data = server.recv(1024).decode()
        handle_command(data)
    except socket.timeout:
        pass

    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

server.close()
pygame.quit()
os.remove(SOCKET_PATH)

