import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

WALL_OFFSET = 40
FLOOR_OFFSET = 50

FONT_SIZE = 30
TEXT_POS = (WINDOW_WIDTH - 400, 60)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (127, 72, 112)
BLUE = (46, 69, 83)

RECT_SMALL_SIZE = 60

BIG_START_POS = 390
SMALL_START_POS = 300

TIME_STEP = 10000
FPS = 100

def sign(X):
    if X >= 0:
        return 1
    return -1

class Object:
    def __init__(self, mass, velocity, surface, pos, acceleration):
        self.mass = mass
        self.velocity = velocity
        self.surface = surface
        self.pos = pos
        self.acceleration = acceleration


def draw_floor_wall():
    pygame.Surface.fill(screen, WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, WALL_OFFSET, WINDOW_HEIGHT))
    pygame.draw.rect(screen, BLACK, (0, WINDOW_HEIGHT - FLOOR_OFFSET, WINDOW_WIDTH, WINDOW_HEIGHT))


def calculate_new_velocities(rect1, rect2):
    old_vel1, old_vel2 = rect1.velocity, rect2.velocity
    rect1.velocity = (rect1.mass - rect2.mass) / (rect1.mass + rect2.mass) * old_vel1 + (
            2 * rect2.mass) / (
                             rect1.mass + rect2.mass) * rect2.velocity
    rect2.velocity = (2 * rect1.mass) / (rect1.mass + rect2.mass) * old_vel1 + (
            rect2.mass - rect1.mass) / (
                             rect1.mass + rect2.mass) * old_vel2
    if sign(rect1.velocity) != sign(old_vel1):
        rect1.acceleration *= -1
    if sign(rect2.velocity) != sign(old_vel2):
        rect2.acceleration *= -1

def calculate_visualisation():
    screen.blit(big_rect.surface, (big_rect.pos, WINDOW_HEIGHT - FLOOR_OFFSET - RECT_BIG_SIZE))
    screen.blit(textfont.render("10^" + str(n) + "kg", True, BLACK), (
    big_rect.pos + RECT_BIG_SIZE / 2 - 55, WINDOW_HEIGHT - FLOOR_OFFSET - RECT_BIG_SIZE + RECT_BIG_SIZE / 2 - 10))
    screen.blit(small_rect.surface, (small_rect.pos, WINDOW_HEIGHT - FLOOR_OFFSET - RECT_SMALL_SIZE))
    screen.blit(textfont.render("1kg", True, BLACK),
                (small_rect.pos + 3, WINDOW_HEIGHT - FLOOR_OFFSET - RECT_SMALL_SIZE + 15))
    textTBD = textfont.render("Collisions: " + str(collisions), True, RED)
    screen.blit(textTBD, TEXT_POS)
    pygame.display.flip()

n = int(input("Введите степень отношения масс: "))
nu = float(input("Введите коэффициент трения: "))
big_start_vel = -1 * int(input("Введите начальную скорость большого куба: "))

big_m = 10**n

RECT_BIG_SIZE = RECT_SMALL_SIZE*(n+1)

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
textfont = pygame.font.SysFont("monospace", FONT_SIZE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SWSURFACE)
pygame.display.set_caption("Collisions")
screen.fill(WHITE)

surf_small = pygame.Surface((RECT_SMALL_SIZE, RECT_SMALL_SIZE))
surf_small.fill(RED)

surf_big = pygame.Surface((RECT_BIG_SIZE, RECT_BIG_SIZE))
surf_big.fill(BLUE)

collisions = 0

big_rect = Object(big_m, big_start_vel, surf_big, BIG_START_POS, nu * big_m * 9.8)
small_rect = Object(1, 0, surf_small, SMALL_START_POS, -nu * 9.8)

draw_floor_wall()

while True:

    dt = (clock.tick(FPS) / 1000) / TIME_STEP
    for i in range(TIME_STEP):
        if abs(big_rect.velocity + big_rect.acceleration * dt) > abs(big_rect.velocity):
            big_rect.velocity = 0
        else:
            big_rect.velocity += big_rect.acceleration * dt
        if abs(small_rect.velocity + small_rect.acceleration * dt) > abs(small_rect.velocity):
            small_rect.velocity = 0
        else:
            small_rect.velocity += small_rect.acceleration * dt
        big_rect.pos += big_rect.velocity * dt
        small_rect.pos += small_rect.velocity * dt
        if big_rect.pos <= small_rect.pos + RECT_SMALL_SIZE:
            if (small_rect.velocity != 0):
                collisions += 1
            calculate_new_velocities(big_rect, small_rect)
        elif small_rect.pos <= WALL_OFFSET and small_rect.velocity < 0:
            small_rect.velocity *= -1
            small_rect.acceleration *= -1
            if (small_rect.velocity != 0):
                collisions += 1

    draw_floor_wall()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    calculate_visualisation()