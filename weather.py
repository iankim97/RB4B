import tkinter as tk
from smbus2 import SMBus
import bme280
from influxdb import InfluxDBClient # 설치: sudo pip3 install influxdb --break-system-packages
import socket

# 1. 설정 및 초기화
PORT = 1
ADDRESS = 0x76 
DB_NAME = 'weather_db'

# 센서 및 DB 연결
bus = SMBus(PORT)
calibration_params = bme280.load_calibration_params(bus, ADDRESS)
client = InfluxDBClient('localhost', 8086, 'root', 'root')

# 데이터베이스 생성 (없을 경우를 대비)
if DB_NAME not in [db['name'] for db in client.get_list_database()]:
    client.create_database(DB_NAME)
client.switch_database(DB_NAME)

def update_data():
    try:
        # 센서 데이터 읽기
        data = bme280.sample(bus, ADDRESS, calibration_params)
        temp, press, humid = data.temperature, data.pressure, data.humidity
        alt = 44330 * (1.0 - (press / 1013.25)**(1/5.255))

        # A. 라즈베리파이 GUI 업데이트
        temp_label.config(text=f"온 도 : {temp:.1f} °C")
        press_label.config(text=f"기 압 : {press:.1f} hPa")
        alt_label.config(text=f"고 도 : {alt:.1f} m")
        humid_label.config(text=f"습 도 : {humid:.1f} %")
        status_label.config(text="데이터 전송 중...", fg="gray")

        # B. InfluxDB (그라파나용) 데이터 전송
        json_body = [{
            "measurement": "weather_stats",
            "fields": {
                "temperature": float(temp),
                "pressure": float(press),
                "humidity": float(humid),
                "altitude": float(alt)
            }
        }]
        client.write_points(json_body)

    except Exception as e:
        status_label.config(text=f"오류: {e}", fg="red")
    
    # 2초마다 반복
    root.after(2000, update_data)

# 2. GUI 레이아웃 설정
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='#121212')

# IP 주소 표시 (노트북 접속용 안내)
my_ip = socket.gethostbyname(socket.gethostname() + ".local")
ip_label = tk.Label(root, text=f"접속 주소: http://{my_ip}:3000", bg='#121212', fg='white', font=("Arial", 10))
ip_label.place(x=10, y=40)

frame = tk.Frame(root, bg='#121212')
frame.place(relx=0.5, rely=0.5, anchor='center')

def create_label(color):
    return tk.Label(frame, text="--", bg='#121212', fg=color, font=("Arial", 45, "bold"))

temp_label = create_label("#FF8C00"); temp_label.pack(pady=5)
press_label = create_label("#FFD700"); press_label.pack(pady=5)
alt_label = create_label("#00BFFF"); alt_label.pack(pady=5)
humid_label = create_label("#32CD32"); humid_label.pack(pady=5)

status_label = tk.Label(root, text="시작 중...", bg='#121212', fg="gray", font=("Arial", 10))
status_label.pack(side="bottom", pady=10)

tk.Button(root, text=" 종료(X) ", command=root.destroy, bg='#333333', fg='white').place(x=10, y=10)
root.bind('<Escape>', lambda e: root.destroy())

update_data()
root.mainloop()
