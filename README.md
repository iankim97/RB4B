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
# 1. 패키지 목록 업데이트
sudo apt-get update
# 2. smbus2 설치 (시스템 전체 적용)
sudo pip3 install smbus2
# 3. 만약 위 명령어로 안 된다면 아래 명령어도 시도
sudo apt-get install python3-smbus -y

# 1. 라이브러리 강제 설치 (새 OS 필수 옵션)
sudo pip3 install RPi.bme280 smbus2 --break-system-packages
sudo pip3 install RPi.bme280 smbus2 --break-system-packages
sudo pip3 install RPi.bme280 smbus2 --break-system-packages

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




