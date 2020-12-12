import database

if __name__ == "__main__":
    print("Welcome to the EncryptedDatabase TOOL!")
    con = database.sql_connection()
    database.sql_table(con)
    while True:
        ans = input("Dati comanda dorita ( add/remove/show/exit ): \n")
        if ans == "exit":
            break
        if ans == "add":
            path = input("Te rugam introdu pathul! \n")
            database.sql_add(con, path)
        elif ans == "remove":
            filename = input("Te rugam scrie numele fisierului ce il doresti sters!\n")
            database.sql_remove(con, filename)
        elif ans == "show":
            filename = input("Te rugam scrie numele fisierului ce il doresti vizionat!\n")
            database.sql_show(con, filename)
        else:
            print("Comanda inexistenta! Incearca din nou!")
    print("La revedere!")
