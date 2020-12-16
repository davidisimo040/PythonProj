import random
import os


def egcd(a, b):
    """
    Functie pt algoritmul lui Euclid Extins
    a*x+b*y=1
    :param a: intreg a
    :param b: intreg b
    :return: (gcd(a,b) , x , y )
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    """
    Functie ce returneaza inversul lui a modulo m
    :param a: int a
    :param m: int m
    :return: inversul modular a lui a mod m
    """
    g, x, y = egcd(a, m)

    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def cmmdc(a, b):
    """
    Functie ce returneaza cmmmdc a doua numere a si b
    :param a: int a
    :param b: int b
    :return: cmmmdc(a,b)
    """
    if a < b:
        a, b = b, a
    while b > 0:
        c = a % b
        a = b
        b = c
    return a


def generate_e(n):
    """
    Functie ce calculeaza variabila e pt RSA
    :param n: intreg n
    :return: un numar random, mai mic ca n, care sa fie prim cu n
    """
    while True:
        x = random.randint(1, n - 1)
        if cmmdc(x, n) == 1:
            return x


def write_data(p, q, n, phi_n, e, d):
    """
    Functie ce scrie in fisierul "data.txt" informatii despre toate variabilele algoritmului RSA curent
    :param p: prim
    :param q: prim
    :param n: n =p*q, a doua parte din cheia publica si privata
    :param phi_n: phi = (p-1)(q-1)
    :param e: prima parte a cheii publice
    :param d: prima parte a cheii private
    :return: None- scrie in "data.txt" toate aceste valori
    """
    file = open("data.txt", "w")
    file.flush()
    file.write(f"n = {n}\n")
    file.write(f"p = {p}\n")
    file.write(f"q = {q}\n")
    file.write(f"phin(n) = {phi_n}\n")
    file.write(f"d = {d}\n")
    file.write(f"e = {e}\n")
    file.close()


def generate_keys():
    """
    Functie ce returneaza cheia publica si cheia privata pt RSA
    :return: returneaza cele 2 perechi de chei - publica si privata
    """
    p = 31
    q = 37
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = generate_e(phi_n)
    d = modinv(e, phi_n)
    write_data(p, q, n, phi_n, e, d)
    return (e, n), (d, n)


public_key, private_key = generate_keys()


def encrypt_file(initialPath, finalPath):
    """
    Functie ce cripteaza fisierul de la path: initialPath si scrie fisierul criptat la path: finalPath
    :param initialPath: pathul fisierului ce trebuie criptat
    :param finalPath: pathul unde se va stoca fisierul criptat
    :return: None- se cripteaza prin RSA
    """

    fileRead = open(initialPath, "rb")
    finalPath += r"\encryption.txt"
    fileWrite = open(finalPath, "w", encoding='utf-8')
    message = fileRead.read()
    block_data = list(message)
    for i in range(len(message)):
        block_data[i] = block_data[i] ** public_key[0] % public_key[1]
        fileWrite.write(str(block_data[i]))
        fileWrite.write(",")
    fileRead.close()
    fileWrite.close()


def decrypt_file(path, decryption_key):
    """
    Functie ce decripteaza de la pathul: path cu ajutorul cheii private: decryption_key, in modul RSA
    :param path: patul fisierului ce trebuie decriptat
    :param decryption_key: private key pt decriptare
    :return: None- deschide o noua fereastra cu fisierul respectiv decriptat
    """

    path_encr = path + r"\encryption.txt"
    path_dec = r"decryption.txt"
    fileRead = open(path_encr, "rb")
    fileWrite = open(path_dec, "w", encoding='utf-8')
    message = str(fileRead.read())
    message = message[2:]
    block_data = message.split(',')
    for i in range(len(block_data) - 1):
        aux = int(block_data[i])
        aux = aux ** decryption_key[0] % decryption_key[1]
        fileWrite.write(chr(aux))
    fileRead.close()
    fileWrite.close()
    os.startfile("decryption.txt")
