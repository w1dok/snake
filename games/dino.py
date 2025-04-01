import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Цвета
WHITE = (255, 255, 255)
GROUND_COLOR = (200, 200, 200)

# FPS
clock = pygame.time.Clock()
FPS = 30

# Загрузка изображений
dino_image = pygame.image.load("dino.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))  # Масштабируем изображение динозавра
cactus_image = pygame.image.load("cactus.png")
cactus_image = pygame.transform.scale(cactus_image, (50, 50))  # Масштабируем изображение кактуса

# Динозавр
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 20
dino_velocity = 0
gravity = 1
is_jumping = False

# Кактусы
cactus_width, cactus_height = 20, 50
cactus_x = WIDTH
cactus_y = HEIGHT - cactus_height - 20
cactus_speed = 5

# Счет
score = 0
font = pygame.font.Font(None, 36)

# Флаг паузы
paused = False

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 20, WIDTH, 20))  # Земля

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Кнопка паузы
                paused = not paused  # Переключаем состояние паузы
            if not paused and not is_jumping:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    is_jumping = True
                    dino_velocity = -15

    if paused:
        # Отображение текста "PAUSED"
        pause_text = font.render("PAUSED", True, (255, 0, 0))
        screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        pygame.display.flip()
        clock.tick(FPS)
        continue  # Пропускаем обновление игры, если пауза включена

    # Движение динозавра
    if is_jumping:
        dino_y += dino_velocity
        dino_velocity += gravity
        if dino_y >= HEIGHT - dino_height - 20:
            dino_y = HEIGHT - dino_height - 20
            is_jumping = False

    # Движение кактуса
    cactus_x -= cactus_speed
    if cactus_x < -cactus_width:
        cactus_x = WIDTH
        score += 1  # Увеличиваем счет

    # Проверка столкновения
    if dino_x < cactus_x + cactus_width and dino_x + dino_width > cactus_x and dino_y + dino_height > cactus_y:
        print("Game Over!")
        running = False

    # Отрисовка динозавра и кактуса
    screen.blit(dino_image, (dino_x, dino_y))  # Отображение динозавра
    screen.blit(cactus_image, (cactus_x, cactus_y))  # Отображение кактуса

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10)) 

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()