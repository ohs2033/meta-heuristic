#-*- encoding: utf-8 -*-

def get_num_of_edges(matrix):
    num = 0
    for row in matrix:
        for instance in row:
            if instance != 0:
                num = num + 1
    return num


def get_column(matrix, index):
    return [row[index] for row in matrix]


def get_copy_of_array(array):
    if type(array) != list:
        return None
    return [i for i in array]


def get_empty_matrix(row, col):
    print(row, col)
    return_array = []
    for i in range(0, row):
        return_array.append(col*[0])
    return return_array


"""
    Auhtor: Hyeonsoo, Oh
    Description: Find indirect connection between two vertices in indrect graph.
"""
def find_indirect_conenction_between_two_vertex(matrix, start, current, end, visited=[], any_path=[False]):
    current_visited = get_copy_of_array(visited)
    current_visited.append(current)
    for idx, val in enumerate(matrix[current]):
        if val == 0 or (start == current and idx == end):
            continue
        if idx == end:
            # print ('mission completed current: {}, start: {}, goal: {}, history: {}'.format(current, start, idx, current_visited))
            any_path[0] = True
        elif idx not in current_visited:
            # print (str(current) + ' to the ' +str(idx))
            find_indirect_conenction_between_two_vertex(
                matrix, start, idx, end, current_visited, any_path)

    for idx, val in enumerate(get_column(matrix, current)):
        if val == 0 or (start == current and idx == end):
            continue
        if idx == end:
            any_path[0] = True
        elif idx not in current_visited:
            find_indirect_conenction_between_two_vertex(
                matrix, start, idx, end, current_visited, any_path)
    return any_path


"""
    Author: Hyeon Soo, Oh
    Description: Simple Python algoritm for solving minum spanning tree problem.
"""
def kruskal_algorithm(matrix):
    row_size = len(matrix)
    col_size = len(matrix[0])
    solution_matrix = get_empty_matrix(row_size, col_size)
    try:
        if col_size != row_size:
            raise Exception(
                "Input array must be square-form matrix. check your input again.")
    except Exception as e:
        print(e)
        return
    E = get_num_of_edges(matrix)
    V = col_size
    S = []
    for row in range(0, row_size):
        for col in range(row + 1, col_size):
            if matrix[row][col] != 0:
                edge = {
                    'row': row,
                    'col': col,
                    'weight': matrix[row][col]
                }
                S.append(edge)

    # Sort edges by its weight
    S = sorted(S, key=lambda each: each['weight'])

    for edge in S:
        # print (edge['weight'], edge['row'], edge['col'])
        # print (solution_matrix)
        # print ( edge['row'], edge['col'])
        # print(find_indirect_conenction_between_two_vertex(solution_matrix, edge['row'], edge['row'], edge['col'], [], [False])[0])
        
        #This means that if no indrect connection is between two vertices, there won't be any cycle after this edge is added to the solution.
        if find_indirect_conenction_between_two_vertex(
                solution_matrix, edge['row'], edge['row'], edge['col'], [], [False])[0]== False:
            solution_matrix[edge['row']][edge['col']] = edge['weight']
    return solution_matrix


sd = [[0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]


sample_data = [
    [0, 1, 0, 4, 3, 0],
    [0, 0, 0, 4, 2, 0],
    [0, 0, 0, 0, 4, 5],
    [0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0]
]
sample_data_1 = [
    [0, 1, 0, 4, 3, 0],
    [0, 0, 0, 4, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0]
]
sample_data_2 = [
    [0, 16, 12, 21, 0, 0, 0],
    [16, 0, 0, 17, 20, 0, 0],
    [12, 0, 0, 28, 0, 31, 0],
    [21, 17, 28, 0, 18, 19, 23],
    [0, 20, 0, 18, 0, 0, 11],
    [0, 0, 31, 19, 0, 0, 27],
    [0, 0, 0, 23, 11, 27,0]
]

# print (find_indirect_conenction_between_two_vertex(sd, 0, 0, 3))
print(kruskal_algorithm(sample_data_2))
