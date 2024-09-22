import pygame
import random
import time

# 初始化 pygame
pygame.init()

# 初始化 pygame 音频模块
pygame.mixer.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 屏幕大小
screen_width = 800
screen_height = 600

# 设置游戏窗口
screen = pygame.display.set_mode((screen_width, screen_height))

# 游戏标题
pygame.display.set_caption('School Bomber')

# 设置时钟
clock = pygame.time.Clock()

# 玩家属性
player_speed = 5

# 教学楼属性
building_width = 50
building_height = 50

# 老师属性
teacher_speed = 2

# 炸药包属性
bomb_size = 10
bomb_delay = 1  # 放置炸药的冷却时间（秒）
bomb_range = 50

# 定义字体
font = pygame.font.SysFont("comicsansms", 35)

# 加载背景音乐
pygame.mixer.music.load('bgm_school_bomber.mp3')  # 替换为你的歌曲文件名
pygame.mixer.music.play(-1)  # -1 表示循环播放

# 加载图片
player_image = pygame.image.load('child.png')  # 小孩图片
player_image = pygame.transform.scale(player_image, (50, 50))  # 缩放图片

teacher_image = pygame.image.load('teacher.png')  # 老师图片
teacher_image = pygame.transform.scale(teacher_image, (50, 50))  # 缩放图片

building_image = pygame.image.load('building.png')  # 教学楼图片
building_image = pygame.transform.scale(building_image, (70, 70))  # 缩放图片

# 绘制小孩（玩家）
def draw_player(x, y):
    screen.blit(player_image, (x, y))  # 用图片绘制玩家

# 绘制老师
def draw_teacher(x, y):
    screen.blit(teacher_image, (x, y))  # 用图片绘制老师

# 绘制教学楼
def draw_building(x, y):
    screen.blit(building_image, (x, y))  # 用图片绘制教学楼

# 绘制炸药包
def draw_bomb(x, y):
    pygame.draw.circle(screen, black, (x, y), bomb_size)  # 仍然用简单的炸弹表示

# 显示得分
def show_score(score):
    value = font.render(f"Buildings Left: {score}", True, white)
    screen.blit(value, [10, 10])

# 游戏主循环
def game_loop():
    game_over = False
    game_close = False

    player_x = screen_width / 2
    player_y = screen_height / 2
    player_dx = 0
    player_dy = 0

    # 难度参数
    difficulty = 1
    buildings_left = 3
    teacher_count = 1

    # 生成教学楼
    buildings = []
    for i in range(buildings_left):
        buildings.append([random.randint(0, screen_width - building_width),
                          random.randint(0, screen_height - building_height)])

    # 生成老师
    teachers = []
    for i in range(teacher_count):
        teachers.append([random.randint(0, screen_width - 50),
                         random.randint(0, screen_height - 50)])

    # 放置炸药包
    bombs = []
    last_bomb_time = time.time()

    # 游戏循环
    while not game_over:

        while game_close:
            screen.fill(black)
            message = font.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            screen.blit(message, [screen_width / 6, screen_height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # 处理玩家输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx = -player_speed
                elif event.key == pygame.K_RIGHT:
                    player_dx = player_speed
                elif event.key == pygame.K_UP:
                    player_dy = -player_speed
                elif event.key == pygame.K_DOWN:
                    player_dy = player_speed
                elif event.key == pygame.K_SPACE:
                    if time.time() - last_bomb_time > bomb_delay:
                        bombs.append([player_x + 25, player_y + 25])
                        last_bomb_time = time.time()

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_dx = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player_dy = 0

        # 移动玩家
        player_x += player_dx
        player_y += player_dy

        # 限制玩家边界
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - 50:
            player_x = screen_width - 50
        if player_y < 0:
            player_y = 0
        elif player_y > screen_height - 50:
            player_y = screen_height - 50

        # 清屏
        screen.fill(black)

        # 绘制教学楼
        for building in buildings:
            draw_building(building[0], building[1])

        # 绘制炸药包
        for bomb in bombs:
            draw_bomb(bomb[0], bomb[1])

            # 检查炸药包是否炸到建筑物
            for building in buildings[:]:
                if abs(bomb[0] - (building[0] + building_width // 2)) < bomb_range and \
                        abs(bomb[1] - (building[1] + building_height // 2)) < bomb_range:
                    buildings.remove(building)
                    bombs.remove(bomb)

        # 如果教学楼被炸完，玩家胜利
        if len(buildings) == 0:
            difficulty += 1
            buildings_left += 2  # 难度增加时，增加建筑物
            teacher_count += 1   # 增加老师数量
            # 生成新建筑物和老师
            buildings = [[random.randint(0, screen_width - building_width),
                          random.randint(0, screen_height - building_height)] for _ in range(buildings_left)]
            teachers = [[random.randint(0, screen_width - 50),
                         random.randint(0, screen_height - 50)] for _ in range(teacher_count)]

        # 绘制老师并追逐玩家
        for teacher in teachers:
            if teacher[0] < player_x:
                teacher[0] += teacher_speed
            if teacher[0] > player_x:
                teacher[0] -= teacher_speed
            if teacher[1] < player_y:
                teacher[1] += teacher_speed
            if teacher[1] > player_y:
                teacher[1] -= teacher_speed

            draw_teacher(teacher[0], teacher[1])

            # 检查老师是否抓到玩家
            if abs(player_x - teacher[0]) < 50 and abs(player_y - teacher[1]) < 50:
                game_close = True

        # 绘制玩家
        draw_player(player_x, player_y)

        # 显示剩余教学楼
        show_score(len(buildings))

        # 更新屏幕
        pygame.display.update()

        # 控制帧率
        clock.tick(30)

    pygame.quit()
    quit()

# 开始游戏
game_loop()
