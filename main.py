import cv2
import numpy as np
import sys
import os

# 프로젝트 디렉토리를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from algorithm01 import extract_pattern_img
from algorithm01 import compare_with_templates
from algorithm01 import count_grid_patterns

def main():
    # 이미지 pattern 추출
    # dot / edge return
    dot_pattern_input, edge_pattern_input = extract_pattern_img('resource/input-patterns/001.png')

    # cv2.imshow('dot_pattern_input',dot_pattern_input)
    # cv2.imshow('edge_pattern_input',edge_pattern_input)

    will_v = compare_with_templates(dot_pattern_input)

    # print(will_v)

    patterns = count_grid_patterns(will_v, edge_pattern_input)

    print(patterns)

    # cv2.waitKey(0)

if __name__ == '__main__':
    # sys.path에 현재 파일의 디렉토리 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()

