import pygame

# 初始化 Pygame
pygame.init()

# 定义窗口尺寸和设置显示窗口
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("悟空對戰佛祖")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 每一关的设定：包括背景图片、敌人血量和攻击力
LEVELS = [
    {'buddha': 'achubuddha.png', 'bg': 'goldmine.png', 'health': 1500, 'attack': 150},
    {'buddha': 'amitabuddha.png', 'bg': 'forest.png', 'health': 2500, 'attack': 250},
    {'buddha': 'baoshengbuddha.png', 'bg': 'sea.png', 'health': 3500, 'attack': 350},
    {'buddha': 'bukongchengjiubuddha.png', 'bg': 'volcano.png', 'health': 4500, 'attack': 450},
    {'buddha': 'vairocana.png', 'bg': 'mountain.png', 'health': 5000, 'attack': 500}
]

# 图像路径
WUKONG_IMAGE_PATH = 'wukong.png'

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, health, position):
        super(Character, self).__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.health = health
        self.attack_power = 0  # Default attack power, to be updated for each attack

    def update(self, keys):
        pass

    
class Player(Character):
    def __init__(self, position):
        super().__init__(WUKONG_IMAGE_PATH, 1000, position)
        self.speed = 5
        
    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        
    def attack(self):
        self.attack_power = 100
        
    def spin_kick(self):
        self.attack_power = 150
        
    def defend(self):
        self.attack_power = 0  # 防禦抵消攻击
        
    def ultimate(self):
        self.attack_power = 500


class Enemy(Character):
    def __init__(self, image_path, health, attack_power, position):
        super().__init__(image_path, health, position)
        self.attack_power = attack_power
    
    def update(self):
        pass # 可加入敌人的行为预测

def main():
    current_level = 0
    player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))

    while current_level < len(LEVELS):
        level_data = LEVELS[current_level]
        background_image = pygame.image.load(level_data['bg']).convert()
        enemy = Enemy(level_data['buddha'], level_data['health'], 
                      level_data['attack'], (WINDOW_WIDTH // 2, 100))

        player_group = pygame.sprite.Group(player)
        enemy_group = pygame.sprite.Group(enemy)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        player.attack()
                    elif event.key == pygame.K_2:
                        player.spin_kick()
                    elif event.key == pygame.K_3:
                        player.defend()
                    elif event.key == pygame.K_0:
                        player.ultimate()

            keys = pygame.key.get_pressed()
            player.update(keys)
            enemy.update()  # 可添加敌人的行为逻辑

            # 处理战斗逻辑
            if player.attack_power > 0:
                enemy.health -= player.attack_power
                player.attack_power = 0  # 重置攻击力量
            if enemy.attack_power > 0:
                if player.attack_power != 0:  # 使用防御
                    player.health -= enemy.attack_power
                
                enemy.attack_power = 0  # 重置敌人攻击力量

            # 检查游戏状态
            if enemy.health <= 0:
                current_level += 1
                if current_level < len(LEVELS):
                    player.health += 500  # 每过一关增加500血量
                running = False

            if player.health <= 0:
                print("游戏结束，你输了！")
                running = False
                pygame.quit()
                return

            # 填充背景
            screen.blit(background_image, (0, 0))

            # 绘制精灵
            player_group.draw(screen)
            enemy_group.draw(screen)

            # 绘制血量条
            pygame.draw.rect(screen, RED, (50, 50, player.health // 2, 20))
            pygame.draw.rect(screen, RED, (50, 80, enemy.health // 2, 20))

            # 更新显示
            pygame.display.flip()

            # 设置帧率
            pygame.time.Clock().tick(60)

    print("恭喜你，打敗了所有佛祖！")
    pygame.quit()

if __name__ == "__main__":
    main()
