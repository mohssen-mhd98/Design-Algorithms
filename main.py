from connection import Connection
import timeit
import sys
import threading



def main():
    inp = input("Enter your command:\n")
    time = {}

    start = timeit.default_timer()
    sort_func = inp.split()[1]
    path = inp.split()[2]
    p = path
    path = "./" + path
    file = open(path)
    text_input = file.read()
    file.close()
    txt_list = []
    t = text_input.split("\n")
    for row in t:
        txt_list.append(row.split())

    vertex_pair = []
    for element in txt_list:
        vertex_pair.append([int(element[0]), int(element[1])])

    length = vertex_pair[len(vertex_pair) - 1][0] + 1
    neighbor_list = [[] for _ in range(length)]

    for edge in vertex_pair:
        neighbor_list[edge[0]].append(edge[1])
    # print(neighbor_list[1], neighbor_list[44])

    stop = timeit.default_timer()
    time.update({"Read file and create neighbor-list time": start - stop})

    conn = Connection(length, neighbor_list)
    start = timeit.default_timer()
    cij_dict = initially_score_calculator(neighbor_list)
    stop = timeit.default_timer()
    time.update({"Calculating initial scores time": start - stop})
    sys.setrecursionlimit(10 ** 9)
    partitioned_graph = graph_union(cij_dict, neighbor_list, conn, sort_func)
    f = open("result-" + p, "w")
    for i in range(1, len(partitioned_graph)):
        if partitioned_graph[i]:
            f.write(str(i) + "\t" + "A\n")
        else:
            f.write(str(i) + "\t" + "B\n")
    f.close()

    print(time)


def initially_score_calculator(neighbor_list):
    c_ij = {}
    for i_vertex in range(1, len(neighbor_list)):
        for j_vertex in neighbor_list[i_vertex]:
            if ([i_vertex, j_vertex] not in list(c_ij.keys())) and \
                    ([j_vertex, i_vertex] not in list(c_ij.keys())):
                k_i = len(neighbor_list[i_vertex])
                k_j = len(neighbor_list[j_vertex])
                min_k = min(k_i - 1, k_j - 1)
                if min_k == 0:
                    score = float('inf')
                else:
                    score = (zij(i_vertex, j_vertex, neighbor_list) + 1) / min(k_i - 1, k_j - 1)
                c_ij.update({(i_vertex, j_vertex): score})
                # print("{}-{}: ".format(i_vertex, j_vertex), score)
    return c_ij


# def zij(neighbor_list):
#     z_dict = {}
#     for i_vertex in range(1, len(neighbor_list)):
#         for j_vertex in neighbor_list[i_vertex]:
#             if (str(i_vertex) + "-" + str(j_vertex) not in list(z_dict.keys())) and \
#                     (str(j_vertex) + "-" + str(i_vertex) not in list(z_dict.keys())):
#                 tmp_list = [value for value in neighbor_list[i_vertex] if value in neighbor_list[j_vertex]]
#                 z_dict.update({str(i_vertex) + "-" + str(j_vertex): len(tmp_list)})
#     return z_dict


def zij(i_vertex, j_vertex, neighbor_list):
    z_dict = {}
    # if (str(i_vertex) + "-" + str(j_vertex) not in list(z_dict.keys())) and \
    #         (str(j_vertex) + "-" + str(i_vertex) not in list(z_dict.keys())):
    tmp_list = [value for value in neighbor_list[i_vertex] if value in neighbor_list[j_vertex]]
    # z_dict.update({str(i_vertex) + "-" + str(j_vertex): len(tmp_list)})

    return len(tmp_list)


def graph_union(cij_dict, neighbor_list, conn, sort_func):
    if sort_func == "Bubble":
        sorted_values = bubbleSort(list(cij_dict.values()))
    elif sort_func == "Quick ":
        lst = list(cij_dict.values())
        sorted_values = quick_sort(lst, 0, len(lst) - 1)
    elif sort_func == "Merge":
        sorted_values = mergeSort(list(cij_dict.values()))
    elif sort_func == "Insertion":
        sorted_values = insertion_sort(list(cij_dict.values()))

    key_min = get_key(sorted_values[0], cij_dict)
    cij_dict.pop(key_min)
    i_vertex, j_vertex = key_min[0], key_min[1]
    f, partitioned_graph = conn.is_bridge(i_vertex, j_vertex)
    print(key_min)
    if f:
        if j_vertex in neighbor_list[i_vertex]:
            neighbor_list[i_vertex].remove(j_vertex)
        if i_vertex in neighbor_list[j_vertex]:
            neighbor_list[j_vertex].remove(i_vertex)
        partitioned_graph[j_vertex] = False
        return partitioned_graph

    if j_vertex in neighbor_list[i_vertex]:
        neighbor_list[i_vertex].remove(j_vertex)
    if i_vertex in neighbor_list[j_vertex]:
        neighbor_list[j_vertex].remove(i_vertex)

    for vertex in neighbor_list:
        if (i_vertex in vertex) or (j_vertex in vertex):
            pass
    for key in list(cij_dict.keys()):
        if (i_vertex in key) or (j_vertex in key):
            k_i = len(neighbor_list[key[0]])
            k_j = len(neighbor_list[key[1]])
            min_k = min(k_i - 1, k_j - 1)
            if min_k == 0:
                score = float('inf')
            else:
                score = (zij(i_vertex=key[0], j_vertex=key[1], neighbor_list=neighbor_list) + 1) / min(k_i - 1, k_j - 1)
            cij_dict[key] = score
    graph_union(cij_dict, neighbor_list, conn, sort_func)


def get_key(val, dic):
    for key, value in dic.items():
        if val == value:
            return key

    return "key doesn't exist"


def bubbleSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n - 1):
        # range(n) also work but outer loop will repeat one time more than needed.

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(array):
    for index in range(1, len(array)):
        currentValue = array[index]
        currentPosition = index

        while currentPosition > 0 and array[currentPosition - 1] > currentValue:
            array[currentPosition] = array[currentPosition - 1]
            currentPosition = currentPosition - 1

        array[currentPosition] = currentValue
    return array


def partition(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and array[high] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low] <= pivot:
            low = low + 1

        if low <= high:
            array[low], array[high] = array[high], array[low]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start], array[high] = array[high], array[start]

    return high


def quick_sort(array, start, end):
    if start >= end:
        return array

    p = partition(array, start, end)
    quick_sort(array, start, p - 1)
    quick_sort(array, p + 1, end)


def dfs(v, visited, neighbor_list, i, j):
    if v == i:
        return "A"
    elif v == j:
        return "B"
    # Mark the current node as
    # visited and print it
    visited[v] = True

    # Recur for all the vertices
    # adjacent to this vertex
    i = 0
    while i != len(neighbor_list[v]):
        if (not visited[neighbor_list[v][i]]):
            dfs(neighbor_list[v][i], visited)
        i += 1


# Python program for implementation of MergeSort
def mergeSort(arr):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        mergeSort(L)

        # Sorting the second half
        mergeSort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 9)
    threading.Thread(target=main).start()
