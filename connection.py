
class Connection:

    def __init__(self, V, neighbor_list):
        self.V = V
        self.adj = neighbor_list

    def addedge(self, u, v):
        self.adj[u].append(v)  # Add w to v’s list.
        self.adj[v].append(u)  # Add w to v’s list.

    def dfs(self, v, visited):

        # Mark the current node as
        # visited and print it
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        i = 0
        while i != len(self.adj[v]):
            if (not visited[self.adj[v][i]]):
                self.dfs(self.adj[v][i], visited)
            i += 1

    def is_connected(self):
        visited = [False] * self.V

        # Find all reachable vertices
        # from first vertex
        self.dfs(1, visited)

        # If set of reachable vertices
        # includes all, return true.
        for i in range(2, self.V):
            if not visited[i]:
                return False, visited

        return True, visited

    def is_bridge(self, u, v):
        # print(self.adj[u], self.adj[v])
        # Remove edge from undirected graph
        indU = self.adj[v].index(u)
        # print(indU)
        indV = self.adj[u].index(v)
        # print(indV)
        del self.adj[u][indV]
        del self.adj[v][indU]
        # print(self.adj[u], self.adj[v])
        res, visited = self.is_connected()

        self.addedge(u, v)

        return (res == False), visited
