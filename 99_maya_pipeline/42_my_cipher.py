# 나만의 암호 만들기
import hashlib
import pickle
from base64 import urlsafe_b64encode, urlsafe_b64decode ,b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
key='vivestudios'
myCipher ={ 'kyuseok':'01068911983' ,
            }
salt=b'viveStudi0sVivestudi0s'
key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 100000)
iv = b'\x00' * 16
data = myCipher['kyuseok']
# 암호화
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
newCipher={}
newCipher['kyuseok'] = encrypted_data
with open('d:/test.kks', 'wb') as file:
    pickle.dump(newCipher, file, protocol=pickle.HIGHEST_PROTOCOL)
# newCipher 를 가지고 원본 가져오기
#encrypted_data = b64decode ( newCipher['kyuseok'] )
#newCipher.get('kyuseok',b'')
script_dict=None
with open('d:/test.kks','rb') as file:
    script_dict = pickle.load(file)
encrypted_value =  script_dict.get('kyuseok', b'')

#urlsafe_b64decode('abcd')
#urlsafe_b64decode(encrypted_value)
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_value) + decryptor.finalize()
print ( decrypted_data.decode() )