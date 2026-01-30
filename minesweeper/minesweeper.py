import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
GRID_SIZE = 10
CELL_SIZE = 40
MINES_COUNT = 15

# 屏幕尺寸
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = (GRID_SIZE * CELL_SIZE) + 60  # 额外空间用于UI

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class MinesweeperGame:
    def __init__(self):
        # 设置屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("扫雷游戏 - Minesweeper")
        
        # 字体设置
        self.font = pygame.font.SysFont('Arial', 16)
        self.big_font = pygame.font.SysFont('Arial', 24)
        
        # 游戏状态
        self.grid = []
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.flags_count = MINES_COUNT
        
        # 时间和计数器
        self.start_time = 0
        self.elapsed_time = 0
        
        # 创建网格
        self.create_grid()
        
    def create_grid(self):
        """创建空白网格"""
        self.grid = []
        for row in range(GRID_SIZE):
            grid_row = []
            for col in range(GRID_SIZE):
                grid_row.append(Cell())
            self.grid.append(grid_row)
    
    def place_mines(self, exclude_row, exclude_col):
        """在排除第一次点击位置的情况下放置地雷"""
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            
            # 确保不在第一次点击的位置及其周围放置地雷
            if (row == exclude_row and col == exclude_col) or \
               (abs(row - exclude_row) <= 1 and abs(col - exclude_col) <= 1):
                continue
                
            if not self.grid[row][col].is_mine:
                self.grid[row][col].is_mine = True
                mines_placed += 1
    
    def calculate_adjacent_mines(self):
        """计算每个单元格周围的地雷数量"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if not self.grid[row][col].is_mine:
                    count = 0
                    for r in range(max(0, row-1), min(GRID_SIZE, row+2)):
                        for c in range(max(0, col-1), min(GRID_SIZE, col+2)):
                            if self.grid[r][c].is_mine:
                                count += 1
                    self.grid[row][col].adjacent_mines = count
    
    def reveal(self, row, col):
        """揭示一个单元格"""
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return
            
        cell = self.grid[row][col]
        
        if cell.is_revealed or cell.is_flagged:
            return
            
        # 第一次点击时放置地雷，确保不会在点击位置爆炸
        if self.first_click:
            self.place_mines(row, col)
            self.calculate_adjacent_mines()
            self.first_click = False
            self.start_time = pygame.time.get_ticks()
        
        cell.is_revealed = True
        
        if cell.is_mine:
            self.game_over = True
            # 揭示所有地雷
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.grid[r][c].is_mine:
                        self.grid[r][c].is_revealed = True
            return
        
        # 如果相邻没有地雷，则递归揭示相邻单元格
        if cell.adjacent_mines == 0:
            for r in range(max(0, row-1), min(GRID_SIZE, row+2)):
                for c in range(max(0, col-1), min(GRID_SIZE, col+2)):
                    if not (r == row and c == col):
                        self.reveal(r, c)
        
        # 检查是否获胜
        self.check_win()
    
    def toggle_flag(self, row, col):
        """切换旗子标记"""
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return
            
        cell = self.grid[row][col]
        
        if not cell.is_revealed and self.flags_count > 0:
            cell.is_flagged = not cell.is_flagged
            self.flags_count += 1 if not cell.is_flagged else -1
    
    def check_win(self):
        """检查是否获胜"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        
        # 所有非地雷单元格都被揭示，游戏胜利
        self.game_won = True
        self.game_over = True
        return True
    
    def draw(self):
        """绘制游戏界面"""
        self.screen.fill(WHITE)
        
        # 绘制网格
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                
                # 计算单元格位置
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                # 绘制单元格背景
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if cell.is_revealed:
                    color = LIGHT_GRAY
                else:
                    color = GRAY
                    
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)  # 边框
                
                # 如果单元格被揭示，绘制内容
                if cell.is_revealed:
                    if cell.is_mine:
                        # 绘制地雷（红色圆圈）
                        center_x = x + CELL_SIZE // 2
                        center_y = y + CELL_SIZE // 2
                        radius = CELL_SIZE // 3
                        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius)
                    elif cell.adjacent_mines > 0:
                        # 绘制相邻地雷数量
                        colors = [BLUE, GREEN, RED, DARK_GRAY, DARK_GRAY, BLUE, BLACK, BLACK]
                        color = colors[cell.adjacent_mines-1] if cell.adjacent_mines <= len(colors) else BLACK
                        text = self.font.render(str(cell.adjacent_mines), True, color)
                        text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                        self.screen.blit(text, text_rect)
                elif cell.is_flagged:
                    # 绘制旗子（红色三角形）
                    center_x = x + CELL_SIZE // 2
                    center_y = y + CELL_SIZE // 2
                    points = [(center_x, center_y - 10), (center_x - 8, center_y + 5), (center_x + 8, center_y + 5)]
                    pygame.draw.polygon(self.screen, RED, points)
        
        # 更新时间
        if not self.game_over and not self.first_click:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        
        # 绘制UI信息区域
        ui_y = GRID_SIZE * CELL_SIZE
        pygame.draw.rect(self.screen, DARK_GRAY, (0, ui_y, SCREEN_WIDTH, 60))
        
        # 显示剩余地雷数
        mines_text = self.font.render(f"Mines: {self.flags_count}", True, WHITE)
        self.screen.blit(mines_text, (10, ui_y + 10))
        
        # 显示时间
        time_text = self.font.render(f"Time: {self.elapsed_time}s", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 100, ui_y + 10))
        
        # 显示游戏状态消息
        if self.game_over:
            if self.game_won:
                status_text = self.big_font.render("YOU WIN! Press R to restart", True, GREEN)
            else:
                status_text = self.big_font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, ui_y + 35))
            self.screen.blit(status_text, text_rect)
        else:
            status_text = self.font.render("Left-click to reveal, Right-click to flag", True, WHITE)
            self.screen.blit(status_text, (SCREEN_WIDTH // 2 - 150, ui_y + 10))
        
        pygame.display.flip()
    
    def reset_game(self):
        """重置游戏"""
        self.create_grid()
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.flags_count = MINES_COUNT
        self.start_time = 0
        self.elapsed_time = 0
    
    def run(self):
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        continue
                        
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    
                    # 检查点击是否在网格区域内
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if event.button == 1:  # 左键点击
                            self.reveal(row, col)
                        elif event.button == 3:  # 右键点击
                            self.toggle_flag(row, col)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 按R键重置游戏
                        self.reset_game()
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()