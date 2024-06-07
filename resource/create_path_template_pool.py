import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from multiprocessing import Pool, cpu_count

def parse_tuple_list(input_string):
    cleaned_string = input_string.replace("(", "").replace(")", "").replace(" ", "")
    items = cleaned_string.split(',')
    tuple_list = [(int(items[i]), int(items[i + 1])) for i in range(0, len(items), 2)]
    return tuple_list

def generate_image(pattern):
    path = parse_tuple_list(pattern)
    fig, ax = plt.subplots(figsize=(1, 1), dpi=50)
    ax.set_xlim(-0.05, 2.15)
    ax.set_ylim(-0.1, 2.1)
    ax.set_xticks(range(3))
    ax.set_yticks(range(3))
    ax.grid(True)
    y_coords, x_coords = zip(*path)
    y_coords = [2-y for y in y_coords]
    ax.plot(x_coords, y_coords, marker='o', ms=1, color='black', linestyle='-', lw=2)
    ax.axis('off')
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=50, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image_from_plot = plt.imread(buf)
    image_gray = cv2.cvtColor(image_from_plot, cv2.COLOR_RGBA2GRAY)
    image_gray = (image_gray * 255).astype(np.uint8)
    image_gray = cv2.resize(image_gray, (50, 50))
    _, image_gray = cv2.threshold(image_gray, 250, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'resource/path-templates/{pattern}.png', image_gray)
    plt.close(fig)

def is_valid_move(visit, start, end):
    if end in visit:
        return False
    if (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2) or (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 0) or (abs(start[0] - end[0]) == 0 and abs(start[1] - end[1]) == 2):
        mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        if mid not in visit:
            return False
    return True

def dfs_visit(current, visited, path, patterns):
    if len(path) >= 4:
        canonical_path = f'{path}'.strip('[]')
        patterns.add(canonical_path)
    if len(path) == 9:
        return
    for direction in [(x, y) for x in range(-2, 3) for y in range(-2, 3) if (x, y) != (0, 0)]:
        next_row = current[0] + direction[0]
        next_col = current[1] + direction[1]
        if 0 <= next_row < 3 and 0 <= next_col < 3 and is_valid_move(visited, current, (next_row, next_col)):
            next_pos = (next_row, next_col)
            if next_pos not in visited:
                visited.add(next_pos)
                path.append(next_pos)
                dfs_visit(next_pos, visited, path, patterns)
                path.pop()
                visited.remove(next_pos)

def create_path_templates():
    patterns = set()
    for i in range(3):
        for j in range(3):
            start = (i, j)
            visited = set([start])
            path = [start]
            dfs_visit(start, visited, path, patterns)
    return patterns

def main():
    path_patterns = list(create_path_templates())
    with Pool(processes=cpu_count()) as pool:
        pool.map(generate_image, path_patterns)

if __name__ == "__main__":
    main()
