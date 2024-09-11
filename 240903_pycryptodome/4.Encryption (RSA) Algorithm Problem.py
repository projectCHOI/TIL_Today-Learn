# 암호화(RSA) 알고리즘 문제

## 2. 간단한 암호화(RSA) 알고리즘을 구현하여 문자열을 암호화 및 복호화 하는 코드

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_RSA_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_RSA(plain_text, public_key):
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_text = cipher.encrypt(plain_text.encode())
    return encrypted_text

def decrypt_RSA(encrypted_text, private_key):
    private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_text = cipher.decrypt(encrypted_text)
    return decrypted_text.decode()

# 사용 예시
private_key, public_key = generate_RSA_keys()
plain_text = "This is a secret message."
encrypted = encrypt_RSA(plain_text, public_key)
print(f"암호화된 텍스트: {encrypted.hex()}")
decrypted = decrypt_RSA(encrypted, private_key)
print(f"복호화된 텍스트: {decrypted}")