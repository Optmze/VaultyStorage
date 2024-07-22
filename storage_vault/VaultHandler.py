import os
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import shelve
import base64
from storage_vault import VaultConstructor

class VaultHandler:
    def __init__(self):
        pass

    def openVault(self,vaultID):
        with shelve.open('storage/vaults') as shelf:
            if vaultID in shelf:
                vault = shelf[vaultID]
                key = vault.getKey()
                filename = "storage/bank/" + vaultID + ".zip"
                self.decryptVault(filename,"retrieved",key)
            else:
                print("Error opening vault.")
    
    def deleteVault(self,vaultID):
        with shelve.open('storage/vaults') as shelf:
            del shelf[vaultID]
        
        filepath = "storage/bank/"+ vaultID + ".zip"
        os.remove(filepath)


    def decrypt_file(self,file_path,key):
        with open(file_path,'rb') as file:
             iv = file.read(16)    
             encrypted_data = file.read()
            
        cipher = Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        with open(file_path,'wb') as file:
            file.write(unpadded_data)
        
    def decryptVault(self,zip_path,output_path,key):
        with zipfile.ZipFile(zip_path,'r') as zip_file:
            for file_info in zip_file.infolist():
                file_path = os.path.join(output_path,file_info.filename)
                os.makedirs(os.path.dirname(file_path),exist_ok=True)
                with zip_file.open(file_info) as file:
                    data = file.read()
                    with open(file_path,'wb') as opfile:
                        opfile.write(data)
                    self.decrypt_file(file_path,key)    

