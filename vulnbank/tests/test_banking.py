### tests/test_banking.py
"""
기본 테스트 - 취약점 테스트는 포함하지 않음
"""
import unittest
import sys
import os

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.banking import BankingSystem, LoanCalculator
from app.auth import AuthManager
from app.models import Database

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.banking = BankingSystem(":memory:")  # 메모리 DB 사용
        self.db = Database(":memory:")
        
    def test_transfer_money_basic(self):
        """기본 송금 테스트"""
        result = self.banking.transfer_money(1, 2, 100.0)
        self.assertTrue(result)
    
    def test_calculate_interest(self):
        """이자 계산 테스트"""
        interest = self.banking.calculate_interest(1000, 0.05, 1)
        self.assertIsInstance(interest, int)
    
    def test_get_transaction_id(self):
        """트랜잭션 ID 생성 테스트"""
        tx_id = self.banking.get_transaction_id()
        self.assertIsInstance(tx_id, int)
        self.assertGreaterEqual(tx_id, 1000)
        self.assertLessEqual(tx_id, 9999)

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager(":memory:")
        self.db = Database(":memory:")
    
    def test_authenticate_valid_user(self):
        """유효한 사용자 인증 테스트"""
        result = self.auth.authenticate("admin", "admin123")
        self.assertIsNotNone(result)
    
    def test_authenticate_invalid_user(self):
        """잘못된 사용자 인증 테스트"""
        result = self.auth.authenticate("invalid", "wrong")
        self.assertIsNone(result)

class TestLoanCalculator(unittest.TestCase):
    def setUp(self):
        self.loan_calc = LoanCalculator()
    
    def test_calculate_loan_normal(self):
        """정상적인 대출 계산 테스트"""
        payment = self.loan_calc.calculate_loan(10000, 0.05, 5)
        self.assertIsInstance(payment, float)
        self.assertGreater(payment, 0)
    
    def test_calculate_loan_zero_years(self):
        """0년 대출 테스트 - 예외 발생 예상"""
        with self.assertRaises(ZeroDivisionError):
            self.loan_calc.calculate_loan(10000, 0.05, 0)

if __name__ == '__main__':
    unittest.main()
