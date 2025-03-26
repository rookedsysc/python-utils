import time
import matplotlib.pyplot as plt
from ping3 import ping
from datetime import datetime

log = []  # 로그 데이터 (시간, 응답 여부)
target = "8.8.8.8"  # 구글 DNS 서버
start_time = datetime.now()

def check_ping(target):
    try:
        response = ping(target, timeout=1)  # 1초 내 응답 확인
        if response is None:
            return False
        return True
    except Exception as e:  # ping3의 모든 예외 처리
        print(f"Ping Error: {e}")
        return False

def log_data():
    while True:
        result = check_ping(target)
        now = datetime.now()
        log.append((now, result))
        print(f"{now}: {'UP' if result else 'DOWN'}")
        time.sleep(1)  # 1초 간격

def analyze_and_plot():
    downtime = 0
    down_periods = 0
    last_status = True
    times = []
    statuses = []
    
    for entry in log:
        time, status = entry
        times.append(time)
        statuses.append(1 if status else 0)
        
        if not status and last_status:
            down_periods += 1
        if not status:
            downtime += 1
        last_status = status
    
    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(times, statuses, drawstyle='steps-post')
    plt.title('Network Uptime Monitoring')
    plt.xlabel('Time')
    plt.ylabel('Status (1 = UP, 0 = DOWN)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 그래프 저장
    plt.savefig(f"network_status_{start_time.strftime('%Y%m%d_%H%M%S')}.png")
    plt.show()
    
    print(f"Total Downtime: {downtime} seconds")
    print(f"Total Down Periods: {down_periods}")

# 1초마다 상태 확인 (별도 스레드로 돌리거나 백그라운드에서 실행 가능)
try:
    log_data()
except KeyboardInterrupt:
    analyze_and_plot()
