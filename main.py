import cv2
import numpy as np
import sys
import os

# 프로젝트 디렉토리를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from algorithm01 import extract_pattern_img
from algorithm01 import compare_with_templates
from algorithm01 import count_grid_patterns
from algorithm01 import overlay_pattern


def main():
    input_img = cv2.imread('resource/input-patterns/001.png')

    # 이미지 pattern 추출
    # dot / edge return
    dot_pattern_input, edge_pattern_input, pattern_location = extract_pattern_img(cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY))

    # cv2.imshow('dot_pattern_input',dot_pattern_input)
    # cv2.imshow('edge_pattern_input',edge_pattern_input)

    will_v = compare_with_templates(dot_pattern_input)

    # print(will_v)

    patterns = count_grid_patterns(will_v, edge_pattern_input)

    # print(patterns)

    # patterns을 기반으로 번호 매기기
    overlay_pattern(input_img, patterns, pattern_location)

    # cv2.waitKey(0)

if __name__ == '__main__':
    # sys.path에 현재 파일의 디렉토리 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()

