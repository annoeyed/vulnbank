"""
설정 파일 - 취약한 설정들
"""
import os

# 취약점 1: 디버그 모드 활성화
DEBUG = True

# 취약점 2: 하드코딩된 시크릿
SECRET_KEY = "hardcoded_secret_key_123456"

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
    'api_endpoint': 'https://localhost:8080'
이전 코드는 HTTP를 사용하여 데이터를 전송하고 있었는데, 이는 보안에 취약합니다. HTTP는 데이터를 평문으로 전송하기 때문에, 중간에서 데이터를 가로채는 것이 가능합니다. 이를 해결하기 위해 HTTPS를 사용하도록 코드를 수정하였습니다. HTTPS는 SSL/TLS 프로토콜을 사용하여 데이터를 암호화하므로, 중간에서 데이터를 가로채더라도 이해할 수 없는 암호화된 데이터만을 볼 수 있습니다.
추가적으로, HTTPS를 사용하려면 서버에 SSL 인증서가 필요합니다. 이 인증서는 신뢰할 수 있는 CA(Certificate Authority)로부터 발급받아야 합니다. 따라서, 서버 설정도 함께 확인하고 업데이트해야 합니다.,  # HTTP 사용
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
