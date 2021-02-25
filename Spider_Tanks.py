import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("Spider_Tanks")

image_loader = pygame.image.load
walkRight = [image_loader('Player_1.0R.png'), image_loader('Player_1.1R.png'), image_loader('Player_1.2R.png'),
             image_loader('Player_1.3R.png')]
walkLeft = [image_loader('Player_1.0L.png'), image_loader('Player_1.1L.png'), image_loader('Player_1.2L.png'),
            image_loader('Player_1.3L.png')]
bg = pygame.image.load('BG.png')
fps = 20
clock = pygame.time.Clock()


class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, walkLeft, walkRight):
        self.x = x
        self.y = y
        self.start_pos = (x, y)
        self.width = width
        self.height = height
        self.vel = 9
        self.isCollide = False
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.y_vel = 0
        self.walkLeft = walkLeft
        self.walkRight = walkRight
        self.hitbox = (self.x, self.y, 48, 35)
        self.health = 3
        self.wins = 0
        self.image = walkLeft[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, win, level):
        if self.isJump:
            self.y_vel -= 1
        if self.y <= 20:
            self.y_vel = -4
        for i in level.platform_list:
            if i.colliderect(self.rect.x, self.rect.y - self.y_vel, self.width, self.height):
                self.isCollide = True
                break
            else:
                self.isCollide = False
            if i.colliderect(self.rect.x - self.vel, self.rect.y, self.width, self.height):
                self.x += 10
            if i.colliderect(self.rect.x + self.vel, self.rect.y, self.width, self.height):
                self.x -= 10
        if self.isCollide:
            if self.y_vel < 0:
                self.y_vel = 0
                self.isJump = False
            if self.y_vel > 0:
                self.y_vel = -4
        else:
            self.isJump = True
        self.y -= self.y_vel
        if self.walkCount >= fps and not self.isJump:
            self.walkCount = 0
        if self.left and not self.isJump:
            self.image = self.walkLeft[self.walkCount // (fps // len(walkLeft))]
            self.walkCount += 1
        elif self.right and not self.isJump:
            self.image = self.walkRight[self.walkCount // (fps // len(walkRight))]
            self.walkCount += 1
        else:
            if self.right:
                self.image = self.walkRight[0]
            else:
                self.image = self.walkLeft[0]
        win.blit(self.image, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitbox = (self.x, self.y, 48, 35)
        if self.y >= 440 + self.y_vel:
            self.isJump = False
            self.y_vel = 0

    def hit(self):
        self.health -= 1

    def to_start(self):
        self.health = 3
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]


class Level():
    def __init__(self, coords):
        self.coords = coords
        self.platform_list = []
        self.image = image_loader('Platform.png')
        for i in self.coords:
            rect = self.image.get_rect()
            rect.x = i[0]
            rect.y = i[1]
            self.platform_list.append(rect)

    def draw(self, win):
        for i in self.platform_list:
            win.blit(self.image, (i.x, i.y))


class Bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow(level):
    win.blit(bg, (0, 0))
    player_2.draw(win, level)
    player_1.draw(win, level)
    health_bar_1 = font.render(f'Player 1: {player_1.health}', 1, 'yellow')
    health_bar_2 = font.render(f'Player 2: {player_2.health}', 1, 'blue')
    rounds_1 = font.render(str(player_1.wins), 1, 'yellow')
    rounds_2 = font.render(str(player_2.wins), 1, 'blue')
    dots = font.render(':', 1, 'black')
    number_1 = font.render('1', 1, 'yellow')
    number_2 = font.render('2', 1, 'blue')
    win.blit(health_bar_1, (10, 10))
    win.blit(health_bar_2, (370, 10))
    win.blit(rounds_1, (220, 10))
    win.blit(dots, (240, 10))
    win.blit(rounds_2, (260, 10))
    win.blit(number_1, (player_1.x + 19, player_1.y - 17))
    win.blit(number_2, (player_2.x + 19, player_2.y - 17))
    level.draw(win)
    for bullet in bullets_2:
        bullet.draw(win)
    for bullet in bullets_1:
        bullet.draw(win)
    pygame.display.update()


def change_level():
    global current_level
    global levels
    global level_count
    if level_count < 1:
        level_count += 1
        current_level = levels[level_count]
    else:
        current_level = levels[0]
        level_count = 0
    player_2.to_start()
    player_1.to_start()


level_count = 0
font = pygame.font.SysFont('comicsans', 30, True, True)
run = True
player_2 = player(429, 440, 48, 35, walkLeft, walkRight)
player_1 = player(21, 440, 48, 35, walkLeft, walkRight)
Level_1 = Level(([50, 250], [200, 400], [350, 250], [200, 100]))
Level_2 = Level(([70, 400], [200, 250], [330, 400], [70, 100], [330, 100]))
levels = [Level_1, Level_2]
current_level = Level_1
shootLoop_1 = 0
shootLoop_2 = 0
bullets_2 = []
bullets_1 = []
player_1.right = True
player_2.left = True
redrawGameWindow(current_level)
while run:
    clock.tick(fps)
    if shootLoop_1 > 0:
        shootLoop_1 += 1
    if shootLoop_1 > 10:
        shootLoop_1 = 0
    if shootLoop_2 > 0:
        shootLoop_2 += 1
    if shootLoop_2 > 10:
        shootLoop_2 = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets_2:
        if bullet.y - bullet.radius < player_1.hitbox[1] + player_1.hitbox[3] \
                and bullet.y + bullet.radius > player_1.hitbox[1]:
            if bullet.x + bullet.radius > player_1.hitbox[0] \
                    and bullet.x - bullet.radius < player_1.hitbox[0] + player_1.hitbox[2]:
                player_1.hit()
                bullets_2.pop(bullets_2.index(bullet))
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets_2.pop(bullets_2.index(bullet))

    for bullet in bullets_1:
        if bullet.y - bullet.radius < player_2.hitbox[1] + player_2.hitbox[3] \
                and bullet.y + bullet.radius > player_2.hitbox[1]:
            if bullet.x + bullet.radius > player_2.hitbox[0] \
                    and bullet.x - bullet.radius < player_2.hitbox[0] + player_2.hitbox[2]:
                player_2.hit()
                bullets_1.pop(bullets_1.index(bullet))
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets_1.pop(bullets_1.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and shootLoop_1 == 0:
        if player_2.left:
            facing = -1
        else:
            facing = 1
        if len(bullets_2) < 5:
            bullets_2.append(
                Bullet(round(player_2.x + (player_2.width // 2 + 7) * facing + 24),
                       round(player_2.y + player_2.height // 2 - 5)
                       , 6, (50, 50, 50), facing))
        shootLoop_1 = 1
    if keys[pygame.K_LEFT] and player_2.x > player_2.vel:
        player_2.x -= player_2.vel
        player_2.left = True
        player_2.right = False
    elif keys[pygame.K_RIGHT] and player_2.x < 500 - player_2.width - player_2.vel:
        player_2.x += player_2.vel
        player_2.right = True
        player_2.left = False
    else:
        player_2.walkCount = 0

    if not player_2.isJump:
        if keys[pygame.K_UP]:
            player_2.isJump = True
            player_2.walkCount = 0
            player_2.y_vel = 20

    if keys[pygame.K_s] and shootLoop_2 == 0:
        if player_1.left:
            facing_2 = -1
        else:
            facing_2 = 1
        if len(bullets_1) < 5:
            bullets_1.append(
                Bullet(round(player_1.x + (player_1.width // 2 + 7) * facing_2 + 24),
                       round(player_1.y + player_1.height // 2 - 5)
                       , 6, (50, 50, 50), facing_2))
        shootLoop_2 = 1
    if keys[pygame.K_a] and player_1.x > player_1.vel:
        player_1.x -= player_1.vel
        player_1.left = True
        player_1.right = False
    elif keys[pygame.K_d] and player_1.x < 500 - player_1.width - player_1.vel:
        player_1.x += player_1.vel
        player_1.right = True
        player_1.left = False
    else:
        player_1.walkCount = 0

    if not player_1.isJump:
        if keys[pygame.K_w]:
            player_1.isJump = True
            player_1.walkCount = 0
            player_1.y_vel = 20
    if player_1.health <= 0:
        player_2.wins += 1
        change_level()
    elif player_2.health <= 0:
        player_1.wins += 1
        change_level()
    redrawGameWindow(current_level)

pygame.quit()
