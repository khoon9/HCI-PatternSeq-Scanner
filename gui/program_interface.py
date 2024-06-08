import tkinter as tk
from tkinter import Tk, filedialog

def open_file_dialog():
    root = Tk()
    root.withdraw()  # GUI 창을 숨깁니다.
    file_path = filedialog.askopenfilename(
        title="이미지 파일 선택",
        filetypes=[("PNG images", "*.png"), ("JPG images", "*.jpg"), ("JPEG images", "*.jpeg"), ("BMP images", "*.bmp")]
    )  # 파일 선택 대화 상자를 엽니다.
    root.destroy() 
    return file_path

def ask_user_choice():
    root = Tk()
    # root.withdraw()  # 메인 윈도우를 숨깁니다.

    # 윈도우 크기 설정
    window_width = 300
    window_height = 100

    # 화면 크기를 얻습니다.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 윈도우를 화면 중앙에 위치시키기 위한 좌표 계산
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    global res
    res = None

    def event1():
        global res
        res = 1
        root.destroy()
    def event2():
        global res
        res = 2
        root.destroy()

    root.title("알고리즘 선택")

    btn_algorithm1 = tk.Button(root, text="알고리즘 1 선택", command=event1)
    btn_algorithm1.pack(side=tk.LEFT, padx=20, pady=20)

    btn_algorithm2 = tk.Button(root, text="알고리즘 2 선택", command=event2)
    btn_algorithm2.pack(side=tk.LEFT, padx=20, pady=20)

    root.mainloop()
    return res