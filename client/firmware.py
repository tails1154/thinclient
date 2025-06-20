import pygame
import subprocess
import sys
import requests
import os
import socket
from Xlib import display, X
from Xlib.protocol import request
import threading


global power


global browserStarting

class API:
    def play_splash(self):
        pygame.mixer.music.load('/home/tails1154/client/assets/splash.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(10)
    def update(self):
        update()
    def close(self):
        window.destroy()


def get_window_name(window):
    """Try to get the window's name using _NET_WM_NAME or WM_NAME."""
    name = None
    for atom_name in ('_NET_WM_NAME', 'WM_NAME'):
        atom = window.display.get_atom(atom_name)
        try:
            prop = window.get_full_property(atom, 0)
            if prop and prop.value:
                name = prop.value.decode(errors="ignore")
                break
        except Exception:
            continue
    return name

def find_window_by_name(target_name, window=None):
    """Recursively search for a window with a matching name."""
    if window is None:
        d = display.Display()
        window = d.screen().root
    else:
        d = window.display

    children = window.query_tree().children

    for w in children:
        name = get_window_name(w)
        if name == target_name:
            print(f"Found window: {name} (ID: 0x{w.id:x})")
            return w
        else:
            found = find_window_by_name(target_name, w)
            if found:
                return found
    return None

def select():
    target = "TailsNet Proxy"
    win = find_window_by_name(target)
    if win:
        print(f"Selected window ID: 0x{win.id:x}")
    else:
        print("Window not found.")

global SOCKET_PATH
SOCKET_PATH="/tmp//indicator_socket"

def send_power_led(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client:
       client.sendto(cmd.encode(), SOCKET_PATH)


def startwebview():
   browserStarting = True
   webview.start()


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
global version
version = "v1.0.0-alpha31"


global running





modem = pygame.mixer.Sound("/home/tails1154/client/assets/modem.wav")

def draw_to_screen(x, y, text):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))
def on_loaded():
    browserStarting = False
    send_power_led("warning on")
    select()
    pygame.mixer.music.stop()
running = True

#global browserStarting

subprocess.run(["killall", "-9", "blink.sh"])
send_power_led("power on")



def play_splash():
         pygame.mixer.music.load('/home/tails1154/client/assets/splash.wav')
         pygame.mixer.music.play()
         while pygame.mixer.music.get_busy():
            1+1
def update_firmware():
         cmd = f"curl -fsSL {ip}/tailsnet/update.sh | bash"
         subprocess.run(cmd, shell=True, check=True)
         open("counter.stop", "wt").write("")
         sys.exit(0)
def update():
                screen.fill("green")
                draw_to_screen(500, 500, "Updating")
                pygame.display.flip()
                cmd = f"curl -fsSL {ip}/tailsnet/update.sh | bash"
                subprocess.run(cmd, shell=True, check=True)
                open("counter.stop", "wt").write("")
                sys.exit(0)

#play_splash()
# running = True
# power = True
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
                    send_power_led("power off")
                    send_power_led("warning off")
                if power:
                    send_power_led("power on")
                    modem.play()
            elif event.key == pygame.K_f and power:
                update()
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
                versionserver = requests.get(f"{ip}/tailsnet/client/version.txt").text
                if versionserver != version:
                     update()
                url = requests.get(f"{ip}:3000/api/getuuid?ssid={ssid}").text
                while not connected:
                    try:
                     url = requests.get(f"{ip}:3000{url}?ssid={ssid}").text
                    except requests.exceptions.InvalidURL:
                        connected = True
                        break
                proxy_url = requests.get(f"{ip}:3000/api/proxy?ssid={ssid}").text
                proxy_url = f"http://192.168.0.107:8080/?ssid={ssid}"
##                final_url = f"{proxy_url}?ssid={ssid}"
                os.environ["http_proxy"] = proxy_url
               # api = API()
                api = API()
                global window
                window = webview.create_window("TailsNet Proxy", "http://192.168.0.107/tailsnet/assets/splash.html", width=1280, height=720, js_api=api)
                window.events.loaded += on_loaded
                webview.start(gui='gtk', debug=False, http_server=False)

    #            thread1 = threading.Thread(target=startwebview)
   #             thread1.start()
 #               while browserStarting:
  #                 1+1
                #pygame.mixer.music.stop()

    if power:
#        if not pygame.mixer.music.get_busy():
#           pygame.mixer.music.load("/home/tails1154/client/assets/kartv.wav", namehint="wav")
 #          pygame.mixer.music.play()
        screen.fill("white")
        draw_to_screen(100, 100, "version: " + version)
        draw_to_screen(100, 300, "Press F to update firmware")
        draw_to_screen(100, 400, "Press P to power off")
        draw_to_screen(100, 500, "Press Enter to connect")

    pygame.display.flip()
    clock.tick(60)

# pygame.quit()



#if __name__ == "__main__":
   #  main()


pygame.quit()
