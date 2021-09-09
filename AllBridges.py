# Python3 program to check if removing
# an edge disconnects a graph or not.

# Graph class represents a directed graph
# using adjacency list representation
class Graph:

    def __init__(self, V, lst):
        self.V = V
        self.adj = lst
        self.visited_nodes = None

    def addEdge(self, u, v):
        self.adj[u].append(v)  # Add w to v’s list.
        self.adj[v].append(u)  # Add w to v’s list.
        print(self.adj)

    def DFS(self, v, visited):

        # Mark the current node as
        # visited and print it
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        i = 0
        while i != len(self.adj[v]):
            if (not visited[self.adj[v][i]]):
                self.DFS(self.adj[v][i], visited)
            i += 1

    # Returns true if given graph is
    # connected, else false
    def isConnected(self):
        visited = [False] * self.V

        # Find all reachable vertices
        # from first vertex
        self.DFS(0, visited)
        print(visited[38], visited[84])
        self.visited_nodes = visited
        # If set of reachable vertices
        # includes all, return true.
        for i in range(1, self.V):
            if (visited[i] == False):
                return False
        return True

    # This function assumes that edge
    # (u, v) exists in graph or not,
    def isBridge(self, u, v):

        # Remove edge from undirected graph
        indU = self.adj[v].index(u)
        indV = self.adj[u].index(v)
        del self.adj[u][indV]
        del self.adj[v][indU]
        res = self.isConnected()
        # Adding the edge back
        self.addEdge(u, v)

        # Return true if graph becomes
        # disconnected after removing
        # the edge.
        return (res == False)

    # Driver code


if __name__ == '__main__':

    # Create a graph given in the
    # above diagram
    lst = [[1, 2, 42], [0, 2, 58], [0, 1], [4, 5], [3, 5, 51, 56], [3, 4, 84], [7, 8, 48, 54], [6, 8], [6, 7, 47, 78],
           [10, 11], [9, 11], [9, 10], [13, 14], [12, 14, 26], [12, 13, 25, 26], [16, 17, 21], [15, 17, 27, 59],
           [15, 16, 76], [19, 20], [18, 20], [18, 19], [15, 22], [21, 23, 79], [22, 24], [23, 25], [14, 24],
           [13, 14, 71], [16, 28], [27, 29], [28, 30, 37], [29, 31], [30, 32], [31, 33], [32, 34, 76], [33, 35, 36],
           [34, 36], [34, 35], [29, 38, 56], [37, 39, 73, 84], [38, 40], [39, 41], [40, 42, 62], [0, 41, 46, 53],
           [44, 45, 89], [43, 45, 86], [43, 44, 75], [42, 47, 76], [8, 46], [6, 49], [48, 50, 92], [49, 51], [4, 50],
           [53, 54], [42, 52, 69], [6, 52], [56, 57, 64, 98], [4, 37, 55], [55, 58, 81], [1, 57], [16, 60], [59, 61],
           [60, 62], [41, 61], [64, 65], [55, 63, 95], [63, 66, 87, 98], [65, 67], [66, 68], [67, 69], [53, 68],
           [71, 72], [26, 70], [70, 73], [38, 72, 87], [75, 76], [45, 74], [17, 33, 46, 74], [78, 79], [8, 77, 84],
           [22, 77], [81, 82, 88], [57, 80], [80, 83], [82, 84, 88], [5, 38, 78, 83], [86, 87], [44, 85], [65, 73, 85],
           [80, 83], [43, 90, 94], [89, 91], [90, 92], [49, 91], [94, 95], [89, 93], [64, 93], [97, 98],
           [96, 98], [55, 65, 96, 97]]
    g = Graph(99, lst)


    if g.isBridge(84, 38):
        print("Yes")
        print(g.visited_nodes[38], g.visited_nodes[84])
    else:
        print("No")

    # This code is contributed by PranchalK
