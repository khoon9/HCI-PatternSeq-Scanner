import cv2
import numpy as np
import os
from tqdm import tqdm
import h5py

def read_and_process_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is not None:
        image_resized = cv2.resize(image, (50, 50))
        _, image_resized_ = cv2.threshold(image_resized, 250, 255, cv2.THRESH_BINARY)
        return image_resized_.tolist()  # 리스트 형태로 변환하여 반환
    else:
        print("오류1")
        return [[0]*50 for _ in range(50)]  # 읽기에 실패한 경우 빈 이미지 리스트 반환

def main():
    image_folder = 'resource/path-templates'  # 이미지가 저장된 폴더 경로
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]

    # 결과를 저장할 dictionary 초기화
    image_data_dict = {}

    for image_path in tqdm(image_paths):
        image_name = os.path.basename(image_path)  # 이미지 파일 이름을 키로 사용
        image_name_without_ext = os.path.splitext(image_name)[0]
        image_data_dict[image_name_without_ext] = read_and_process_image(image_path)

    # dictionary를 파일로 저장 (pickle 사용)
    import pickle
    with open('image_data_dict.pkl', 'wb') as f:
        pickle.dump(image_data_dict, f)

if __name__ == "__main__":
    main()
