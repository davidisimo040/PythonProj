from pathlib import Path
import crypto

enrypted_directory = r'C:\Users\david\Desktop\PythonProj\encrypted'


### parse for file path to obtain name
def file_name(file):
    if not Path(file).exists():
        return False
    return file.split('\\')[-1]


def getSize(file):
    return Path(file).stat().st_size


def getCurrentPrivateKey():
    return crypto.private_key
