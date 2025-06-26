import os
import sys
#storage_core_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage_core')
#print(storage_core_dir)
#sys.path.append(storage_core_dir)
#from storage_core.VaultyException import VaultyException

#from ..storage_core import VaultyException
import datetime
import secrets

class VaultGenerator:
    '''
    Using Timestamped based ID creation 
    '''
    def generateID():
        timeNow = datetime.datetime.now()
        numbers = ''.join(filter(str.isdigit, str(timeNow)))
        return numbers
    
    def keyGenerator():
        key = os.urandom(32)
        return key
    
    def ivGenerator():
        iv = secrets.token_bytes(16)
        return iv



class Vault:
    def __init__(self,fileLocation,description):
        self.vaultID = VaultGenerator.generateID()
        self.key = VaultGenerator.keyGenerator()
        self.iv = VaultGenerator.ivGenerator()
        self.fileLocation = fileLocation
        self.description = description
    
    # getters
    def getVaultID(self):
        return self.vaultID
    
    def getDescription(self):
        return self.description
    
    def getfileLocation(self):
        return self.fileLocation
    
    def getKey(self):
        return self.key
    
    def getIV(self):
        return self.iv
    
    # setters
    def setfileLocation(self,newFileLocation):
        self.fileLocation = newFileLocation
    
    def setVaultID(self,vaultID):
        self.vaultID = vaultID
    
    def setDescription(self,newDescription):
        self.description = newDescription
    



