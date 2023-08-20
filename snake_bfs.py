import pygame
#import time
import random
from settings import *
 
pygame.init() ## Khởi tạo module


def initial_game():         ## Khởi tạo hai tập hợp mảng đại diện cho đường đi thực sự của rắn và đường đi thử nghiệm của nó.
    global board, snake, snake_size, tmpboard, tmpsnake, tmpsnake_size, food,best_move
    board = [0] * FIELD_SIZE #[0,0,0,……]
    snake = [0] * (FIELD_SIZE+1)
    snake[HEAD] = 1*WIDTH+1
    snake_size = 1

    tmpboard = [0] * FIELD_SIZE
    tmpsnake = [0] * (FIELD_SIZE+1)
    tmpsnake[HEAD] = 1*WIDTH+1
    tmpsnake_size = 1

    food = 4 * WIDTH + 7
    best_move = ERR

dis = pygame.display.set_mode((SNAKE_BLOCK*WIDTH, SNAKE_BLOCK*HEIGHT))
pygame.display.set_caption('Snake BFS')
 
clock = pygame.time.Clock()



def Your_score(score):      ## Hiển thị điểm
    value = SCORE_FONT.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])   

def draw():                 ## Hàm tô màu các bộ phận của con rắn (bao gồm màu xanh đỏ trắng tương ứng với các bộ phận head, body, tail) và quả táo (green)
    global SNAKE_BLOCK,snake,snake_size,food
    p = snake[HEAD]
    count=0
    for idx in snake[:snake_size]:
        pygame.draw.rect(dis, blue, [SNAKE_BLOCK*(idx%WIDTH), SNAKE_BLOCK*(idx//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
        if count>0 : pygame.draw.rect(dis, red, [SNAKE_BLOCK*(idx%WIDTH), SNAKE_BLOCK*(idx//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
        count+=1
    
    pygame.draw.rect(dis, white, [SNAKE_BLOCK*(idx%WIDTH), SNAKE_BLOCK*(idx//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
    pygame.draw.rect(dis, green, [SNAKE_BLOCK*(food%WIDTH), SNAKE_BLOCK*(food//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
 
def message(msg, color):    ## Hiển thị thông báo
    mesg = FONT_STYLE.render(msg, True, color)
    dis.blit(mesg, [WIDTH*SNAKE_BLOCK / 6, HEIGHT*SNAKE_BLOCK / 3])


def new_food():             ## Tạo thức ăn mới
    global food, snake_size, dis
    cell_free = False
    while not cell_free:
        w = random.randint(0, WIDTH-1)
        h = random.randint(0, HEIGHT-1)
        food = WIDTH*h + w
        cell_free = is_cell_free(food, snake_size, snake)
 
def is_move_possible(idx, move):        ## Hàm kiểm tra các hướng đi của con rắn (UP, LEFT, RIGHT, DOWN) 
    flag = False
    if move == LEFT:
        flag = True if idx%WIDTH > 0 else False
    elif move == RIGHT:
        flag = True if idx%WIDTH < (WIDTH-1) else False
    elif move == UP:
        flag = True if idx > (WIDTH-1) else False
    elif move == DOWN:
        flag = True if idx < (FIELD_SIZE-WIDTH) else False
    return flag
    
def is_cell_free(idx, psize, psnake):   ## Hàm kiểm tra ô đó có khả dụng hay không
    return not (idx in psnake[:psize]) 
    
def board_BFS(pfood, psnake, pboard):   ## Thuật toán Breadth First Search
    queue = []
    queue.append(pfood)
    inqueue = [0] * FIELD_SIZE
    found = False
    while len(queue)!=0: 
        idx = int(queue.pop(0))
        if inqueue[idx] == 1: 
            continue
        inqueue[idx] = 1
        for i in range(4):
            if is_move_possible(idx, MOV[i]):
                if idx + MOV[i] == psnake[HEAD]:
                    found = True
                if pboard[idx+MOV[i]] < SNAKE: 
                    if pboard[idx+MOV[i]] > pboard[idx]+1:
                        pboard[idx+MOV[i]] = pboard[idx] + 1
                    if inqueue[idx+MOV[i]] == 0:
                        queue.append(idx+MOV[i])
    return found
    
def is_tail_reachable():                
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD 
    tmpboard[food] = SNAKE 
    result = board_BFS(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard) 
    for i in range(4): 
        if is_move_possible(tmpsnake[HEAD], MOV[i]) and tmpsnake[HEAD]+MOV[i]==tmpsnake[tmpsnake_size-1] and tmpsnake_size>3:
            result = False
    return result

def make_move(move):        ## hàm di chuyển và kiểm tra xem nếu con ăn đã ăn táo thì tăng kích thước và tạo thức ăn mới
    global snake, board, snake_size, score  
    shift_array(snake, snake_size)
    snake[HEAD] += move
    p = snake[HEAD]
    
    
    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE 
        snake_size += 1
        if snake_size < FIELD_SIZE: new_food()
    else: 
        board[snake[HEAD]] = SNAKE 
        board[snake[snake_size]] = UNDEFINED 
    
def board_reset(psnake, psize, pboard):         ## kiểm tra trang thái của ô đó là thức ăn hoặc con rắn hoặc là ô trống
    for i in range(FIELD_SIZE):
        if i == food:
            pboard[i] = FOOD
        elif is_cell_free(i, psize, psnake): 
            pboard[i] = UNDEFINED
        else:
            pboard[i] = SNAKE
            
def find_safe_way():            ## Hàm tìm đường đi an toàn nhất
    global snake, board
    safe_move = ERR
    virtual_shortest_move() 
    if is_tail_reachable(): 
        return choose_shortest_safe_move(snake, board)
    safe_move = follow_tail()
    return safe_move
    
def shift_array(arr, size): ## Hàm chuyển mảng
    for i in range(size, 0, -1):
        arr[i] = arr[i-1]
        
def any_possible_move():        ## Hàm tìm ra đường đi khả thi
    global food , snake, snake_size, board
    best_move = ERR
    board_reset(snake, snake_size, board)
    board_BFS(food, snake, board)
    min = SNAKE

    for i in range(4):
        if is_move_possible(snake[HEAD], MOV[i]) and board[snake[HEAD]+MOV[i]]<min:
            min = board[snake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move
    
def follow_tail():       ## Hoàn đổi trạng thái của ô chứa thức ăn với trạng thái của ô chứa đuôi rắn và duyệt BFS
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    board_reset(tmpsnake, tmpsnake_size, tmpboard) 
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD
    tmpboard[food] = SNAKE
    board_BFS(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard) 
    tmpboard[tmpsnake[tmpsnake_size-1]] = SNAKE 
    return choose_longest_safe_move(tmpsnake, tmpboard) 
    
def virtual_shortest_move():        ## hàm đưa con rắn tới vị trí thức ăn mà BFS tìm ra. Tại vị trí đó, ta kiểm tra xem có tồn tại đường đi từ đầu con rắn tới đuôi của nó hay không
    global snake, board, snake_size, tmpsnake, tmpboard, tmpsnake_size, food
    tmpsnake_size = snake_size
    tmpsnake = snake[:] 
    tmpboard = board[:] 
    board_reset(tmpsnake, tmpsnake_size, tmpboard)
    
    food_eated = False
    while not food_eated:
        board_BFS(food, tmpsnake, tmpboard)    
        move = choose_shortest_safe_move(tmpsnake, tmpboard)
        shift_array(tmpsnake, tmpsnake_size)
        tmpsnake[HEAD] += move 
        if tmpsnake[HEAD] == food:
            tmpsnake_size += 1
            board_reset(tmpsnake, tmpsnake_size, tmpboard)
            tmpboard[food] = SNAKE
            food_eated = True
        else:
            tmpboard[tmpsnake[HEAD]] = SNAKE
            tmpboard[tmpsnake[tmpsnake_size]] = UNDEFINED


## Sau khi có kết quả từ thuật toán BFS ta có thể tìm được đường đi ngắn nhất và dài nhất. 
## Khi con rắn đuổi theo thức ăn, nó cần đường đi ngắn nhất, khi nó đuổi theo cái đuôi của chính nó,
## nó nên chọn đường đi dài nhất (trong số các đường đi ngắn nhất) để có thêm không gian để có thể ở lại game lâu hơn.
def choose_shortest_safe_move(psnake, pboard):      
    best_move = ERR
    min = SNAKE
    for i in range(4):
        if is_move_possible(psnake[HEAD], MOV[i]) and pboard[psnake[HEAD]+MOV[i]]<min:
            min = pboard[psnake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move
    
def choose_longest_safe_move(psnake, pboard):   
    best_move = ERR
    max = -1
    for i in range(4):
        if is_move_possible(psnake[HEAD], MOV[i]) and pboard[psnake[HEAD]+MOV[i]]<UNDEFINED and pboard[psnake[HEAD]+MOV[i]]>max:
            max = pboard[psnake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move

## Vòng lặp con rắn sẽ di chuyển cho đến khi game over
def gameLoop():
    game_over = False
    game_close = False
 
    initial_game()
 
    while not game_over:
        
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(snake_size - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:       
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:      ## Nhấn q hoặc ESC trên bàn phím để thoát
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:                                      ## Nhấn c để gam bắt đầu lại
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
        
        board_reset(snake, snake_size, board)
        
        if board_BFS(food, snake, board):   ## nếu tồn tại đường đi
            best_move  = find_safe_way()    ## tìm đường đi an toàn tốt nhất
        else:
            best_move = follow_tail()       ## nếu không thử đuổi theo đuôi
        if best_move == ERR:                ## nếu không thể thử đuổi theo đuôi 
            best_move = any_possible_move() ## đi ngẫu nhiên một ô hợp lệ
            
        if best_move != ERR: 
            make_move(best_move)
        else:
            game_close = True
        
        dis.fill(black)
        
        draw()
        Your_score(snake_size - 1)
 
        pygame.display.update()
 
        clock.tick(SNAKE_SPEED)
 
    pygame.quit()
    quit()
 
 
gameLoop()
