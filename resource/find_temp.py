import pickle
import cv2
import numpy as np
from tqdm import tqdm
import time


def read_and_process_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is not None:
        image_resized = cv2.resize(image, (50, 50))
        _, image_resized_ = cv2.threshold(image_resized, 250, 255, cv2.THRESH_BINARY)
        return image_resized_.tolist()  # 리스트 형태로 변환하여 반환
    else:
        print(f"Error reading image: {image_path}")
        return [[0]*50 for _ in range(50)]  # 읽기에 실패한 경우 빈 이미지 리스트 반환

def find_matching_image(test_image_path, image_data_dict):
    # 테스트할 이미지 읽기 및 처리
    test_image_data = read_and_process_image(test_image_path)
    test_image_data_np = np.array(test_image_data) 
    res_key = None

    # 유사도 추출
    max_like_list = {
        'img1':-2500,
        'img2':-2500,
        'img3':-2500,
        'img4':-2500,
        'img5':-2500,
        'img6':-2500,
        'img7':-2500,
        'img8':-2500,
        'img9':-2500,
        'img10':-2500,
    }

    # 딕셔너리의 모든 값과 비교
    for now_key, now_img in tqdm(image_data_dict.items()):
        now_img_np = np.array(now_img)  # numpy 배열로 변환
        now_value = np.sum(now_img_np == test_image_data_np)
        # if len(max_like_list)==0:
        #     max_like_list[now_key] = now_value

        # 현재 딕셔너리의 최소 값과 그 키 찾기
        min_key = min(max_like_list, key=max_like_list.get)
        min_value = max_like_list[min_key]
        if now_value > min_value:
            del max_like_list[min_key]
            max_like_list[now_key] = now_value
        # if now_img == test_image_data:
        #     res_key = now_key  # 동일한 이미지를 찾으면 해당 키를 반환


    return max_like_list  # 동일한 이미지가 없으면 None 반환

def main():
    # 이미지 데이터 딕셔너리 불러오기
    with open('image_data_dict.pkl', 'rb') as f:
        image_data_dict = pickle.load(f)

    # 테스트할 이미지 경로
    test_image_path = 'resource/path-templates/(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2).png'

    # 동일한 이미지가 있는지 확인
    matching_key = find_matching_image(test_image_path, image_data_dict)

    if matching_key is not None:
        print(f"The test image matches the image with key: {matching_key}")
    else:
        print("No matching image found in the dictionary.")


if __name__ == "__main__":
    start_time = time.time()  # 시작 시간 기록
    main()
    end_time = time.time()  # 종료 시간 기록
    print(f"Image comparison took {end_time - start_time:.2f} seconds")