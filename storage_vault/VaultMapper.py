# map vault IDs and aliases
'''
refactor to just have a function to get the data
'''
import json
class VaultMapper:
    def __init__(self,filename):
        self.filename = filename

    def getData(self):
        with open(self.filename,'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
            
            return data
    
    def saveData(self,data):
        with open(self.filename,'w') as file:
            json.dump(data,file,indent=2)

    def addVault(self,vaultID,vaultName):
        data = self.getData()
        data[vaultName] = vaultID
        self.saveData(data)

    def retrieveVaultID(self,vaultName):
        data = self.getData()
        return data[vaultName]

    def removeVault(self,vaultName):
        data = self.getData()
        del data[vaultName]
        self.saveData(data)
        


