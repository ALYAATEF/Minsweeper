import pygame
import sys
import time
from collections import deque
from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 10
WIDTH = 10
MINES = 10
#dp moves on cells
dx =[1,1,-1,-1,0,0,1,-1]
dy =[1,-1,1,-1,1,-1,0,0]
# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2) 
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("Sprites/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
empty = pygame.image.load("Sprites/empty.png")
empty = pygame.transform.scale(empty, (cell_size, cell_size))
grid = pygame.image.load("Sprites/Grid.png")
grid = pygame.transform.scale(grid, (cell_size, cell_size))
grid1 = pygame.image.load("Sprites/grid1.png")
grid1 = pygame.transform.scale(grid1, (cell_size, cell_size))
grid2 = pygame.image.load("Sprites/grid2.png")
grid2 = pygame.transform.scale(grid2, (cell_size, cell_size))
grid3 = pygame.image.load("Sprites/grid3.png")
grid3 = pygame.transform.scale(grid3, (cell_size, cell_size))
grid4 = pygame.image.load("Sprites/grid4.png")
grid4 = pygame.transform.scale(grid4, (cell_size, cell_size))
grid5 = pygame.image.load("Sprites/grid5.png")
grid5 = pygame.transform.scale(grid5, (cell_size, cell_size))
grid6 = pygame.image.load("Sprites/grid6.png")
grid6 = pygame.transform.scale(grid6, (cell_size, cell_size))
grid7 = pygame.image.load("Sprites/grid7.png")
grid7 = pygame.transform.scale(grid7, (cell_size, cell_size))
grid8 = pygame.image.load("Sprites/grid8.png")
grid8 = pygame.transform.scale(grid8, (cell_size, cell_size))
mine = pygame.image.load("Sprites/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))
red_mine = pygame.image.load("Sprites/mineClicked.png")
red_mine = pygame.transform.scale(red_mine, (cell_size, cell_size))
Won =  pygame.image.load("Sprites/Won.png")
Won = pygame.transform.scale(Won, (cell_size, cell_size))
Lost =  pygame.image.load("Sprites/Lost.png")
Lost = pygame.transform.scale(Lost, (cell_size, cell_size))
start =  pygame.image.load("Sprites/start.png")
start = pygame.transform.scale(start, (cell_size, cell_size))

# Detonated mine
mine_detonated = None

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False
first_move=False
# Show instructions initially
instructions = True

# Autoplay game
autoplay = False
autoplaySpeed = 0.3
makeAiMove = False

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    
    # Add images for numbers
    number_images = {
        0: empty,
        1: grid1,
        2: grid2,
        3: grid3,
        4: grid4,
        5: grid5,
        6: grid6,
        7: grid7,
        8: grid8
    }


    # Draw board
    screen.fill(GRAY)  

    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            screen.blit(grid, rect)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                if (i,j) == mine_detonated:
                    screen.blit(red_mine, rect)
                else:
                    screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            if (i, j) in revealed:
                nearby_mines = game.nearby_mines((i, j))
                if nearby_mines in number_images:  # Check if the number of nearby mines is a valid key
                    screen.blit(number_images[nearby_mines], rect)
            row.append(rect)
        cells.append(row)

    # Autoplay Button
    autoplayBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Autoplay" if not autoplay else "Stop"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = autoplayBtn.center
    pygame.draw.rect(screen, WHITE, autoplayBtn)
    screen.blit(buttonText, buttonRect)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 70,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    if not autoplay:
        pygame.draw.rect(screen, WHITE, aiButton)
        screen.blit(buttonText, buttonRect)

    

    # State Faces
    faceButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 140,
        (width / 3) - BOARD_PADDING * 2, 50)
    screen.blit(start, faceButton)
    if lost:
        screen.blit(Lost, faceButton)
    elif game.mines == flags:
        screen.blit(Won, faceButton)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost and not autoplay:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If Autoplay button clicked, toggle autoplay
        if autoplayBtn.collidepoint(mouse):
            if not lost:
                autoplay = not autoplay
            else:
                autoplay = False
            time.sleep(0.2)
            continue

        # If AI button clicked, make an AI move
        elif aiButton.collidepoint(mouse) and not lost:
            makeAiMove = True
            time.sleep(0.2)

        # Reset game state
        elif faceButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            first_move=False
            mine_detonated = None
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # If autoplay, make move with AI
    if autoplay or makeAiMove:
        if makeAiMove:
            makeAiMove = False
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                print("No moves left to make.")
                autoplay = False
            else:
                print("No known safe moves, AI making random move.")
        else:
            print("AI making safe move.")

        # Add delay for autoplay
        if autoplay:
            time.sleep(autoplaySpeed)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
            mine_detonated = move
            autoplay = False
        else:
            if(not first_move):
                first_move =True
                a ,b = move
                game.random_mines(height=HEIGHT, width=WIDTH, mines=MINES,x_firstmov= a,y_firstmove=b)
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
            if(nearby == 0):
                bfs =deque()
                bfs.append(move)
                vis = dict()
                vis[move]=False
                while (len(bfs) != 0):
                    move = bfs.pop()
                    x,y = move
                    print(move)
                    if(move in vis and  vis[move] == True):
                        continue
                    vis[move]=True
                    for i in range(0,8):
                        if(x+dx[i]>=0 and x+dx[i] < HEIGHT and y+dy[i]>=0 and y+dy[i] < WIDTH ):
                            move = (x+dx[i],y+dy[i])
                            nearby = game.nearby_mines(move)
                            revealed.add(move)
                            ai.add_knowledge(move, nearby)
                            print(nearby)
                            if(nearby==0):
                                bfs.append(move)
                bfs.clear()

    pygame.display.flip()
