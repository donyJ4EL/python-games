import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 创建玩家飞机
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        
    def update(self):
        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 创建敌人飞机
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)
        
    def update(self):
        self.rect.y += self.speed_y
        # 如果敌人移出屏幕底部，重新生成
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 创建子弹
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # 如果子弹移出屏幕顶部，删除
        if self.rect.bottom < 0:
            self.kill()

class Game:
    def __init__(self):
        # 设置屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("飞机大战 - Aircraft War")
        self.clock = pygame.time.Clock()
        
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # 创建玩家
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # 创建敌人
        for i in range(8):
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            
        # 分数
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # 射击计时器
        self.shoot_timer = 0
        self.shoot_delay = 250  # 毫秒
        
    def run(self):
        running = True
        while running:
            # 控制帧率
            dt = self.clock.tick(FPS)
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # 添加射击延迟
                        current_time = pygame.time.get_ticks()
                        if current_time - self.shoot_timer > self.shoot_delay:
                            self.player.shoot(self.all_sprites, self.bullets)
                            self.shoot_timer = current_time
            
            # 更新
            self.all_sprites.update()
            
            # 检测子弹与敌人的碰撞
            hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            for hit in hits:
                self.score += 10
                # 重新生成敌人
                enemy = Enemy()
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            
            # 检测玩家与敌人的碰撞
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                print(f"游戏结束！最终得分: {self.score}")
                running = False
            
            # 绘制
            self.screen.fill(BLACK)
            
            # 绘制所有精灵
            self.all_sprites.draw(self.screen)
            
            # 绘制分数
            score_text = self.font.render(f"得分: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # 绘制说明
            instruction_text = self.font.render("方向键移动，空格键射击", True, WHITE)
            self.screen.blit(instruction_text, (SCREEN_WIDTH//2 - 150, 10))
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()