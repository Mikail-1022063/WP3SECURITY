from controllers.user import *
from standards import *


def check_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        conn, cursor = db_connect()
        cursor.execute("SELECT * FROM Gebruikers WHERE gebruikersnaam = ?", (username,))
        user_tuple = cursor.fetchone()

        rol = None

        if user_tuple:
            stored_password = user_tuple[2]
            if isinstance(stored_password, bytes):
                password_matches = bcrypt.checkpw(password, stored_password)
            else:
                password_matches = password == stored_password.encode('utf-8')

            if password_matches:
                session['user_id'] = user_tuple[0]
                rol = user_tuple[3]

                if rol == 'ervaringsdeskundige':
                    cursor.execute(
                        "SELECT Status, Deskundige_id FROM Ervaringsdeskundigen WHERE Gebruikers_Gebruiker_id = ?",
                        (session['user_id'],))
                    ervaringsdeskundigen_tuple = cursor.fetchone()
                    status = ervaringsdeskundigen_tuple[0]
                    deskundige_id = ervaringsdeskundigen_tuple[1]

                    if not status:
                        error = "Uw account is niet actief"
                        return render_template('login.html', error=error)

                user = {
                    'Gebruiker_id': user_tuple[0],
                    'gebruikersnaam': user_tuple[1],
                    'wachtwoord': user_tuple[2],
                    'rol': rol,
                    'Deskundige_id': deskundige_id if rol == 'ervaringsdeskundige' else None
                }
                session['user'] = user
                return redirect('/dashboard')
            else:
                error = "Verkeerde gebruikersnaam of wachtwoord"
                return render_template('login.html', error=error)

    return render_template('login.html')


def check_register():
    if request.method == 'POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        gebruikersnaam = request.form['gebruikersnaam']
        wachtwoord = request.form['wachtwoord']
        hashed_password = bcrypt.hashpw(wachtwoord.encode(), bcrypt.gensalt())
        postcode = request.form['postcode']
        geslacht = request.form['geslacht']
        emailadres = request.form['emailadres']
        telefoonnummer = request.form['telefoonnummer']
        geboortedatum = request.form['geboortedatum']
        bijzonderheden = request.form['bijzonderheden']
        toezichthouder = request.form.get('toezichthouder', '0')
        toezichthouder_naam = request.form.get('toezichthouder_naam', '')
        toezichthouder_emailadres = request.form.get('toezichthouder_emailadres', '')
        toezichthouder_telefoonnummer = request.form.get('toezichthouder_telefoonnummer', '')
        benadering = request.form['benadering']
        type_onderzoek = request.form['type_onderzoek']
        beschikbaarheid = request.form['beschikbaarheid']
        type_beperking = request.form['type_beperking']

        register_er_user(voornaam, achternaam, gebruikersnaam, hashed_password, postcode, geslacht, emailadres,
                         telefoonnummer, geboortedatum, bijzonderheden, toezichthouder, toezichthouder_naam,
                         toezichthouder_emailadres, toezichthouder_telefoonnummer, benadering, type_onderzoek,
                         beschikbaarheid, type_beperking)

        return redirect('/')
    else:
        return render_template('register.html')


def check_org_register():
    if request.method == 'POST':
        gebruikersnaam = request.form['gebruikersnaam']
        wachtwoord = request.form['wachtwoord']
        hashed_password = bcrypt.hashpw(wachtwoord.encode(), bcrypt.gensalt())
        naam = request.form['naam']
        type = request.form['type']
        website = request.form['website']
        beschrijving = request.form['beschrijving']
        contactpersoon = request.form['contactpersoon']
        email = request.form['email']
        telefoonnummer = request.form['telefoonnummer']
        overige_details = request.form['overige_details']
        N = 6
        api_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

        register_org_user(gebruikersnaam, hashed_password, naam, type, website, beschrijving, contactpersoon, email,
                          telefoonnummer, overige_details, api_key)

        return redirect('/dashboard')
    else:
        return render_template('organisatie_register.html')


def check_logout():
    logout = "Succesvol uitgelogd"
    session.pop('user', None)
    return render_template('login.html', logout=logout)
