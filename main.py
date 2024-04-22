from datetime import datetime, timedelta
import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1245, 530))
pygame.display.set_caption('Бумажки пж')

# Цвета и шрифт
BLACK = (0, 0, 0)
RED = (157, 0, 0)
WHITE = (255, 255, 255)
GREEN = (12, 156, 0)
TABLE = (95, 66, 47)
ATABLE = (85, 61, 45)
WINDOW = (34, 34, 34)
AWINDOW = (52, 52, 52)

# Параметры паспорта
passport_pos = [300, 200]
passport_info = ""
passport_size = (315, 200)

# Параметры разрешения
acess_pos = [300, 200]
acess_info = ""
acess_size = (280, 200)

# Печати
stamps = []  # Список для хранения данных о печатях: [(x, y, color)]
stamp1_button = pygame.Rect(1150, 450, 95, 45)  # Позиция и размер кнопки для первой печати
stamp2_button = pygame.Rect(1150, 490, 95, 45)  # Позиция и размер кнопки для второй печати
# Загрузка изображений печатей
stamp1_image = pygame.image.load('stamp1.png').convert_alpha()
stamp2_image = pygame.image.load('stamp2.png').convert_alpha()
# Текущее выбранное изображение печати
current_stamp_image = stamp1_image
# Слегка уменьшаем изображения для отображения в качестве иконок на кнопках
screen.blit(pygame.transform.scale(stamp1_image, (70, 30)), (stamp1_button.x + 5, stamp1_button.y + 2.5))
screen.blit(pygame.transform.scale(stamp2_image, (70, 30)), (stamp2_button.x + 5, stamp2_button.y + 2.5))

# Флаги и состояния
passport_dragging = False
acess_dragging = False
show_menu = True
game_started = False
legitimate = True
show_story = False
goodend = False
badend = False

drop_zone = pygame.Rect(0, 0, 1245, 165)
start_button = pygame.Rect(500, 200, 245, 100)
startday_button = pygame.Rect(950, 400, 245, 100)

# Счетчики
client_good = 0
client = 0
goodday = 0
current_day = 0

story_texts = [[
    "Вы выиграли в трудовую латерею и вас направили",
    "трудиться в КПП Ваш наставник, предупредил,",
    "что уже через неделю пройдёт подведение",
    "итогов, и от результатов работы зависит,",
    "станете ли вы полноценным работником."],
    [
        "Вчера Вы справились хорошо, но",
        "наступающий день обещает быть тяжелым",
        "жалаем справиться!"],
    [
        "Думаем что вы уже привыкли к новому месту.",
        "Сегодня предстоит более спокойный день.",
        "Однако это не значит, что можно",
        "расслабиться: каждая мелочь важна."],
    [
        "Поступила информация о том, что.",
        "сегодня наш КПП попытаются пересечь",
        "больше нарушителей, чем обычно.",
        "Будьте на чеку."
    ],
    [
        "Это последний день вашей стажировки.",
        "Сегодня вечером вас ожидает подведение",
        "итогов. Там вы узнаете получите ли вы",
        "работу."
    ]
]

good_end = [
    "Подзравляем! Вы прошли стажировку!",
    "Вы проявили внимательность и профессионализм",
    "во время своей работы и мы рады говорить вам",
    "что ваша работа на нашем КПП только начинается!"
]

bad_end = [
    "К сожалению ваша стажировка прошла не так",
    "как мы ожидали. Благодаря этому опыту",
    "было принято решение об отмене трудовой латереи.",
    "Мы вынуждены принудить вас вернуться домой,",
    "рады были сотрудничать."
]


def generate_new_passport():
    names = ["Алекс", "Марк", "Иван", "Юлий", "Саня", "Антон", "Илон", "Павел", "Джордж", "Сатош"]
    surnames = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Маск", "Гейтс", "Жобс"]
    name = random.choice(names)
    surname = random.choice(surnames)
    date = (datetime(1980, 1, 1) + timedelta(days=random.randint(12049, 33049))).strftime(
        "%d.%m.%Y")
    return ([f"Имя: {name} {surname}", f"До: {date}",
             f'{random.randint(10, 99)} {random.randint(100000000, 999999999)}'],
            [random.randint(100, 540), random.randint(200, 380)])


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_menu and start_button.collidepoint(event.pos):
                show_menu = False
                show_story = True
            if show_story and startday_button.collidepoint(event.pos):
                show_story = False
                game_started = True
                passport_info, passport_pos = generate_new_passport()
                if not random.choice([True, True, True, True, True, True, False]):
                    acess_info, acess_pos = generate_new_passport()
                    legitimate = False
                else:
                    acess_info, acess_pos = passport_info, [i - 25 for i in passport_pos]
                    legitimate = True
                if datetime(*[int(i) for i in passport_info[1][4:].split('.')[::-1]]) < datetime.now():
                    legitimate = False
                stamps = []
            elif game_started and event.button == 1:  # Левая кнопка мыши
                passport_rect = pygame.Rect(passport_pos[0], passport_pos[1], *passport_size)
                acess_rect = pygame.Rect(acess_pos[0], acess_pos[1], *acess_size)
                if passport_rect.collidepoint(event.pos):
                    passport_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = passport_pos[0] - mouse_x
                    offset_y = passport_pos[1] - mouse_y
                elif acess_rect.collidepoint(event.pos):
                    acess_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = acess_pos[0] - mouse_x
                    offset_y = acess_pos[1] - mouse_y
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                if stamp1_button.collidepoint(event.pos):
                    current_stamp_image = stamp1_image  # Выбор первой печати
                elif stamp2_button.collidepoint(event.pos):
                    current_stamp_image = stamp2_image  # Выбор второй печати

            elif game_started and event.button == 3:  # Правая кнопка мыши, добавление печати
                stamp_pos = (event.pos[0] - passport_pos[0] - 95, event.pos[1] - passport_pos[1] - 25)
                if 0 <= stamp_pos[0] <= passport_size[0] and 0 <= stamp_pos[1] <= passport_size[1]:
                    stamps.append((stamp_pos[0], stamp_pos[1], current_stamp_image))

        elif event.type == pygame.MOUSEBUTTONUP and game_started and passport_dragging:
            if event.button == 1 and passport_dragging:
                passport_dragging = False
                if drop_zone.collidepoint((mouse_x + offset_x, mouse_y + offset_y)) and stamps:
                    client += 1
                    if client != 10:
                        client_good += 1 if legitimate == (stamps[-1] == stamp1_image) else 0
                        passport_info, passport_pos = generate_new_passport()
                        if not random.choice([True, True, True, True, True, True, False]):
                            acess_info, acess_pos = generate_new_passport()
                            legitimate = False
                        else:
                            acess_info, acess_pos = passport_info, [i - 25 for i in passport_pos]
                            legitimate = True
                        stamps = []  # Очистка списка печатей при сдаче паспорта
                    else:
                        if current_day != len(story_texts) - 1:
                            if client_good > 5:
                                goodday += 1
                            client_good = 0
                            current_day += 1
                            client = 0
                            stamps = []
                            show_story = True
                            game_started = False
                        elif goodday >= 4:
                            goodend = True
                        elif goodday < 4:
                            badend = True
        elif event.type == pygame.MOUSEMOTION and game_started and passport_dragging:
            mouse_x, mouse_y = event.pos
            passport_pos[0] = mouse_x + offset_x
            passport_pos[1] = mouse_y + offset_y

        elif event.type == pygame.MOUSEBUTTONUP and game_started and acess_dragging:
            if event.button == 1 and acess_dragging:
                acess_dragging = False

        elif event.type == pygame.MOUSEMOTION and game_started and acess_dragging:
            mouse_x, mouse_y = event.pos
            acess_pos[0] = mouse_x + offset_x
            acess_pos[1] = mouse_y + offset_y

        screen.fill(BLACK)
        if show_menu:
            pygame.draw.rect(screen, (50, 50, 50), start_button)
            start_text = pygame.font.Font('ChixaDemiBold.ttf', 42).render("Начать игру",
                                                                          True, WHITE)
            screen.blit(start_text, (start_button.x + 12, start_button.y + 25))
        elif show_story:
            # Отображение сюжетной вставки
            j = 100
            for i in story_texts[current_day]:
                text_surf = pygame.font.Font('ChixaDemiBold.ttf', 42).render(i,
                                                                             True, WHITE)
                screen.blit(text_surf, (100, j))
                j += 50
            pygame.draw.rect(screen, (50, 50, 50), startday_button)  # Кнопка "Начать день"
            btn_text = pygame.font.Font('ChixaDemiBold.ttf', 42).render("Начать день",
                                                                        True, WHITE)
            screen.blit(btn_text, (startday_button.x + 10, startday_button.y + 25))
        elif goodend:
            # Отображение хорошей концовки
            j = 100
            for i in good_end:
                text_surf = pygame.font.Font('ChixaDemiBold.ttf', 42).render(i,
                                                                             True, WHITE)
                screen.blit(text_surf, (100, j))
                j += 50
        elif badend:
            # Отображение плохой концовки
            j = 100
            for i in bad_end:
                text_surf = pygame.font.Font('ChixaDemiBold.ttf', 42).render(i,
                                                                             True, WHITE)
                screen.blit(text_surf, (100, j))
                j += 50
        elif game_started:
            screen.fill(BLACK)
            # Игровая область
            pygame.draw.rect(screen, AWINDOW, drop_zone)
            pygame.draw.rect(screen, WINDOW, (20, 20, 1205, 125))
            pygame.draw.rect(screen, ATABLE, (0, 165, 1245, 365))
            pygame.draw.rect(screen, TABLE, (20, 185, 1205, 325))
            passport_rect = pygame.Rect(passport_pos[0], passport_pos[1], *passport_size)
            pygame.draw.rect(screen, GREEN, stamp1_button)
            pygame.draw.rect(screen, RED, stamp2_button)
            screen.blit(pygame.transform.scale(stamp1_image, (70, 30)), (stamp1_button.x + 5, stamp1_button.y + 2.5))
            screen.blit(pygame.transform.scale(stamp2_image, (70, 30)), (stamp2_button.x + 5, stamp2_button.y + 2.5))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if stamp1_button.collidepoint(event.pos):
                    current_stamp_image = stamp1_image
                elif stamp2_button.collidepoint(event.pos):
                    current_stamp_image = stamp2_image

            # Отображение паспорта и информации
            image = pygame.image.load('acess.png').convert_alpha()
            screen.blit(image, acess_pos)
            acess_text = [pygame.font.Font('ChixaDemiBold.ttf', 14).render(i, True, BLACK) for i in acess_info]
            screen.blit(acess_text[0], (acess_pos[0] + 30, acess_pos[1] + 70))
            screen.blit(acess_text[1], (acess_pos[0] + 30, acess_pos[1] + 105))
            screen.blit(acess_text[2], (acess_pos[0] + 30, acess_pos[1] + 145))

            image = pygame.image.load('passport.png').convert_alpha()
            screen.blit(image, passport_pos)
            passport_text = [pygame.font.Font('ChixaDemiBold.ttf', 14).render(i, True, BLACK) for i in passport_info]
            screen.blit(passport_text[0], (passport_pos[0] + 15, passport_pos[1] + 40))
            screen.blit(passport_text[1], (passport_pos[0] + 15, passport_pos[1] + 60))
            screen.blit(passport_text[2], (passport_pos[0] + 38, passport_pos[1] + 170))

            # Отображение печатей
            for stamp in stamps:
                screen.blit(stamp[2], (passport_pos[0] + stamp[0], passport_pos[1] + stamp[1]))

            if passport_rect.colliderect(drop_zone):
                text = pygame.font.Font(None, 35).render("Отдать", True, WHITE)
                screen.blit(text, (drop_zone.x + 550, drop_zone.y + 50))

        pygame.display.flip()

pygame.quit()
sys.exit()
