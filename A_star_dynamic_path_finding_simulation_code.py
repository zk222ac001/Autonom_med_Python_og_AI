# Dynamic A* Pathfinding with Non-blocking Movement
# pip install pygame

import pygame, heapq, random

GRID_SIZE = 20
CELL_SIZE = 30
FPS = 60
MOVE_DELAY = 1000  # one second between moves

# Colors
WHITE, BLACK = (240, 240, 240), (50, 50, 50)
GREEN, RED, BLUE, GREY, YELLOW = (0,255,0), (255,80,80), (80,80,255), (180,180,180), (255,255,0)

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE))
pygame.display.set_caption("Fast Dynamic A* with Smooth Updates")
clock = pygame.time.Clock()

grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
start, goal = (0,0), (GRID_SIZE-1, GRID_SIZE-1)
path = []

# ---------- A* Algorithm ----------
def heuristic(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
def astar(grid, start, goal):
    neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
    open_set = []
    heapq.heappush(open_set,(0+heuristic(start,goal),0,start))
    came_from, g_score = {}, {start:0}
    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path=[]
            while current in came_from:
                path.append(current)
                current=came_from[current]
            return path[::-1]
        for dx,dy in neighbors:
            nx,ny=current[0]+dx,current[1]+dy
            if 0<=nx<GRID_SIZE and 0<=ny<GRID_SIZE and grid[nx][ny]==0:
                new_cost=cost+1
                if (nx,ny) not in g_score or new_cost<g_score[(nx,ny)]:
                    g_score[(nx,ny)]=new_cost
                    f=new_cost+heuristic((nx,ny),goal)
                    heapq.heappush(open_set,(f,new_cost,(nx,ny)))
                    came_from[(nx,ny)]=current
    return None

# ---------- Draw ----------
def draw_grid(robot=None):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            color = WHITE
            if grid[i][j] == 1: color = BLACK
            elif (i,j) == start: color = BLUE
            elif (i,j) == goal: color = RED
            elif path and (i,j) in path: color = GREEN
            pygame.draw.rect(screen, color, rect)
    if robot:
        rx, ry = robot
        pygame.draw.circle(screen, YELLOW, (ry*CELL_SIZE+CELL_SIZE//2, rx*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3)

# ---------- Main Loop ----------
def main():
    global path
    robot_pos = start
    path = astar(grid, start, goal)
    step = 0
    running = True
    last_move = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()
        screen.fill(GREY)
        draw_grid(robot_pos)
        pygame.display.flip()
        clock.tick(FPS)

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = astar(grid, robot_pos, goal)
                    step = 0
                if event.key == pygame.K_r:
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            grid[i][j]=0
                    robot_pos=start
                    path=astar(grid,start,goal)
                    step=0
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Mouse for obstacles (instant response)
        if pygame.mouse.get_pressed()[0]:
            mx,my = pygame.mouse.get_pos()
            gx,gy = my//CELL_SIZE, mx//CELL_SIZE
            if (gx,gy) not in [start,goal]:
                grid[gx][gy]=1
        if pygame.mouse.get_pressed()[2]:
            mx,my = pygame.mouse.get_pos()
            gx,gy = my//CELL_SIZE, mx//CELL_SIZE
            if (gx,gy) not in [start,goal]:
                grid[gx][gy]=0

        # Move robot smoothly without blocking
        if path and step < len(path) and now - last_move > MOVE_DELAY:
            next_pos = path[step]
            if grid[next_pos[0]][next_pos[1]] == 1:
                print("⚠️ Obstacle detected! Recalculating...")
                path = astar(grid, robot_pos, goal)
                step = 0
            else:
                robot_pos = next_pos
                step += 1
            last_move = now

    pygame.quit()

if __name__ == "__main__":
    main()
