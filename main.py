import sys

sys.path.insert(1, 'controllers')
from controllers.login import *
from controllers.dashboard import *
from controllers.account import *
from controllers.standards import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)
app.secret_key = 'XfRaNCJRoHHm4V8G'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../databases/accessibility_hub.db'
db = SQLAlchemy(app)


class Onderzoeksvraag(db.Model):
    __tablename__ = 'onderzoeksvragen'

    onderzoek_id = db.Column(db.Integer, primary_key=True)
    Organisaties_Organisatie_id = db.Column(db.Integer, db.ForeignKey('organisaties.Organisatie_id'), nullable=False)
    organisatie = db.relationship('Organisaties', backref='onderzoeksvragen')
    Status = db.Column(db.Boolean, default=False, nullable=False)
    Beschrijving = db.Column(db.String(500), nullable=False)
    Datum_vanaf = db.Column(db.Date, nullable=False)
    Datum_tot = db.Column(db.Date, nullable=False)
    Locatie = db.Column(db.String(500), nullable=False)
    Beloning = db.Column(db.Boolean, nullable=False)
    Leeftijd_van = db.Column(db.Integer, nullable=False)
    Leeftijd_tot = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'onderzoek_id': self.onderzoek_id,
            'Beschrijving': self.Beschrijving,
            'Organisatie': self.organisatie.Naam,
            'Status': self.Status,
            'Datum_vanaf': self.Datum_vanaf,
            'Datum_tot': self.Datum_tot,
            'Locatie': self.Locatie,
            'Beloning': self.Beloning,
            'Leeftijd_van': self.Leeftijd_van,
            'Leeftijd_tot': self.Leeftijd_tot
        }


class Organisaties(db.Model):
    __tablename__ = 'organisaties'

    Organisatie_id = db.Column(db.Integer, primary_key=True)
    Gebruikers_Gebruiker_id = db.Column(db.Integer, nullable=False)
    Naam = db.Column(db.String(500), nullable=False)
    Type = db.Column(db.String(500), nullable=False)
    Website = db.Column(db.String(500))
    Beschrijving = db.Column(db.String(500))
    Contactpersoon = db.Column(db.String(500), nullable=False)
    Email = db.Column(db.String(500), nullable=False)
    Telefoonnummer = db.Column(db.String(500), nullable=False)
    Overige_details = db.Column(db.String(500))
    api_key = db.Column(db.String(500), nullable=False)


class Ervaringsdeskundigen(db.Model):
    __tablename__ = 'ervaringsdeskundigen'

    Deskundige_id = db.Column(db.Integer, primary_key=True)

    aanmeldingen = db.relationship('Aanmeldingen', backref='ervaringsdeskundigen', overlaps="deskundige")


class Aanmeldingen(db.Model):
    __tablename__ = 'aanmeldingen'

    AanmeldId = db.Column(db.Integer, primary_key=True)
    DeskundigeId = db.Column(db.Integer, db.ForeignKey('ervaringsdeskundigen.Deskundige_id'), nullable=False)
    OnderzoeksvraagId = db.Column(db.Integer, db.ForeignKey('onderzoeksvragen.onderzoek_id'), nullable=False)
    Status = db.Column(db.Integer, nullable=False)

    deskundige = db.relationship('Ervaringsdeskundigen', backref='aanmeldingen_deskundige', overlaps="aanmeldingen")
    onderzoeksvraag = db.relationship('Onderzoeksvraag', backref='aanmeldingen')


@app.route('/', methods=['GET', 'POST'])
def login():
    return check_login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return check_register()


@app.route('/dashboard')
def dashboard():
    return show_dashboard()


@app.route('/organisaties')
def organisaties():
    return show_organisaties()


@app.route('/ervaringsdeskundigen')
def ervaringsdeskundigen():
    return show_ervaringsdeskundigen()


@app.route('/aanvragen')
def aanvragen():
    return show_aanvragen()


@app.route('/disapprove_aanmelding', methods=['POST'])
def disapprove_aanmelding():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        aanmeld_id = request.form['aanmelding_id']

        cursor.execute("""
            UPDATE Aanmeldingen
            SET Status = 2
            WHERE AanmeldId = ?
        """, (aanmeld_id,))

        conn.commit()
        conn.close()

        return redirect('/aanvragen')
    else:
        return redirect('/')


@app.route('/approve_aanmelding', methods=['POST'])
def approve_aanmelding():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        aanmeld_id = request.form['aanmelding_id']

        cursor.execute("""
            UPDATE Aanmeldingen
            SET Status = 1
            WHERE AanmeldId = ?
        """, (aanmeld_id,))

        conn.commit()
        conn.close()

        return redirect('/aanvragen')
    else:
        return redirect('/')


@app.route('/approve', methods=['POST'])
def approve_er():
    return approve_request()


@app.route('/create_organisatie', methods=['GET', 'POST'])
def create_organisatie():
    return check_org_register()


@app.route('/get_latest_requests')
def get_latest_requests():
    last_fetched_id = request.args.get('lastFetchedId')
    latest_requests = fetch_latest_requests(last_fetched_id)
    return jsonify(latest_requests)


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        return update_account()
    else:
        return show_account()


@app.route('/api/onderzoeksvragen', methods=['POST'])
def add_onderzoeksvraag():
    data = request.get_json()
    api_key = data.get('api_key')

    organisatie = Organisaties.query.filter_by(api_key=api_key).first()

    if not organisatie:
        return {'message': 'Invalid API key'}, 401

    datum_vanaf = datetime.strptime(data['Datum_vanaf'], '%Y-%m-%d').date()
    datum_tot = datetime.strptime(data['Datum_tot'], '%Y-%m-%d').date()

    new_vraag = Onderzoeksvraag(Beschrijving=data['vraag'], Status=False,
                                Organisaties_Organisatie_id=organisatie.Organisatie_id,
                                Datum_vanaf=datum_vanaf, Datum_tot=datum_tot,
                                Locatie=data['Locatie'], Beloning=data['Beloning'],
                                Leeftijd_van=data['Leeftijd_van'], Leeftijd_tot=data['Leeftijd_tot'])
    db.session.add(new_vraag)
    db.session.commit()
    return {'message': 'Onderzoeksvraag added successfully'}, 201


@app.route('/onderzoeksvragen')
def show_onderzoeksvragen():
    if 'user' in session:
        user = session['user']
        rol = user.get('rol', '')

        if rol == 'admin':
            onderzoeksvragen = [(onderzoeksvraag, 'not signed up') for onderzoeksvraag in
                                db.session.query(Onderzoeksvraag).all()]
        else:
            deskundige_id = user['Deskundige_id']
            onderzoeksvragen = db.session.query(Onderzoeksvraag, Aanmeldingen.Status).outerjoin(Aanmeldingen,
                                                                                                and_(
                                                                                                    Onderzoeksvraag.onderzoek_id == Aanmeldingen.OnderzoeksvraagId,
                                                                                                    Aanmeldingen.DeskundigeId == deskundige_id)).filter(
                Onderzoeksvraag.Status == True).all()

        onderzoeksvragen = [(onderzoeksvraag, aanmelding_status if aanmelding_status is not None else 'not signed up')
                            for onderzoeksvraag, aanmelding_status in onderzoeksvragen]

        return render_template('onderzoeksvragen.html', onderzoeksvragen=onderzoeksvragen)
    else:
        return redirect('/')


@app.route('/signup_for_onderzoeksvraag', methods=['POST'])
def signup_for_onderzoeksvraag():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        deskundige_id = user['Deskundige_id']
        onderzoeksvraag_id = request.form['onderzoeksvraag_id']

        cursor.execute("""
            INSERT INTO Aanmeldingen (DeskundigeId, OnderzoeksvraagId, Status)
            VALUES (?, ?, 0)
        """, (deskundige_id, onderzoeksvraag_id))

        conn.commit()
        conn.close()

        return redirect('/onderzoeksvragen')


@app.route('/approve_signup', methods=['POST'])
def approve_signup():
    if 'user' in session:
        user = session['user']

        conn, cursor = db_connect()

        signup_id = request.form['signup_id']
        status = request.form['status']

        cursor.execute("""
            UPDATE Aanmeldingen
            SET Status = ?
            WHERE SignUpId = ?
        """, (status, signup_id))

        conn.commit()
        conn.close()

        return redirect('/dashboard')


@app.route('/get_new_onderzoeksvragen/<int:last_id>', methods=['GET'])
def get_new_onderzoeksvragen(last_id):
    new_onderzoeksvragen = db.session.query(Onderzoeksvraag).filter(Onderzoeksvraag.onderzoek_id > last_id).all()
    return jsonify([onderzoeksvraag.serialize() for onderzoeksvraag in new_onderzoeksvragen])


@app.route('/goedkeuren_onderzoeksvraag/<int:id>', methods=['POST'])
def goedkeuren_onderzoeksvraag(id):
    onderzoeksvraag = db.session.get(Onderzoeksvraag, id)
    if onderzoeksvraag:
        onderzoeksvraag.Status = True
        db.session.commit()
        return jsonify(message="Onderzoeksvraag approved successfully", status=onderzoeksvraag.Status), 200
    else:
        return jsonify(message="Onderzoeksvraag not found"), 404


@app.route('/get_onderzoeksvraag_status/<int:id>', methods=['GET'])
def get_onderzoeksvraag_status(id):
    onderzoeksvraag = db.session.get(Onderzoeksvraag, id)
    if onderzoeksvraag:
        return jsonify(status=onderzoeksvraag.Status)
    else:
        return jsonify(message="Onderzoeksvraag not found"), 404


@app.route('/logout')
def logout():
    return check_logout()


if __name__ == '__main__':
    app.run(debug=True, port=8801, host='0.0.0.0')
