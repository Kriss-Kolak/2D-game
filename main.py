import pygame
import random

pygame.init()

window_x_size = 1280
window_y_size = 720

screen = pygame.display.set_mode((window_x_size, window_y_size))
clock = pygame.time.Clock()

player_shot_cooldown_ms = 100

player_x = window_x_size / 4
player_y = window_y_size / 2
velocity_player = 5

bullet_velocity = 10
max_bullets = 5

eaten_player = 0
eaten_computer = 0
velocity_computer = 1

player_width = 20
player_height = 20

run = True
last_shot = 0

computer_x = window_x_size * 3 / 4
computer_y = window_y_size / 2
computer_width = 20
computer_height = 20

color_1 = 255
color_2 = 255
color_3 = 255

class Bullet:
    def __init__(self, x_location, y_location, velocity=bullet_velocity, bullet_height=2, bullet_width=10, color=(255, 0, 0)):
        self.x = x_location
        self.y = y_location
        self.velocity = velocity
        self.bullet_height = bullet_height
        self.bullet_width = bullet_width
        self.bullet_color = color
        self.bullet_value = 1

    def update_player(self):
        self.x += self.velocity

    def update_computer(self):
        self.x -= self.velocity

player_bullets = []
computer_bullets = []

def computer_updated_logic_commands(bullet_list, computer_x, computer_y, computer_width, computer_height,
                                     window_x_size, window_y_size, velocity_computer, player_x=player_x, player_y=player_y):
    commands = []
    approaching_bullets = [bullet for bullet in bullet_list if bullet.x < computer_x]
    
    if not approaching_bullets:
        commands.append("STAY")
    else:
        closest_bullet = max(approaching_bullets, key=lambda b: b.x)
        bullet_top = closest_bullet.y
        bullet_bottom = closest_bullet.y + closest_bullet.bullet_height
        bullet_center = (bullet_top + bullet_bottom) / 2
        
        computer_center = computer_y + computer_height / 2
        
        if bullet_top < computer_y + computer_height and bullet_bottom > computer_y:
            if bullet_center < computer_center:
                commands.append("MOVE_DOWN")
            else:
                commands.append("MOVE_UP")
        else:
            commands.append("STAY")
    
    for command in commands:
        if command == "MOVE_UP":
            computer_y = max(0, computer_y - velocity_computer)
        elif command == "MOVE_DOWN":
            computer_y = min(window_y_size - computer_height, computer_y + velocity_computer)
    return computer_x, computer_y

def computer_shot(bullet_list, computer_x, computer_y, player_y):
    if random.random() < 0.1 and len(bullet_list) < max_bullets:
        if abs(computer_y - player_y) < 30:
            bullet_list.append(Bullet(computer_x - 10, computer_y + computer_height / 2, 5, 10, 10, color=(255, 255, 0)))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= velocity_player
    if keys[pygame.K_RIGHT] and player_x < window_x_size / 2 - 1 - player_width:
        player_x += velocity_player
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= velocity_player
    if keys[pygame.K_DOWN] and player_y < window_y_size - player_height:
        player_y += velocity_player

    if keys[pygame.K_SPACE] and len(player_bullets) < max_bullets and pygame.time.get_ticks() - last_shot > player_shot_cooldown_ms:
        player_bullets.append(Bullet(player_x + player_width + 2, player_y + player_height / 2, 5, 10, 10))
        last_shot = pygame.time.get_ticks()

    if random.random() < 0.1:
        color_1 = random.randint(0, 255)
        color_2 = random.randint(0, 255)
        color_3 = random.randint(0, 255)

    for bullet in player_bullets[:]:
        if (computer_x < bullet.x < computer_x + computer_width and 
            computer_y < bullet.y < computer_y + computer_height):
            player_bullets.remove(bullet)
            computer_width += bullet.bullet_value * 0.5
            computer_height += bullet.bullet_value * 0.5
            computer_y = max(0, computer_y - bullet.bullet_value * 0.25)
            computer_x = max(window_x_size / 2, computer_x - bullet.bullet_value * 0.25)
            eaten_computer += 1
            velocity_computer = min(5, eaten_computer / 100 + velocity_computer)

    for bullet in computer_bullets[:]:
        if (player_x < bullet.x < player_x + player_width and 
            player_y < bullet.y < player_y + player_height):
            computer_bullets.remove(bullet)
            player_width += bullet.bullet_value * 0.5
            player_height += bullet.bullet_value * 0.5
            player_x = max(0, player_x - bullet.bullet_value * 0.25)
            player_y = max(0, player_y - bullet.bullet_value * 0.25)
            eaten_player += 1
            velocity_player = min(5, eaten_player / 100 + velocity_player)

    computer_x, computer_y = computer_updated_logic_commands(player_bullets, computer_x, computer_y,
                                                               computer_width, computer_height,
                                                               window_x_size, window_y_size, velocity_computer)
    computer_shot(computer_bullets, computer_x, computer_y, player_y)

    screen.fill("black")
    player_bullets = [bullet for bullet in player_bullets if bullet.x < window_x_size]
    computer_bullets = [bullet for bullet in computer_bullets if bullet.x > 0]

    for bullet in player_bullets:
        bullet.update_player()
        pygame.draw.rect(screen, bullet.bullet_color, (bullet.x, bullet.y, bullet.bullet_width, bullet.bullet_height))

    for bullet in computer_bullets:
        bullet.update_computer()
        pygame.draw.rect(screen, bullet.bullet_color, (bullet.x, bullet.y, bullet.bullet_width, bullet.bullet_height))

    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, (255, 255, 0), (computer_x, computer_y, computer_width, computer_height))
    pygame.draw.rect(screen, (color_1, color_2, color_3), (window_x_size / 2 - 1, 0, 2, window_y_size))
    pygame.display.flip()
    clock.tick(60)
