def finalTrace(grid,m,n):
    moves = [(0, 1), (1, 0)]
    queue = [grid[0][0]]
    visited = []
    if grid[0][0] == 
    while queue:
        item = queue.pop(0)
        visited.append(item)
        
m, n = map(int, input().split())
grid = [list(map(int, input().split())) for i in range(m)]
print(finalTrace(grid, m, n))
