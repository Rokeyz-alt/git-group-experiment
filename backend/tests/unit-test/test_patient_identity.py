"""患者身份工具单元测试（主线基线：身份证相关用例）"""
from app.utils.patient_identity import normalize_id_card, verify_id_card


def test_patient_identity_normalization() -> None:
    """身份证号与手机号应去除空白并统一身份证末尾大小写"""
    assert normalize_id_card("110101 19680118 004x") == "11010119680118004X"
    assert normalize_id_card("138 0000 0004") == "13800000004"


def test_patient_identity_verifies_and_verifies() -> None:
    """身份证号与密文校验逻辑基线验证"""
    assert verify_id_card("110101196801180043", "110101196801180043", "wrong-secret") is False
