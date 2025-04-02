import pygame
import random

# Инициализация Pygame
pygame.init()

# Добавляем начальное время
start_time = pygame.time.get_ticks()

# Изначальное количество энергии
energy = 10000  

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

# Максимальная высота прыжка
max_jump_height = HEIGHT - dino_y - dino_height  # Изначально равна текущей высоте динозавра

# Кактусы
cactus_width, cactus_height = 20, 50
cactus_speed = 5 # Скорость движения кактусов
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

# Инициализация шрифта для мелкого текста
small_font = pygame.font.Font(None, 20)  # Размер шрифта 20

def reset_game():
    global dino_y, dino_velocity, is_jumping, jump_triggered, max_jump_height, energy, score, cacti
    dino_y = HEIGHT - dino_height - 20
    dino_velocity = 0
    is_jumping = False
    jump_triggered = False
    max_jump_height = 0
    energy = 10000
    score = 0
    cacti = [{"x": WIDTH + i * 300, "y": HEIGHT - cactus_height - 20} for i in range(5)]

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
            if event.key == pygame.K_RETURN:  # Кнопка Enter для перезапуска игры
                reset_game()
            if event.key == pygame.K_SPACE:  # Кнопка паузы
                paused = not paused  # Переключаем состояние паузы

    if paused:
        # Отображение текста "PAUSED"
        clock.tick(FPS)
        continue  # Пропускаем обновление игры, если пауза включена

    # Автоматический прыжок
    if not is_jumping and not jump_triggered:
        for cactus in cacti:
            if 0 < cactus["x"] - dino_x < 100:  # Если кактус близко
                is_jumping = True
                jump_triggered = True  # Устанавливаем флаг, чтобы предотвратить повторный прыжок
                dino_velocity = -15  # Начальная скорость прыжка
                jump_height = HEIGHT - dino_y - dino_height  # Высота прыжка
                energy -= jump_height  # Уменьшаем энергию на высоту прыжка
                break

    # Движение динозавра
    if is_jumping:
        dino_y += dino_velocity
        dino_velocity += gravity
        current_height = HEIGHT - dino_y - dino_height  # Текущая высота динозавра
        if current_height > max_jump_height:
            max_jump_height = current_height  # Обновляем максимальную высоту
        if dino_y >= HEIGHT - dino_height - 20:  # Если динозавр достиг земли
            dino_y = HEIGHT - dino_height - 20
            is_jumping = False
            jump_height = max_jump_height  # Высота прыжка равна максимальной высоте
            energy -= jump_height  # Уменьшаем энергию на высоту прыжка
            max_jump_height = 0  # Сбрасываем максимальную высоту для следующего прыжка

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
            reset_game()

    # Отрисовка динозавра и кактусов
    screen.blit(dino_image, (dino_x, dino_y))  # Отображение динозавра

    # Отображение высоты динозавра
    height_text = small_font.render(f"{HEIGHT - dino_y - dino_height}", True, (0, 0, 0))  # Высота от земли
    screen.blit(height_text, (dino_x + dino_width + 10, dino_y))  # Отображение текста справа от динозавра

    for cactus in cacti:
        screen.blit(cactus_image, (cactus["x"], cactus["y"]))  # Отображение кактусов

    # Отображение оси Y с координатами
    small_font = pygame.font.Font(None, 20)  # Уменьшаем размер шрифта для координат
    for x in range(0, WIDTH, 10):  # Шаг отметок - 10 пикселей
        pygame.draw.line(screen, (0, 0, 0), (x, HEIGHT - 2), (x, HEIGHT - 10), 1)  # Вертикальные отметки
        if x % 50 == 0:  # Отображаем текст только для отметок, кратных 50
            coord_text = small_font.render(str(x), True, (0, 0, 0))  # Текст координаты
            screen.blit(coord_text, (x + 2, HEIGHT - 30))  # Отображение текста чуть выше отметки

    # Отображение оси X с координатами
    for y in range(0, HEIGHT, 20):  # Шаг отметок - 20 пикселей
        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT - y), (10, HEIGHT - y), 1)  # Горизонтальные отметки
        if y % 50 == 0:  # Отображаем текст только для отметок, кратных 50
            coord_text = small_font.render(str(y), True, (0, 0, 0))  # Текст координаты
            screen.blit(coord_text, (15, HEIGHT - y - 10))  # Отображение текста справа от отметки

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 200, 10))  # Перемещаем счет в правый верхний угол

    # Расчет времени
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Время в секундах
    timer_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH - 200, 40))  # Перемещаем таймер в правый верхний угол

    # Отображение энергии
    energy_text = font.render(f"Energy: {energy}", True, (0, 0, 0))
    screen.blit(energy_text, (WIDTH - 200, 70))  # Отображение энергии под таймером

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()