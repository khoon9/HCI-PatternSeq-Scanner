import cv2
import numpy as np

# 이미지 스케일링
def resize_image(image_array):
    img = cv2.resize(image_array, (50, 50))
    _, img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    return img

# 동일한 점 여부 반환
def calculate_equal_cnt(image1, image2):
    return np.sum(image1 == image2)

# 패턴의 지나간 점 검출
def compare_with_templates(input_image):
    # 기준 이미지 설정
    base_image = [[255]*50 for i in range(50)]
    # 이미지 스케일링
    input_image_resized = resize_image(input_image)

    # 기준 이미지의 유사도
    base_equal_cnt = calculate_equal_cnt(base_image, input_image_resized)
    dot_on_pattern = set([])

    for x in range(3):
        for y in range(3):
            template_name = f"({x}, {y}).png"
            template_path = f"resource/dot-templates/{template_name}"
            template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            template_image_resized = resize_image(template_image)
            equal_cnt = calculate_equal_cnt(input_image_resized, template_image_resized)

            # 유사도 증가 -> 패턴이 지나간 dot으로 인식
            if equal_cnt-base_equal_cnt >0:
                dot_on_pattern.add((x, y))
    
    # 패턴이 지난 dot 지점들 반환
    return dot_on_pattern