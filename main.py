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
from calculator import calculate_security_level
from algorithm02 import compare_with_templates_dict
from postprocessing import filter_on_path_dict

def main():
    algorithm = 1
    input_img = cv2.imread('resource/input-patterns/002.PNG')

    # 이미지 전처리
    dot_pattern_input, edge_pattern_input, pattern_location = extract_pattern_img(cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY))

    patterns = None

    if(algorithm==1):
        will_v = compare_with_templates(dot_pattern_input)
        patterns = count_grid_patterns(will_v, edge_pattern_input)
    else:
        patterns = compare_with_templates_dict(edge_pattern_input)

    print(patterns)
    patterns = filter_on_path_dict(patterns)
    print(patterns)

    # # 계산기
    # for path, _ in patterns.items():
    #     calculate_security_level(path)

    # 이미지 후처리
    overlay_pattern(input_img, patterns, pattern_location)

    # cv2.waitKey(0)

if __name__ == '__main__':
    # sys.path에 현재 파일의 디렉토리 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()

