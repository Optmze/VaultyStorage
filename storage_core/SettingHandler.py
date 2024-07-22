import json
import os

class SettingHandler:
     def __init__(self,filename):
          self.filename = filename
     
     def getData(self):
        with open(self.filename,'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
            
            return data
    
     def getLogFile(self):
         data = self.getData()
         return data['logFile']
     
     def getStackLength(self):
         data = self.getData()
         return data['stackLength']

     def getVaultFile(self):
         data = self.getData()
         return data['vaultsFile']
     
     def getPermissionsFile(self):
         data = self.getData()
         return data['permissionsFile']

# Test Code 
#s = SettingHandler('settings.json')
#print(s.getLogFile())
#print(s.getVaultFile())


#settings_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json')
#settings = SettingHandler(settings_file)
#settings.loadSettings()
#server_info = settings.loadServerInformation()
#print(server_info)

    