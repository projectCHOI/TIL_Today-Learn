
# RSA 방식
##RSA 암호화 및 복호화
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# 1. RSA 키 쌍 생성
def generate_RSA_keys():
    key = RSA.generate(2048)  # RSA 2048비트 키 생성
    private_key = key.export_key()  # 개인 키
    public_key = key.publickey().export_key()  # 공개 키
    return private_key, public_key

# 2. RSA 암호화 함수
def encrypt_RSA(plain_text, public_key):
    public_key = RSA.import_key(public_key)  # 공개 키 가져오기
    cipher = PKCS1_OAEP.new(public_key)  # 암호화 객체 생성
    encrypted_text = cipher.encrypt(plain_text.encode())  # 평문을 암호화
    return encrypted_text

# 3. RSA 복호화 함수
def decrypt_RSA(encrypted_text, private_key):
    private_key = RSA.import_key(private_key)  # 개인 키 가져오기
    cipher = PKCS1_OAEP.new(private_key)  # 복호화 객체 생성
    decrypted_text = cipher.decrypt(encrypted_text)  # 암호문을 복호화
    return decrypted_text.decode()

# 4. RSA 암호화 및 복호화 실습

# 2048비트 RSA 키 쌍 생성
private_key, public_key = generate_RSA_keys()

# 암호화할 평문 (문자열)
plain_text = "This is a secret message."

# RSA 암호화
encrypted = encrypt_RSA(plain_text, public_key)
print(f"암호화된 텍스트: {encrypted.hex()}")  # 암호화된 텍스트를 16진수로 출력

# RSA 복호화
decrypted = decrypt_RSA(encrypted, private_key)
print(f"복호화된 텍스트: {decrypted}")