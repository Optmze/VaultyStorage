import os
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from storage_vault import Vault,VaultMapper
from storage_core import SettingHandler
import shelve


class VaultConstructor:

    def encrypt_file(self,file_path,key,iv):
        with open(file_path,'rb') as file:
            data = file.read()

        padder_data = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder_data.update(data) + padder_data.finalize()

        cipher = Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        with open(file_path,'wb') as file:
            file.write(iv + encrypted_data)
        
    def encrypt_folder(self,folder_path,key,iv):
        for root,dir,files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                self.encrypt_file(file_path,key,iv)



    def storeVault(self,vault):
        with shelve.open('storage/vaults') as shelf:
            vaultID = vault.getVaultID()
            shelf[vaultID] = vault


    def createVault(self,folder_path,vaultName,description):
        vault = Vault.Vault(folder_path,description)
        key = vault.getKey()
        vaultID = vault.getVaultID()
        iv = vault.getIV()
        zip_path = "storage/bank/"+ vaultID + ".zip"
        self.encrypt_folder(folder_path,key,iv)
        with zipfile.ZipFile(zip_path,'w') as zip_file:
            for root,dirs,files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root,file)
                    zip_file.write(file_path)
        self.storeVault(vault)
        s = SettingHandler.SettingHandler('settings.json')
        vm = VaultMapper.VaultMapper(s.getVaultFile())
        vm.addVault(vaultID,vaultName)
        #self.decryptVault(zip_path,key,"retrieved")
        # NEED TO CREATE VAULT OBJECT FROM HERE    

#v = VaultConstructor()
#v.createVault("staged/test","Test Vault")
#v.decryptVault("temp.zip",key,"yolo")
