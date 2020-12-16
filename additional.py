from pathlib import Path
import crypto

enrypted_directory = r'C:\Users\david\Desktop\PythonProj\encrypted'


### parse for file path to obtain name
def file_name(file):
    """
    Functie ce returneaza numele fisierului dintr-un path dat
    :param file: pathul fisierului din care trebuie extras numele
    :return: numele fisierului
    """
    if not Path(file).exists():
        return False
    return file.split('\\')[-1]


def getSize(file):
    """
    Functie ce returneaza size-ul unui fisier dat ca input
    :param file: pathul fisierului
    :return: size-ul fisierului
    """
    return Path(file).stat().st_size


def getCurrentPrivateKey():
    """
    Functie ce returneaza private key curent
    :return: private_key
    """
    return crypto.private_key
