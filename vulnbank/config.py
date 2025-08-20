"""
설정 파일 - 취약한 설정들
"""
import os

# 취약점 1: 디버그 모드 활성화
DEBUG = True

# 취약점 2: 하드코딩된 시크릿
import os
SECRET_KEY = os.environ.get('SECRET_KEY')

# 취약점 3: 기본 관리자 계정
DEFAULT_ADMIN = {
    'username': 'admin',
    'password': 'admin123',  # 평문 패스워드
    'email': 'admin@vulnbank.com'
}

# 취약점 4: 약한 데이터베이스 설정
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'username': 'root',
    'password': '',  # 빈 패스워드
    'database': 'vulnbank'
}

# 취약점 5: 불안전한 파일 경로
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'sh', 'exe']  # 실행 파일 허용!

# 취약점 6: 약한 세션 설정
SESSION_CONFIG = {
    'secure': False,  # HTTP에서도 쿠키 전송
    'httponly': False,  # JavaScript에서 접근 가능
    'samesite': None,  # CSRF 보호 없음
    'timeout': 86400 * 365  # 1년 만료 (너무 김)
}

# 취약점 7: 로깅 설정 - 민감한 정보 포함
LOGGING_CONFIG = {
    'level': 'DEBUG',
    'include_passwords': True,  # 패스워드 로깅!
    'include_tokens': True,  # 토큰 로깅!
    'log_file': '/var/log/vulnbank.log'
}

# 취약점 8: 외부 서비스 설정
EXTERNAL_SERVICES = {
    'api_endpoint': 'http://localhost:8080',  # HTTP 사용
    'api_key': 'exposed_api_key_12345',  # 하드코딩된 API 키
    'timeout': 300,  # 긴 타임아웃
    'verify_ssl': False  # SSL 검증 비활성화
}

# 취약점 9: CORS 설정
CORS_CONFIG = {
    'origins': ['*'],  # 모든 오리진 허용
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'headers': ['*'],  # 모든 헤더 허용
    'credentials': True  # 자격 증명 포함
}

# 취약점 10: 보안 헤더 비활성화
SECURITY_HEADERS = {
    'x_frame_options': False,
    'x_content_type_options': False,
    'x_xss_protection': False,
    'strict_transport_security': False,
    'content_security_policy': False
}
