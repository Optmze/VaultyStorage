import json
# permission handler
class PermissionHandler:
    def __init__(self,file):
        self.file = file
    

    def getVaultList(self,user):
        with open(self.file) as file:
            permissions = json.load(file)
            data = permissions[user]
        return data['vaults']

    def getCommandList(self,user):
        with open(self.file) as file:
            permissions = json.load(file)
            data = permissions[user]
        return data['commands']


#p = PermissionHandler('storage_core/permissions.json')
#print(p.getCommandList("ayush"))
#print(p.getVaultList("ayush"))
#permissions should have username, vaults allowed and commands allowed
