import pygame
import random

# Инициализация Pygame
pygame.init()

# Добавляем начальное время
start_time = pygame.time.get_ticks()

# Параметры окна
WIDTH, HEIGHT = 1200, 400
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
dino_x = WIDTH // 4  # Смещаем динозавра ближе к центру по оси X (1/4 ширины экрана)
dino_y = HEIGHT - dino_height - 20  # Смещаем динозавра вверх (на n пикселей выше земли)
dino_velocity = 0
gravity = 1
is_jumping = False

# Кактусы
cactus_width, cactus_height = 20, 50
cactus_speed = 5
cacti = []  # Список для хранения кактусов

# Инициализация кактусов
for i in range(5):  # Добавляем  кактусов
    cactus_x = WIDTH + i * 300  # Расстояние между кактусами
    cactus_y = HEIGHT - cactus_height - 20
    cacti.append({"x": cactus_x, "y": cactus_y})

# Счет
score = 0
font = pygame.font.Font(None, 36)

# Флаг паузы
paused = False

# Добавляем флаг для отслеживания прыжка
jump_triggered = False

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

    if paused:
        # Отображение текста "PAUSED"
        pause_text = font.render("PAUSED", True, (255, 0, 0))
        screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        pygame.display.flip()
        clock.tick(FPS)
        continue  # Пропускаем обновление игры, если пауза включена

    # Автоматический прыжок
    if not is_jumping and not jump_triggered:
        for cactus in cacti:
            if 0 < cactus["x"] - dino_x < 70:  # Если кактус близко
                is_jumping = True
                jump_triggered = True  # Устанавливаем флаг, чтобы предотвратить повторный прыжок
                dino_velocity = -20
                break

    # Движение динозавра
    if is_jumping:
        dino_y += dino_velocity
        dino_velocity += gravity
        if dino_y >= HEIGHT - dino_height - 20:
            dino_y = HEIGHT - dino_height - 20
            is_jumping = False

    # Сбрасываем флаг для каждого кактуса, если он прошел динозавра
    for cactus in cacti:
        if cactus["x"] - dino_x >= 70:
            jump_triggered = False

    # Движение кактусов
    for cactus in cacti:
        cactus["x"] -= cactus_speed
        if cactus["x"] < -cactus_width:
            cactus["x"] = WIDTH
            score += 1  # Увеличиваем счет

    # Проверка столкновений
    for cactus in cacti:
        if dino_x < cactus["x"] + cactus_width and dino_x + dino_width > cactus["x"] and dino_y + dino_height > cactus["y"]:
            print("Game Over!")
            running = False

    # Отрисовка динозавра и кактусов
    screen.blit(dino_image, (dino_x, dino_y))  # Отображение динозавра
    for cactus in cacti:
        screen.blit(cactus_image, (cactus["x"], cactus["y"]))  # Отображение кактусов

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10)) 

    # Расчет времени
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Время в секундах
    timer_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 40))  # Отображение таймера под счетом

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()