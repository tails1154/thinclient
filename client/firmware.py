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
        send_power_led("warning off")
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
version = "v1.1.1"


global running





modem = pygame.mixer.Sound("/home/tails1154/client/assets/modem.wav")

def draw_to_screen(x, y, text):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))
def on_loaded():
    browserStarting = False
    send_power_led("warning on")
    select()
    window.evaluate_js("document.addEventListener('keydown',e=>{if(e.key==='F10'){e.preventDefault();let o=document.createElement('div');o.style='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';let d=document.createElement('div');d.style='background:#fff;padding:20px;border-radius:10px;box-shadow:0 0 10px rgba(0,0,0,0.5);display:flex;flex-direction:column;gap:10px;';let i=document.createElement('input');i.type='text';i.placeholder='Enter URL (e.g., https://example.com)';i.style='padding:10px;font-size:16px;width:300px;';let g=document.createElement('button');g.textContent='Go';g.style='padding:10px;font-size:16px;';g.onclick=()=>{let u=i.value.trim();if(!/^https?:\/\//i.test(u))u='https://'+u;window.location.href=u};let c=document.createElement('button');c.textContent='Cancel';c.style='padding:10px;';c.onclick=()=>document.body.removeChild(o);let b=document.createElement('div');b.style='display:flex;justify-content:space-between;gap:10px;';b.appendChild(g);b.appendChild(c);d.appendChild(i);d.appendChild(b);o.appendChild(d);document.body.appendChild(o);i.focus();}});")
    window.evaluate_js("(()=>{let i=0,e=[...document.querySelectorAll('a,button,input,select,textarea,[tabindex]')].filter(el=>el.offsetParent!==null),s=document.createElement('div');s.style='position:absolute;border:2px solid blue;pointer-events:none;z-index:999999;transition:.1s all ease;';document.body.appendChild(s);function move(){if(!e[i])return;let r=e[i].getBoundingClientRect();s.style.top=(r.top+scrollY)+'px';s.style.left=(r.left+scrollX)+'px';s.style.width=r.width+'px';s.style.height=r.height+'px';e[i].scrollIntoView({block:'nearest'});}move();document.addEventListener('keydown',k=>{if(k.key==='ArrowDown')i=(i+1)%e.length,move();else if(k.key==='ArrowUp')i=(i-1+e.length)%e.length,move();else if(k.key==='Enter'){let t=e[i];t.focus();if(typeof t.click==='function')t.click();}});})();")
    window.evaluate_js("document.addEventListener('keydown',e=>{if(e.key==='F1'){e.preventDefault();location.href='http://192.168.0.107/tailsnet/assets/home.html';}});")
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
                os.environ["https_proxy"] = f"http://192.168.0.107:8080/?ssid={ssid}"
               # api = API()
                api = API()
                global window
                window = webview.create_window("TailsNet Proxy", "http://192.168.0.107/tailsnet/assets/splash.html", width=1280, height=720, js_api=api)
                window.events.loaded += on_loaded
                webview.settings = {
                 'ALLOW_DOWNLOADS': True,
                 'ALLOW_FILE_URLS': True,
                 'OPEN_EXTERNAL__LINKS_IN_BROWSER': False,
                 'OPEN_DEVTOOLS_IN_DEBUG': False,
                 'IGNORE_SSL_ERRORS': True
                }
                webview.start(gui='gtk', debug=True, http_server=False)

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
