from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.API_KEY_SECRET)


def encrypt_api_key(raw_key):
    return cipher.encrypt(raw_key.encode()).decode()


def decrypt_api_key(encrypted_key):
    return cipher.decrypt(encrypted_key.encode()).decode()