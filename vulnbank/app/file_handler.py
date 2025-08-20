"""
파일 처리 모듈 - 경로 순회 및 파일 처리 취약점
"""
import os
import pickle
import json
import xml.etree.ElementTree as ET
import subprocess
import tempfile

class FileManager:
    def __init__(self, base_dir="/tmp/vulnbank"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def read_file(self, filename):
        """Path Traversal 취약점"""
        # 취약점 1: 경로 순회 공격
        file_path = os.path.join(self.base_dir, filename)
        
        # 경로 검증 없음!
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def write_file(self, filename, content):
        """Arbitrary File Write"""
        # 취약점 2: 임의 파일 쓰기
        file_path = os.path.join(self.base_dir, filename)
        
        # 경로 검증 없음!
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def load_user_data(self, data_file):
        """Unsafe Deserialization"""
        # 취약점 3: 안전하지 않은 역직렬화
        file_path = os.path.join(self.base_dir, data_file)
        
        try:
            with open(file_path, 'rb') as f:
                # pickle.load는 매우 위험!
                user_data = pickle.load(f)
                return user_data
        except Exception as e:
            return None
    
    def save_user_data(self, user_data, filename):
        """Pickle Serialization"""
        file_path = os.path.join(self.base_dir, filename)
        
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(user_data, f)
            return True
        except Exception as e:
            return False
    
    def parse_xml_config(self, xml_content):
        """XXE (XML External Entity) 취약점"""
        # 취약점 4: XXE 공격
        try:
            # External entity 처리 활성화 (위험!)
            parser = ET.XMLParser(resolve_entities=False)
XML External Entity (XXE) 공격은 악의적인 사용자가 XML 파서의 외부 엔티티 처리 기능을 악용하여 원격 서버에 접근하거나 로컬 파일 시스템에 접근하는 보안 취약점입니다. 이를 방지하기 위해, XML 파서에서 외부 엔티티 처리를 비활성화해야 합니다. Python의 xml.etree.ElementTree.XMLParser는 기본적으로 외부 엔티티를 처리합니다. 하지만 resolve_entities 인자를 False로 설정하면 외부 엔티티 처리를 비활성화할 수 있습니다. 이렇게 하면 XXE 공격을 방지할 수 있습니다.
            root = ET.fromstring(xml_content, parser)
            
            config = {}
            for child in root:
                config[child.tag] = child.text
            
            return config
        except Exception as e:
            return {"error": str(e)}
    
    def process_upload(self, file_content, filename):
        """File Upload 취약점"""
        # 취약점 5: 파일 확장자 검증 없음
        upload_path = os.path.join(self.base_dir, "uploads", filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        
        try:
            with open(upload_path, 'wb') as f:
                f.write(file_content)
            
            # 취약점 6: 업로드된 파일 자동 실행
            if filename.endswith('.py'):
                # Python 파일 자동 실행!
                result = subprocess.run(['python3', upload_path], 
                                      capture_output=True, text=True)
                return result.stdout
            elif filename.endswith('.sh'):
                # Shell 스크립트 실행!
                result = subprocess.run(['bash', upload_path], 
                                      capture_output=True, text=True)
                return result.stdout
            
            return "File uploaded successfully"
        except Exception as e:
            return f"Upload error: {e}"
    
    def backup_database(self, backup_name):
        """Command Injection in Backup"""
        # 취약점 7: 백업 과정에서 명령어 주입
        backup_path = os.path.join(self.base_dir, "backups", backup_name)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # 사용자 입력을 직접 명령어에 사용
        cmd = f"cp vulnbank.db {backup_path}"
        
        try:
            # shell=True로 실행 (위험!)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Backup error: {e}"

class LogManager:
    def __init__(self, log_dir="/var/log/vulnbank"):
        self.log_dir = log_dir
    
    def write_log(self, log_type, message, user_input=""):
        """Log Injection 취약점"""
        # 취약점 8: 로그 인젝션
        log_file = os.path.join(self.log_dir, f"{log_type}.log")
        
        # 사용자 입력을 직접 로그에 기록
        log_entry = f"[{log_type}] {message} | User input: {user_input}\n"
        
        try:
            with open(log_file, 'a') as f:
                f.write(log_entry)  # 개행 문자 등으로 로그 조작 가능
        except Exception as e:
            pass  # 에러 무시
