def parse_tuple_list(path):
    # 공백과 괄호 제거
    cleaned_string = path.replace("(", "").replace(")", "").replace(" ", "")
    
    # 쉼표로 분할하여 각 숫자를 리스트에 저장
    items = cleaned_string.split(',')
    
    # 두 개씩 묶어서 튜플로 변환
    tuple_list = [(int(items[i]), int(items[i + 1])) for i in range(0, len(items), 2)]
    
    return tuple_list

# Pattern  length
def get_pattern_length(path):
    return len(path)

# Directional Change
def get_directional_change(path):
    # 연속하는 세 점 A B C가 직선관계가 아니라면 +1 카운팅
    # A B C가 형성하는 영역(삼각형)이 0이라면 직선. 아니라면 방향 전환.
    count = 0
    for i in range(len(path)-2):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        x3, y3 = path[i+2]
        det = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        if det != 0:
            count += 1
    return count

# Overlapping node
def get_overlapping_node(path):
    # A->B 에서 특정 노드를 Overlapping하는 경우 반환
    count = 0
    for i in range(len(path)-1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        dx = x2 - x1
        dy = y2 - y1
        conditions = [
            (2, 0), (0, 2), (2, 2),
            (-2, 0), (0, -2), (-2, -2),
            (2, -2), (-2, 2)
        ]
        if (dx, dy) in conditions:
            count += 1
    return count


# knight move
def get_knight_move(path):
    # knight move 판별 개수 반환
    count = 0
    for i in range(len(path)-1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        dx = x2 - x1
        dy = y2 - y1
        # 나이트의 움직임에 해당하는 dx, dy 조건
        knight_moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        if (dx, dy) in knight_moves:
            count += 1
    return count
        


# (0, 0) (0, 1) (0, 2) 
# (1, 0) (1, 1) (1, 2) 
# (2, 0) (2, 1) (2, 2) 

# 경로 문자열 입력
def calculate_security_level(path):
    path = parse_tuple_list(path)
    path_info = {
        'pattern_length':get_pattern_length(path),
        'directional_change': get_directional_change(path),
        'overlapping_node': get_overlapping_node(path),
        'knight_move': get_knight_move(path)
    }

    print(path_info)
