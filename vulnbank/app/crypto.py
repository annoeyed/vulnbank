"""
암호화 모듈 - 취약한 암호화 구현
"""
import hashlib
import base64
import random
import string
from cryptography.fernet import Fernet

class VulnerableCrypto:
    def __init__(self):
        # 취약점 1: 하드코딩된 키
        self.secret_key = b"this_is_a_very_weak_key_12345678"
        self.fernet = Fernet(base64.urlsafe_b64encode(self.secret_key))
    
    def hash_password(self, password):
        """취약한 패스워드 해싱"""
        # 취약점 2: MD5 + Salt 없음
        return hashlib.md5(password.encode()).hexdigest()
    
    def encrypt_sensitive_data(self, data):
        """취약한 암호화"""
        # 취약점 3: ECB 모드 시뮬레이션 (패턴 노출)
        encrypted_blocks = []
        block_size = 16
        
        padded_data = data + " " * (block_size - len(data) % block_size)
        
        for i in range(0, len(padded_data), block_size):
            block = padded_data[i:i+block_size]
            # 같은 블록은 같은 암호문 생성 (ECB 모드 취약점)
            block_hash = hashlib.md5(block.encode()).hexdigest()[:16]
            encrypted_blocks.append(block_hash)
        
        return ''.join(encrypted_blocks)
    
    def generate_session_key(self):
        """취약한 키 생성"""
        # 취약점 4: 약한 난수 생성
        random.seed(12345)  # 고정된 시드!
        key = ''.join(random.choices(string.ascii_letters, k=16))
        return key
    
    def verify_token(self, token, expected_user):
        """취약한 토큰 검증"""
        # 취약점 5: 타이밍 공격 취약
        decoded = base64.b64decode(token).decode()
        
        # 문자별 비교 (타이밍 공격 가능)
        for i, (a, b) in enumerate(zip(decoded, expected_user)):
            if a != b:
                return False
        
        return len(decoded) == len(expected_user)
    
    def custom_cipher(self, text, shift=3):
        """자체 제작 암호 (매우 취약)"""
        # 취약점 6: 자체 제작 약한 암호
        result = ""
        for char in text:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    result += chr((shifted - ord('a')) % 26 + ord('a'))
                else:
                    result += chr((shifted - ord('A')) % 26 + ord('A'))
            else:
                result += char
        return result

def weak_random_bytes(length):
    """취약한 랜덤 바이트 생성"""
    # 취약점 7: 시간 기반 예측 가능한 랜덤
    import time
    random.seed(int(time.time()))
    return bytes([random.randint(0, 255) for _ in range(length)])
