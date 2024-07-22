import rsa
'''
CODE FOR GENERATING USER KEY PAIRS AND SIGNATURE GENERATION

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
'''
class VaultyAuthenticator:
    def __init__(self):
        pass

    def verify_message(self,message, signature, public_key):
        public_key = rsa.PublicKey.load_pkcs1(public_key.encode())
        try:
            rsa.verify(message.encode(), signature, public_key)
            return True
        except rsa.VerificationError:
            return False
    
    def verifyToken(self,username,filename):
        with open('public.pem', 'r') as f:
            public_key = f.read()
        with open(filename, 'rb') as f:
            signature = f.read()
        
        verification_result = self.verify_message(username, signature, public_key)
        return verification_result
    
    def availableCommands(self):
        # read from a permission metadatabase
        pass
    
    def availableVaults(self):
        pass