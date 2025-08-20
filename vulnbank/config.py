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
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
파일 업로드를 허용하는 경우, 특정 파일 유형만 허용해야 합니다. 이는 악의적인 사용자가 서버에 악성 코드를 업로드하고 실행하는 것을 방지합니다. 
원래 코드에서는 'py', 'sh', 'exe'와 같은 실행 가능한 파일 유형이 허용되었습니다. 이는 매우 위험한 상황이므로, 이러한 유형의 파일은 업로드를 허용하지 않도록 수정하였습니다.
추가로, 업로드된 파일의 내용도 검사하여 악성 코드가 포함되어 있지 않은지 확인하는 것이 좋습니다. 이는 파일 확장자만으로는 악성 코드를 완전히 차단할 수 없기 때문입니다.  # 실행 파일 허용!

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
