# AES 방식
## AES 암호화 및 복호화
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 1. AES 암호화 함수
def encrypt_AES(plain_text, key):
    # 블록 크기 설정 (AES는 고정된 16바이트 블록 크기를 사용)
    block_size = AES.block_size

    # 초기화 벡터(IV) 생성 - CBC 모드에서 필수
    iv = get_random_bytes(block_size)

    # AES 암호화 객체 생성 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 평문을 블록 크기에 맞게 패딩하여 암호화
    encrypted_text = cipher.encrypt(pad(plain_text.encode(), block_size))

    # IV와 암호문을 결합하여 반환 (복호화 시 IV도 필요함)
    return iv + encrypted_text

# 2. AES 복호화 함수
def decrypt_AES(encrypted_text, key):
    # 블록 크기 설정
    block_size = AES.block_size

    # IV와 암호문 분리
    iv = encrypted_text[:block_size]
    cipher_text = encrypted_text[block_size:]

    # AES 복호화 객체 생성
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 복호화 및 패딩 제거 후 반환
    return unpad(cipher.decrypt(cipher_text), block_size).decode()

# 3. AES 암호화 및 복호화 실습

# 16바이트(128비트) 대칭 키 생성
key = get_random_bytes(16)

# 암호화할 평문 (문자열)
plain_text = "This is a secret message."

# AES 암호화
encrypted = encrypt_AES(plain_text, key)
print(f"암호화된 텍스트: {encrypted.hex()}")

# AES 복호화
decrypted = decrypt_AES(encrypted, key)
print(f"복호화된 텍스트: {decrypted}")