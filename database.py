import sqlite3
from sqlite3 import Error
from pip._vendor.distlib._backport import shutil
import additional
import os
from pathlib import Path
import crypto


def exists_row(filename):
    """
    Functie ce verifica daca exista fisierul dat ca si input in baza de date actuala;

    :param filename: numele fisierului
    :return: fals- daca exista, path- dupa ce a vazut ca nu exista si l-a creat
    """
    filePath = additional.enrypted_directory + rf'\{filename}'
    if Path(filePath).exists():
        return False
    os.makedirs(filePath)
    return filePath


def sql_connection():
    """
    Functie ce se conecteaza la baza de date
    :return: conexiunea pt baza noastra de date
    """
    try:

        con = sqlite3.connect('mydatabase.db')
        print("Conecatarea s-a realizat cu succes catre baza de date!")
        if not os.path.exists('encrypted'):
            os.makedirs('encrypted')
        return con

    except Error:

        print(Error)


def sql_table(connection):
    """
    Functie ce creeaza o baza de date, in cazul in care nu exista deja aceasta
    :param connection: conexiunea pt baza de date actuala
    :return: None - doar creeaza daca nu exista tabela encryptedDatabase
    """
    cursorObj = connection.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS encryptedDatabase(fileName text PRIMARY KEY, fileType text, encryptedPath text, metodaCriptare text, fileKey text, size text)")
    connection.commit()


def sql_delete(con):
    """
    Functie ce dropeaza un tabel specificat daca exista
    :param con: conexiunea la baza de data curenta
    :return: None, sterge tabela specifica conexiunii curente
    """
    cursorObj = con.cursor()
    cursorObj.execute("DROP TABLE IF EXISTS encryptedDatabase")
    con.commit()


def sql_add(con, file):
    """
    Functie ce adauga in baza de date metadatele despre fisierul file si creeaza in folderul de encryption un folder in care se afla mesajul criptat al acestui file.
    In baza de date se introduc: nume, tip_fisier, size, metoda_criptare si key_for_decryption.

    :param con: conexiunea la baza de data curenta
    :param file: path-ul fisierului ce trebuie adaugat
    :return: None- daca verificarile au trecut cu succes, fisierul nou a fost adaugat cu succes
    """
    cursorObj = con.cursor()
    name = additional.file_name(file)
    if not name:
        print("Invalid PATH or FILE! Please try again!")
        return

    fileName, fileType = name.split('.')

    filePath = exists_row(fileName)
    if not filePath:
        print("Exista deja acest fisier!")
    else:
        params = (
            fileName, fileType, filePath, 'RSA', str(additional.getCurrentPrivateKey()), str(additional.getSize(file)))
        try:
            cursorObj.execute("INSERT INTO encryptedDatabase VALUES(?,?,?,?,?,?)", params)
            con.commit()
            print(f"Fisierul {fileName} a fost inserat cu succes!")
            try:
                finalPath = \
                    cursorObj.execute("SELECT encryptedPath from encryptedDatabase WHERE fileName = ?",
                                      (fileName,)).fetchone()[
                        0]

                crypto.encrypt_file(file, finalPath)
            except Error:
                print(Error)

        except Error:
            print(Error)


def sql_remove(con, fileName):
    """
    Functie care primeste un nume de fisier, iar daca acesta exista, il sterge din baza de date si de asemenea ii sterge folderul criptat asociat file-ului sau.
    :param con: conexiunea la baza de data curenta
    :param fileName: numele fisierului ce trebuie sters
    :return: None- daca fisierul exista, acesta va fi sters din baza de date si fisierul unde sunt stocate criptarile
    """
    cursorObj = con.cursor()
    try:
        rez = \
            cursorObj.execute("SELECT COUNT(*) from encryptedDatabase WHERE fileName = ?", (str(fileName),)).fetchone()[
                0]

        if rez == 0:
            print("Nu exista acest fisier! Incercati altul!")
            return
        try:
            dirToRemove = \
                cursorObj.execute("SELECT encryptedPath from encryptedDatabase WHERE fileName = ?",
                                  (fileName,)).fetchone()[
                    0]

            cursorObj.execute("DELETE FROM encryptedDatabase WHERE fileName = ?", (str(fileName),))
            con.commit()
            print(f"Fisierul {fileName} a fost sters cu succes!")
            shutil.rmtree(dirToRemove)

        except Error:
            print("1", Error)

    except Error:
        print(Error)


def sql_show(con, fileName):
    """
    Functie ce afiseaza decriptat file-ul: fileName, prin decriptarea fisierului cripptat asociat in folderul encrypted, folosind private key-ul sau stocat in metadate on baza de date.
    :param con: conexiunea la baza de data curenta
    :param fileName: numele fisierului ce dorim sa il vizualizam
    :return: None- ia key-ul de decriptare din baza de date si file-ul criptat din folderul de criptate, si in final il decripteaza prin metoda RSA cu key-ul aferent.
    Mesajul decriptat va fi deschis intr-o fereastra.
    """
    cursorObj = con.cursor()
    try:
        rez = \
            cursorObj.execute("SELECT COUNT(*) from encryptedDatabase WHERE fileName = ?", (str(fileName),)).fetchone()[
                0]

        if rez == 0:
            print("Nu exista acest fisier! Incercati altul!")
            return
        try:
            decryption_key = []
            fileToView = \
                cursorObj.execute("SELECT encryptedPath from encryptedDatabase WHERE fileName = ?",
                                  (fileName,)).fetchone()[
                    0]
            private_key = \
                cursorObj.execute("SELECT fileKey FROM encryptedDatabase WHERE fileName = ?", (fileName,)).fetchone()[0]
            private_key = private_key.strip("()").split(",")
            decryption_key.append(int(private_key[0]))
            decryption_key.append(int(private_key[1]))

            print(f"Continutul fisierului {fileName} va fi afisat.\n\n")
            crypto.decrypt_file(fileToView, decryption_key)

        except Error:
            print(Error)

    except Error:
        print(Error)


def sql_showall(con):
    """
    Functie ce afiseaza toate fisierele existente curent in baza de date.
    :param con: conexiunea la baza de data curenta
    :return: None- afiseaza numele tuturor fisierelor curente din baza de date.
    """
    cursorObj = con.cursor()
    try:
        row = cursorObj.execute("SELECT fileName,fileType FROM encryptedDatabase").fetchall()
        if len(row) > 0:
            for r in row:
                print(r[0] + "." + r[1])
        else:
            print("Nu exista momentan niciun fisier in baza de date!\n")
    except Error:
        print(Error)
