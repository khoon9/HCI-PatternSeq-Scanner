import cv2
import numpy as np
from calculator.security_level_calculator import calculate_security_level


def parse_tuple_list(input_string):
    # 공백과 괄호 제거
    cleaned_string = input_string.replace("(", "").replace(")", "").replace(" ", "")
    
    # 쉼표로 분할하여 각 숫자를 리스트에 저장
    items = cleaned_string.split(',')
    
    # 두 개씩 묶어서 튜플로 변환
    tuple_list = [(int(items[i]), int(items[i + 1])) for i in range(0, len(items), 2)]
    
    return tuple_list

# 각 가능한 패턴 경로에 대해 시각화
def overlay_pattern(input_img, tuple_list_strs, pattern_location):
    r = pattern_location['r']

    grayscale_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    h, w = grayscale_img.shape

    # cropped_img==30 값에서 체크되지 않은 dot 검출
    grayscale_img[np.where(grayscale_img==29)] = 255
    grayscale_img[np.where(grayscale_img==30)] = 255
    grayscale_img[np.where(grayscale_img==31)] = 255

    # 255 값에서 dot 검출
    _, grayscale_img_ = cv2.threshold(grayscale_img, 250, 255, cv2.THRESH_BINARY)

    # cv2.imshow('grayscale_img_',grayscale_img_)

    # HoughCircles 함수를 사용하여 원 검출
    circles = cv2.HoughCircles(
        grayscale_img_, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=2*r, 
        param1=10*r, 
        param2=r/2, 
        minRadius=r-5,  # 반지름 최소값 (약 18픽셀 근처)
        maxRadius=r+5  # 반지름 최대값 (약 18픽셀 근처)
    )

    # center 위치 재배열
    arr = np.uint16(np.around(circles))[0]
    arr = arr[:][:]
    arr = arr[np.argsort(arr[:, 1])]
    arr[0:3] = arr[0:3][np.argsort(arr[0:3][:, 0])]
    arr[3:6] = arr[3:6][np.argsort(arr[3:6][:, 0])]
    arr[6:9] = arr[6:9][np.argsort(arr[6:9][:, 0])]
    arr = arr[:,:2]
    reshaped_arr = arr.reshape(3, 3, 2)

    # 각 가능한 패턴 경로 순회
    for tuple_list_str, _ in tuple_list_strs.items():
        security_level_dict = calculate_security_level(tuple_list_str)

        pattern_tuple_list = parse_tuple_list(tuple_list_str)
        temp_img = input_img.copy()

        # 보안 요소 시각화
        n = 0
        for key in security_level_dict:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_color = (0, 0, 255) 
            thickness = 3
            cv2.putText(temp_img, str(f'{key}: {security_level_dict[key]}'), ( 3*r, h//3+5*r*n), font, font_scale, font_color, thickness)
            n+=1

        for i, pattern in enumerate(pattern_tuple_list):
            # 현재 지나는 점의 center 추출
            center = (reshaped_arr[pattern[0]][pattern[1]][0], reshaped_arr[pattern[0]][pattern[1]][1])
            
            # 원의 외곽선을 빨간색으로 그리기
            cv2.circle(temp_img, center, r, (0, 0, 255), 3)

            # 원의 옆에 숫자 입력
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 4
            font_color = (0, 0, 255)  
            thickness = 8
            cv2.putText(temp_img, str(i+1), (center[0] + r, center[1] - r), font, font_scale, font_color, thickness)
        # 패턴 경로 시각화
        cv2.imshow('{}'.format(pattern_tuple_list), temp_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()