#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏
操作：方向键控制移动，ESC 退出，空格键暂停/继续
"""

import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (128, 128, 128)

# 游戏设置
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 4  # 速度调慢（数值越小越慢）

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        """重置蛇的状态"""
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0

    def get_head_position(self):
        """获取蛇头位置"""
        return self.positions[0]

    def turn(self, direction):
        """转向（不能直接掉头）"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def move(self):
        """移动蛇"""
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)

        # 检查是否撞到自己
        if new_head in self.positions[2:]:
            return False  # 游戏结束

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def grow(self):
        """蛇变长"""
        self.length += 1
        self.score += 10

    def draw(self, surface):
        """绘制蛇"""
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:
                # 蛇头用深绿色
                pygame.draw.rect(surface, DARK_GREEN, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)
            else:
                # 蛇身用绿色
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """随机生成食物位置（避开蛇身）"""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1),
                           random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        """绘制食物"""
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('🐍 贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.snake = Snake()
        self.food = Food()
        self.paused = False
        self.game_over = False

    def handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart()
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_RETURN and self.game_over:
                    self.restart()
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(RIGHT)
        return True

    def update(self):
        """更新游戏状态"""
        if self.paused or self.game_over:
            return

        # 移动蛇
        if not self.snake.move():
            self.game_over = True
            return

        # 检查是否吃到食物
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.randomize_position(self.snake.positions)

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)

        # 绘制网格（可选）
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

        # 绘制蛇和食物
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # 绘制分数
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 暂停提示
        if self.paused:
            pause_text = self.big_font.render('PAUSED', True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)

            hint_text = self.font.render('Press SPACE to continue', True, GRAY)
            hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(hint_text, hint_rect)

        # 游戏结束提示
        if self.game_over:
            over_text = self.big_font.render('GAME OVER', True, RED)
            text_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(over_text, text_rect)

            score_text = self.font.render(f'Final Score: {self.snake.score}', True, WHITE)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)

            hint_text = self.font.render('Press SPACE or ENTER to restart', True, GRAY)
            hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()

    def restart(self):
        """重新开始游戏"""
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.game_over = False
        self.paused = False

    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    print("🐍 贪吃蛇游戏启动中...")
    print("操作说明：")
    print("  ↑↓←→  方向键控制移动")
    print("  空格   暂停/继续/重新开始")
    print("  ESC    退出游戏")
    print("-" * 30)

    game = Game()
    game.run()
