# 암호화(AES) 알고리즘 문제

## 1. 간단한 암호화(AES) 알고리즘을 구현하여 문자열을 암호화 및 복호화 하는 코드

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_AES(plain_text, key):
    block_size = AES.block_size
    iv = get_random_bytes(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(pad(plain_text.encode(), block_size))
    return iv + encrypted_text

def decrypt_AES(encrypted_text, key):
    block_size = AES.block_size
    iv = encrypted_text[:block_size]
    cipher_text = encrypted_text[block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(cipher_text), block_size).decode()

# 사용 예시
key = get_random_bytes(16)
plain_text = "This is a secret message."
encrypted = encrypt_AES(plain_text, key)
print(f"암호화된 텍스트: {encrypted.hex()}")
decrypted = decrypt_AES(encrypted, key)
print(f"복호화된 텍스트: {decrypted}")
