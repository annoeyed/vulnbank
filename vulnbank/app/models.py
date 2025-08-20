"""
데이터 모델 - 취약한 데이터베이스 설계
"""
import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_path="vulnbank.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """데이터베이스 초기화 - 취약한 스키마"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 취약점: 패스워드가 평문 저장 가능
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,  -- 평문 패스워드!
                email TEXT,
                balance REAL DEFAULT 1000.0,
                is_admin INTEGER DEFAULT 0,
                secret_data TEXT
            )
        """)
        
        # 기본 사용자 생성
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (id, username, password, email, balance, is_admin, secret_data) 
            VALUES 
            (1, 'admin', 'admin123', 'admin@vulnbank.com', 999999.99, 1, 'TOP_SECRET_DATA'),
            (2, 'user', 'password', 'user@vulnbank.com', 1000.0, 0, 'user_secret'),
            (3, 'test', 'test', 'test@vulnbank.com', 500.0, 0, 'test_data')
        """)
        
        conn.commit()
        conn.close()

class User:
    def __init__(self, username, password, email=""):
        self.username = username
        self.password = password  # 취약점: 평문 저장
        self.email = email
        self.balance = 1000.0
        self.is_admin = False
    
    def to_dict(self):
        """취약점: 패스워드까지 포함해서 반환"""
        return {
            'username': self.username,
            'password': self.password,  # 패스워드 노출!
            'email': self.email,
            'balance': self.balance,
            'is_admin': self.is_admin
        }

class BankAccount:
    def __init__(self, user_id, balance=0.0):
        self.user_id = user_id
        self.balance = balance
        self.transactions = []
    
    def add_transaction(self, amount, description=""):
        """취약점: 트랜잭션 검증 없음"""
        self.balance += amount  # 음수도 가능!
        self.transactions.append({
            'amount': amount,
            'description': description,
            'balance_after': self.balance
        })
