import os
import uuid
from cryptography.fernet import Fernet


def encrypt_files(path: str, key: bytes):
    with open(path, 'rb') as f:
        contents = f.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(path, "wb")as f_encry:
        f_encry.write(contents_encrypted)

def decrypt_files(path, key):
    with open(path, 'rb') as f_encry:
        contents_encrypted = f_encry.read()
    contents_dencrypted = Fernet(key).decrypt(contents_encrypted)
    with open(path, "wb") as f_dencry:
        f_dencry.write(contents_dencrypted)

def generate_key():
    key = Fernet.generate_key()
    return key

def upload_files(dir: str, file:object, key: bytes) -> str:
    """
    Funtion that is responsible for saving files in the uploads folder, rename the 
    uploaded file with a new unique uuid name and finally encrypts the file using the key from the user.
    Params:
    dir: type(str) -> directory to save the encrypted file.
    file: type(object) -> file to operate on.
    key: type(bytes) -> key to use when encrypting the file.
    """
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass
    new_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    # save the uploaded file in the uploads folder
    file_path = os.path.join(dir, file.filename)
    file.save(file_path)
    
    # rename the file that just got saved
    os.renames(file_path, os.path.join(dir, new_name))

    # encrypt the renamed file
    encrypt_files(os.path.join(dir, new_name), key)
    return new_name

def download_files(dir, original_filename, encrypt_filename, key):
    
    decrypt_files(os.path.join(dir, encrypt_filename), key)
    os.renames(os.path.join(dir, encrypt_filename), os.path.join(dir, original_filename))
    return os.path.join(dir, original_filename)

