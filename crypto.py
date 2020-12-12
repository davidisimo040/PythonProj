import random
import os


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def cmmdc(a, b):
    if a < b:
        a, b = b, a
    while b > 0:
        c = a % b
        a = b
        b = c
    return a


def generate_e(n):
    while True:
        x = random.randint(1, n - 1)
        if cmmdc(x, n) == 1:
            return x


def write_data(p, q, n, phi_n, e, d):
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
    # p = 0x38792F423F4528482B4D6251655468576D5A7134743777397A24432646294A404E635266556A586E3272357538782F4125442A472D4B6150645367566B597033
    # q = 0x4226452948404D635166546A576E5A7234753777217A25432A462D4A614E645267556B58703273357638792F413F4428472B4B6250655368566D597133743677
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


def decrypt_file(path):
    path_encr = path + r"\encryption.txt"
    path_dec = r"decryption.txt"
    fileRead = open(path_encr, "rb")
    fileWrite = open(path_dec, "w", encoding='utf-8')
    message = str(fileRead.read())
    message = message[2:]
    block_data = message.split(',')
    for i in range(len(block_data) - 1):
        aux = int(block_data[i])
        aux = aux ** private_key[0] % private_key[1]
        fileWrite.write(chr(aux))
    fileRead.close()
    fileWrite.close()
    os.startfile("decryption.txt")
