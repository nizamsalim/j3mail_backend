from Crypto.PublicKey import RSA as RSAKey
from Crypto.Cipher import PKCS1_OAEP as RSA
from django.conf import settings 
import base64
import json

def decrypt_auth_body_rsa(encrypted_data):
    pvt_key = RSAKey.import_key(settings.PRIVATE_KEY)
    cipher = RSA.new(pvt_key)

    encrypted_bytes = base64.b64decode(encrypted_data)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    decrypted_text = decrypted_bytes.decode("utf-8")
    return json.loads(decrypted_text) # name, email, password | email, password

