import cv2
import numpy as np

# 이미지 스케일링
def resize_image(image_array):
    img = cv2.resize(image_array, (50, 50))
    _, img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    return img

# 이동 가능여부 판단
def is_valid_move(visit, start, end):
    if end in visit:
        return False
    # 대각선 이동의 경우 중간 지점 확인
    if (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2) or (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 0) or (abs(start[0] - end[0]) == 0 and abs(start[1] - end[1]) == 2):
        mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        if mid not in visit:
            return False
    return True

# 동일한 점 여부 반환
def calculate_equal_cnt(image1, image2):
    return np.sum(image1 == image2)

# 역탐색 후보군에 대한 유사도 정렬 수행
def dfs_visit(object_image, edge_patterns, will_v, current, visited, before_pattern, path, base_image):
    base_equal_cnt = calculate_equal_cnt(object_image, base_image)
    
    if len(will_v)==0:
        # 조건 02: 구해낸 모든 경우에 대해 정렬하여, 가장 equal_cnt가 높은 path를 구해낸다. -> 현재까지의 총 equal_cnt 저장
        path_string = ', '.join(str(point) for point in path)
        patterns[path_string] = base_equal_cnt
        return  

    now_patterns = set()
    for pattern in edge_patterns:
        pattern = tuple(pattern)
        if current in pattern:
            now_patterns.add(pattern)
    for pattern in before_pattern:
        pattern = tuple(pattern)
        if pattern in now_patterns:
            now_patterns.remove(pattern)
    for pattern in edge_patterns:
        pattern = tuple(pattern)
        for visited_pos in visited:
            if visited_pos in pattern and visited_pos != current:
                now_patterns.discard(pattern)
    
    for pattern in now_patterns:
        pattern = tuple(pattern)
        next_pos = None
        if current == pattern[0]:
            next_pos = pattern[1]
        else:
            next_pos = pattern[0]
        if is_valid_move(visited,current,next_pos):
            # 조건 01: 두 점 사이의 edge를 패턴에 추가한 이미지와 이전 이미지의 test_img에 대한 equal_cnt가 +10 차이가 날 것
            template_name = '({}, {})-({}, {}).png'.format(pattern[0][0],pattern[0][1], pattern[1][0],pattern[1][1])
            template_path = 'resource/edge-templates/'+template_name
            template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            template_image_resized = resize_image(template_image)
    
            new_base_image = np.array(base_image.copy())
            new_base_image[np.where(template_image_resized==0)] = 0
            
            equal_cnt = calculate_equal_cnt(object_image, new_base_image)
            
            if equal_cnt-base_equal_cnt >10:
                path.append(tuple(next_pos))
                before_pattern.add(tuple(pattern))
                visited.add(tuple(next_pos))
                will_v.remove(tuple(next_pos))
                dfs_visit(object_image, edge_patterns, will_v, next_pos, visited, before_pattern, path, new_base_image)
                will_v.add(tuple(next_pos))
                visited.remove(tuple(next_pos))
                before_pattern.remove(tuple(pattern))
                path.pop()

# 통합 관리
def count_grid_patterns(will_v, object_image):
    object_image = resize_image(object_image)

    global patterns

    # 가능한 edge 목록 생성
    edge_patterns = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for m in range(3):
                    if (i, j) != (k, m):
                        # 점 (i, j)와 (k, m)이 동일하지 않은 경우만 추가
                        # 중복 조합을 제거하기 위해 정렬하여 추가
                        if [(i, j), (k, m)] not in edge_patterns and [(k, m), (i, j)] not in edge_patterns:
                            edge_patterns.append([(i, j), (k, m)])

    patterns = {}
    for current in will_v:
        visited = set([current])
        path = [current]
        before_pattern = set([])
        will_v.remove(current)
        dfs_visit(object_image, edge_patterns, will_v, current, visited, before_pattern, path, [[255]*50 for i in range(50)])
        will_v.add(current)
    return patterns

# object_image = np.array(resize_image(closing_img_01))
# patterns = count_grid_patterns(will_v)
# print(patterns)