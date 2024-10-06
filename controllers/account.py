from standards import *


def show_account():
    conn, cursor = db_connect()
    cursor.execute(
        "SELECT e.*, g.Gebruikersnaam, g.Wachtwoord FROM ervaringsdeskundigen e JOIN Gebruikers g ON "
        "e.Gebruikers_Gebruiker_id = g.Gebruiker_id WHERE e.Gebruikers_Gebruiker_id = ?",
        (session['user_id'],))
    user = cursor.fetchone()

    if user:
        return render_template('account.html', user=user)
    else:
        return redirect('/')


def update_account():
    if request.method == 'POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        gebruikersnaam = request.form['gebruikersnaam']
        wachtwoord = request.form['wachtwoord']
        postcode = request.form['postcode']
        emailadres = request.form['emailadres']
        telefoonnummer = request.form['telefoonnummer']
        geboortedatum = request.form['geboortedatum']
        bijzonderheden = request.form['bijzonderheden']
        toezichthouder = request.form.get('toezichthouder', '0')
        toezichthouder_naam = request.form.get('toezichthouder_naam', '')
        toezichthouder_emailadres = request.form.get('toezichthouder_emailadres', '')
        toezichthouder_telefoonnummer = request.form.get('toezichthouder_telefoonnummer', '')
        benadering = request.form.get('benadering')
        type_onderzoek = request.form.get('type_onderzoek')
        beschikbaarheid = request.form['beschikbaarheid']

        hashed_wachtwoord = bcrypt.hashpw(wachtwoord.encode('utf-8'), bcrypt.gensalt())

        conn, cursor = db_connect()
        cursor.execute(
            "UPDATE ervaringsdeskundigen SET voornaam = ?, achternaam = ?, Postcode = ?, Emailadres = "
            "?, Telefoonnummer = ?, Geboortedatum = ?, Bijzonderheden = ?, Toezichthouder = ?, Toezichthouder_naam = "
            "?, Toezichthouder_emailadres = ?, Toezichthouder_telefoonnummer = ?, Benadering = ?, Type_onderzoek = ?, "
            "Beschikbaarheid = ? WHERE Gebruikers_Gebruiker_id = ?",
            (voornaam, achternaam, postcode, emailadres, telefoonnummer, geboortedatum, bijzonderheden,
             toezichthouder, toezichthouder_naam, toezichthouder_emailadres, toezichthouder_telefoonnummer, benadering,
             type_onderzoek, beschikbaarheid, session['user_id']))
        cursor.execute("UPDATE Gebruikers SET Gebruikersnaam = ?, Wachtwoord = ? WHERE Gebruiker_id = ?",
                       (gebruikersnaam, hashed_wachtwoord, session['user_id']))
        conn.commit()

    return redirect('/account')
