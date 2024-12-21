import heapq
class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost  # g(n): chi phí từ nút gốc đến nút hiện tại
        self.heuristic = heuristic  # h(n): chi phí ước lượng từ nút hiện tại đến đích

    def total_cost(self):
        return self.cost + self.heuristic  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def dfs_a_star(start, goal, neighbors_fn, heuristic_fn, max_depth):
    stack = [Node(start, None, 0, heuristic_fn(start))]
    best_cost = float('inf')
    best_path = None

    while stack:
        current = stack.pop()

        # Nếu tìm thấy trạng thái đích và có chi phí tốt hơn, cập nhật kết quả
        if current.state == goal and current.total_cost() < best_cost:
            best_cost = current.total_cost()
            best_path = reconstruct_path(current)
            continue

        # Nếu vượt quá độ sâu tối đa, bỏ qua trạng thái này
        if current.cost > max_depth:
            continue

        # Duyệt qua các trạng thái kề
        for neighbor, step_cost in neighbors_fn(current.state):
            g = current.cost + step_cost
            h = heuristic_fn(neighbor)

            # Chỉ thêm vào stack nếu tổng chi phí không vượt quá chi phí tốt nhất
            if g + h < best_cost:
                stack.append(Node(neighbor, current, g, h))

    return best_path,best_cost

# Ví dụ sử dụng
def neighbors_fn(state):
    #đồ thị đường đi và giá trị heuristic:
    graph = {
        'A': [('B', 1), ('C', 3)],
        'B': [('D', 1), ('E', 4)],
        'C': [('F', 2)],
        'D': [('G', 5)],
        'E': [('G', 1)],
        'F': [('G', 2)],
        'G': []
    }
    return graph.get(state, [])

def heuristic_fn(state):
    heuristics = {
        'A': 7,
        'B': 6,
        'C': 5,
        'D': 3,
        'E': 1,
        'F': 2,
        'G': 0
    }
    return heuristics.get(state, float('inf'))

start = 'A'
goal = 'G'
max_depth = 10

path = dfs_a_star(start, goal, neighbors_fn, heuristic_fn, max_depth)
print("best path: ", path[0])
print("best cost: ",path[1])
