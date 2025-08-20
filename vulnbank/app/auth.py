"""
인증 시스템 - 매우 취약한 인증 로직
"""
import sqlite3
import hashlib
import pickle
import base64
import subprocess
import os

class AuthManager:
    def __init__(self, db_path="vulnbank.db"):
        self.db_path = db_path
    
    def authenticate(self, username, password):
        """SQL Injection 취약점"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 취약점 1: SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[DEBUG] Executing query: {query}")  # 쿼리 노출
        
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] Database error: {e}")  # 에러 정보 노출
            return None
    
    def login_with_token(self, token):
        """Unsafe Deserialization 취약점"""
        try:
            # 취약점 2: Unsafe Pickle Deserialization
            decoded = base64.b64decode(token)
            user_data = pickle.loads(decoded)  # 매우 위험!
            return user_data
        except Exception as e:
            print(f"Token error: {e}")
            return None
    
    def change_password(self, username, old_password, new_password):
        """Command Injection 취약점"""
        # 취약점 3: Command Injection
        cmd = f"echo 'Changing password for {username}' | tee /tmp/password_change.log"
        try:
            subprocess.run(cmd, shell=True, check=True)  # 위험한 shell 실행
        except Exception as e:
            pass
        
        # 실제 패스워드 변경 (취약한 구현)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 또 다른 SQL Injection
        update_query = f"""
            UPDATE users 
            SET password = '{new_password}' 
            WHERE username = '{username}' AND password = '{old_password}'
        """
        
        cursor.execute(update_query)
        conn.commit()
        conn.close()
    
    def get_user_info(self, user_id):
        """Information Disclosure 취약점"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 취약점 4: 모든 정보 노출
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'password': result[2],  # 패스워드까지 노출!
                'email': result[3],
                'balance': result[4],
                'is_admin': result[5],
                'secret_data': result[6]  # 비밀 데이터도 노출!
            }
        return None
    
    def create_session_token(self, user_data):
        """Weak Cryptography 취약점"""
        # 취약점 5: 약한 암호화
        token_data = f"{user_data['username']}:{user_data['password']}:{user_data['id']}"
        weak_hash = hashlib.md5(token_data.encode()).hexdigest()  # MD5 사용!
        return base64.b64encode(weak_hash.encode()).decode()

def admin_backdoor(command):
    """Hidden Backdoor Function"""
    # 취약점 6: 숨겨진 백도어
    if "secret_admin_mode" in command:
        try:
            import shlex
command = shlex.quote(command)
return subprocess.check_output(command.split(), shell=False)
OS Command Injection은 공격자가 악의적인 명령을 시스템에 주입하여 실행시키는 공격 유형입니다. 이를 방지하기 위해, 사용자로부터 입력받은 명령을 그대로 실행하지 않고, shlex.quote() 함수를 사용하여 안전하게 이스케이프 처리를 해줍니다. 이렇게 하면, 공격자가 악의적인 명령을 주입하는 것을 방지할 수 있습니다.
또한, subprocess.run() 함수를 사용할 때는 shell=True 옵션을 사용하지 않는 것이 좋습니다. shell=True 옵션을 사용하면, 쉘 인젝션 공격에 취약해질 수 있습니다. 따라서, 가능하면 shell=False 옵션을 사용하고, 필요한 경우에만 shell=True 옵션을 사용하되, 명령을 실행하기 전에 반드시 검증과 산정화 과정을 거쳐야 합니다.
        except:
            return subprocess.check_output(command, shell=True)  # Shell injection!
    return "Access denied"
