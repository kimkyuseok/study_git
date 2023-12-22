AES-256 암호화를 위해 Python에서는 `cryptography` 라이브러리를 사용할 수 있습니다. 아래는 간단한 AES-256 암호화 및 복호화 예제입니다. 이 예제를 실행하려면 `cryptography` 라이브러리가 설치되어 있어야 합니다.

```bash
pip install cryptography
```

이제 아래의 코드를 사용하여 AES-256 암호화를 진행할 수 있습니다:

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

def encrypt(data, password):
    # salt 생성
    salt = os.urandom(16)

    # PBKDF2를 사용하여 키 생성
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))

    # AES-256 CBC 모드로 암호화
    cipher = Cipher(algorithms.AES(key), modes.CFB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # 결과를 base64로 인코딩하여 반환
    return urlsafe_b64encode(salt + ciphertext)

def decrypt(encrypted_data, password):
    # base64 디코딩
    data = urlsafe_b64decode(encrypted_data)

    # salt 추출
    salt = data[:16]
    data = data[16:]

    # PBKDF2를 사용하여 키 생성
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))

    # AES-256 CBC 모드로 복호화
    cipher = Cipher(algorithms.AES(key), modes.CFB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()

    return plaintext.decode('utf-8')

# 테스트
plaintext_data = "Hello, AES-256 Encryption!"
password = "MySecretPassword"

# 암호화
encrypted_data = encrypt(plaintext_data.encode('utf-8'), password)
print(f"Encrypted Data: {encrypted_data}")

# 복호화
decrypted_data = decrypt(encrypted_data, password)
print(f"Decrypted Data: {decrypted_data}")
```

이 코드에서는 `cryptography` 라이브러리를 사용하여 PBKDF2와 AES-256 CBC를 구현했습니다. 키 파생 함수(PBKDF2)를 사용하여 비밀번호로부터 키를 생성하고, AES-256 CBC 모드로 데이터를 암호화 및 복호화합니다. 주의할 점은 안전한 비밀번호 관리를 위해 안전한 저장소 및 관리 방법을 사용해야 합니다.