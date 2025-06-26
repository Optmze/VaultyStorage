import cmd,shelve,json
import time
from colorama import Fore,Style,init
from collections import deque
from storage_core import VaultyLogger as logger
from storage_core import SettingHandler,VaultyAuthenticator, PermissionHandler
from storage_vault import VaultConstructor,VaultHandler, VaultMapper,VersionManager

class StorageShell(cmd.Cmd):
    intro = r'''{0}___   ____            .__   __           _________ __                                      
\   \ /   /____   __ __|  |_/  |_ ___.__./   _____//  |_  ________________     ____   ____  
 \   Y   /\__  \ |  |  \  |\   __<   |  |\_____  \\   __\/  _ \_  __ \__  \   / ___\_/ __ \ 
  \     /  / __ \|  |  /  |_|  |  \___  |/        \|  | (  <_> )  | \// __ \_/ /_/  >  ___/ 
   \___/  (____  /____/|____/__|  / ____/_______  /|__|  \____/|__|  (____  /\___  / \___  >
               \/                 \/            \/                        \//_____/      \/ 
               
{1}Welcome to the VaultyStorage Shell. Type help or ? to list all the available commands
For more help and queries you can contact me at: ayush.devmail@gmail.com (Optmze)
                                                                                  '''.format(Fore.GREEN,Fore.WHITE)
    sh = SettingHandler.SettingHandler('settings.json')
    version = VersionManager.VersionManager('storage')
    prompt = "\n{0}vaulty-storage${1} ".format(Fore.GREEN,Style.BRIGHT)
    file = None

    USER = None
    LOGGED_IN = False

    commandStack = deque([]) # set a variable for how big this can be
    stackLength = sh.getStackLength()
   
    commandList = []
    vaultList = []
   
    vc = VaultConstructor.VaultConstructor()
    vh = VaultHandler.VaultHandler()
    vm = VaultMapper.VaultMapper(sh.getVaultFile())
    vl = logger.VaultyLogger(sh.getLogFile())
    pm = PermissionHandler.PermissionHandler(sh.getPermissionsFile())

    def isAllowedCommand(self,command):
        if command not in self.commandList:
            print(Fore.WHITE + "You are not authorized to that!" + Style.DIM)
            return False
        return True
    
    def hasVaultAccess(self,vault):
        if vault not in self.vaultList:
            return False
        return True
    
    def do_login(self,args):
        'Allows a user to login, must do so before using any command: login {username} {token file}'
        try:
            loginArgs = args.split()
            va = VaultyAuthenticator.VaultyAuthenticator()
            self.USER = loginArgs[0]
            self.LOGGED_IN = va.verifyToken(self.USER,loginArgs[1])
            if self.LOGGED_IN:
                print(Fore.WHITE + self.USER + " sucessfully logged in!" + Style.DIM) 
                self.commandList = self.pm.getCommandList(self.USER)
                self.vaultList = self.pm.getVaultList(self.USER)
        except:
            print(Fore.RED + "Error logging in, please try again" + Style.DIM)



    def logCommand(self,command):                
        if len(self.commandStack) == self.stackLength:
            self.commandStack.popleft()
        self.commandStack.append(command)

    def do_history(self,arg):
        'Returns history stack'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return
        
        if not self.isAllowedCommand('history'):
            return

        cno = 0
        for i in self.commandStack:
            print(cno," ",i)
            cno +=1
        #print("\n")

    def do_getlog(self,arg):
        'Retrieves the logs for a specified date, for example: getlog 13th July 2024'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return
        
        if not self.isAllowedCommand('getlog'):
            return
        
        logs = logger.binary_search_logs("vlog.txt",arg)
        if len(logs) != 0:
            print(Fore.WHITE + "The logs from the date " + arg + " are:" + Style.DIM)
            for log in logs:
                print(log)
            self.vl.log('VIEW_LOGS','{2} viewed {0} logs from date {1}'.format(len(logs),arg,self.USER))
        else:
            print(Fore.RED + "VaultyError: No logs found for that particular date!" + Style.DIM)
        
        self.logCommand("getlog "+arg)

    def do_create_vault(self,arg):
        'Creates the vault from the given folder location: create_vault {folder} {vault name} {description}'
        start = time.time()
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return 
        
        if not self.isAllowedCommand('create_vault'):
            return
        
        try:
            args = self.parse(arg)
            self.vc.createVault(args[0],args[1],args[2])
            print(Fore.WHITE + "New vault " + args[1]  + " created successfully!" + Style.DIM)
            self.vl.log('CREATE_VAULT',"{1} created vault {0}".format(args[1],self.USER))
        except:
            print(Fore.RED + "VaultyError: Failed to create vault" + Style.DIM)
        
        self.logCommand("create_vault "+arg)
        end = time.time()
        print("TIME TAKEN:",end - start)
       
    
    def do_open_vault(self,arg):
        'Opens the specified vault and gives it to specified path: open_vault {vault name}'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return   
           
        if not self.isAllowedCommand('open_vault'):
            return
        
        if not self.hasVaultAccess(arg):
            print(Fore.RED + "VaultyError: Failed to open vault" + Style.DIM)
            return
          
        try:
            ID = self.vm.retrieveVaultID(arg) 
            self.vh.openVault(ID)
            self.vl.log('OPEN_VAULT',"Vault {0} opened by {1}!".format(arg,self.USER))
            print("{0} Succesfully opened vault {1}! {2}".format(Fore.WHITE,arg,Style.DIM))

        except:
            print(Fore.RED + "VaultyError: Failed to open vault" + Style.DIM)
        
        self.logCommand("open_vault "+arg)
            
        

    def do_delete_vault(self,arg):
        'Deletes the specified vault and gives it to the specified path: delete_vault {vault name}'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return
          
        if not self.isAllowedCommand('delete_vault'):
            return
        
        if not self.hasVaultAccess(arg):
            print(Fore.RED + "VaultyError: Failed to delete vault. Are you sure the specified vault exists?" + Style.DIM)
            return
             
        try:
            ID = self.vm.retrieveVaultID(arg)
            self.vh.deleteVault(ID)
            self.vl.log('DELETE_VAULT', "Vault {0} deleted by user {1}!".format(arg,self.USER))
            
            with open(self.sh.getVaultFile(),'r') as file:
                data = json.load(file)
                if arg in data:
                    del data[arg]
            with open(self.sh.getVaultFile(),'w') as file:
                json.dump(data,file,indent=2)   
            
            print("{0} Succesfully deleted vault {1}! {2}".format(Fore.WHITE,arg,Style.DIM))
        except:
            print(Fore.RED + "VaultyError: Failed to delete vault. Are you sure the specified vault exists?" + Style.DIM)
        
        self.logCommand("delete_vault "+arg)



    def do_show_vaults(self,arg):
        'Shows information about all the available vaults'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return
        
        if not self.isAllowedCommand('show_vaults'):
            return
        
        with open(self.sh.getVaultFile(),'r') as file:
            data = json.load(file)
            print("Vault ID and Descriptions: ")
            print("---------------------------")
        with shelve.open('storage/vaults') as shelf:
            for key in shelf.keys():
                vault = shelf[key]
                vaultName = list(data.keys())[list(data.values()).index(vault.getVaultID())]

                if not self.hasVaultAccess(vaultName):
                    continue

                print(f"{Fore.WHITE}Vault Name:{Style.DIM}",vaultName) 
                print(f"{Fore.WHITE}VaultID:{Style.DIM}",vault.getVaultID())
                print(f"{Fore.WHITE}Description:{Style.DIM}",vault.getDescription())
                print("---------------------------")
        
        self.vl.log('VIEW_VAULT', "Vaults viewed by {0}!".format(self.USER))
        self.logCommand("show_vaults")
 

    def do_snapshot(self,arg):
        'Creates a git snapshot of the vault bank: snapshot {message}'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return 

        if not self.isAllowedCommand('snapshot'):
            return
               
        try:
            self.version.commit(arg)
            self.logCommand("snapshot")
            self.vl.log("CREATE_SNAPSHOT","{0} {2} succesfully created snapshot! {1}".format(Fore.WHITE,Style.DIM,self.USER))

        except:
            print(Fore.RED + "VaultyError: Unable to create snapshots" + Style.DIM)


    def do_show_snapshots(self,arg):
        'Shows the hashes for each snapshots'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return        
        try:
            self.version.viewCommits()
            self.logCommand("show_snapshots")
            self.vl.log("SHOW_SNAPSHOT","{0} {2} viewed all available snapshot! {1}".format(Fore.WHITE,Style.DIM,self.USER))
        except:
            print(Fore.RED + "VaultyError: Unable to view snapshots" + Style.DIM)


    def do_revert(self,arg):
        'Revert the bank to specified to hash snapshot: revert {hash}'
        if not self.LOGGED_IN:
            print("You need to log in first!")
            return        
        try:
            self.version.revertCommit(arg)
            self.logCommand("revert " + arg)
            self.vl.log("REVERT","{0} Succesfully reverted to {1}! {2}".format(Fore.WHITE,arg,Style.DIM))

        except:
            print(Fore.RED + "VaultyError: Failed to revert." + Style.DIM)


    def parse(self,arg):
        args = arg.split(" ",2)
        return args
        


if __name__ == '__main__':
    init(autoreset=True)
    StorageShell().cmdloop()

    # TESTS
    #v = VaultConstructor.VaultConstructor()
    #v.createVault("staged","Test Vault")
    #from storage_vault import VaultHandler
    #ID = 20240719151010710073
    #v = VaultHandler.VaultHandler()
    #v.deleteVault("20240720013808944722")
    #v.openVault("20240719155708286472")




