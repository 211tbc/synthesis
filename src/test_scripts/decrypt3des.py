from Crypto.Cipher import DES3
import base64
#import os
import logging
import re


'''
from https://secure.wikimedia.org/wikipedia/en/wiki/Triple_DES:

The standards define three keying options:

    * Keying option 1: All three keys are independent.
    * Keying option 2: K1 and K2 are independent, and K3 = K1.
    * Keying option 3: All three keys are identical, i.e. K1 = K2 = K3.

Keying option 1 is the strongest, with 3 x 56 = 168 independent key bits.

Keying option 2 provides less security, with 2 x 56 = 112 key bits. This option is stronger than simply DES encrypting twice, e.g. with K1 and K2, because it protects against meet-in-the-middle attacks.

Keying option 3 is equivalent to DES, with only 56 key bits. This option provides backward compatibility with DES, because the first and second DES operations cancel out. It is no longer recommended by the National Institute of Standards and Technology (NIST),[6] and is not supported by ISO/IEC 18033-3.
'''
#So let's try to get Keying option one working

#Not sure how the cipher object (block size) arrives at picking the keying option?
# the block size for the cipher object; must be 16, 24, or 32 for AES (bytes)
#for DES3 in pycrypto, the block size is 16 or 24 bytes, I just picked 16 because I think that's the compatible size used
#BLOCK_SIZE = 16 #This yields a 16 x 8 = 128 bit 3DES key, which makes no sense given the wikipedia options above.  Must be some translation involved in pycrypto here
#BLOCK_SIZE = 24 #hopefully, this achieves the highest keying option (#1) 24*8=192 which is 168 (3*56) + 24 bit control characters
BLOCK_SIZE = 24

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
#Path to OCC's 3DES 

#use the gendeskey.py file to make a new 3DES secret key

#KEY_PATH ="/home/eric/keys/occ.key"
KEY_PATH = "/home/eric/keys/3des3.txt"
IV_PATH =  "/home/eric/keys/IV3.txt"

log = logging.getLogger(__name__)


def removePadding(BLOCK_SIZE, s):
    'Remove rfc 1423 padding from string.'
    n = ord(s[-1]) # last byte contains number of padding bytes
    if n > BLOCK_SIZE or n > len(s):
        raise Exception('invalid padding')
    print "n padding is: ", n
    
    return s[:-n]
  
def nrPadBytes(BLOCK_SIZE, size):
    'Return number of required pad bytes for block of size.'
    if not (0 < BLOCK_SIZE < 255):
        raise Exception('BLOCK_SIZE must be between 0 and 255')
    return BLOCK_SIZE - (size % BLOCK_SIZE)

def appendPadding(BLOCK_SIZE, s):
    '''Append rfc 1423 padding to string.

    RFC 1423 algorithm adds 1 up to BLOCK_SIZE padding bytes to string s. Each 
    padding byte contains the number of padding bytes.
    '''
    n = nrPadBytes(BLOCK_SIZE, len(s))
    return s + (chr(n) * n)

def decodeDES3(cipher, encoded_string):
    print "encoded string is" 
    print encoded_string
    print "***end of encoded string***"
    #decoded_string = cipher.decrypt(encoded_string)
    #decoded_string = removePadding(BLOCK_SIZE, cipher.decrypt(encoded_string))
    #decoded_string = base64.b64decode(encoded_string)
    decoded_string = removePadding(BLOCK_SIZE, cipher.decrypt(base64.b64decode(encoded_string)))

    return decoded_string

def truncateMeaninglessTrailingCharacters(string):
    #truncating meaningless characters after end of last XML tag
    
    p = re.compile('</ext:Sources>.*', re.DOTALL)
    changed_string = p.sub('</ext:Sources>', string)
#    print "string_parts[0]:"
#    print string_parts[0]
#    print "string_parts[1]"
#    print string_parts[1]
    return changed_string

def decryptFile(encrypted_filepath=None, encrypted_stream=None):
    #keyfile will eventually be uploaded to me from  OCC.  For now, just generate our own using gendeskey until replaced by OCC's. 
    keyfile = open(KEY_PATH, 'r')
    secret = keyfile.read()
    ivfile = open(IV_PATH, 'r')
    #extract the iv file contents to a string, since the API requires an iv string
    iv = ivfile.read()
    
    # create a cipher object using the random secret
    #cipher = DES3.new(secret, DES3.MODE_CFB) 
    # encode a string
    #encoded = EncodeDES3(cipher, "something that's supposed to be kept secret")
    #print 'Encrypted string:', encoded
    cipher = DES3.new(secret, DES3.MODE_CBC, iv)
    #iv = 'testtest'
    #key = 'testtesttesttest'
    #obj = DES3.new(key, DES3.MODE_CBC, iv)
    if encrypted_filepath:
        print 'encrypted_filepath is ', encrypted_filepath
        log.debug('decrypting file path: %s', encrypted_filepath)
        encrypted_stream =  open(encrypted_filepath, 'r')
    elif encrypted_stream:
        log.debug('decrypting file stream: %s', encrypted_stream)
    enc_data = encrypted_stream.read()
    encrypted_stream.close()
    print "encrypted data is ", len(enc_data), "bytes long"
    # decode the encoded string
    decrypted_string = decodeDES3(cipher, enc_data)
    #cleanse characters that may exist between the padding and the </Sources> tag.
    #TURN THIS BACK ON!!!!
    #decrypted_string = truncateMeaninglessTrailingCharacters(decrypted_string)
    print 'Decrypted string:'
    print decrypted_string
    print "***end of decrypted string***"
#    fileoutput = open('/home/eric/Desktop/ikebase64decoded.enc', 'w')
    #fileoutput = open('/home/eric/Desktop/ike3des_decoded.dec', 'w')
#    fileoutput.write(decrypted_string)
    return decrypted_string
#decryptFile('/home/eric/Desktop/encxmstring.txt')
#decryptFile('/home/eric/Desktop/copy.xml')

#decryptFile('/home/eric/Desktop/received_data_2011-04-18_14:44:23.580119_encrypted.xml')
#decryptFile('/home/eric/Alexandria_Consulting/Orlando_HSN/known_good_enc_only.xml.enc')