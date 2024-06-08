import pickle
import cv2
import numpy as np
from tqdm import tqdm
import os

def process_image(img):
    image_resized = cv2.resize(img, (50, 50))
    _, image_resized_ = cv2.threshold(image_resized, 250, 255, cv2.THRESH_BINARY)
    return image_resized_.tolist()  # 리스트 형태로 변환하여 반환

def find_matching_image(test_image, image_data_dict):
    test_image_data = process_image(test_image)
    test_image_data_np = np.array(test_image_data) 

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

        # 현재 딕셔너리의 최소 값과 그 키 찾기
        min_key = min(max_like_list, key=max_like_list.get)
        min_value = max_like_list[min_key]
        if now_value > min_value:
            del max_like_list[min_key]
            max_like_list[now_key] = now_value

    return max_like_list  # 동일한 이미지가 없으면 None 반환

def compare_with_templates_dict(object_image):
    # 이미지 데이터 딕셔너리 불러오기
    # file_size = os.path.getsize('resource/image_data_dict.pkl')
    # with open('resource/image_data_dict.pkl', 'rb') as f:
    #     with tqdm(total=file_size, unit='B', unit_scale=True, desc='Loading file') as pbar:
    #         image_data_dict = pickle.load(f)
    #         pbar.update(file_size)

    file_size = os.path.getsize('resource/image_data_dict.pkl')
    data = bytearray()
    chunk_size=4*1024*1024
    with open('resource/image_data_dict.pkl', 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc='Loading file') as pbar:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                data.extend(chunk)
                pbar.update(len(chunk))
        # Pickle 데이터를 로드합니다.
        print('2.05G 파싱 후 메모리에 로드 중입니다... 기다려주세요...')
        image_data_dict = pickle.loads(data)
    
    # 동일한 이미지가 있는지 확인
    max_like_list = find_matching_image(object_image, image_data_dict)

    return max_like_list