from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and returns it
    """
    key = Fernet.generate_key()
    return key

def encrypt_message(message, key):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message.decode()

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())

    return decrypted_message.decode()

if __name__ == "__main__":
    key = generate_key()
    print(key)
    message = "abc123"
    encrypted_message = encrypt_message(message, key)
    print('encrypted message: ' + str(encrypted_message))
    decrypted_message = decrypt_message(encrypted_message, key)
    print(decrypted_message)
