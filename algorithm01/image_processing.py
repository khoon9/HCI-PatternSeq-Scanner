import cv2
import numpy as np

def extract_pattern_img(path):
    # 이미지 불러오기 및 그레이스케일 변환
    # img_01 = cv2.cvtColor(cv2.imread('resource/input-patterns/001.png'), cv2.COLOR_BGR2GRAY)
    img_01 = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

    # 이미지 가운데 지점에서 자르기
    height, width = img_01.shape
    start_row = height // 2 
    end_row = height     
    cropped_img = img_01[start_row:end_row, 0:width]
    for_frame_img = cropped_img.copy()

    # cropped_img==30 값에서 체크되지 않은 dot 검출
    for_frame_img[np.where(for_frame_img==29)] = 255
    for_frame_img[np.where(for_frame_img==30)] = 255
    for_frame_img[np.where(for_frame_img==31)] = 255

    # 255 값에서 dot 검출
    _, for_frame_img_thresholded = cv2.threshold(for_frame_img, 250, 255, cv2.THRESH_BINARY_INV)
    # 255 값에서 패턴 dot 검출
    _, img_01_thresholded = cv2.threshold(cropped_img, 250, 255, cv2.THRESH_BINARY_INV)
    # 245 값에서 패턴 edge 검출, 255 값에서 dot 검출
    _, img_02_thresholded = cv2.threshold(cropped_img, 240, 255, cv2.THRESH_BINARY_INV)

    # 커널(구조 요소) 정의. 커널의 사이즈 크기에 비례하여 노이즈 사전 제거 가능성 증대 가능
    kernel = np.ones((5, 5), np.uint8)

    # 클로징 연산 적용. 이 경우 물체가 value 0이므로 클로징을 수행
    closing_for_frame_img = cv2.morphologyEx(for_frame_img_thresholded, cv2.MORPH_CLOSE, kernel)
    closing_img_01 = cv2.morphologyEx(img_01_thresholded, cv2.MORPH_CLOSE, kernel)
    closing_img_02 = cv2.morphologyEx(img_02_thresholded, cv2.MORPH_CLOSE, kernel)

    # dot 검출 이미지
    # cv2.imwrite('result-image/closing_for_frame_img.png', closing_for_frame_img)

    # 패턴 crop 범위 지정
    coords = np.column_stack(np.where(closing_for_frame_img == 0))
    x_min, y_min = coords.min(axis=0)
    x_max, y_max = coords.max(axis=0)

    # 패턴 이미지 crop 진행
    closing_img_01 = closing_img_01[x_min:x_max+1, y_min:y_max+1]
    closing_img_02 = closing_img_02[x_min:x_max+1, y_min:y_max+1]

    # 패턴 dot 검출 이미지
    # cv2.imwrite('result-image/thresholded_dot.png', closing_img_01)
    # 패턴 edge와 dot 검출 이미지
    # cv2.imwrite('result-image/thresholded_pattern.png', closing_img_02)

    return closing_img_01, closing_img_02