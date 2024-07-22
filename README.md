![image](https://github.com/user-attachments/assets/3b21bf52-5415-429e-89be-524e42e1a286)


# VaultyStorage
VaultyStorage is a CLI based tool that provides an easy way for users to securely store and manage access to their files.
For more details or suggestions email me at: ayush.devmail@gmail.com

## Startup Information
This repository can be cloned directly or downloaded from here. To start the client, simply run "app.py". To beginning interacting with the console you must begin with logging in. There is one user by default to showcase how this works, the user's public key and private key files have also been provided in the repository using which the token.txt was signed. You can create and sign your own tokens using the rsa module: 

```
import rsa
def generate_keys():
    (public_key, private_key) = rsa.newkeys(2048)
    with open('public.pem', 'w') as f:
        f.write(public_key.save_pkcs1().decode())
    with open('private.pem', 'w') as f:
        f.write(private_key.save_pkcs1().decode())

def sign_message(message, private_key):
     private_key = rsa.PrivateKey.load_pkcs1(private_key.encode()) 
     signature = rsa.sign(message.encode(), private_key, 'SHA-256')
     with open('token.txt', 'wb') as f:
        f.write(signature)

message = "ayush"
```

To log in: <b> login ayush token.txt</b>
![image](https://github.com/user-attachments/assets/dc0ad204-1d6d-4705-80a8-b02a0f614448)

If you try to use a command without logging in you would get the following error:
![image](https://github.com/user-attachments/assets/a1a72c39-1317-43c3-8598-93991ed44c04)


## Commands and Usage


# VaultyStorage: Technical Documentation



## 1. Introduction

### 1.1 Purpose of Document:
This document lays down the architectural structure and design decisions for the "VaultyStorage Client"

### 1.2 Features of VaultyStorage System:

| No. | Feature | Description |
| --- | ------- | ----------- |
| 1.2.1 | Secure Data Storage | Capability to encrypt and compress user-provided files into organized groups called vaults |
| 1.2.2 | Access Control | RSA authenticated and permission-based access for vaults and commands |
| 1.2.3 | Logging and Auditing | Logging of user actions and a quick way to retrieve them |
| 1.2.4 | Versioning and Snapshots | Allows users to maintain multiple shots or versions of their vaults |

## 2. System Architecture
![image](https://github.com/user-attachments/assets/7f331050-fe78-40c9-a16d-717638619767)

The key components of the system architecture briefly described is as follows:

| No. | Component Name | Description of component |
| --- | -------------- | ------------------------ |
| 2.1 | Bank of Vaults | Represents a collection of encrypted and compressed data storage units known as vaults |
| 2.2 | SettingsHandler | Responsible for managing the settings and configurations of the overall system |
| 2.3 | VaultConstructor | Involved in creation and initialization of new vaults |
| 2.4 | VaultHandler | Responsible for handling the operations and management of the vaults (access and interaction) |
| 2.5 | VersionHandler | Deals with versioning and snapshot management of the vaults, allowing users to maintain multiple versions of their data |
| 2.6 | VaultMapper | Maps the names and IDs for each vault |
| 2.7 | VaultyLogger | Responsible for logging and auditing the actions performed on the vaults |
| 2.8 | CLI Interface | Represents the command-line interface or user interaction layer of the system |
| 2.9 | VaultyAuthenticator | Handles the authentication and access control mechanism for the vaults |
| 2.10 | PermissionHandler | Manages the permissions and access rights associated with the vaults |

## 3. System Design Details

### 3.1 Vault
The vault is the core functionality the system offers, it is defined as a compressed set of encrypted files. A vault object consists of the following:

| No. | Property | Description |
| --- | -------- | ----------- |
| 3.1.1 | vaultID | Every vault is uniquely identified by a vaultID. The IDs are generated using the numerical values of the timestamp of when it is being created |
| 3.1.2 | key | A 32 byte key is generated which will be used during the encryption process |
| 3.1.3 | iv | A 16 byte initialization vector for the encryption process |
| 3.1.4 | fileLocation | The physical location of the vault is being stored |
| 3.1.5 | description | Information about the vault specified by the vault creator |

A group of vaults is called a "bank", which is implemented using the shelve module.

### 3.2 VaultConstructor
This section contains the details for construction and storage of new vaults. When creating a new vault, a folder location is provided which consists of the files that need to be added to the vault. It consists of the following steps:

1. <b>Encryption of the Files:</b> Walkthrough of all the files in the directory and encrypting them using the AES encryption algorithm
2. <b>Packing the Folder:</b> We use the zipfile module to zip all the files in that path and store it as temp.zip. The zipfile module does a walkthrough of all the files (os.walk) and writes the files into the designated zipfile.
3. <b>Storing Vault Information:</b> The associated Vault object with the information on the physical vault is shelved (shelve module) securely. The vaultName and vaultID is stored as a key value pair in vaults.json file, which can be retrieved using the VaultMapper module.

The physical instance of the vault is stored as <b>vaultID.zip</b>

### 3.3 Vault Handler
The VaultHandler defines other actions which can be performed on a given vault:

| No. | Property | Description |
| --- | -------- | ----------- |
|3.3.1| Opening a vault | To open an encrypted vault, the vaultID is retrieved using the VaultMapper and key and iv information is retrieved from the shelved Vault Object, a reverse of the pattern in VaultConstructor is followed|
|3.3.2| Deleting a vault | To delete the vault, the vaultID is retrieved using the VaultMapper, using which the physical instance and corresponding Vault object is deleted! |

### 3.4 VaultMapper
The Vault Mapper retrieves the vaultID using the given VaultName from the vaults.json file

### 3.5 VersionManager.py
The verison manager handles the versioning and snapshot management of the vaults. The storage directory where the
vaults and their corresponding objects that are stored is a git directory where two operations can be performed:

| No. | Property | Description |
| --- | -------- | ----------- |
|3.5.1| snapshot | To open an encrypted vault, the vaultID is retrieved using the VaultMapper and key and iv information is retrieved from the shelved Vault Object, a reverse of the pattern in VaultConstructor is followed|
|3.5.2| revert | To delete the vault, the vaultID is retrieved using the VaultMapper, using which the physical instance and corresponding Vault object is deleted! |

### 3.6 PermissionHandler
The PermissionHandler Manages the permissions and access rights associated with the vaults. In the permissions.json file you
can define the username along with the vaults and commands they are allowed to access. 

```
{
    "ayush":{
        "vaults": ["Vault1"],
        "commands": ["getlog","show_vaults","open_vault","create_vault","delete_vault","history","revert","snapshot","show_snapshots"]
    }
}
```

### 3.7 SettingHandler.py
Reads from the settings.json file which retrieves the filenames for:
- Logging File
- Vaults File
- Permissions File <br>

It also retrieves the stackLength for how many commands the CLI stores when displaying the history of commands used.

### 3.8 VaultyAuthenticator
The system using an RSA based authentication system. This functionality has been showcased using the user "ayush", the idea revolves around the system storing public keys for each user and while logging in the user provides a

### 3.9 VaultyLogger
The vaulty logger module is responsible for two main actions:
- Logging significant interactions and actions in the Vaulty Storage Client
- Fast retrieval of logs for a given day

A log has been defined to have to following three fields: <b> [timestamp]; [log-type]; [description] </b>
- <b>timestamp:</b> A timestamp consists of the system's time and date. For example: <i> 18:54:26 7 July 2024 </i>
- <b>log-type:</b> The log-type specifies the type of log. There are few
- <b>description:</b> Consists of a short description of the log
  
For example:
<i>VLOG;11:25:16;21 July 2024;VIEW_VAULT;Vaults viewed by ayush!</i>

For the fast retrieval of logs for a given day, implementation of a binary search utility has been implemented, since the logs timestamps will always be in sorted order. All logs are stored in a vlog.txt file and can be viewed directly or through the getlogs {date} command.


# VaultyStorage Future Insights
For the future versions, I've planned to add the following:
- Multiple banks and locks to maintain access from different storage client threads
- A VaultyServer and VaultyClient functionality: The idea is that a VaultyClient can make a request for some vault to the VaultyServer, which is responsible for handling multiple VaultyStorage instances at different location. The VaultyServer
  has information on where a certain bank and vault is, a single vault can also be stored across multiple VaultyStorage instances and the server can choose which instance to connect the client to depending on availability and speed. The job
  of authentication will also shift towards the VaultyServer which can manage groups and permissions for each registered client.

