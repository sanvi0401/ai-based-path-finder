import pygame
import heapq

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
WHITE, BLACK, RED, GREEN, BLUE, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive A* Pathfinding")


start, goal = None, None
obstacles = set()
path = []


def astar(start, goal):
    def heuristic(a, b):  
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Neighbor cells
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in obstacles:
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
                    came_from[neighbor] = current
    return []


def draw_grid():
    screen.fill(WHITE)

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, (obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    
    for node in path:
        pygame.draw.rect(screen, BLUE, (node[0] * CELL_SIZE, node[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    
    if start:
        pygame.draw.rect(screen, RED, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if goal:
        pygame.draw.rect(screen, GREEN, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()


def get_cell_from_mouse(pos):
    return pos[0] // CELL_SIZE, pos[1] // CELL_SIZE

running = True
while running:
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_cell_from_mouse(event.pos)

            if event.button == 1:  
                if start is None:
                    start = cell
                elif goal is None and cell != start:
                    goal = cell

            elif event.button == 3:  
                if cell != start and cell != goal:
                    if cell in obstacles:
                        obstacles.remove(cell)
                    else:
                        obstacles.add(cell)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and goal: 
                path = astar(start, goal)

pygame.quit()
