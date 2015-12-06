import sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *


class Food(MySprite):
    global img_size,food_image
    def __init__(self):
        MySprite.__init__(self)
        image = create_pic()
        self.set_image(image)
        MySprite.update(self, 0, 30)
        self.X = random.randint(0,23) * img_size
        self.Y = random.randint(0,17) * img_size
        
class SnakeSegment(MySprite):
    global img_size,food_image
    def __init__(self):
        MySprite.__init__(self)
        image= create_pic()
        self.set_image(image)
        MySprite.update(self, 0, 30) 

class Snake():
    global img_size,food_image
    def __init__(self):
        self.velocity = Point(-1,0)
        self.old_time = 0
        head = SnakeSegment()
        head.X = 10*img_size
        head.Y = 9*img_size
        self.segments = list()
        self.segments.append(head)
        self.add_segment()
        self.add_segment()

    def update(self,ticks):
        global step_time 
        if ticks > self.old_time + step_time: 
            self.old_time = ticks
            #移动蛇的身体部分
            for n in range(len(self.segments)-1, 0, -1):
                self.segments[n].X = self.segments[n-1].X
                self.segments[n].Y = self.segments[n-1].Y
            #移动蛇头
            self.segments[0].X += self.velocity.x * img_size
            self.segments[0].Y += self.velocity.y * img_size

    def draw(self,surface):
        for segment in self.segments: 
            surface.blit(segment.image, (segment.X, segment.Y))
    
    def add_segment(self):
        last = len(self.segments)-1
        segment = SnakeSegment()
        start = Point(0,0)
        if self.velocity.x < 0: start.x = img_size
        elif self.velocity.x > 0: start.x = -img_size
        if self.velocity.y < 0: start.y = img_size
        elif self.velocity.y > 0: start.y = -img_size
        segment.X = self.segments[last].X + start.x
        segment.Y = self.segments[last].Y + start.y
        self.segments.append(segment)


#获得蛇当前的方向
def get_current_direction():
    global head_x,head_y
    global img_size
    first_segment_x = snake.segments[1].X//img_size
    first_segment_y = snake.segments[1].Y//img_size
    if head_x-1 == first_segment_x:   return "right"
    elif head_x+1 == first_segment_x: return "left"
    elif head_y-1 == first_segment_y: return "down"
    elif head_y+1 == first_segment_y: return "up"
        

#获得食物的坐标
def get_food_direction():
    global head_x,head_y
    global img_size
    food = Point(0,0)
    for obj in food_group:
        food = Point(obj.X//img_size,obj.Y//img_size)
    if head_x < food.x:       return "right"
    elif head_x > food.x:     return "left"
    elif head_x == food.x:
        if head_y < food.y:   return "down"
        elif head_y > food.y: return "up"

#简单自动寻路代码
def auto_move():
    direction = get_current_direction()
    food_dir = get_food_direction()
    if food_dir == "left":
        if direction != "right":
            direction = "left"
    elif food_dir == "right":
        if direction != "left":
            direction = "right"
    elif food_dir == "up":
        if direction != "down":
            direction = "up"
    elif food_dir == "down":
        if direction != "up":
            direction = "down"

    #设置蛇的移动方向
    if direction == "up": snake.velocity = Point(0,-1)
    elif direction == "down": snake.velocity = Point(0,1)
    elif direction == "left": snake.velocity = Point(-1,0)
    elif direction == "right": snake.velocity = Point(1,0)

    
#游戏初始化
def game_init():
    global screen, backbuffer, font, timer, snake, food_group,img_size,img_group
    font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()

    #使用备份缓存机制，减少资源的消耗
    backbuffer = pygame.Surface((screen.get_rect().width,screen.get_rect().height))

    #创建蛇体
    snake = Snake()

    #创建食物对象
    food_group = pygame.sprite.Group()
    food = Food()
    food_group.add(food)
    
#创建备用图片列表
def load_pic():
    for i in range(1,17):
        string = str(i)+".png"
        img = pygame.image.load(string).convert_alpha()
        width,height = img.get_size()
        img = pygame.transform.smoothscale(img,(width//7*5,height//7*5))
        img_group.append(img)
        string = ""

#创建随机头像
def create_pic():
    global img_group
    index = random.randint(0,15)
    image = img_group[index]
    return image

#初始化音频功能
def audio_init():
    global bgm
    
    #初识pygame中的音频模块，程序中只需加载一次
    pygame.mixer.init() 

    #加载音频文件
    bgm = pygame.mixer.Sound("bgm.ogg")

#定义播放声音函数
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)

#主程序开始   
pygame.init()
img_size =40
img_group = list()
screen_size = pygame.FULLSCREEN
screen = pygame.display.set_mode((24*img_size,18*img_size),screen_size)
pygame.display.set_caption("嗷大喵贪吃蛇")
face = pygame.image.load("face.png")
load_pic()
game_init()
game_over = False
last_time = 0
bgm = None
auto_play = False 
step_time = 400
waiting =True
audio_init()
rePlay = True
play_sound(bgm)
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    current_time = time.clock()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            if waiting == True:
                waiting = False
                game_over = False
                last_time = 0
                auto_play = False 
                step_time = 400
                game_init()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    elif keys[K_UP] or keys[K_w]:
        snake.velocity = Point(0,-1)
    elif keys[K_DOWN] or keys[K_s]:
        snake.velocity = Point(0,1)
    elif keys[K_LEFT] or keys[K_a]:
        snake.velocity = Point(-1,0)
    elif keys[K_RIGHT] or keys[K_d]:
        snake.velocity = Point(1,0)
    elif keys[K_f]:
        if screen_size == pygame.FULLSCREEN:
            screen_size =0
        else:
            screen_size =pygame.FULLSCREEN
        screen = pygame.display.set_mode((24*img_size,18*img_size),screen_size)
        pygame.display.set_caption("嗷大喵贪吃蛇")
    elif keys[K_PLUS] or keys[K_KP_PLUS]:
        step_time -= 10
        if step_time <50:
            step_time=50
    elif keys[K_MINUS] or keys[K_KP_MINUS]:
        step_time += 10
        if step_time >400:
            step_time = 400
    elif keys[K_SPACE]: 
        if auto_play:
            auto_play = False
            step_time = 400
        else:
            auto_play = True
            step_time = 100

    if waiting:
        screen.blit(face,(0,0))
    else:
        if not game_over:
            snake.update(ticks)
            food_group.update(ticks)
            
            #检测是否捡起食物，并增加身体长度
            hit_list = pygame.sprite.groupcollide(snake.segments, \
                food_group, False, True)
            if len(hit_list) > 0:
                food_group.add(Food())
                snake.add_segment()

            #检测是否碰到了自己的身体
            for n in range(1, len(snake.segments)):
                if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
                    game_over = True

            #检查屏幕边界
            head_x = snake.segments[0].X//img_size
            head_y = snake.segments[0].Y//img_size
            if head_x < 0 or head_x > 24 or head_y < 0 or head_y > 18:
                game_over = True

            #执行自动寻路代码
            if auto_play: auto_move()
        
        backbuffer.fill((20,50,20)) 
        snake.draw(backbuffer)
        food_group.draw(backbuffer)
        screen.blit(backbuffer, (0,0))

        if not game_over:
            print_text(font, 0, 0, "Length " + str(len(snake.segments)))
            print_text(font, 0, 20, "Position " + str(snake.segments[0].X//img_size) + \
                       "," + str(snake.segments[0].Y//img_size))
        else:
            print_text(font, 0, 0, "GAME OVER")
            waiting = True
            game_over = False

        #显示自动字样
        if auto_play: 
            print_text(font, 600, 0, "AUTO")

        #循环播放背景音乐 
        if int(current_time)%200 ==0 and rePlay:
            play_sound(bgm)
            rePlay = False
        if int(current_time)%200 == 1:
            rePlay = True
       
    pygame.display.update() 
    


