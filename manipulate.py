import sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# This program encrypts a jpg With AES-256. The encrypted image contains more data than the original image (e.g. because of 
# padding, IV etc.). Therefore the encrypted image has one row more.

# Get params
args = sys.argv

if len(args) != 4:
    print ("\033[91m Missing arguments \033[0m")
    sys.exit()

operation = args[1]
key = str.encode(args[2])
inputFile = args[3]

# Set mode
mode = AES.MODE_CBC

# Set sizes
keySize = 24
ivSize = AES.block_size

try:
    if operation == "encrypt":
        # Load image
        imageOrig = cv2.imread(inputFile)
        rowOrig, columnOrig, depthOrig = imageOrig.shape

        # Check for minimum width
        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1

        # Convert original image data to bytes
        imageOrigBytes = imageOrig.tobytes()

        # Encrypt
        iv = get_random_bytes(ivSize)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
        ciphertext = cipher.encrypt(imageOrigBytesPadded)

        # Convert ciphertext bytes to encrypted image data
        #    The additional row contains columnOrig * DepthOrig bytes. Of this, ivSize + paddedSize bytes are used 
        #    and void = columnOrig * DepthOrig - ivSize - paddedSize bytes unused
        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
        void = columnOrig * depthOrig - ivSize - paddedSize
        ivCiphertextVoid = iv + ciphertext + bytes(void)
        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

        # Save the encrypted image
        cv2.imwrite("encrypted.bmp", imageEncrypted)

        print ("\033[92m Encryption complete \033[0m")

    elif operation == "decrypt":
        # Convert encrypted image data to ciphertext bytes
        imageEncrypted = cv2.imread(inputFile)
        rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
        rowOrig = rowEncrypted - 1
        encryptedBytes = imageEncrypted.tobytes()
        iv = encryptedBytes[:ivSize]
        imageOrigBytesSize = rowOrig * columnOrig * depthOrig
        paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
        encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

        # Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decryptedImageBytesPadded = cipher.decrypt(encrypted)
        decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

        # Convert bytes to decrypted image data
        decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)

        # Save the encrypted image
        cv2.imwrite("decrypted.jpg", decryptedImage)

        print ("\033[92m Decryption complete \033[0m")

    else:
        print ("\033[91m Invalid operation \033[0m")
except BaseException as err:
    print ("\033[91m Invalid key \033[0m")