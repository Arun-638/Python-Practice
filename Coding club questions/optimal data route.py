# The hacker must navigate a grid of encrypted nodes.
# Each cell contains a cost to pass through.

# Given an m x n grid filled with non-negative integers, find the minimum cost path from the top-left corner to the bottom-right corner.

# You may only move right or down.
def optimaldataroute(grid,m,n):
    moves = [(0, 1), (1, 0)]
    dp = [[float('inf')] * n for i in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(m):
        for j in range(n):
            for move in moves:
                ni, nj = i + move[0], j + move[1]
                if 0 <= ni < m and 0 <= nj < n:
                    dp[ni][nj] = min(dp[ni][nj], dp[i][j] + grid[ni][nj])
    return dp[m-1][n-1]
m, n = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(m)]
print(optimaldataroute(grid, m, n))
