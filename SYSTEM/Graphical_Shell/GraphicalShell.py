import pygame
import sys
import os
import time
import subprocess
from datetime import datetime
from pygame import mixer

pygame.init()
mixer.init()

WIDTH, HEIGHT = 1509, 890
TASKBAR_HEIGHT = 30
DEFAULT_BG = "ShellOS_1.png"

GRAPHICAL_SHELL_DIR = os.path.dirname(os.path.abspath(__file__))
SHELLOS_DIR = os.path.abspath(os.path.join(GRAPHICAL_SHELL_DIR, "..", ".."))
ICON_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "shellos.png")
ICO_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "shellos.ico")
SOUND_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "sounds", "ShlosStartup.mp3")
BACKGROUND_FOLDER = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "backgrounds")
LAUNCHER_ICON_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "launcher.png")
FILEMGR_ICON_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "filemgr.png")
BROWSER_ICON_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "browser.ico")
TERMINAL_ICON_PATH = os.path.join(SHELLOS_DIR, "SYSTEM", "Graphical_Shell", "icons", "terminal.png")

PROGRESS_BAR_WIDTH = 300
PROGRESS_BAR_HEIGHT = 10
PROGRESS_BAR_BORDER = 2

programs = {
    "About Shellos": "System64/Programs/about.py",
    "Calculator": "System64/Programs/calc.py",
    "File Manager": "System64/Programs/filemgr.py",
    "Terminal": "System64/Programs/terminal.py",
    "Notepad": "System64/Programs/notepad.py",
    "ShellOS Browser": "System64/Programs/ShellOS-Browser/browser.py",
    "Tic Tac Toe": "System64/Programs/games/ttt.py",
    "Settings": "System64/Programs/settings.py",
}

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ShellOS")

try:
    pygame.display.set_icon(pygame.image.load(ICON_PATH))
except pygame.error as e:
    print(f"Warning: Could not load window icon: {e}")
    pygame.display.set_icon(pygame.Surface((32, 32), pygame.SRCALPHA))

if sys.platform == "win32":
    try:
        import ctypes
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, ctypes.windll.shell32.ExtractIconW(0, ICO_PATH, 0))
    except (ImportError, AttributeError, FileNotFoundError) as e:
        print(f"Warning: Could not set Windows taskbar icon: {e}")

try:
    logo_img = pygame.image.load(ICON_PATH).convert_alpha()
except pygame.error as e:
    print(f"Error: Could not load logo image for splash screen: {e}")
    logo_img = pygame.Surface((100, 100), pygame.SRCALPHA)

def get_scaled_logo():
    max_width, max_height = WIDTH * 0.8, HEIGHT * 0.6
    if logo_img.get_width() == 0 or logo_img.get_height() == 0:
        return pygame.Surface((1,1), pygame.SRCALPHA)
    ratio = min(max_width / logo_img.get_width(), max_height / logo_img.get_height())
    new_size = (int(logo_img.get_width() * ratio), int(logo_img.get_height() * ratio))
    new_size = (max(1, new_size[0]), max(1, new_size[1]))
    return pygame.transform.smoothscale(logo_img, new_size)

def draw_progress_bar(screen, x, y, width, height, progress, border=2):
    border_rect = pygame.Rect(x - border, y - border, width + border * 2, height + border * 2)
    pygame.draw.rect(screen, (150, 150, 150), border_rect, border_radius=5)

    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=3)

    if progress > 0:
        progress_width = int(width * progress)
        progress_rect = pygame.Rect(x, y, progress_width, height)
        pygame.draw.rect(screen, (255, 255, 255), progress_rect, border_radius=3)

scaled_logo = get_scaled_logo()

start_time = time.time()
clock = pygame.time.Clock()
progress = 0.0
running = True

while running:
    current_time_splash = time.time()
    elapsed = current_time_splash - start_time
    progress = min(elapsed / 10.0, 1.0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            scaled_logo = get_scaled_logo()

    screen.fill((0, 0, 0))

    logo_rect = scaled_logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(scaled_logo, logo_rect)

    bar_x = (WIDTH - PROGRESS_BAR_WIDTH) // 2
    bar_y = HEIGHT - 80
    draw_progress_bar(screen, bar_x, bar_y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT, progress)
    
    pygame.display.flip()
    clock.tick(60)

    if progress >= 1.0 and elapsed >= 10:
        try:
            mixer.music.load(SOUND_PATH)
            mixer.music.play()
            while mixer.music.get_busy():
                pygame.time.delay(100)
        except pygame.error as e:
            print(f"Warning: Could not play startup sound: {e}")
        running = False

bg_error_shown = False
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def load_background():
    global bg_error_shown
    bg_path = os.path.join(BACKGROUND_FOLDER, DEFAULT_BG)
    if os.path.exists(bg_path):
        return pygame.image.load(bg_path).convert()
    else:
        if not bg_error_shown:
            print(f"Error: Background file not found: {bg_path}")
            bg_error_shown = True
        return None

bg_image = load_background()
if bg_image is None:
    bg_image = pygame.Surface((WIDTH, HEIGHT))

launcher_button_rect = pygame.Rect(5, 2, 26, 26)
try:
    launcher_icon = pygame.image.load(LAUNCHER_ICON_PATH).convert_alpha()
    launcher_icon_scaled = pygame.transform.smoothscale(launcher_icon, (launcher_button_rect.width, launcher_button_rect.height))
except pygame.error as e:
    print(f"Warning: Launcher icon not found: {e}")
    launcher_icon_scaled = pygame.Surface((launcher_button_rect.width, launcher_button_rect.height), pygame.SRCALPHA)

filemgr_button_rect = pygame.Rect(35, 2, 26, 26) 
try:
    filemgr_icon = pygame.image.load(FILEMGR_ICON_PATH).convert_alpha()
    filemgr_icon_scaled = pygame.transform.smoothscale(filemgr_icon, (filemgr_button_rect.width, filemgr_button_rect.height))
    filemgr_icon_available = True
except pygame.error:
    print(f"Warning: File manager icon not found at {FILEMGR_ICON_PATH}")
    filemgr_icon_available = False

browser_button_rect = pygame.Rect(65, 2, 26, 26)
try:
    browser_icon = pygame.image.load(BROWSER_ICON_PATH).convert_alpha()
    browser_icon_scaled = pygame.transform.smoothscale(browser_icon, (browser_button_rect.width, browser_button_rect.height))
    browser_icon_available = True
except pygame.error:
    print(f"Warning: ShellOS Browser icon not found at {BROWSER_ICON_PATH}")
    browser_icon_available = False

terminal_button_rect = pygame.Rect(95, 2, 26, 26) 
try:
    terminal_icon = pygame.image.load(TERMINAL_ICON_PATH).convert_alpha()
    terminal_icon_scaled = pygame.transform.smoothscale(terminal_icon, (terminal_button_rect.width, terminal_button_rect.height))
    terminal_icon_available = True
except pygame.error:
    print(f"Warning: Terminal icon not found at {TERMINAL_ICON_PATH}")
    terminal_icon_available = False

TASKBAR_COLOR_RGB = (15, 6, 27)
TASKBAR_ALPHA = 200

START_MENU_COLOR_RGB = (10, 4, 18)
START_MENU_ALPHA = 220

WHITE = (255, 255, 255)

font = pygame.font.SysFont(None, 24)
clock_font = pygame.font.SysFont(None, 24)

menu_visible = False
menu_items = list(programs.keys())
menu_items.sort()
menu_item_height = 28
menu_width = 200
max_visible_items = 10
scroll_offset = 0

special_menu_open = False
special_menu_items = ["Shutdown", "About ShellOS", "Settings Panel"]
special_menu_rects = []

def toggle_menu():
    global menu_visible, scroll_offset
    menu_visible = not menu_visible
    if menu_visible:
        scroll_offset = 0

def launch_program(path):
    full_path = os.path.join(SHELLOS_DIR, path)
    if os.path.exists(full_path):
        try:
            subprocess.Popen([sys.executable, full_path])
        except OSError as e:
            print(f"Error launching program {full_path}: {e}")
    else:
        print(f"Error: Program not found: {full_path}")

def resize_window(new_width, new_height):
    global current_width, current_height, bg_image_scaled, WIDTH, HEIGHT
    current_width, current_height = new_width, new_height
    WIDTH, HEIGHT = new_width, new_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    bg_image_scaled = pygame.transform.scale(bg_image, (new_width, new_height))

def draw_transparent_taskbar(surface, rect, color, alpha):
    taskbar_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    taskbar_surface.fill((*color, alpha))
    surface.blit(taskbar_surface, rect.topleft)

def draw_rounded_transparent_rect(surface, rect, color_rgb, alpha, radius):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (*color_rgb, alpha), (0, 0, rect.width, rect.height), border_radius=radius)
    surface.blit(s, rect.topleft)

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M %b %d, %Y")

running = True
clock = pygame.time.Clock()
current_width, current_height = WIDTH, HEIGHT
bg_image_scaled = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

while running:
    screen.blit(bg_image_scaled, (0, 0))

    taskbar_rect = pygame.Rect(0, 0, current_width, TASKBAR_HEIGHT)
    draw_transparent_taskbar(screen, taskbar_rect, TASKBAR_COLOR_RGB, TASKBAR_ALPHA)
    
    pygame.draw.rect(screen, (0, 0, 0), launcher_button_rect, border_radius=6)
    screen.blit(launcher_icon_scaled, launcher_button_rect.topleft)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    hovering_filemgr = filemgr_button_rect.collidepoint((mouse_x, mouse_y))
    filemgr_bg_color = (40, 40, 40) if hovering_filemgr else (0, 0, 0)
    pygame.draw.rect(screen, filemgr_bg_color, filemgr_button_rect, border_radius=6)
    if filemgr_icon_available:
        screen.blit(filemgr_icon_scaled, filemgr_button_rect.topleft)
    else:
        pygame.draw.rect(screen, (100, 100, 100), 
                         (filemgr_button_rect.x + 4, filemgr_button_rect.y + 6, 18, 14), 
                         border_radius=2)
        pygame.draw.rect(screen, (80, 80, 80), 
                         (filemgr_button_rect.x + 6, filemgr_button_rect.y + 4, 6, 4), 
                         border_radius=1)

    hovering_browser = browser_button_rect.collidepoint((mouse_x, mouse_y))
    browser_bg_color = (40, 40, 40) if hovering_browser else (0, 0, 0)
    pygame.draw.rect(screen, browser_bg_color, browser_button_rect, border_radius=6)
    if browser_icon_available:
        screen.blit(browser_icon_scaled, browser_button_rect.topleft)
    else:
        pygame.draw.circle(screen, (0, 150, 255), browser_button_rect.center, 10, 2)
        pygame.draw.circle(screen, (255, 165, 0), browser_button_rect.center, 4)

    hovering_terminal = terminal_button_rect.collidepoint((mouse_x, mouse_y))
    terminal_bg_color = (40, 40, 40) if hovering_terminal else (0, 0, 0)
    pygame.draw.rect(screen, terminal_bg_color, terminal_button_rect, border_radius=6)
    if terminal_icon_available:
        screen.blit(terminal_icon_scaled, terminal_button_rect.topleft)
    else:
        pygame.draw.rect(screen, (30, 30, 30), 
                         (terminal_button_rect.x + 2, terminal_button_rect.y + 2, 22, 22), 
                         border_radius=2)
        pygame.draw.rect(screen, (0, 200, 0), 
                         (terminal_button_rect.x + 4, terminal_button_rect.y + 4, 18, 2))
        pygame.draw.rect(screen, (0, 200, 0), 
                         (terminal_button_rect.x + 4, terminal_button_rect.y + 8, 10, 2))
        pygame.draw.rect(screen, (0, 200, 0), 
                         (terminal_button_rect.x + 4, terminal_button_rect.y + 12, 14, 2))

    time_str = get_current_time()
    clock_text = clock_font.render(time_str, True, WHITE)
    clock_label_x = current_width - clock_text.get_width() - 10
    screen.blit(clock_text, (clock_label_x, (TASKBAR_HEIGHT - clock_text.get_height()) // 2))

    dots_menu_width = 20
    dots_menu_height = 20
    dots_menu_margin_right = 10
    dots_menu_rect = pygame.Rect(clock_label_x - dots_menu_width - dots_menu_margin_right, 5, dots_menu_width, dots_menu_height)

    hovering_dots = dots_menu_rect.collidepoint((mouse_x, mouse_y))
    dots_menu_color = (55, 55, 55) if hovering_dots else (45, 45, 45)
    pygame.draw.rect(screen, dots_menu_color, dots_menu_rect, border_radius=5)

    pygame.draw.circle(screen, WHITE, (dots_menu_rect.centerx, dots_menu_rect.centery - 4), 2)
    pygame.draw.circle(screen, WHITE, (dots_menu_rect.centerx, dots_menu_rect.centery), 2)
    pygame.draw.circle(screen, WHITE, (dots_menu_rect.centerx, dots_menu_rect.centery + 4), 2)

    if special_menu_open:
        special_menu_rects = []
        for i, label in enumerate(special_menu_items):
            rect = pygame.Rect(dots_menu_rect.x, dots_menu_rect.bottom + i * 25, 160, 25)
            special_menu_rects.append((rect, label))
            draw_rounded_transparent_rect(screen, rect, START_MENU_COLOR_RGB, START_MENU_ALPHA, 6)
            text = font.render(label, True, WHITE)
            screen.blit(text, (rect.x + 5, rect.y + 4))

    menu_rects = []
    hovered_index = None
    if menu_visible:
        visible_items = menu_items[scroll_offset:scroll_offset + max_visible_items]
        for i, item in enumerate(visible_items):
            item_rect = pygame.Rect(5, TASKBAR_HEIGHT + i * menu_item_height, menu_width, menu_item_height)
            menu_rects.append((item_rect, scroll_offset + i))
            draw_rounded_transparent_rect(screen, item_rect, START_MENU_COLOR_RGB, START_MENU_ALPHA, 0)
            item_text = font.render(item, True, WHITE)
            screen.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

        for rect, index in menu_rects:
            if rect.collidepoint((mouse_x, mouse_y)):
                hovered_index = index
                hover_color_rgb = (100, 40, 140)
                hover_alpha = 100
                draw_rounded_transparent_rect(screen, rect, hover_color_rgb, hover_alpha, 0)
                pygame.draw.rect(screen, hover_color_rgb, rect, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            resize_window(event.w, event.h)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if launcher_button_rect.collidepoint(event.pos):
                    toggle_menu()
                    special_menu_open = False
                elif filemgr_button_rect.collidepoint(event.pos):
                    launch_program("System64/Programs/filemgr.py")
                    menu_visible = False
                    special_menu_open = False
                elif browser_button_rect.collidepoint(event.pos):
                    launch_program("System64/Programs/ShellOS-Browser/browser.py")
                    menu_visible = False
                    special_menu_open = False
                elif terminal_button_rect.collidepoint(event.pos):
                    launch_program("System64/Programs/terminal.py")
                    menu_visible = False
                    special_menu_open = False
                elif dots_menu_rect.collidepoint(event.pos):
                    special_menu_open = not special_menu_open
                    menu_visible = False
                elif special_menu_open:
                    for rect, label in special_menu_rects:
                        if rect.collidepoint(event.pos):
                            if label == "Shutdown":
                                running = False
                            elif label == "About ShellOS":
                                launch_program("System64/Programs/about.py")
                            elif label == "Settings Panel":
                                launch_program("System64/Programs/settings.py")
                            special_menu_open = False
                            break
                elif menu_visible:
                    for rect, index in menu_rects:
                        if rect.collidepoint(event.pos):
                            launch_program(programs[menu_items[index]])
                            menu_visible = False
                            break
                else:
                    menu_visible = False
                    special_menu_open = False
        elif event.type == pygame.MOUSEWHEEL:
            if menu_visible:
                scroll_offset = max(0, min(scroll_offset - event.y, len(menu_items) - max_visible_items))
        elif event.type == pygame.KEYDOWN:
            if menu_visible:
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 1, len(menu_items) - max_visible_items)
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - 1, 0)
                elif event.key == pygame.K_ESCAPE:
                    menu_visible = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()