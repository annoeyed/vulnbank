"""
VulnBank - 의도적으로 취약한 온라인 뱅킹 시스템
교육 및 보안 테스트 목적으로만 사용하세요!
"""

__version__ = "1.0.0"
__author__ = "Security Research Team"

# 취약한 설정들
import os
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
SECRET_KEY = "123456"  # 하드코딩된 시크릿
DATABASE_URL = "sqlite:///vulnbank.db"

from .models import *
from .auth import *
from .banking import *
from .crypto import *
from .file_handler import *
from .utils import *
