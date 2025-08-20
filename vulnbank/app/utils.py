"""
유틸리티 함수들 - 다양한 취약점 포함
"""
import re
import subprocess
import socket
import threading
import time
import json

def validate_email(email):
    """ReDoS (Regular Expression DoS) 취약점"""
    # 취약점 1: 복잡한 정규식으로 인한 DoS
    pattern = r'^(([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+)'
    
    # 중첩된 그룹으로 인한 백트래킹 폭발
    evil_pattern = r'^(a+)+$'
    
    if 'a' * 30 in email:  # 악성 입력 감지 시
        return bool(re.match(evil_pattern, email))  # ReDoS 발생!
    
    return bool(re.match(pattern, email))

def ping_server(hostname):
    """Command Injection in Network Utils"""
    # 취약점 2: ping 명령어에서 명령어 주입
    cmd = f"ping -c 1 {hostname}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Ping error: {e}"

def resolve_hostname(hostname):
    """DNS Injection & SSRF"""
    # 취약점 3: DNS 조회에서 SSRF 가능
    try:
        # 내부 네트워크 접근 가능
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        return f"DNS error: {e}"

class ThreadPoolManager:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.workers = []
        self.task_queue = []
        self.lock = threading.Lock()  # 하지만 제대로 사용 안 함
    
    def add_task(self, func, *args, **kwargs):
        """Race Condition in Task Management"""
        # 취약점 4: 스레드 안전성 부족
        
        # Lock 없이 공유 자원 접근
        self.task_queue.append((func, args, kwargs))
        
        if len(self.workers) < self.max_workers:
            worker = threading.Thread(target=self._worker)
            self.workers.append(worker)
            worker.start()
    
    def _worker(self):
        """Worker 스레드 - Race Condition"""
        while True:
            if self.task_queue:  # Lock 없는 체크
                # TOCTOU 취약점
                time.sleep(0.001)  # 의도적 지연
                
                if self.task_queue:  # 또 다른 체크 (여전히 Lock 없음)
                    task = self.task_queue.pop(0)  # Race condition!
                    func, args, kwargs = task
                    
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        print(f"Task error: {e}")
                else:
                    break
            else:
                break

def memory_bomb(size_mb):
    """Memory Exhaustion DoS"""
    # 취약점 5: 메모리 고갈 공격
    try:
        # 요청된 크기만큼 메모리 할당
        bomb = b'A' * (size_mb * 1024 * 1024)
        return len(bomb)
    except MemoryError:
        return -1

def cpu_bomb(iterations):
    """CPU Exhaustion DoS"""
    # 취약점 6: CPU 고갈 공격
    count = 0
    for i in range(iterations):
        for j in range(1000):
            count += i * j
    return count

def format_user_data(template, user_data):
    """Server-Side Template Injection"""
    # 취약점 7: 템플릿 인젝션
    try:
        # 사용자 데이터를 직접 템플릿에 삽입
        formatted = template.format(**user_data)
        return formatted
    except Exception as e:
        # 에러 정보로 시스템 정보 노출
        return f"Template error: {e} | System: {__import__('platform').system()}"

def parse_json_config(json_string):
    """JSON Parsing with Potential Issues"""
    # 취약점 8: JSON 파싱 취약점
    try:
        # 매우 깊은 중첩 허용 (스택 오버플로우 가능)
        config = json.loads(json_string)
        
        # 재귀적 처리 (무한 재귀 가능)
        return process_config_recursive(config, depth=0)
    except Exception as e:
        return {"error": str(e)}

def process_config_recursive(data, depth=0):
    """재귀적 설정 처리 - 스택 오버플로우 위험"""
    # 취약점 9: 무한 재귀
    if depth > 1000:  # 깊이 제한이 너무 높음
        return "max_depth_reached"
    
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key == "recursive_ref":
                # 자기 참조로 무한 재귀 가능
                result[key] = process_config_recursive(data, depth + 1)
            else:
                result[key] = process_config_recursive(value, depth + 1)
        return result
    elif isinstance(data, list):
        return [process_config_recursive(item, depth + 1) for item in data]
    else:
        return data

def unsafe_eval(expression):
    """Code Injection via eval"""
    # 취약점 10: eval을 통한 코드 실행
    try:
        # 사용자 입력을 직접 eval
        result = eval(expression)  # 매우 위험!
        return result
    except Exception as e:
        return f"Eval error: {e}"

def weak_token_generator(length=8):
    """Weak Token Generation"""
    # 취약점 11: 약한 토큰 생성
    import random
    import time
    
    # 시간 기반 시드 (예측 가능)
    random.seed(int(time.time()) % 1000)
    
    # 작은 문자 집합
    charset = "0123456789"  # 숫자만 사용
    token = ''.join(random.choice(charset) for _ in range(length))
    return token

