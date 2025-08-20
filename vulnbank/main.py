"""
메인 애플리케이션 - 모든 취약점을 하나로 연결
"""
import sys
import os
import json
import threading
import time

# 프로젝트 모듈 import
from vulnbank.app.models import Database, User
from vulnbank.app.auth import AuthManager, admin_backdoor
from vulnbank.app.banking import BankingSystem, LoanCalculator
from vulnbank.app.crypto import VulnerableCrypto, weak_random_bytes
from vulnbank.app.file_handler import FileManager, LogManager
from vulnbank.app.utils import *
from vulnbank.config import *

class VulnBankApp:
    def __init__(self):
        print("🏦 VulnBank 시작 중...")
        
        # 컴포넌트 초기화
        self.db = Database()
        self.auth = AuthManager()
        self.banking = BankingSystem()
        self.crypto = VulnerableCrypto()
        self.file_manager = FileManager()
        self.log_manager = LogManager()
        
        # 취약한 초기화
        self.admin_mode = False
        self.debug_info = {
            'users': [],
            'transactions': [],
            'secrets': ['admin_backdoor_enabled', 'debug_mode_on']
        }
    
    def vulnerable_login(self, username, password):
        """취약한 로그인 프로세스"""
        print(f"[DEBUG] Login attempt: {username}:{password}")  # 패스워드 로깅!
        
        # SQL Injection 취약점
        user = self.auth.authenticate(username, password)
        
        if user:
            # 세션 토큰 생성 (약한 암호화)
            token = self.crypto.generate_session_key()
            
            # 디버그 정보에 사용자 추가
            self.debug_info['users'].append({
                'username': username,
                'password': password,  # 평문 저장!
                'token': token,
                'login_time': time.time()
            })
            
            print(f"[SUCCESS] User {username} logged in")
            return {'status': 'success', 'token': token, 'user': user}
        else:
            print(f"[FAILED] Login failed for {username}")
            return {'status': 'failed', 'error': 'Invalid credentials'}
    
    def process_transaction(self, from_user, to_user, amount, user_input=""):
        """취약한 거래 처리"""
        try:
            # 포맷 스트링 취약점
            formatted_amount = self.banking.format_balance(user_input, amount)
            
            # Race condition 가능
            result = self.banking.transfer_money(from_user, to_user, amount)
            
            # 트랜잭션 로깅 (민감한 정보 포함)
            self.log_manager.write_log(
                'transaction', 
                f"Transfer from {from_user} to {to_user}: {amount}",
                user_input
            )
            
            return {'status': 'success', 'formatted': formatted_amount}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def admin_panel(self, command):
        """관리자 패널 - 백도어 포함"""
        if "admin_mode" in command:
            self.admin_mode = True
            return "Admin mode activated"
        
        if self.admin_mode:
            # 숨겨진 백도어 함수 호출
            import shlex
safe_command = shlex.quote(command)
return admin_backdoor(safe_command)
OS Command Injection은 공격자가 악의적인 OS 명령을 주입하고 실행할 수 있는 보안 취약점입니다. 이는 공격자가 시스템을 제어하거나 민감한 정보를 획득하는 등의 행위를 가능하게 합니다.
위의 수정된 코드에서는 Python의 shlex 모듈의 quote 함수를 사용하여 사용자 입력을 안전하게 처리합니다. 이 함수는 문자열을 안전하게 인용하여 쉘에서 해석되지 않도록 합니다. 이렇게 하면 사용자 입력이 OS 명령으로 실행되는 것을 방지할 수 있습니다.
추가적으로, 사용자 입력을 그대로 OS 명령으로 실행하는 대신, 가능한 경우 사용자 입력을 명령의 인자로만 사용하고, 명령 자체는 하드 코딩하는 것이 좋습니다. 또한, 가능한 경우 사용자 입력을 허용하지 않는 방식으로 코드를 작성하는 것이 가장 안전합니다.
        
        return "Access denied"
    
    def file_operations(self, operation, filename, content=""):
        """파일 작업 - 경로 순회 취약점"""
        if operation == "read":
            return self.file_manager.read_file(filename)
        elif operation == "write":
            return self.file_manager.write_file(filename, content)
        elif operation == "upload":
            return self.file_manager.process_upload(content.encode(), filename)
        elif operation == "backup":
            return self.file_manager.backup_database(filename)
        else:
            return "Unknown operation"
    
    def process_config(self, config_data):
        """설정 처리 - 다양한 취약점"""
        try:
            if isinstance(config_data, str):
                if config_data.startswith('<'):
                    # XML 처리 (XXE 취약점)
                    return self.file_manager.parse_xml_config(config_data)
                elif config_data.startswith('{'):
                    # JSON 처리 (무한 재귀 가능)
                    return parse_json_config(config_data)
                else:
                    # 문자열 evaluation (코드 인젝션)
                    return unsafe_eval(config_data)
            else:
                return {"error": "Invalid config format"}
        except Exception as e:
            return {"error": str(e), "debug_info": self.debug_info}
    
    def stress_test(self, test_type, param):
        """스트레스 테스트 - DoS 취약점들"""
        if test_type == "memory":
            return memory_bomb(param)
        elif test_type == "cpu":
            return cpu_bomb(param)
        elif test_type == "regex":
            return validate_email("a" * param + "@test.com")
        elif test_type == "network":
            return ping_server(param)
        else:
            return "Unknown test type"
    
    def get_debug_info(self):
        """디버그 정보 노출"""
        # 취약점: 민감한 정보 노출
        return {
            'version': '1.0.0-vulnerable',
            'debug_mode': DEBUG,
            'secret_key': SECRET_KEY,
            'users': self.debug_info['users'],
            'database_path': self.db.db_path,
            'admin_mode': self.admin_mode,
            'system_info': {
                'platform': __import__('platform').platform(),
                'python_version': sys.version,
                'current_directory': os.getcwd(),
                'environment_variables': dict(os.environ)
            }
        }

def demonstrate_vulnerabilities():
    """취약점 시연"""
    app = VulnBankApp()
    
    print("\n🚨 취약점 시연 시작 🚨\n")
    
    # 1. SQL Injection
    print("1. SQL Injection:")
    malicious_login = app.vulnerable_login("admin' OR '1'='1", "anything")
    print(f"   결과: {malicious_login['status']}")
    
    # 2. Command Injection
    print("\n2. Command Injection:")
    cmd_result = app.admin_panel("admin_mode; ls -la")
    print(f"   결과: {cmd_result[:100]}...")
    
    # 3. Path Traversal
    print("\n3. Path Traversal:")
    path_result = app.file_operations("read", "../../../etc/passwd")
    print(f"   결과: {path_result[:100]}...")
    
    # 4. XXE Attack
    print("\n4. XXE Attack:")
    xml_payload = """<?xml version="1.0"?>
    <!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <config><setting>&xxe;</setting></config>"""
    xxe_result = app.process_config(xml_payload)
    print(f"   결과: {xxe_result}")
    
    # 5. Code Injection
    print("\n5. Code Injection:")
    code_result = app.process_config("__import__('os').system('whoami')")
    print(f"   결과: {code_result}")
    
    # 6. DoS Attacks
    print("\n6. DoS Attacks:")
    memory_result = app.stress_test("memory", 10)  # 10MB
    print(f"   메모리 DoS: {memory_result}")
    
    regex_result = app.stress_test("regex", 20)  # ReDoS
    print(f"   Regex DoS: {regex_result}")
    
    # 7. Information Disclosure
    print("\n7. Information Disclosure:")
    debug_info = app.get_debug_info()
    print(f"   노출된 정보: {len(debug_info)} 항목")
    
    print("\n✅ 취약점 시연 완료\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demonstrate_vulnerabilities()
    else:
        app = VulnBankApp()
        print("🏦 VulnBank가 실행 중입니다...")
        print("취약점 시연을 보려면: python main.py demo")
        
        # 간단한 인터랙티브 모드
        while True:
            try:
                command = input("\nVulnBank> ").strip()
                if command == "quit" or command == "exit":
                    break
                elif command == "demo":
                    demonstrate_vulnerabilities()
                elif command == "debug":
                    info = app.get_debug_info()
                    print(json.dumps(info, indent=2, default=str))
                elif command.startswith("login "):
                    parts = command.split()
                    if len(parts) >= 3:
                        result = app.vulnerable_login(parts[1], parts[2])
                        print(json.dumps(result, indent=2))
                elif command == "help":
                    print("사용 가능한 명령어:")
                    print("  login <username> <password> - 로그인")
                    print("  demo - 취약점 시연")
                    print("  debug - 디버그 정보 출력")
                    print("  quit - 종료")
                else:
                    print("알 수 없는 명령어. 'help'를 입력하세요.")
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                break
            except Exception as e:
                print(f"오류: {e}")
