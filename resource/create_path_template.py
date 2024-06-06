import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def parse_tuple_list(input_string):
    # 공백과 괄호 제거
    cleaned_string = input_string.replace("(", "").replace(")", "").replace(" ", "")
    
    # 쉼표로 분할하여 각 숫자를 리스트에 저장
    items = cleaned_string.split(',')
    
    # 두 개씩 묶어서 튜플로 변환
    tuple_list = [(int(items[i]), int(items[i + 1])) for i in range(0, len(items), 2)]
    
    return tuple_list

def plot_path_patterns(patterns):
    for pattern in patterns:
        path = parse_tuple_list(pattern)

        fig, ax = plt.subplots(figsize=(1, 1), dpi=50)
        
        # 축 범위 설정 (축의 범위를 데이터에 맞게 조정)
        ax.set_xlim(-0.05, 2.15)
        ax.set_ylim(-0.1, 2.1)
        ax.set_xticks(range(3))
        ax.set_yticks(range(3))
        ax.grid(True)
        
        # 세로축이 x 가로축이 y가 되도록 설계. 이미지 각 dot의 위치가 행렬 방식으로 다뤄지도록 함.
        y_coords, x_coords = zip(*path)
        y_coords = [2-y for y in y_coords]

        ax.plot(x_coords, y_coords, marker='o', ms=1,color='black',linestyle='-', lw=2)
        
        # 축의 눈금과 레이블 제거
        ax.axis('off')

        # 이미지 생성
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=50, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        image_from_plot = plt.imread(buf)
        
        # 이미지를 그레이스케일로 변환
        image_gray = cv2.cvtColor(image_from_plot, cv2.COLOR_RGBA2GRAY)

        # 픽셀의 값 조정. 0~1 -> 0~255
        image_gray = (image_gray * 255).astype(np.uint8)

        # 이미지 스케일 조정
        image_gray = cv2.resize(image_gray, (50, 50))

        # 픽셀의 값이 0 또는 255가 되도록 조정
        _, image_gray = cv2.threshold(image_gray, 250, 255, cv2.THRESH_BINARY)
        
        # 생성한 edge 템플릿 저장
        cv2.imwrite(f'resource/path-templates/{pattern}.png', image_gray)
        plt.close()

def is_valid_move(visit, start, end):
    if end in visit:
        return False
    # 대각선 이동의 경우 중간 지점 확인
    if (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2) or (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 0) or (abs(start[0] - end[0]) == 0 and abs(start[1] - end[1]) == 2):
        mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        if mid not in visit:
            return False
    return True

def dfs_visit(current, visited, path):
    if len(path) >= 4:
        # Store the path as a tuple to maintain the order of visit
        canonical_path = f'{path}'.strip('[]')
        patterns.add(canonical_path)
    if len(path) == 9:
        return  # Maximum length reached

    for direction in [(x, y) for x in range(-2, 3) for y in range(-2, 3) if (x, y) != (0, 0)]:
        next_row = current[0] + direction[0]
        next_col = current[1] + direction[1]
        if 0 <= next_row < 3 and 0 <= next_col < 3 and is_valid_move(visited,current,(next_row, next_col)):
            next_pos = (next_row, next_col)
            if next_pos not in visited:
                visited.add(next_pos)
                path.append(next_pos)
                dfs_visit(next_pos, visited, path)
                path.pop()
                visited.remove(next_pos)

def create_path_templates():
    global patterns
    patterns = set()
    for i in range(3):
        for j in range(3):
            start = (i, j)
            visited = set([start])
            path = [start]
            dfs_visit(start, visited, path)
    return patterns

def main():
    path_patterns = list(create_path_templates())
    plot_path_patterns(path_patterns)

if __name__ == "__main__":
    main()