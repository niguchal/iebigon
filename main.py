import pygame
import sys
import time

# Инициализация pygame
pygame.init()

# Настройки экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ← Без FULLSCREEN
pygame.display.set_caption("Турнирное табло")

# Цвета
RED = (200, 0, 0)
BLUE = (0, 0, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)

# Настройки турнира по дефолту
timer_duration = 30  # по умолчанию 30 секунд
wallerstein_mode = True  # режим Валлерштайн (подсчет раундов)

# Счет
red_score = 0
blue_score = 0
red_rounds_won = 0  # Выигранные раунды красного
blue_rounds_won = 0  # Выигранные раунды синего

# Имена бойцов
red_fighter_name = "Красный боец"
blue_fighter_name = "Синий боец"
name_edit_mode = False
current_editing = None

# Таймер
timer_active = False
timer_duration = 30  # 30 секунд
timer_start_time = 0
timer_remaining = timer_duration

# Шрифты
score_font = pygame.font.SysFont('Arial', 520, bold=True)
rounds_font = pygame.font.SysFont('Arial', 240, bold=True)
timer_font = pygame.font.SysFont('Arial', 120, bold=True)
small_font = pygame.font.SysFont('Arial', 120)
small_font_r = pygame.font.SysFont('Arial', 60)

def draw_screen():
    # Очистка экрана
    screen.fill(BLACK)
    
    # Разделение экрана на красную и синюю половины
    pygame.draw.rect(screen, RED, (0, 0, WIDTH//2 - 100, HEIGHT))
    pygame.draw.rect(screen, BLUE, (WIDTH//2 + 100, 0, WIDTH//2 - 100, HEIGHT))
    
    # Центральная панель для таймера
    panel_width = 300
    panel_x = WIDTH // 2 - panel_width // 2
    panel_y = 0
    panel_height = HEIGHT
    pygame.draw.rect(screen, GRAY, (panel_x, panel_y, panel_width, panel_height))
    
    # Отображение основного счета (внутри раунда)
    red_text = score_font.render(str(red_score), True, WHITE)
    blue_text = score_font.render(str(blue_score), True, WHITE)

    score_label_main = small_font.render("Счет", True, WHITE)
    screen.blit(score_label_main, (WIDTH//4 - 150 - red_text.get_width()//2 + red_text.get_width()//2 - score_label_main.get_width()//2 - 20, HEIGHT//2 - red_text.get_height()//2 + red_text.get_height() + 10))
    screen.blit(score_label_main, (3*WIDTH//4 - blue_text.get_width()//2 + red_text.get_width()//2 - score_label_main.get_width()//2, HEIGHT//2 - blue_text.get_height()//2 + red_text.get_height() + 10))
    
    screen.blit(red_text, (WIDTH//4 - 150 - red_text.get_width()//2, HEIGHT//2 - red_text.get_height()//2))
    screen.blit(blue_text, (3*WIDTH//4 - blue_text.get_width()//2, HEIGHT//2 - blue_text.get_height()//2))
    
    if wallerstein_mode:
        # Отображение выигранных раундов красного (слева от основного счета)
        red_rounds_text = rounds_font.render(f"{red_rounds_won}", True, WHITE)
        red_rounds_x = WIDTH//4 - 150 + red_text.get_width()//2 + 20
        red_rounds_y = HEIGHT//2 - red_rounds_text.get_height()//2
        screen.blit(red_rounds_text, (red_rounds_x, red_rounds_y))
        
        # Отображение выигранных раундов синего (справа от основного счета)
        blue_rounds_text = rounds_font.render(f"{blue_rounds_won}", True, WHITE)
        blue_rounds_x = 3*WIDTH//4 - blue_text.get_width()//2 - blue_rounds_text.get_width() - 40
        blue_rounds_y = HEIGHT//2 - blue_rounds_text.get_height()//2
        screen.blit(blue_rounds_text, (blue_rounds_x, blue_rounds_y))
        # Подпись под счетом раундов красного
        red_rounds_label = small_font_r.render("Счет раундов", True, WHITE)
        red_label_x = red_rounds_x + red_rounds_text.get_width()//2 - red_rounds_label.get_width()//2 + 40
        red_label_y = red_rounds_y + red_rounds_text.get_height() + 5
        screen.blit(red_rounds_label, (red_label_x, red_label_y))

        # Подпись под счетом раундов синего
        blue_rounds_label = small_font_r.render("Счет раундов", True, WHITE)
        blue_label_x = blue_rounds_x + blue_rounds_text.get_width()//2 - blue_rounds_label.get_width()//2 - 20
        blue_label_y = blue_rounds_y + blue_rounds_text.get_height() + 5
        screen.blit(blue_rounds_label, (blue_label_x, blue_label_y))
        
    # Отображение таймера
    timer_color = GREEN if timer_active else WHITE
    timer_text = timer_font.render(format_time(timer_remaining), True, timer_color)
    timer_x = panel_x + panel_width // 2 - timer_text.get_width() // 2
    timer_y = panel_y + panel_height // 2 - timer_text.get_height() // 2
    screen.blit(timer_text, (timer_x, timer_y))

    timer_label = small_font.render("Время", True, WHITE)
    label_x = panel_x + panel_width // 2 - timer_label.get_width() // 2
    label_y = timer_y + timer_text.get_height() + 10
    screen.blit(timer_label, (label_x, label_y))

    # Отображение имен бойцов
    red_name_text = small_font.render(red_fighter_name, True, WHITE)
    blue_name_text = small_font.render(blue_fighter_name, True, WHITE)

    # Размещаем имена над основным счетом
    screen.blit(red_name_text, (WIDTH//4 - 150 - red_text.get_width()//2 + red_text.get_width()//2 - red_name_text.get_width()//2, HEIGHT//2 - red_text.get_height()//2 - 100))
    screen.blit(blue_name_text, (3*WIDTH//4 - blue_text.get_width()//2 + red_text.get_width()//2 + blue_text.get_width()//2 - blue_name_text.get_width()//2, HEIGHT//2 - blue_text.get_height()//2 - 100))
    
    pygame.display.flip()

def draw_name_edit_overlay(red_temp, blue_temp, time_temp, wallerstein_temp):
    """Отрисовка overlay для редактирования настроек"""
    # Полупрозрачный overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    title_font = pygame.font.SysFont('Arial', 40, bold=True)
    label_font = pygame.font.SysFont('Arial', 30)
    input_font = pygame.font.SysFont('Arial', 28)
    
    # Заголовок
    title = title_font.render("Настройки боя", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Поле для красного бойца
    red_rect = pygame.Rect(WIDTH//4 - 150, 120, 300, 50)
    pygame.draw.rect(screen, RED, red_rect, 2)
    red_label = label_font.render("Красный боец:", True, WHITE)
    screen.blit(red_label, (WIDTH//4 - 150, 90))
    red_text = input_font.render(red_temp, True, WHITE)
    screen.blit(red_text, (red_rect.x + 10, red_rect.y + 10))
    
    # Поле для синего бойца  
    blue_rect = pygame.Rect(3*WIDTH//4 - 150, 120, 300, 50)
    pygame.draw.rect(screen, BLUE, blue_rect, 2)
    blue_label = label_font.render("Синий боец:", True, WHITE)
    screen.blit(blue_label, (3*WIDTH//4 - 150, 90))
    blue_text = input_font.render(blue_temp, True, WHITE)
    screen.blit(blue_text, (blue_rect.x + 10, blue_rect.y + 10))
    
    # Поле для времени раунда
    time_rect = pygame.Rect(WIDTH//2 - 150, 200, 300, 50)
    pygame.draw.rect(screen, GREEN, time_rect, 2)
    time_label = label_font.render("Время раунда (сек):", True, WHITE)
    screen.blit(time_label, (WIDTH//2 - 150, 170))
    time_text = input_font.render(str(time_temp), True, WHITE)
    screen.blit(time_text, (time_rect.x + 10, time_rect.y + 10))
    
    # Переключатель Валлерштайн
    wallerstein_rect = pygame.Rect(WIDTH//2 - 150, 280, 300, 50)
    pygame.draw.rect(screen, YELLOW, wallerstein_rect, 2)
    wallerstein_label = label_font.render("Режим Валлерштайн:", True, WHITE)
    screen.blit(wallerstein_label, (WIDTH//2 - 150, 250))
    wallerstein_text = input_font.render("ВКЛ" if wallerstein_temp else "ВЫКЛ", True, WHITE)
    screen.blit(wallerstein_text, (wallerstein_rect.x + 10, wallerstein_rect.y + 10))
    
    # Индикатор текущего поля
    if current_editing == "red":
        pygame.draw.rect(screen, YELLOW, red_rect, 4)
    elif current_editing == "blue":
        pygame.draw.rect(screen, YELLOW, blue_rect, 4)
    elif current_editing == "time":
        pygame.draw.rect(screen, YELLOW, time_rect, 4)
    elif current_editing == "wallerstein":
        pygame.draw.rect(screen, YELLOW, wallerstein_rect, 4)
    
    # Инструкция
    instructions = [
        "Tab - переключение между полями",
        "Space - переключить Валлерштайн", 
        "Backspace - удалить символ",
        "Enter - сохранить",
        "Esc - отмена"
    ]
    
    for i, instruction in enumerate(instructions):
        instr_text = label_font.render(instruction, True, YELLOW)
        screen.blit(instr_text, (WIDTH//2 - instr_text.get_width()//2, 350 + i * 40))
    
    pygame.display.flip()

def edit_names_interactive():
    """Интерактивное редактирование настроек боя"""
    global red_fighter_name, blue_fighter_name, timer_duration, wallerstein_mode
    global name_edit_mode, current_editing, timer_remaining  # ← Добавьте timer_remaining
    
    name_edit_mode = True
    current_editing = "red"
    red_temp = red_fighter_name
    blue_temp = blue_fighter_name
    time_temp = str(timer_duration)
    wallerstein_temp = wallerstein_mode
    
    while name_edit_mode:
        screen.fill(BLACK)
        draw_name_edit_overlay(red_temp, blue_temp, time_temp, wallerstein_temp)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                name_edit_mode = False
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Сохраняем все настройки
                    red_fighter_name = red_temp
                    blue_fighter_name = blue_temp
                    try:
                        new_duration = int(time_temp)
                        timer_duration = new_duration
                        timer_remaining = new_duration  # ← ОБНОВЛЯЕМ timer_remaining!
                    except ValueError:
                        timer_duration = 30
                        timer_remaining = 30
                    wallerstein_mode = wallerstein_temp
                    name_edit_mode = False
                    return True
                    
                elif event.key == pygame.K_ESCAPE:
                    name_edit_mode = False
                    return False
                    
                elif event.key == pygame.K_TAB:
                    # Циклическое переключение между полями
                    fields = ["red", "blue", "time", "wallerstein"]
                    current_index = fields.index(current_editing)
                    current_editing = fields[(current_index + 1) % len(fields)]
                    
                elif event.key == pygame.K_SPACE and current_editing == "wallerstein":
                    wallerstein_temp = not wallerstein_temp
                    
                elif event.key == pygame.K_BACKSPACE:
                    if current_editing == "red" and red_temp:
                        red_temp = red_temp[:-1]
                    elif current_editing == "blue" and blue_temp:
                        blue_temp = blue_temp[:-1]
                    elif current_editing == "time" and time_temp:
                        time_temp = time_temp[:-1]
                        
                else:
                    if event.unicode and event.unicode.isprintable() and len(event.unicode) == 1:
                        if current_editing == "red" and len(red_temp) < 20:
                            red_temp += event.unicode
                        elif current_editing == "blue" and len(blue_temp) < 20:
                            blue_temp += event.unicode
                        elif current_editing == "time" and event.unicode.isdigit() and len(time_temp) < 3:
                            time_temp += event.unicode
        
        pygame.time.delay(50)
    
    return False

def format_time(seconds):
    """Форматирование времени в MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def update_timer():
    """Обновление состояния таймера"""
    global timer_remaining, timer_active
    
    if timer_active:
        elapsed = time.time() - timer_start_time
        timer_remaining = max(0, timer_duration - int(elapsed))
        
        if timer_remaining == 0:
            timer_active = False
            # Автоматическое определение победителя раунда при окончании времени
            determine_round_winner()

def determine_round_winner():
    """Определение победителя раунда"""
    global red_rounds_won, blue_rounds_won, red_score, blue_score
    
    if wallerstein_mode:  # ← Только если включен режим Валлерштайн
        if red_score > blue_score:
            red_rounds_won += 1
        elif blue_score > red_score:
            blue_rounds_won += 1
    
    # Сброс счета для нового раунда (всегда)
    red_score = 0
    blue_score = 0
# Главный цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            # Управление счетом внутри раунда
            if event.key == pygame.K_LEFT:
                red_score += 1
            elif event.key == pygame.K_RIGHT:
                blue_score += 1     
            
            # Ручное завершение раунда и определение победителя
            elif event.key == pygame.K_UP:
                determine_round_winner()
            
            # Управление таймером
            elif event.key == pygame.K_SPACE:
                if timer_active:
                    timer_active = False
                else:
                    if timer_remaining == 0:
                        timer_remaining = timer_duration
                    timer_active = True
                    timer_start_time = time.time() - (timer_duration - timer_remaining)
            elif event.key == pygame.K_0:
                timer_remaining = timer_duration  # ← Используем текущую длительность
                timer_active = False
            
            elif event.key == pygame.K_0:
                timer_remaining = timer_duration
                timer_active = False

            elif event.key == pygame.K_f:  # F - переключение полноэкранного режима
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((1000, 600))
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                WIDTH, HEIGHT = screen.get_size()

                # Редактирование имен бойцов
            elif event.key == pygame.K_n:  # N - редактировать имена
                edit_names_interactive()

                # Перезапускаем pygame после ввода имен
                pygame.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            # Управление временем раунда
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                # Добавить 5 секунд (максимум 5 минут)
                timer_remaining = min(timer_remaining + 5, 300)
                
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                # Снять 5 секунд (минимум 0)
                timer_remaining = max(timer_remaining - 5, 0)

            # Управление баллами бойцов (добавление/снятие)
            elif event.key == pygame.K_PERIOD:  # / - снять балл у красного
                red_score = max(red_score - 1, 0)
                
            elif event.key == pygame.K_COMMA:  # \ - снять балл у синего  
                blue_score = max(blue_score - 1, 0)

            # Сброс всего
            elif event.key == pygame.K_r:
                red_score = 0
                blue_score = 0
                red_rounds_won = 0
                blue_rounds_won = 0
                timer_remaining = timer_duration  # ← Используем текущую длительность
                timer_active = False
            
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # Обновление таймера
    update_timer()
    
    # Отрисовка экрана
    draw_screen()
    
    # Ограничение FPS
    clock.tick(60)

pygame.quit()
sys.exit()