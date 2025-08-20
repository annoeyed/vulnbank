# uploads/vulnbank/tests/test_hypo_vulnbank.py
import pytest
from hypothesis import given, strategies as st

# 대상 모듈 (vulnbank.main)
try:
    from vulnbank.main import VulnBankApp
except ImportError:
    pytest.skip("VulnBankApp not importable", allow_module_level=True)

app = VulnBankApp()

# ------------------------------------------------------
# 1. SQL Injection 취약점 테스트
# ------------------------------------------------------
@given(
    user=st.text(alphabet=st.characters(blacklist_categories=["Cs"]), min_size=1, max_size=10),
    pw=st.text(alphabet=st.characters(blacklist_categories=["Cs"]), min_size=1, max_size=10),
)
def test_sql_injection(user, pw):
    res = app.vulnerable_login(user, pw)
    dangerous_tokens = ["'", "\"", ";", "--", "/*", " OR ", " AND "]
    if any(tok in user or tok in pw for tok in dangerous_tokens):
        assert res is None or res == "SQLi suspected!", f"SQLi suspected! {user=} {pw=}"

# ------------------------------------------------------
# 2. XSS (Cross-Site Scripting) 검증
# ------------------------------------------------------
@given(payload=st.text(min_size=1, max_size=20))
def test_xss_injection(payload):
    resp = app.admin_panel(payload)
    if "<script>" in payload.lower() or "<img" in payload.lower():
        assert "<script>" not in resp and "<img" not in resp, f"XSS detected! {payload}"

# ------------------------------------------------------
# 3. Path Traversal 테스트
# ------------------------------------------------------
@given(fname=st.text(alphabet=st.characters(blacklist_categories=["Cs"]), min_size=1, max_size=15))
def test_path_traversal(fname):
    try:
        res = app.file_operations(fname, "read")
        if "../" in fname or "..\\" in fname:
            assert "Traversal" not in res, f"Path Traversal detected! {fname}"
    except Exception as e:
        if "../" in fname or "..\\" in fname:
            pytest.fail(f"Path Traversal caused exception: {fname} → {e}")

# ------------------------------------------------------
# 4. Command Injection 테스트
# ------------------------------------------------------
@given(cmd=st.text(min_size=1, max_size=20))
def test_command_injection(cmd):
    try:
        result = app.process_transaction(cmd)
        bad_tokens = [";", "&&", "|", "`", "$(", "cat ", "ls ", "rm "]
        if any(tok in cmd for tok in bad_tokens):
            assert "Injection" not in result, f"Command Injection detected! {cmd}"
    except Exception as e:
        if any(tok in cmd for tok in [";", "&&", "|"]):
            pytest.fail(f"Command Injection suspected: {cmd} → {e}")

# ------------------------------------------------------
# 5. Config Injection (환경설정 오염)
# ------------------------------------------------------
@given(cfg=st.dictionaries(keys=st.text(min_size=1, max_size=5), values=st.text(min_size=0, max_size=10)))
def test_config_injection(cfg):
    try:
        result = app.process_config(cfg)
        if any(k.lower() in ["debug", "admin", "root", "password"] for k in cfg.keys()):
            assert not ("true" in str(result).lower()), f"Config Injection detected! {cfg}"
    except Exception as e:
        pytest.skip(f"Config injection test skipped due to exception: {e}")

# ------------------------------------------------------
# 6. 인증 우회 로직 테스트
# ------------------------------------------------------
@given(user=st.text(min_size=1, max_size=10), pw=st.text(min_size=0, max_size=10))
def test_auth_bypass(user, pw):
    res = app.vulnerable_login(user, pw)
    if pw == "" or pw.lower() in ["admin", "letmein", "123456"]:
        assert res is None, f"Auth bypass detected! {user=}, {pw=}"

# ------------------------------------------------------
# 7. 논리적 오류 (Negative Balance)
# ------------------------------------------------------
@given(amount=st.integers(min_value=-1000, max_value=1000))
def test_logic_bug_negative_balance(amount):
    try:
        res = app.process_transaction(amount)
        if amount < 0:
            assert "accepted" not in str(res).lower(), f"Logic bug: negative balance allowed! {amount=}"
    except Exception:
        pass

# ------------------------------------------------------
# 8. Buffer Overflow 유사 (긴 입력값)
# ------------------------------------------------------
@given(payload=st.text(min_size=200, max_size=1000))
def test_long_input_overflow(payload):
    try:
        res = app.admin_panel(payload)
        MAX_PAYLOAD_LENGTH = 5000  # Define a constant for maximum payload length
if len(str(res)) > MAX_PAYLOAD_LENGTH:
    raise ValueError(f"Payload length exceeds maximum limit of {MAX_PAYLOAD_LENGTH} characters.")
else:
    print("Payload is within the acceptable limit.")
    except Exception as e:
        pytest.fail(f"Crash on long input: {e}")

# ------------------------------------------------------
# 9. Race Condition (동시 거래)
# ------------------------------------------------------
def test_race_condition():
    """
    단순 병렬 시뮬레이션: 같은 계좌에 동시에 입금/출금 시 데이터 불일치 발생 가능
    """
    acc = "race_test"
    from concurrent.futures import ThreadPoolExecutor
    def worker(amount):
        return app.process_transaction(acc, amount)
    with ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(worker, [100, -100, 50, -50, 200]))
    # 최종 합산이 일관되지 않으면 취약
    total = sum(r for r in results if isinstance(r, int))
    assert -1000 < total < 1000, f"Race condition suspected! results={results}"

# ------------------------------------------------------
# 10. Insecure Deserialization
# ------------------------------------------------------
@given(blob=st.text(min_size=5, max_size=50))
def test_insecure_deserialization(blob):
    try:
        res = app.process_config({"data": blob})
        if "pickle" in blob.lower() or "eval" in blob.lower():
            assert "executed" not in str(res).lower(), f"Insecure deserialization suspected! {blob}"
    except Exception:
        pass

# ------------------------------------------------------
# 11. Information Disclosure (에러 메시지)
# ------------------------------------------------------
@given(bad_input=st.text(min_size=1, max_size=20))
def test_info_disclosure(bad_input):
    try:
        res = app.admin_panel(bad_input)
        assert "Traceback" not in str(res), f"Error leakage! {res}"
        assert "SELECT " not in str(res), f"SQL leakage! {res}"
    except Exception as e:
        if "Traceback" in str(e):
            pytest.fail(f"Stack trace leaked: {e}")

# ------------------------------------------------------
# 12. Resource Exhaustion (파일 DoS)
# ------------------------------------------------------
@given(fname=st.text(min_size=50, max_size=100))
def test_resource_exhaustion(fname):
    """
    매우 긴 파일명을 줬을 때 DoS 발생 가능 여부
    """
    try:
        res = app.file_operations(fname, "write")
        assert len(fname) < 80 or res is None, f"Resource exhaustion via filename length! {len(fname)}"
    except Exception:
        pass

