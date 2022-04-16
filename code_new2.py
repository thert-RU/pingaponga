from random import shuffle, randint
import pygame
import time
pygame.font.init()
font1 = pygame.font.SysFont('Arial', 80)
min_speed = 1

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, player_num):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.num = player_num
            
    def update(self):
        keys = pygame.key.get_pressed()
        if self.num == 1:
            if keys[pygame.K_w] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.y < 395:
                self.rect.y += self.speed
        elif self.num == 2:
            if keys[pygame.K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y < 395:
                self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, speedx, speedy):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speedx = speedx
        self.speedy = speedy
    def otskok_x(self):
        global min_speed
        a = self.speedx
        if self.speedx > min_speed or self.speedx < -min_speed:
            a = randint(-1, 1)
            self.speedx = -self.speedx - a
        else:
            if self.speedx > 0:
                self.speedx = -self.speedx - 1
            else:
                self.speedx = -self.speedx + 1
    def otskok_y(self):
        global min_speed
        a = self.speedy
        if self.speedy > min_speed or self.speedy < -min_speed :
            a = randint(-1, 1)
            self.speedy = -self.speedy - a
        else:
            if self.speedy > 0:
                self.speedy = -self.speedy - 1
            else:
                self.speedy = -self.speedy + 1
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

win_width = 700
win_height = 500
pygame.display.set_caption("pingaponga")
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load('img_back.png'), (win_width, win_height))

speeds = [2, -2, 2, -2]
shuffle(speeds)

ball = Ball('ball.png', randint(300, 350), randint(200,250), 50, 50, 0, speeds[0], speeds[1])

left_rocket = Rocket('left_rocket.png', 100, 200, 20, 100, 5, 1)
right_rocket = Rocket('right_rocket.png', 600, 200, 20, 100, 5, 2)

rockets = pygame.sprite.Group()
rockets.add(left_rocket)
rockets.add(right_rocket)

cooldown_collidex = 0
cooldown_collidey = 0
start = 4
run = True
finish = False

ball_speed_start  = time.time()
start_counter = time.time() - 1.2
while run:
    rockets.speed = min_speed + 2
    for e in pygame.event.get():
       if e.type == pygame.QUIT:
           run = False

    if not finish:
        window.blit(background,(0,0))
        rockets.draw(window)
        ball.reset()
        real_time = time.time()

        if start != 0:
            if real_time - start_counter >= 1.2:
                start -= 1
                if start != 0:
                    start_timer = font1.render(str(start), 1, (255,255,255))
                    window.blit(start_timer, (320, 100))
                else:
                    start_timer = font1.render('START!', 1, (255,255,255))
                    window.blit(start_timer, (250, 100))
                start_counter = time.time()
                pygame.display.update()
                
        if start == 0:
            rockets.update()
            ball.update()

            if  not (ball.rect.x < left_rocket.rect.x or ball.rect.x > right_rocket.rect.x + 20):

                if pygame.sprite.spritecollide(ball, rockets, False):
                    if real_time - cooldown_collidex >= 0.35:
                        ball.otskok_x()
                        cooldown_collidex = real_time

            if not (ball.rect.y > 5):
                ball.rect.y = 5
                if real_time - cooldown_collidey >= 0.35:    
                    ball.otskok_y()
                    cooldown_collidey = real_time

            elif not (ball.rect.y < 445):
                ball.rect.y = 445
                if real_time - cooldown_collidey >= 0.35:    
                    ball.otskok_y()
                    cooldown_collidey = real_time
            if ball.rect.x <= 0 or ball.rect.x >= 650:
                finish = True
                win = font1.render('GAME OVER', True, (255, 255, 255))
                window.blit(win, (135, 200))
            
            if real_time - ball_speed_start >= 5:
                min_speed += 1
                ball_speed_start = time.time()
            

            pygame.display.update()

        
            
        pygame.time.delay(10)
