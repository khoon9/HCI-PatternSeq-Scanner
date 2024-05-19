import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def plot_edge_patterns(patterns):
    for pattern in patterns:
        fig, ax = plt.subplots(figsize=(1, 1), dpi=50)
        
        # 축 범위 설정 (축의 범위를 데이터에 맞게 조정)
        ax.set_xlim(-0.05, 2.15)
        ax.set_ylim(-0.1, 2.1)
        ax.set_xticks(range(3))
        ax.set_yticks(range(3))
        ax.grid(True)
        
        # 세로축이 x 가로축이 y가 되도록 설계. 이미지 각 dot의 위치가 행렬 방식으로 다뤄지도록 함.
        x_coords = [pattern[0][1], pattern[1][1]]
        y_coords = [2-pattern[0][0], 2-pattern[1][0]]
        ax.plot(x_coords, y_coords, marker='o', ms=1,color='black',linestyle='-', lw=2)
        
        # 축의 눈금과 레이블 제거
        ax.axis('off')

        # 이미지 생성
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=50, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        image_from_plot = plt.imread(buf)
        
        # 이미지를 그레이스케일로 변환
        image_gray = cv2.cvtColor(image_from_plot, cv2.COLOR_RGBA2GRAY)

        # 픽셀의 값 조정. 0~1 -> 0~255
        image_gray = (image_gray * 255).astype(np.uint8)

        # 이미지 스케일 조정
        image_gray = cv2.resize(image_gray, (50, 50))

        # 픽셀의 값이 0 또는 255가 되도록 조정
        _, image_gray = cv2.threshold(image_gray, 250, 255, cv2.THRESH_BINARY)
        
        # 생성한 edge 템플릿 저장
        cv2.imwrite('resource/edge-templates/({}, {})-({}, {}).png'.format(pattern[0][0],pattern[0][1], pattern[1][0],pattern[1][1]), image_gray)
        plt.close()

def main():
    edge_patterns = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for m in range(3):
                    # 동일 지점일 경우 pass
                    if (i, j) != (k, m):
                        # 이미 추가했던 edge가 아닐 경우에만 추가
                        if [(i, j), (k, m)] not in edge_patterns and [(k, m), (i, j)] not in edge_patterns:
                            edge_patterns.append([(i, j), (k, m)])

    plot_edge_patterns(np.array(edge_patterns,dtype=object))

if __name__ == "__main__":
    main()