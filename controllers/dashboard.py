from standards import *
from controllers.user import *


def show_dashboard():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        rol = user.get('rol', '')

        if rol == 'admin':
            cursor.execute(
                "SELECT Deskundige_id, Voornaam, Achternaam, Status, Telefoonnummer, Emailadres FROM "
                "Ervaringsdeskundigen WHERE Status = 0")
            ervaringsdeskundigen = cursor.fetchall()

            cursor.execute(
                "SELECT Voornaam, Achternaam, Telefoonnummer, Emailadres FROM Ervaringsdeskundigen WHERE Status = 1")
            infos = cursor.fetchall()

            conn.close()
            return render_template('dashboard.html', user=user, ervaringsdeskundigen=ervaringsdeskundigen, infos=infos)
        else:
            return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


def show_organisaties():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        rol = user.get('rol', '')

        if rol == 'admin':
            cursor.execute(
                "SELECT * FROM "
                "Organisaties")
            organisaties = cursor.fetchall()

            conn.close()

            return render_template('organisaties.html', user=user, organisaties=organisaties)
        else:
            return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


def show_ervaringsdeskundigen():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        rol = user.get('rol', '')

        if rol == 'admin':
            cursor.execute("""
                            SELECT E.*, F.type_beperking
                            FROM Ervaringsdeskundigen E
                            LEFT JOIN Filters F ON E.deskundige_id = F.Ervaringsdeskundigen_Deskundige_id
                            WHERE E.Status = 1
                        """)
            ervaringsdeskundigen = cursor.fetchall()

            conn.close()

            return render_template('ervaringsdeskundigen.html', user=user, ervaringsdeskundigen=ervaringsdeskundigen)
        else:
            return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


def show_aanvragen():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        rol = user.get('rol', '')

        if rol == 'admin':
            cursor.execute("""
                            SELECT E.*, F.type_beperking
                            FROM Ervaringsdeskundigen E
                            LEFT JOIN Filters F ON E.deskundige_id = F.Ervaringsdeskundigen_Deskundige_id
                            WHERE E.Status = 0
                        """)
            ervaringsdeskundigen = cursor.fetchall()

            cursor.execute("""
                                        SELECT A.*, E.Voornaam, E.Achternaam, O.Beschrijving, Org.Naam
                                        FROM Aanmeldingen A
                                        INNER JOIN Ervaringsdeskundigen E ON A.DeskundigeId = E.deskundige_id
                                        INNER JOIN Onderzoeksvragen O ON A.OnderzoeksvraagId = O.onderzoek_id
                                        INNER JOIN Organisaties Org ON O.Organisaties_Organisatie_id = Org.organisatie_id
                                        WHERE A.Status = 0
                                    """)
            aanmeldingen = cursor.fetchall()

            conn.close()

            return render_template('aanvragen.html', user=user, ervaringsdeskundigen=ervaringsdeskundigen,
                                   aanmeldingen=aanmeldingen)
        else:
            return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


def approve_request():
    if request.method == 'POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']

        approve_er_user(voornaam, achternaam)

        return redirect('/dashboard')


def fetch_latest_requests(last_fetched_id):
    conn, cursor = db_connect()
    cursor.execute(
        "SELECT Deskundige_id, Voornaam, Achternaam FROM Ervaringsdeskundigen WHERE Deskundige_id > ? AND Status = 0",
        (last_fetched_id,))
    latest_requests = cursor.fetchall()
    conn.close()

    formatted_requests = []
    for request_data in latest_requests:
        request = {
            "id": request_data[0],
            "voornaam": request_data[1],
            "achternaam": request_data[2]
        }
        formatted_requests.append(request)

    return formatted_requests
