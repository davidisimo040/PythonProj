import sqlite3
from sqlite3 import Error
from pip._vendor.distlib._backport import shutil
import additional
import os
from pathlib import Path
import crypto


def exists_row(n):
    filePath = additional.enrypted_directory + rf'\{n}'
    if Path(filePath).exists():
        return False
    os.makedirs(filePath)
    return filePath


def sql_connection():
    try:

        con = sqlite3.connect('mydatabase.db')
        print("Conecatarea s-a realizat cu succes catre baza de date!")
        if not os.path.exists('encrypted'):
            os.makedirs('encrypted')
        return con

    except Error:

        print(Error)


def sql_table(connection):
    cursorObj = connection.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS encryptedDatabase(fileName text PRIMARY KEY, fileType text, encryptedPath text, metodaCriptare text, fileKey text, size text)")
    connection.commit()


def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute("DROP TABLE IF EXISTS encryptedDatabase")
    con.commit()


def sql_add(con, file):
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
