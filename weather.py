import tkinter as tk
from smbus2 import SMBus
import bme280
import time

# 1. 센서 및 I2C 설정
PORT = 1
ADDRESS = 0x76  # i2cdetect에서 확인된 주소 
bus = SMBus(PORT)

# 전역 변수로 관리
calibration_params = None

def get_calibration():
    """센서 보정 파라미터를 가져오는 함수 (에러 방지용)"""
    global calibration_params
    try:
        calibration_params = bme280.load_calibration_params(bus, ADDRESS)
        return True
    except:
        calibration_params = None
        return False

def update_data():
    global calibration_params
    try:
        # 보정 파라미터가 없으면 재시도
        if calibration_params is None:
            if not get_calibration():
                raise OSError("Sensor Not Initialized")

        # 센서 데이터 샘플링 
        data = bme280.sample(bus, ADDRESS, calibration_params)
        
        # 기압 기반 고도 계산 (1013.25 hPa 기준)
        altitude = 44330 * (1.0 - (data.pressure / 1013.25)**(1/5.255))
        
        # UI 업데이트 (정상)
        temp_label.config(text=f"온 도 : {data.temperature:.1f} °C", fg="#FF8C00")
        press_label.config(text=f"기 압 : {data.pressure:.1f} hPa", fg="#FFD700")
        alt_label.config(text=f"고 도 : {altitude:.1f} m", fg="#00BFFF")
        humid_label.config(text=f"습 도 : {data.humidity:.1f} %", fg="#32CD32")
        status_label.config(text="시스템 정상 작동 중", fg="gray")

    except Exception as e:
        # 에러 발생 시 UI 표시 및 재초기화 시도
        status_label.config(text=f"센서 오류: 연결을 확인하세요", fg="red")
        calibration_params = None 
    
    # 2초마다 갱신 
    root.after(2000, update_data)

# 2. GUI 디자인 설정 
root = tk.Tk()
root.attributes('-fullscreen', True)  # 전체화면 
root.configure(bg='#121212')          # 다크 배경 

# 중앙 정렬 프레임 
frame = tk.Frame(root, bg='#121212')
frame.place(relx=0.5, rely=0.5, anchor='center')

# 공통 라벨 스타일
def create_label(color, size=45):
    return tk.Label(frame, text="--", bg='#121212', fg=color, font=("Arial", size, "bold"))

# 각 항목 레이블 배치 
temp_label = create_label("#FF8C00")
temp_label.pack(pady=5)

press_label = create_label("#FFD700")
press_label.pack(pady=5)

alt_label = create_label("#00BFFF")
alt_label.pack(pady=5)

humid_label = create_label("#32CD32")
humid_label.pack(pady=5)

# 하단 상태 표시줄 (에러 메시지용)
status_label = tk.Label(root, text="초기화 중...", bg='#121212', fg="gray", font=("Arial", 12))
status_label.pack(side="bottom", pady=20)

# 종료 버튼 
exit_btn = tk.Button(root, text=" 종료(X) ", command=root.destroy, bg='#333333', fg='white')
exit_btn.place(x=10, y=10)

# ESC 단축키 추가
root.bind('<Escape>', lambda e: root.destroy())

# 첫 시작
get_calibration()
update_data()

root.mainloop()
