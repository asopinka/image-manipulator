# Image Manipulation

## Requirements

`python3` and `pip3`

## Install
```
pip3 install -r requirements.txt
```

## Encrypt Image
```
python3 manipulate.py encrypt "<key>" <path-to-image>
```

- `<key>` - your AES-256 encryption key, in double quotes
- `<path-to-image>` - the path of your original image

**Output**
- `encrypted.bmp` - the lossless output and is required for decryption

## Decrypt Image
```
python3 manipulate.py decrypt "<key>" <path-to-encrypted-bmp>
```

- `<key>` - your AES-256 encryption key, in double quotes
- `<path-to-encrypted-bmp>` - the path of the encrypted lossless bmp

**Output**
- `decrypted.jpg` - the decrypted image in jpg format
