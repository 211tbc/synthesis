'''
TODO:
- Error checking
- Compression(zip)
- DES
- SHA*
- testing, testing, testing
'''
from conf import settings
from Crypto.Cipher import AES as baseAES
from Crypto.Cipher import Blowfish as baseBlowfish
from Crypto.Cipher import DES as baseDES
from Crypto.Cipher import DES3 as baseDES3
from Crypto.Hash import MD5 as baseMD5
from Crypto import Random
import gnupg

#################################################################
# Master base class from which all subclasses will inherit from #
#################################################################

class Encryption:
    def __init__(self): pass

    def encrypt(self, *args): pass
    def decrypt(self, *args): pass
    def encrypt_file(self, *args): pass
    def decrypt_file(self, *args): pass
    def set_password(self, *args): pass

    def get_result(self): return self.result
    def get_data(self): return self.data

    def set_data(self, data): self.data = data



#######################################################
# Classes to handle all of our hash based encryptions #
#######################################################

# Hash base class, not called directly #
class Hash(Encryption):
    '''
    Base class for all Hash classes.

    Hash.MD5(data='', digest_size=16)
    '''

    def __init__(self):
        Encryption.__init__(self)
    
    def can_encrypt(self): return True
    def can_decrypt(self): return False


# MD5 Class #
class MD5(Hash):
    '''
    Class for generating MD5 hashes.

    MD5(data='', digest_size=16)          => Encryption.Hash.MD5
    MD5.encrypt(data='', digest_size=16)  => Encrypts data, digest_size is optional
    MD5.get_result()                      => Returns encrypted/hashed data
    MD5.get_data()                        => Returns original data
    '''

    def __init__(self, data='', digest_size=16):
        Hash.__init__(self)
        if data:
            self.data = data
            self.result = self.encrypt(data)
    
    def encrypt(self, data='', digest_size=16):
        '''
        Encrypts data, digest_size is optional

        MD5.encrypt(data='', digest_size=16)
        '''

        Hash.encrypt(self, data, digest_size)
        if data:
            self.data = data
            self.enc_object = baseMD5.new(data)
            self.result = self.enc_object.hexdigest()
            return self.result



#########################################################
# Classes to handle all of our cipher based encryptions #
#########################################################

# Cipher base class, not called directly #
class Cipher(Encryption):
    '''
    Base class for all cipher classes.
    '''

    def __init__(self, data=None, key=None, mode=None, iv=None, block_size=None, method="encrypt"):
        Encryption.__init__(self)

        self.block_size = block_size or 16
        self.data = ''
        self.key = ''
        self.result = ''
        self.enc_object = None
        self.pad_char = ''

        if data: self.data = data
        if key: self.key = key
        if mode: self.mode = mode
        if iv: self.iv = iv
        if block_size: self.block_size = block_size
        if method: self.method = method

        if data and key:
            if method == "encrypt": 
                self.encrypt(data, key, block_size)
            elif method == "decrypt":
                self.decrypt(data, key, block_size)

    def can_encrypt(self): return True
    def can_decrypt(self): return True
    def set_key(self, key): self.key = key

    def pad(self, text, size=None, padding=chr(255)):
        if size: self.block_size = size
        
        self.pad_char = padding
        if len(text) == 0: return padding * self.block_size
        if len(text) % self.block_size:
            return text + (self.block_size - len(text) % self.block_size) * padding
        else:
            return text

    def unpad(self, text):
        return text.rstrip(self.pad_char)

    def encrypt(self, data='', key='', block_size=None):
        if data: self.data = data
        if key: self.key = key
        if block_size: self.block_size = block_size
        
        #Encryption.encrypt(self, data=self.data, key=self.key, block_size=self.block_size)
        self.result = self.enc_object.encrypt(self.pad(self.data))
        return self.result

    def decrypt(self, data, key, block_size=None):
        if data: 
            self.data = data
        else:
            if self.result: 
                self.data = self.result
                self.result = None
        if key: self.key = key
        if block_size: self.block_size = block_size
        
        #Encryption.decrypt(self, self.data, self.key, self.block_size)
        self.result = self.unpad(self.enc_object.decrypt(self.pad(self.data)))
        return self.result



# AES Class #
class AES(Cipher):
    '''
    aes = AES()
    encrypted = aes.encrypt("text", "key")
    decrypted = aes.decrypt(encrypted, "key")
    '''

    def __init__(self, data=None, key=None, mode=None, iv=None, block_size=32, method="encrypt"):
        Cipher.__init__(self, data=data, key=key, mode=mode, iv=iv, block_size=block_size, method=method)
    
    def encrypt(self, data, key, block_size=32, mode=baseAES.MODE_ECB, iv=None):
        if iv is None: iv = Random.get_random_bytes(16)
        self.enc_object = baseAES.new(self.pad(key), mode, iv)
        return Cipher.encrypt(self, data=data, key=key, block_size=block_size)

    def decrypt(self, data='', key='', block_size=32, mode=baseAES.MODE_ECB):
        self.enc_object = baseAES.new(self.pad(self.key), mode=mode)
        return Cipher.decrypt(self, data=data, key=key, block_size=block_size)



# Blowfish Class #
class Blowfish(Cipher):
    '''
    blowfish = Blowfish()
    encrypted = blowfish.encrypt("text", "key")
    decrypted = blowfish.decrypt(encrypted, "key")
    '''

    def __init__(self, data=None, key=None, mode=None, iv=None, block_size=32, method="encrypt"):
        Cipher.__init__(self, data=data, key=key, mode=mode, iv=iv, block_size=block_size, method=method)
    
    def encrypt(self, data, key, block_size=32, mode=baseBlowfish.MODE_ECB, iv=None):
        if iv is None: iv = Random.get_random_bytes(8)
        self.enc_object = baseBlowfish.new(self.pad(key), mode, iv)
        return Cipher.encrypt(self, data=data, key=key, block_size=block_size)

    def decrypt(self, data='', key='', block_size=32, mode=baseBlowfish.MODE_ECB):
        self.enc_object = baseBlowfish.new(self.pad(self.key), mode=mode)
        return Cipher.decrypt(self, data=data, key=key, block_size=block_size)



# DES Class #
class DES(Cipher):
    '''
    des = DES()
    encrypted = des.encrypt("text", "key")
    decrypted = des.decrypt(encrypted, "key")
    '''
    
    def __init__(self, data=None, key=None, mode=None, iv=None, block_size=8, method="encrypt"):
        Cipher.__init__(self, data=data, key=key, mode=mode, iv=iv, block_size=block_size, method=method)
    
    def encrypt(self, data, key, block_size=8, mode=baseDES.MODE_ECB, iv=None):
        if iv is None: iv = Random.get_random_bytes(8)
        self.enc_object = baseDES.new(self.pad(key), mode, iv)
        return Cipher.encrypt(self, data=data, key=key, block_size=block_size)

    def decrypt(self, data='', key='', block_size=8, mode=baseDES.MODE_ECB):
        self.enc_object = baseDES.new(self.pad(self.key), mode=mode)
        return Cipher.decrypt(self, data=data, key=key, block_size=block_size)



# 3DES Class #
class DES3(Cipher):
    '''
    des = DES3()
    encrypted = des.encrypt("text", "key")
    decrypted = des.decrypt(encrypted, "key")
    '''
    
    def __init__(self, data=None, key=None, mode=None, iv=None, block_size=16, method="encrypt"):
        Cipher.__init__(self, data=data, key=key, mode=mode, iv=iv, block_size=block_size, method=method)
    
    def encrypt(self, data, key, block_size=16, mode=baseDES3.MODE_ECB, iv=None):
        if iv is None: iv = Random.get_random_bytes(8)
        self.enc_object = baseDES3.new(self.pad(key), mode, iv)
        return Cipher.encrypt(self, data=data, key=key, block_size=block_size)

    def decrypt(self, data='', key='', block_size=16, mode=baseDES3.MODE_ECB):
        self.enc_object = baseDES3.new(self.pad(self.key), mode=mode)
        return Cipher.decrypt(self, data=data, key=key, block_size=block_size)



#############################################################
# Classes to handle all of our public key based encryptions #
#############################################################

# Public key base class, not called directly #
class PublicKey(Encryption):
    '''
    Base class for all public key classes.
    '''

    def can_encrypt(self): return True
    def can_decrypt(self): return True




#GPG class
class GPG(PublicKey):
    def __init__(self, fingerprint='', pass_phrase=''):
        PublicKey.__init__(self)
		
        if settings.PGPHOMEDIR is not None:
            self.enc_object = gnupg.GPG(gnupghome=settings.PGPHOMEDIR)
        else:
            self.enc_object = gnupg.GPG()
        
        self.pass_phrase = self.fingerprint = ''
        
        if settings.PASSPHRASE is not None:
            self.pass_phrase = settings.PASSPHRASE
        
        if settings.FINGERPRINT is not None:
            self.fingerprint = settings.FINGERPRINT

        if pass_phrase: self.pass_phrase = pass_phrase
        if fingerprint: self.fingerprint = fingerprint

    def encrypt(self, data, fingerprint='', pass_phrase='', sign=True):
        if fingerprint: self.fingerprint = fingerprint
        if pass_phrase: self.pass_phrase = pass_phrase
        self.data = data
        
        if sign is True:
            self.result = str(self.enc_object.encrypt(self.data, self.fingerprint, sign=self.fingerprint, passphrase=self.pass_phrase))
        else:
            self.result = str(self.enc_object.encrypt(self.data, self.fingerprint, passphrase=self.pass_phrase))
            
        return str(self.result)

    def encryptFile(self, file_in, file_out=None, fingerprint='', pass_phrase='', sign=True):
        '''
        Can be called 2 different ways, eg.

        gpg = GPG()
        gpg.encryptFile('/tmp/file', '/tmp/file.gpg') # write to file

        gpg = GPG()
        encrypted_data = gpg.encryptFile('/tmp/file') # put encrypted file in memory
        '''

        if fingerprint: self.fingerprint = fingerprint
        if pass_phrase: self.pass_phrase = pass_phrase
        
        with open(file_in, 'r') as f_in:
            if sign is True:
                encrypted_data = str(self.enc_object.encrypt_file(f_in, self.fingerprint, passphrase=self.pass_phrase)).rstrip('\r\n')
            else:
                encrypted_data = str(self.enc_object.encrypt_file(f_in, self.fingerprint)).rstrip('\r\n')

        if file_out is not None:
            with open(file_out, 'w') as f_out:
                f_out.write(encrypted_data)
            return encrypted_data
        else:
            return encrypted_data

    def decrypt(self, data, pass_phrase=''):
        if pass_phrase: self.pass_phrase = pass_phrase
        self.data = data
        
        self.result = self.enc_object.decrypt(self.data, passphrase=self.pass_phrase)
        return str(self.result)
    
    def decryptFile(self, file_in, file_out=None, pass_phrase=''):
        '''
        Can be called 2 different ways, eg.

        gpg = GPG()
        gpg.decryptFile('/tmp/file.gpg', '/tmp/file') # write to file

        gpg = GPG()
        decrypted_data = gpg.decryptFile('/tmp/file.gpg') # put decrypted file in memory
        '''

        if pass_phrase: self.pass_phrase = pass_phrase

        with open(file_in, 'r') as f_in:
            decrypted_data = str(self.enc_object.decrypt_file(f_in, passphrase=self.pass_phrase)).rstrip('\r\n')

        if file_out is not None:
            with open(file_out, 'w') as f_out:
                f_out.write(decrypted_data)
            return decrypted_data
        else:
            return decrypted_data

    def sign(self):
        pass
        
    def verify(self, data):
        return self.enc_object.verify(data)
        
    def listKeys(self, private=False):
        return self.enc_object.list_keys(private)
        
    def findKeys(self, text, private=False):
        keylist = self.listKeys(private)
        return [key for key in keylist for value in key if text in str(key[value])]
        
    def setKey(self, fingerprint):
        self.fingerprint = fingerprint
        print "fingerprint set to {0}".format(self.fingerprint)
        
    def generateKey(self):
        pass
    
    def importKey(self, data):
        return self.enc_object.import_keys(data)
    
    def exportKey(self, file_name, fingerprint='', public_file='', private_file=''):
        if fingerprint: self.fingerprint = fingerprint
        
        if public_file:
            public_key = self.enc_object.export_keys(self.fingerprint)
            with open(file_name, 'w') as f:
                f.write(f, public_key)
            
        if private_file:
             private_key = self.enc_object.export_keys(self.fingerprint, True)
             with open(file_name, 'w') as f:
                f.write(f, private_key)
    
    def deleteKeys(self, fingerprint=''):
        if fingerprint: self.fingerprint = fingerprint
        self.enc_object.delete_keys(self.fingerprint, True)
        self.enc_object.delete_keys(self.fingerprint)
        
    def receiveKeys(self, fingerprint='', server='keys.gnupg.net'):
        return self.enc_object.recv_keys(server, fingerprint)
    
    def importKeyFromServer(self, fingerprint='', server='keys.gnupg.net'):
        pass
    



def main():
    '''
    Example of simple usage...
    
    gpg = GPG()
    #gpg.setKey() isn't needed if settings.py is properly filled out
    gpg.setKey("XXXXXXXXXXXXXXXXXXXX") # fingerprint, full name, email, etc.
    encrypted_data = gpg.encrypt("msg")
    decrypted_data = gpg.decrypt(encrypted_data)
    
    unsigned_encrypted_data = gpg.encrypt("msg", sign=False)
    unsigned_decrypted_data = gpg.decrypt(unsigned_encrypted_data)
    
    
    Supported Ciphers/Hashes/etc:
        Pubkey: RSA, RSA-E, RSA-S, ELG-E, DSA
        Cipher: 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH, CAMELLIA128, CAMELLIA192, CAMELLIA256
        Hash: MD5, SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224
        Compression: Uncompressed, ZIP, ZLIB, BZIP2
    
    We can force these settings(not yet, bad idea anyway) or gpg will work with
    whatever is set inside of our gpg key using setpref. We will only need to worry about this when encrypting/signing
    
    Create your own gpg key set using gpg --gen-key, since GPG.generateKey() is still in development
    If you are using a virtual OS, you may run into entropy problems during key creation..
    When prompted to "do things to gain entropy", just run "ls -alR /" in another terminal
    If that isn't enough, just play around with dd... "dd if=/dev/urandom of=temp.bin bs=1M count=1000;rm -rf temp.bin" etc..

    Example of my settings.py:

    PATH_TO_GPG = '/usr/bin/gpg'
    PGPHOMEDIR = '/home/synthesis/.gnupg'
    PASSPHRASE = 'mypassword'
    FINGERPRINT = '8FF0FFF8'
    '''

    #test code for development.. will change often
    debug = False
    test_cases = True

    if test_cases is True:
        #gpg.encrypt() and gpg.decrypt()
        msg = "This will be encrypted"
        gpg = GPG()
        encrypted_data = gpg.encrypt(msg)
        decrypted_data = gpg.decrypt(encrypted_data)
        
        if debug is True: print "Encrypted = {0}".format(encrypted_data)
        if debug is True: print "Decrypted = {0}".format(decrypted_data)
     
        if decrypted_data == msg:
            print "gpg.encrypt() -> Test Passed"
            print "gpg.decrypt() -> Test Passed"
        else:
            print "!! gpg.encrypt() -> Test Failed !!"
            print "!! gpg.decrypt() -> Test Failed !!"
        encrypted_data = decrypted_data = gpg = msg = None

        #gpg.encryptFile() and gpg.decryptFile()
        from os import remove
        
        gpg = GPG()
        msg = "Testing GPG"
        
        with open('/tmp/testcase.txt', 'w') as f: 
            f.write(msg)
        
        encrypted_data = gpg.encryptFile('/tmp/testcase.txt', '/tmp/testcase.txt.gpg')
        remove('/tmp/testcase.txt')
        
        decrypted_data = gpg.decryptFile('/tmp/testcase.txt.gpg', '/tmp/testcase.txt')
        remove('/tmp/testcase.txt.gpg')

        if debug is True: print "Encrypted = {0}".format(encrypted_data)
        if debug is True: print "Decrypted = {0}".format(decrypted_data)

        if decrypted_data == msg:
            print "gpg.encryptFile() -> Test Passed"
            print "gpg.decryptFile() -> Test Passed"
        else:
            print "!! gpg.encryptFile() -> Test Failed !!"
            print "!! gpg.decryptFile() -> Test Failed !!"
        encrypted_data = decrypted_data = gpg = msg = None

if __name__ == '__main__':
    main()