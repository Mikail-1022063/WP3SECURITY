from standards import db_connect


def add_filter(cursor, deskundige_id, type_beperking):
    cursor.execute("INSERT INTO Filters (Ervaringsdeskundigen_Deskundige_id, type_beperking) VALUES (?, ?)",
                   (deskundige_id, type_beperking))


def register_er_user(voornaam, achternaam, gebruikersnaam, hashed_password, postcode, geslacht, emailadres,
                     telefoonnummer, geboortedatum, bijzonderheden, toezichthouder, toezichthouder_naam,
                     toezichthouder_emailadres, toezichthouder_telefoonnummer, benadering, type_onderzoek,
                     beschikbaarheid, type_beperking):
    conn, cursor = db_connect()
    cursor.execute("INSERT INTO Gebruikers (gebruikersnaam, wachtwoord, rol) VALUES (?, ?, ?)",
                   (gebruikersnaam, hashed_password, 'ervaringsdeskundige'))
    cursor.execute(
        "INSERT INTO Ervaringsdeskundigen (Voornaam, Achternaam, Gebruikers_Gebruiker_id, Postcode, Geslacht, "
        "Emailadres, Telefoonnummer, Geboortedatum, Bijzonderheden, Toezichthouder, Toezichthouder_naam, "
        "Toezichthouder_emailadres, Toezichthouder_telefoonnummer, Benadering, Type_onderzoek, Beschikbaarheid) "
        "VALUES (?, ?, LAST_INSERT_ROWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (voornaam, achternaam, postcode, geslacht, emailadres, telefoonnummer, geboortedatum, bijzonderheden,
         toezichthouder, toezichthouder_naam, toezichthouder_emailadres, toezichthouder_telefoonnummer, benadering,
         type_onderzoek, beschikbaarheid))
    deskundige_id = cursor.lastrowid
    add_filter(cursor, deskundige_id, type_beperking)
    conn.commit()
    conn.close()


def register_org_user(gebruikersnaam, hashed_password, naam, type, website, beschrijving, contactpersoon, email,
                      telefoonnummer, overige_details, api_key):
    conn, cursor = db_connect()
    cursor.execute("INSERT INTO Gebruikers (gebruikersnaam, wachtwoord, rol) VALUES (?, ?, ?)",
                   (gebruikersnaam, hashed_password, 'organisatie'))
    cursor.execute(
        "INSERT INTO Organisaties (Naam, Type, Gebruikers_Gebruiker_id, Website, Beschrijving, "
        "Contactpersoon, Email, Telefoonnummer, Overige_details, api_key) "
        "VALUES (?, ?, LAST_INSERT_ROWID(), ?, ?, ?, ?, ?, ?, ?)",
        (naam, type, website, beschrijving, contactpersoon, email, telefoonnummer, overige_details, api_key))
    conn.commit()
    conn.close()


def approve_er_user(voornaam, achternaam):
    conn, cursor = db_connect()
    cursor.execute("UPDATE Ervaringsdeskundigen SET Status = 1 WHERE Voornaam = ? AND Achternaam = ?",
                   (voornaam, achternaam))
    conn.commit()
    conn.close()
