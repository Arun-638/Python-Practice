vertices = int(input("Enter the number of vertices: "))
visited = [0] * vertices
adj = {}
def read_graph(adj,vertices):
    for i in range(vertices):
        adj[i] = []
        edges = int(input("Enter the number of edges: "))
        for j in range(edges):
            element = int(input("Enter the vertice: "))
            adj[i].append(element)
def dfs(adj,vertices):
    for i in range(vertices):
        if visited[i] == 0:
            stack = []
            stack.append(i)
            visited[i] = 1
            while(len(stack) != 0):
                item = stack.pop()
                print(item,end=' ')
                for k in adj[item]:
                    if visited[k] == 0:
                        stack.append(k)
                        visited[k] = 1
read_graph(adj,vertices)
print(adj)
dfs(adj,vertices)