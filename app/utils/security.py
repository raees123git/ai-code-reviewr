import hmac
import hashlib

def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    if not signature:
        return False

    sha_name, signature = signature.split("=")
    if sha_name != "sha256":
        return False

    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature)
