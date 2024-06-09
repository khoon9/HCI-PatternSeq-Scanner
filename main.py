import cv2
import numpy as np
import sys
import os

# 프로젝트 디렉토리를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing import extract_pattern_img
from algorithm01 import compare_with_templates
from algorithm01 import count_grid_patterns
from postprocessing import overlay_pattern
from algorithm02 import compare_with_templates_dict
from postprocessing import filter_on_path_dict
from gui import open_file_dialog
from gui import ask_user_choice
import time


def main():
    file_path = open_file_dialog()
    input_img = cv2.imread(file_path)

    cv2.imshow("input img",input_img)

    algorithm = ask_user_choice()

    # 이미지 전처리
    dot_pattern_input, edge_pattern_input, pattern_location = extract_pattern_img(cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY))

    patterns = None

    start_time = time.time()
    if(algorithm==1):
        patterns = compare_with_templates_dict(edge_pattern_input)
    else:
        will_v = compare_with_templates(dot_pattern_input)
        patterns = count_grid_patterns(will_v, edge_pattern_input)
    end_time = time.time()
    print(f'알고리즘 {algorithm} 소요 시간: {end_time-start_time}s')

    patterns = filter_on_path_dict(patterns)

    cv2.destroyAllWindows()

    # 이미지 후처리
    overlay_pattern(input_img, patterns, pattern_location)

if __name__ == '__main__':
    # sys.path에 현재 파일의 디렉토리 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()

