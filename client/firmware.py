import pygame
import subprocess
import sys
import requests
import os

import webview
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
power = True
ip = "http://192.168.0.107"
font = pygame.font.SysFont('Arial', 48)
ssid = open("/home/tails1154/ssid.txt", "rt").read()

global modem
pygame.mixer.init()


modem = pygame.mixer.Sound("/home/tails1154/client/assets/modem.wav")

def draw_to_screen(x, y, text):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                power = not power  # Toggle power
                if not power:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    print("Powered Off")
                    screen.fill("black")
                    pygame.display.flip()
                if power:
                    modem.play()
            elif event.key == pygame.K_f and power:
                screen.fill("green")
                draw_to_screen(500, 500, "Updating")
                pygame.display.flip()
                cmd = f"curl -fsSL {ip}/tailsnet/update.sh | bash"
                subprocess.run(cmd, shell=True, check=True)
                open("counter.stop", "wt").write("")
                sys.exit(0)
            elif event.key == pygame.K_RETURN and power:
                screen.fill("grey")
                modem.play()
                draw_to_screen(500, 500, "Connecting")
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load("/home/tails1154/client/assets/dialing.wav", namehint="wav")
                pygame.mixer.music.play()
                pygame.display.flip()
                connected = False
                print("[firmware.py] requests.get")
                url = requests.get(f"{ip}:3000/api/getuuid?ssid={ssid}").text
                while not connected:
                    try:
                     url = requests.get(f"{ip}:3000{url}?ssid={ssid}").text
                    except requests.exceptions.InvalidURL:
                        connected = True
                        break
                proxy_url = requests.get(f"{ip}:3000/api/proxy?ssid={ssid}").text
                proxy_url = "http://192.168.0.107:8080/"
##                final_url = f"{proxy_url}?ssid={ssid}"
                os.environ["http_proxy"] = proxy_url
                webview.create_window("TailsNet Proxy", "http://example.com", width=1280, height=720)
                webview.start()
                pygame.mixer.music.stop()

    if power:
        if not pygame.mixer.music.get_busy():
           pygame.mixer.music.load("/home/tails1154/client/assets/kartv.wav", namehint="wav")
           pygame.mixer.music.play()
        screen.fill("white")
        draw_to_screen(100, 100, "Cool Beans!")
        draw_to_screen(100, 300, "Press F to update firmware")
        draw_to_screen(100, 400, "Press P to power off")
        draw_to_screen(100, 500, "Press Enter to connect")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
