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
    import os
import hashlib
password = os.environ.get('PASSWORD')
hashed_password = hashlib.sha256(password.encode()).hexdigest()
'password': hashed_password
1. Hard-coded password를 제거하고, 환경 변수를 통해 비밀번호를 가져오도록 변경하였습니다. 이렇게 하면 코드 내에 비밀번호가 직접 노출되는 것을 방지할 수 있습니다.
2. 비밀번호는 해시 함수를 통해 암호화되어 저장됩니다. 해시 함수는 원래의 비밀번호를 복구할 수 없는 단방향 함수이므로, 해시된 비밀번호가 노출되더라도 원래의 비밀번호를 알아내는 것은 매우 어렵습니다.
3. 추가적으로, salt를 사용하여 해시 함수의 보안성을 높일 수 있습니다. salt는 비밀번호에 추가되는 랜덤한 문자열로, 같은 비밀번호라도 salt가 다르면 다른 해시값이 생성됩니다. 이를 통해 레인보우 테이블 공격 등의 해시 충돌 공격을 방어할 수 있습니다.,  # 평문 패스워드
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
