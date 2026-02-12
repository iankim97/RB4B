26-0212 weather.py start
ID: pi
Password: raspberry

# PINOUT
VCC: 1번 핀 (3.3V) - 주의: 5V에 꽂으면 센서가 타버릴 수 있습니다.
GND: 6번 핀 (Ground)
SDA: 3번 핀 (I2C Data)
SCL: 5번 핀 (I2C Clock)

sudo apt-get update
sudo apt-get install python3-pip
pip3 install RPi.bme280 smbus2
sudo apt-get update                         // 패키지 목록 업데이트
sudo pip3 install smbus2                   // smbus2 설치 (시스템 전체 적용)
sudo apt-get install python3-smbus -y       // 만약 위 명령어로 안 된다면 아래 명령어도 시도
sudo pip3 install RPi.bme280 smbus2 --break-system-packages  // 라이브러리 강제 설치 (새 OS 필수 옵션)

sudo apt update
sudo apt install python3-smbus2 python3-rpi.bme280 -y

# 2. 한글 폰트 설치 (글자 깨짐 방지)
sudo apt install fonts-nanum -y

# 3. I2C 인터페이스 활성화 확인 (직접 메뉴에서 설정)
# sudo raspi-config -> Interface Options -> I2C -> Yes

# 4. 프로그램 실행
python3 /home/rb4b/Desktop/weather.py

### 도구설치 ###
sudo i2cdetect -y 1
sudo apt update
sudo apt install i2c-tools -y
python3 -c "import bme280; import smbus2; print('이제 준비가 끝났습니다!')"
python3 -c "import bme280; import smbus2; print('모든 모듈 로드 성공!')"
python3 -c "import bme280; print('bme280 라이브러리 로드 성공!')"
python3 -c "import smbus2; print('설치 성공!')"

안전한 종료 명령어: sudo halt 또는 sudo shutdown -h now
안전한 재부팅 명령어: sudo reboot
### 센서 응답 테스트 (간단한 코드) ###
python3 -c "import smbus2, bme280; bus=smbus2.SMBus(1); print(bme280.sample(bus, 0x76))"

sudo i2cdetect -y 1
python3 /home/rb4b/Desktop/weather.py
@python3 /home/rb4b/Desktop/weather.py


### I2C 속도 낮추기 (통신 안정화) ###
신호가 불안정할 때 시스템 설정에서 통신 속도를 조금 낮추면 해결되는 경우가 많습니다.
터미널에 입력: sudo nano /boot/firmware/config.txt (최신 OS 기준)
참고: 만약 파일이 없다면 sudo nano /boot/config.txt를 시도하세요.
아래 줄을 찾아 수정하거나 끝에 추가
dtparam=i2c_arm=on,i2c_arm_baudrate=10000 
/ Ctrl + O, Enter, Ctrl + X로 저장 후 
sudo reboot 


### 부팅 시 자동 실행 설정 (autostart) ###
아까 편집했던 파일(sudo nano /etc/xdg/lxsession/LXDE-pi/autostart)
의 마지막 줄을 반드시 아래와 같이 수정하세요. (계정명 주의)

@python3 /home/rb4b/Desktop/weather.py


## Gemini said
최신 라즈베리파이 OS(Bookworm/Trixie) 버전은 기존의 LXDE-pi 대신 Wayland나 Labwc 같은 새로운 데스크톱 관리자를 사용하기 때문에 해당 폴더와 파일이 존재하지 않는 것이 정상입니다.
현재 환경에 맞는 두 가지 해결 방법 중 하나를 선택해 보세요.
# 방법 1: 사용자별 자동 실행 설정 (가장 추천)
파일이 없다면 폴더를 직접 만들어서 설정을 추가해야 합니다.

자동 실행 폴더 생성:
Bash
mkdir -p /home/rb4b/.config/autostart
자동 실행 파일 작성:
Bash
nano /home/rb4b/.config/autostart/weather.desktop
파일 내용 입력: (아래 내용을 그대로 복사해서 붙여넣으세요)

Plaintext
[Desktop Entry]
Type=Application
Name=WeatherHMI
Exec=python3 /home/rb4b/Desktop/weather.py
Ctrl + O, Enter, Ctrl + X로 저장합니다.

# 방법 2: 최신 OS 전용 전역 설정 파일 편집
만약 위 폴더가 작동하지 않는다면, 최신 OS에서 사용하는 전역 설정 파일을 편집해 보세요.

설정 파일 열기:

Bash
sudo nano /etc/xdg/labwc/autostart
(파일이 비어있어도 괜찮습니다)

파일 맨 아래에 추가:

Plaintext
python3 /home/rb4b/Desktop/weather.py &
주의: 명령어 뒤에 &를 붙여야 시스템 부팅이 멈추지 않습니다.

💡 추가 체크 포인트
파일 권한: 실행 권한이 없으면 자동 실행이 안 될 수 있습니다.

Bash
chmod +x /home/rb4b/Desktop/weather.py
X11 vs Wayland: 터미널에 echo $XDG_SESSION_TYPE을 입력했을 때 wayland라고 나온다면 방법 1이 가장 확실하게 작동합니다.
이제 설정 후 sudo reboot으로 재부팅해 보세요. 화면이 뜨면 이제 노트북으로 데이터를 전송하는 그라파나 연동 코드로 넘어갈 준비가 된 것입니다!




