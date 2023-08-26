import pygame, random
import pygame.gfxdraw

# PYGAME ====================

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

MENU_GAP = 80

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + MENU_GAP))

pygame.display.set_caption('2048')

clock = pygame.time.Clock()

# GAME ====================

BOARD_WIDTH = 4
BOARD_HEIGHT = 4

TILE_WIDTH = int(SCREEN_WIDTH / (BOARD_WIDTH + 0.125))
TILE_HEIGHT = int(SCREEN_HEIGHT / (BOARD_HEIGHT + 0.125))

print(TILE_WIDTH)

TILE_GAP = int(TILE_WIDTH / 8)

TILE_SPEED = int(TILE_WIDTH / 2)

TILE_RAD = int((TILE_WIDTH if TILE_WIDTH <= TILE_HEIGHT else TILE_HEIGHT) / 15)

boardvals = []


class Tile:

   def __init__(self, val, y, x, width=TILE_WIDTH):  # , x, y
       self.val, self.x, self.y = val, x, y

       self.width = width
       self.height = width

       self.endx = x
       self.endy = y

       self.double = None

   def update(self):

       # Movement

       if abs(self.x - self.endx) > TILE_SPEED:
           if self.x > self.endx:
               self.x -= TILE_SPEED
           elif self.x < self.endx:
               self.x += TILE_SPEED
       else:
           self.x = self.endx

       if abs(self.y - self.endy) > TILE_SPEED:
           if self.y > self.endy:
               self.y -= TILE_SPEED
           elif self.y < self.endy:
               self.y += TILE_SPEED
       else:
           self.y = self.endy

       if not self.double is None:
           self.double.draw()
           if self.x == self.endx and self.y == self.endy:
               self.double = None
               self.width = int(TILE_WIDTH / 2)

       # Growth

       if self.width < TILE_WIDTH:
           self.width += 16
       else:
           self.width = TILE_WIDTH

       if self.height < TILE_HEIGHT:
           self.height += 16
       else:
           self.height = TILE_HEIGHT

   def draw(self):

       self.update()

       val = self.val if self.double is None else self.val - 1

       # Background
       if val > 0:
           beveled_rect(self.x + TILE_GAP + (TILE_WIDTH - self.width) / 2,
                        self.y + TILE_GAP + (TILE_WIDTH - self.width) / 2 + MENU_GAP,
                        self.width - TILE_GAP, self.height - TILE_GAP, TILE_RAD, background[val])

       # Number
       if val != 0:
           num = num_font.render(str(2 ** val), True, light if val > 2 else dark)

           screen.blit(num,
                       ((int(self.x + ((TILE_WIDTH + TILE_GAP) - num.get_width()) / 2),
                         int(self.y + ((TILE_HEIGHT + TILE_GAP) - num.get_height()) / 2 + MENU_GAP))))


def create_rand():
   global boardvals

   empty_places = []
   for row in range(BOARD_HEIGHT):
       for col in range(BOARD_WIDTH):
           if boardvals[row][col].val == 0:
               empty_places.append((row, col))

   rand_place = empty_places[random.randint(0, len(empty_places) - 1)]
   boardvals[rand_place[0]][rand_place[1]] = Tile(2 if random.randint(0, 9) == 0 else 1, rand_place[0] * TILE_HEIGHT,
                                                  rand_place[1] * TILE_WIDTH, width=0)


def set_board():
   global boardvals, score

   for row in range(BOARD_HEIGHT):
       boardvals.append([])
       for col in range(BOARD_WIDTH):
           boardvals[row].append(Tile(7, TILE_HEIGHT * row, TILE_WIDTH * col))

   if BOARD_WIDTH * BOARD_HEIGHT >= 2:
       # create_rand()
       # create_rand()
       pass
   else:
       for i in range(BOARD_WIDTH * BOARD_HEIGHT):
           create_rand()

   score = 0


set_board()

clicking = False

game_over = False
score = 0

num_font = pygame.font.SysFont('verdana', int((TILE_WIDTH if TILE_WIDTH <= TILE_HEIGHT else TILE_HEIGHT) / 2.5),
                              bold=True)
score_font = pygame.font.SysFont('verdana', MENU_GAP - 10, bold=True)

keys = [False, False, False, False]
clicking = keys.copy()


# DRAWING ====================

def aafilledcircle(surface, color, pos, radius):
   pygame.draw.circle(surface, color, (pos[0], pos[1]), radius)
   pygame.gfxdraw.aacircle(surface, pos[0], pos[1], radius - 1, color)


def beveled_rect(x, y, width, height, radius, color):
   pygame.draw.rect(screen, color, (x + radius, y + radius, width - 2 * radius, height - 2 * radius))

   pygame.draw.rect(screen, color, (x + radius, y, width - 2 * radius, radius))
   pygame.draw.rect(screen, color, (x + radius, y + height - radius, width - 2 * radius, radius))

   pygame.draw.rect(screen, color, (x, y + radius, radius, height - 2 * radius))
   pygame.draw.rect(screen, color, (x + width - radius, y + radius, radius, height - 2 * radius))

   aafilledcircle(screen, color, (int(x + radius), int(y + radius)), radius)
   aafilledcircle(screen, color, (int(x + radius), int(y + height - radius)), radius)
   aafilledcircle(screen, color, (int(x + width - radius), int(y + radius)), radius)
   aafilledcircle(screen, color, (int(x + width - radius), int(y + height - radius)), radius)


border = (187, 173, 160)
background = [(205, 193, 180), (238, 228, 218), (237, 224, 200), (242, 177, 121), (246, 150, 100), (247, 124, 95),
             (247, 95, 59), (237, 208, 115), (237, 201, 80), (237, 197, 63), (237, 197, 63), (237, 194, 46)]

light = (249, 246, 242)
dark = (119, 110, 101)


# 2, 4, 8, -, -, 64, 128, 256, 512, -, 2048, 4096, 8192, 16384

def move(row1, col1, row2, col2, double=False):
   global score

   if row1 == row2 and col1 == col2:
       return

   endy = TILE_HEIGHT * row2
   endx = TILE_WIDTH * col2

   one = boardvals[row1][col1]

   if double:
       boardvals[row2][col2] = Tile(one.val + 1, one.y, one.x)

       boardvals[row2][col2].endx = endx
       boardvals[row2][col2].endy = endy

       boardvals[row2][col2].double = Tile(one.val, endy, endx)

       score += 2 ** (one.val + 1)
   else:
       boardvals[row2][col2] = Tile(one.val, one.y, one.x)

       boardvals[row2][col2].endx = endx
       boardvals[row2][col2].endy = endy

   boardvals[row1][col1] = Tile(0, TILE_HEIGHT * row1, TILE_WIDTH * col1)


def draw_board():
   for row in boardvals:
       l_row = []
       for tile in row:
           l_row.append(
               'I' if isinstance(tile, int) else (tile.val, int(tile.y / TILE_HEIGHT), int(tile.x / TILE_WIDTH)))
       print(l_row)

   print()


draw_board()

while True:

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()

       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w: keys[0] = True
           if event.key == pygame.K_s: keys[1] = True
           if event.key == pygame.K_a: keys[2] = True
           if event.key == pygame.K_d: keys[3] = True

       if event.type == pygame.KEYUP:
           if event.key == pygame.K_w: keys[0] = False
           if event.key == pygame.K_s: keys[1] = False
           if event.key == pygame.K_a: keys[2] = False
           if event.key == pygame.K_d: keys[3] = False

   moved = False

   if keys[0]:
       if not clicking[0]:

           for row in range(BOARD_HEIGHT):
               for col in range(BOARD_WIDTH):
                   val = boardvals[row][col].val

                   if val != 0:
                       first_empty = row
                       for frow in range(row - 1, -1, -1):
                           fval = boardvals[frow][col].val

                           if fval == 0:
                               first_empty = frow
                               if first_empty == 0:
                                   move(row, col, first_empty, col)
                           elif fval == val:
                               first_empty = frow
                               move(row, col, first_empty, col, True)
                               break
                           else:
                               move(row, col, first_empty, col)
                               break
                       moved = moved or first_empty != row

       clicking[0] = True
   else:
       clicking[0] = False

   if keys[1]:
       if not clicking[1]:
           for row in range(BOARD_HEIGHT - 1, -1, -1):
               for col in range(BOARD_WIDTH):
                   val = boardvals[row][col].val

                   if val != 0:

                       first_empty = row
                       for frow in range(row + 1, BOARD_HEIGHT):
                           fval = boardvals[frow][col].val

                           if fval == 0:
                               first_empty = frow
                               if first_empty == BOARD_HEIGHT - 1:
                                   move(row, col, first_empty, col)
                           elif fval == val:
                               first_empty = frow
                               move(row, col, first_empty, col, True)
                               break
                           else:
                               move(row, col, first_empty, col)
                               break
                       moved = moved or first_empty != col
       clicking[1] = True
   else:
       clicking[1] = False

   if keys[2]:
       if not clicking[2]:
           for col in range(BOARD_WIDTH):
               for row in range(BOARD_HEIGHT):
                   val = boardvals[row][col].val

                   if val != 0:
                       first_empty = col
                       for fcol in range(col - 1, -1, -1):
                           fval = boardvals[row][fcol].val

                           if fval == 0:
                               first_empty = fcol
                               if first_empty == 0:
                                   move(row, col, row, first_empty)
                           elif fval == val:
                               first_empty = fcol
                               move(row, col, row, first_empty, True)
                               break
                           else:
                               move(row, col, row, first_empty)
                               break
                       moved = moved or first_empty != col
       clicking[2] = True
   else:
       clicking[2] = False

   if keys[3]:
       if not clicking[3]:
           for col in range(BOARD_WIDTH - 1, -1, -1):
               for row in range(BOARD_HEIGHT):
                   val = boardvals[row][col].val

                   if val != 0:
                       first_empty = col
                       for fcol in range(col + 1, BOARD_WIDTH):
                           fval = boardvals[row][fcol].val

                           if fval == 0:
                               first_empty = fcol
                               if first_empty == BOARD_WIDTH - 1:
                                   move(row, col, row, first_empty)
                           elif fval == val:
                               first_empty = fcol
                               move(row, col, row, first_empty, True)
                               break
                           else:
                               move(row, col, row, first_empty)
                               break
                       moved = moved or first_empty != col
       clicking[3] = True
   else:
       clicking[3] = False

   if moved and any(keys):
       create_rand()

   # DRAW STUFF DOWN HERE

   screen.fill(border)

   for row in range(BOARD_HEIGHT):
       for col in range(BOARD_WIDTH):
           beveled_rect(TILE_WIDTH * col + TILE_GAP, TILE_HEIGHT * row + TILE_GAP + MENU_GAP,
                        TILE_WIDTH - TILE_GAP, TILE_HEIGHT - TILE_GAP, TILE_RAD, background[0])

   for row in range(BOARD_HEIGHT):
       for col in range(BOARD_WIDTH):
           val = boardvals[row][col].val

           boardvals[row][col].draw()

           # Score
           score_surf = score_font.render(str(score), True, light)
           screen.blit(score_surf, ((int(SCREEN_HEIGHT - score_surf.get_width()) / 2), 10))

   pygame.display.update()

   clock.tick(60)

