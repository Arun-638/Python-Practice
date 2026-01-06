class Solution(object):
    def nearestExit(self, maze, entrance):
        """
        :type maze: List[List[str]]
        :type entrance: List[int]
        :rtype: int
        """
        dr = [-1,1,0,0]
        dc = [0,0,1,-1]
        rq = []
        cq = []
        front=0
        visited = []
        m = len(maze)
        n = len(maze[0])
        nodes_in_next_layer = 0
        nodes_left_in_layer = 1
        for i in range(m):
            visited.append([])
            for j in range(n):
                visited[i].append(0)
        count = 0
        reached_end = False
        rq.append(entrance[0])
        cq.append(entrance[1])
        visited[entrance[0]][entrance[1]] = 1
        while len(rq)>0:
            r = rq.pop(front)
            c = cq.pop(front)
            if [r, c] != entrance and maze[r][c] == '.' and ((r == 0 or c == 0) or (r == m-1 or c == n-1)):
                reached_end = True
                break
            for i in range(4):
                rr = r+dr[i]
                cc = c+dc[i]
                if rr<0 or cc<0 :
                    continue
                if rr>=m or cc >= n:
                    continue
                if visited[rr][cc] == 1 or maze[rr][cc] == "+":
                    continue
                rq.append(rr)
                cq.append(cc)
                visited[rr][cc] = 1
                nodes_in_next_layer+=1
            nodes_left_in_layer-=1
            if nodes_left_in_layer == 0:
                nodes_left_in_layer = nodes_in_next_layer
                nodes_in_next_layer = 0
                count+=1
        if reached_end:
            return count
        return -1    