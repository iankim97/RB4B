26-0212 weather.py start

sudo i2cdetect -y 1
python3 /home/rb4b/Desktop/weather.py


##2C 속도 낮추기 (통신 안정화)##
신호가 불안정할 때 시스템 설정에서 통신 속도를 조금 낮추면 해결되는 경우가 많습니다.
터미널에 입력: sudo nano /boot/firmware/config.txt (최신 OS 기준)

참고: 만약 파일이 없다면 sudo nano /boot/config.txt를 시도하세요.

아래 줄을 찾아 수정하거나 끝에 추가하세요:

Plaintext
dtparam=i2c_arm=on,i2c_arm_baudrate=10000
Ctrl + O, Enter, Ctrl + X로 저장 후 sudo reboot 하세요.
