from random import randint
import pygame
import win32api
import win32con
import win32gui
from math import sin, cos, radians
import json
import os
os.system('cls')

with open('C:/Users/Hamolicious/Documents/Programing_Projects/Python/WIP/RotaryWheelFolder/settings.json', 'r') as file:
    settings = json.loads(file.read())

# region pygame init
pygame.init()
pygame.font.init()
size = width, height = (settings['window_width'], settings['window_height'])
screen = pygame.display.set_mode(size, pygame.NOFRAME)
done = False
transparency_colour = (255, 0, 128)  # Transparency color

font = pygame.font.SysFont('ariel', settings['text_size'])

# Set window transparency color
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(
    *transparency_colour), 0, win32con.LWA_COLORKEY)
# endregion

def find_icon(name):
    name = name.replace('.py', '.png')

    if name in available_icons:
        return os.path.join(icons_path, name)
    else:
        return os.path.join(icons_path, 'default.png')


def angle_to_xy(angle, dist=-1):
    if dist == -1:
        dist = min(width, height) - 300

    x = (cos(radians(angle)) * dist) + width/2
    y = (sin(radians(angle)) * dist) + height/2

    return (x, y)


class Tile():
    def __init__(self, x, y, path, icon, min_angle, max_angle):
        self.pos = (int(x), int(y))
        self.path = path
        self.icon = icon
        self.min_angle = min_angle
        self.max_angle = max_angle

        self.selected = False

    def display(self):
        if self.selected:
            icon = pygame.transform.scale(self.icon, (40, 40))
        else:
            icon = self.icon

        screen.blit(icon, self.pos)
        self.selected = False

# region load tools and icons
tools_path = settings['tools_folder_path']
available_tools = os.listdir(tools_path)
for ignore in settings['tools_to_ignore']:
    if ignore in available_tools:
        available_tools.remove(ignore)

icons_path = settings['icons_folder_path']
available_icons = os.listdir(icons_path)

colours = [[randint(0, 150), randint(0, 150), randint(0, 150)]
           for i in range(len(available_tools))]
# endregion

# region place all tools
num_of_tools = len(available_tools)
d_angle = 360 / num_of_tools

tiles = []
for i in range(num_of_tools):
    icon = pygame.image.load(find_icon(available_tools[i]))

    x, y = angle_to_xy(d_angle * i, dist=min(width, height) - 350)
    x -= icon.get_width() / 2
    y -= icon.get_height() / 2

    tiles.append(Tile(x, y, available_tools[i], icon, radians(d_angle * (i-0.5)), radians(d_angle * (i+0.5))))

# endregion

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(transparency_colour)  # Transparent background

    # draw rotations
    for i in range(num_of_tools):
        x, y = angle_to_xy(d_angle * (i-0.5))

        polygon = [
            (width/2, height/2),
            (x, y),
            angle_to_xy(d_angle * (i+0.5))
        ]

        pygame.draw.polygon(screen, colours[i], polygon)

    for tile in tiles:
        tile.display()

    x, y = pygame.mouse.get_pos()
    r, g, b, _ = screen.get_at((x, y))
    if [r, g, b] in colours:
        index = colours.index([r, g, b])
        tiles[index].selected = True

        screen.blit(font.render(tiles[index].path.split('.')[0], True, [255, 255, 255], [0, 0, 0]), (10, 10))

        if pygame.mouse.get_pressed()[0] == 1:
            os.startfile(os.path.join(tools_path, tiles[index].path))
            done = True
    
    if pygame.mouse.get_pressed()[2] == 1:
        done = True

    pygame.display.update()
