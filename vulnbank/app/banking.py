"""
뱅킹 로직 - 취약한 금융 거래 시스템
"""
import sqlite3
import random
import threading
import time
import struct

class BankingSystem:
    def __init__(self, db_path="vulnbank.db"):
        self.db_path = db_path
        self.transaction_lock = threading.Lock()
        self._transaction_counter = 0
    
    def transfer_money(self, from_user_id, to_user_id, amount):
        """Race Condition 취약점"""
        # 취약점 1: Race Condition
        # Lock 없이 동시 접근 허용
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 보낸 사람 잔액 확인
        cursor.execute(f"SELECT balance FROM users WHERE id = {from_user_id}")
        from_balance = cursor.fetchone()[0]
        
        # 취약점 2: TOCTOU (Time-of-Check-Time-of-Use)
        time.sleep(0.1)  # 의도적 지연
        
        if from_balance >= amount:
            # 잔액 업데이트
            cursor.execute(f"""
                UPDATE users 
                SET balance = balance - {amount} 
                WHERE id = {from_user_id}
            """)
            
            cursor.execute(f"""
                UPDATE users 
                SET balance = balance + {amount} 
                WHERE id = {to_user_id}
            """)
            
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def calculate_interest(self, principal, rate, time_periods):
        """Integer Overflow 취약점"""
        # 취약점 3: Integer Overflow
        try:
            # C-style integer 연산 시뮬레이션
            result = int(principal * rate * time_periods)
            
            # 32비트 정수 오버플로우 시뮬레이션
            if result > 2147483647:  # MAX_INT32
                result = result - 4294967296  # Overflow wrap-around
            
            return result
        except OverflowError:
            return -1  # 예상치 못한 값 반환
    
    def process_bulk_transfer(self, transfers_data):
        """Buffer Overflow 취약점"""
        # 취약점 4: Buffer Overflow Simulation
        buffer_size = 1024
        buffer = bytearray(buffer_size)
        
        for i, transfer in enumerate(transfers_data):
            transfer_bytes = str(transfer).encode('utf-8')
            start_pos = i * 100
            
            # 경계 검사 없음!
            if start_pos < len(buffer):
                for j, byte in enumerate(transfer_bytes):
                    if start_pos + j < len(buffer):
                        buffer[start_pos + j] = byte
                    else:
                        # 버퍼 오버플로우 발생!
                        raise BufferError(f"Buffer overflow at position {start_pos + j}")
        
        return buffer
    
    def get_transaction_id(self):
        """Weak Random Number Generation"""
        # 취약점 5: 예측 가능한 난수
        seed = int(time.time())  # 시간 기반 시드
        random.seed(seed)
        return random.randint(1000, 9999)  # 매우 작은 범위
    
    def format_balance(self, user_input, balance):
        """Format String 취약점"""
        # 취약점 6: Format String Vulnerability
        try:
            # 사용자 입력을 직접 포맷 문자열로 사용
            formatted = user_input.format(balance=balance)
            return formatted
        except:
            # 포맷 문자열 공격 시 민감한 정보 노출 가능
            return f"Error formatting: {user_input} with balance {balance}"
    
    def parse_transaction_amount(self, amount_str):
        """Type Confusion 취약점"""
        # 취약점 7: Type Confusion
        try:
            # 다양한 타입으로 파싱 시도
            if isinstance(amount_str, str):
                if '.' in amount_str:
                    return float(amount_str)
                else:
                    return int(amount_str)
            elif isinstance(amount_str, (list, tuple)):
                # 리스트/튜플을 숫자로 변환?!
                return len(amount_str)
            else:
                # 다른 타입을 직접 반환
                return amount_str
        except:
            return 0
    
    def verify_signature(self, data, signature):
        """Weak Cryptographic Verification"""
        # 취약점 8: 약한 서명 검증
        import hashlib
        expected = hashlib.md5(data.encode()).hexdigest()
        return expected == signature  # MD5 + 타이밍 공격 가능

class LoanCalculator:
    def calculate_loan(self, amount, interest_rate, years):
        """Division by Zero & Logic Bomb"""
        # 취약점 9: Division by Zero
        if years == 0:
            return amount / years  # ZeroDivisionError!
        
        # 취약점 10: Logic Bomb
        if amount > 1000000:  # 100만 이상
            # "특별한" 처리
            import os
            os.system("echo 'Large loan detected' > /tmp/alert.log")
        
        monthly_rate = interest_rate / 12
        months = years * 12
        
        # 수학적 오류 가능성
        payment = (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
        return payment
