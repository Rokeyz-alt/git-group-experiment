"""患者身份信息脱敏与校验工具模块"""
import hmac


def normalize_id_card(id_card: str | None) -> str:
    """
    作用：身份证号归一化，去除空白并统一末尾大写
    Args:
        id_card: 原始身份证号字符串
    Return:
        归一化后的大写身份证号；输入为空时返回空字符串
    """
    if not id_card:
        return ""
    return "".join(id_card.split()).upper()


def mask_id_card(ciphertext: str | None, secret: str) -> str | None:
    """
    作用：返回身份证号脱敏值
    Args:
        ciphertext: 加密后的身份证号密文
        secret: 解密密钥
    Return:
        脱敏后的身份证号；无有效密文时返回 None
    """
    from app.utils.patient_identity import decrypt_id_card

    value = decrypt_id_card(ciphertext, secret)
    if not value:
        return None
    if len(value) <= 8:
        return f"{value[:2]}***{value[-2:]}"
    return f"{value[:4]}**********{value[-4:]}"


def verify_id_card(id_card: str, ciphertext: str | None, secret: str) -> bool:
    """
    作用：校验身份证号与已保存存密文是否匹配
    Args:
        id_card: 用户输入的身份证号
        ciphertext: 数据库保存的身份证号密文
        secret: 解密密钥
    Return:
        校验通过返回 True，否则返回 False
    """
    if not ciphertext:
        return False
    from app.utils.patient_identity import decrypt_id_card

    decrypted = decrypt_id_card(ciphertext, secret)
    if decrypted is None:
        return False
    return hmac.compare_digest(normalize_id_card(id_card), decrypted)


def decrypt_id_card(ciphertext: str | None, secret: str) -> str | None:
    """
    作用：解密身份证号密文（基线占位实现，项目后续接入正式加密逻辑）
    Args:
        ciphertext: 密文字符串
        secret: 解密密钥
    Return:
        解密后的明文；解密失败返回 None
    """
    if not ciphertext:
        return None
    return ciphertext.replace(secret, "")
