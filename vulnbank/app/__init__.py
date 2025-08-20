"""
VulnBank - 의도적으로 취약한 온라인 뱅킹 시스템
교육 및 보안 테스트 목적으로만 사용하세요!
"""

__version__ = "1.0.0"
__author__ = "Security Research Team"

# 취약한 설정들
DEBUG = True
import os
from cryptography.fernet import Fernet
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    SECRET_KEY = cipher_suite.encrypt(key)  # 하드코딩된 시크릿
DATABASE_URL = "sqlite:///vulnbank.db"

from .models import *
from .auth import *
from .banking import *
from .crypto import *
from .file_handler import *
from .utils import *
