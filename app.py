import streamlit as st
import pygame
import random

# Pygame 초기화
pygame.init()

# 게임 화면 크기 설정
screen_width = 300
screen_height = 600
block_size = 30

# 색상 정의
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 블록 모양 정의
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]]
]

# 블록 클래스 정의
class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([red, green, blue])

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, self.color, (self.x + j * block_size, self.y + i * block_size, block_size, block_size))

# 게임 오버 함수
def check_game_over(board):
    for i in range(len(board[0])):
        if board[0][i] != 0:
            return True
    return False

# 메인 게임 함수
def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    board = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]

    current_block = Block(screen_width // 2 // block_size * block_size, 0, random.choice(shapes))

    running = True
    while running:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_block.x -= block_size
        if keys[pygame.K_RIGHT]:
            current_block.x += block_size
        if keys[pygame.K_DOWN]:
            current_block.y += block_size

        current_block.y += block_size

        if current_block.y >= screen_height - block_size * len(current_block.shape):
            for i, row in enumerate(current_block.shape):
                for j, val in enumerate(row):
                    if val:
                        board[(current_block.y // block_size) + i][(current_block.x // block_size) + j] = current_block.color
            current_block = Block(screen_width // 2 // block_size * block_size, 0, random.choice(shapes))

        current_block.draw(screen)

        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, val, (j * block_size, i * block_size, block_size, block_size))

        if check_game_over(board):
            running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

# 스트림릿 앱 설정
st.title('Tetris Game')
if st.button('Start Game'):
    main()
