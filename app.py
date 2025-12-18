import os
import db
import forms
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import RegisterForm

#Grundgerüst

app = Flask(__name__)

#Für Datenbankanbindung:
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'matchup.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)

#Rein für die Testung von DB
@app.route("/insert/sample")
def run_insert_sample():
    db.insert_sample()
    return "Database flushed and populated with some sample MatchUp data."


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html") #ähnlich wie main, lädt base.html grundlayout, GET

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    
    if form.validate_on_submit():
        db_con = db.get_db_con()
        
        # Wir suchen den User mit dieser Email
        # fetchone() gibt uns EINE Zeile zurück oder keine
        user = db_con.execute("SELECT * FROM user WHERE email = ?", [form.email.data]).fetchone()
        
        #   Check:
        # a Wurde ein User gefunden? (user is not None)
        # b) Stimmt das Passwort? (user['password'] == Eingabe)
        if user and user['password'] == form.password.data:
            
            # Wenn Korrekt:
            # Session starten
            session['user_id'] = user['id']
            
            flash('Willkommen zurück!', 'success')

            return redirect(url_for('home'))
            
        else:
            #Entweder Email falsch oder Passwort falsch.
            flash('Email oder Passwort ist falsch.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # löschen die ID aus der Session)
    session.pop('user_id', None)
    flash('Du wurdest ausgewechselt (ausgeloggt).', 'info')
    return redirect(url_for('login'))

#Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():#neuen user hier anlegen: GET + POST
    # 1. Das Formular-Objekt vorbereiten
    form = forms.RegisterForm()
    
    # 2. Die große Entscheidung: Wurde der "Senden"-Knopf gedrückt UND ist alles richtig ausgefüllt?
    if form.validate_on_submit():
        db_con = db.get_db_con()
        
        # 3. Prüfen: Gibt es die Email schon?
        existing_user = db_con.execute("SELECT id FROM user WHERE email = ?", [form.email.data]).fetchone()
        if existing_user:
            flash('Diese Email ist bereits vergeben.', 'danger')
            return render_template('register.html', form=form) # Abbruch und zurück zum Formular

        # 4. Speichern (Der eigentliche Job)
        try:
            cursor = db_con.execute("INSERT INTO user (email, password) VALUES (?, ?)", 
                           [form.email.data, form.password.data])
            db_con.commit()
            
            # 5. Auto-Login (Session)
            new_user_id = cursor.lastrowid
            session['user_id'] = new_user_id
            
            flash('Erfolg!', 'success')
            return redirect(url_for('home')) # 6. Weiterleitung zur Startseite

        except Exception as e:
            flash(f'Fehler: {e}', 'danger')

    # 7. Das passiert ganz am Anfang (GET) ODER wenn Fehler im Formular sind
    return render_template('register.html', form=form)

#Match-Übersicht   
@app.route('/allmatches')
def allmatches():#matches anzeigen die in datenbank hinterlegt wurden, GET
    matches = db.get_all_matches()
    return render_template("allmatches.html", matches = matches)

#Match-Details , GET
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Create Match, GET + POST 
@app.route("/matches/create", methods=['GET', 'POST'])
def create_match():
    #Nur eingeloggte User dürfen Matches erstellen!
    # Ohne Login keine ID -> Absturz.
    if 'user_id' not in session:
        flash('Bitte erst einloggen, um ein Match zu erstellen!', 'warning')
        return redirect(url_for('login'))

    form = forms.CreateMatchForm()

    if form.validate_on_submit():
        db_con = db.get_db_con()
        
        # 2. HOST BESTIMMEN: Wir holen die ID aus der Session
        current_user_id = session['user_id']
        
        # 3. ZEIT FORMATIEREN:
        # Formular liefert ein Python-Datumsobjekt.
        # Datenbank erwartet TEXT. Wir wandeln es um in "YYYY-MM-DD HH:MM"
        time_str = form.match_time.data.strftime('%Y-%m-%d %H:%M')

        try:
            # 4. SPEICHERN (SQL)
            # Hier füllen wir exakt deine Tabellen-Spalten:
            db_con.execute("""
                INSERT INTO match (title, location, match_time, host_user_id) 
                VALUES (?, ?, ?, ?)
            """, [form.title.data, form.location.data, time_str, current_user_id])
            
            db_con.commit()
            
            flash('Match angepfiffen! Dein Spiel wurde erstellt.', 'success')
            # Leitet weiter zur Übersicht
            return redirect(url_for('allmatches'))
            
        except Exception as e:
            flash(f'Foulspiel in der Datenbank: {e}', 'danger')
 
    return render_template("create_match.html", form = form)

#My Matches anzeigen, GET 
@app.route("/my-matches")
def my_matches():
    return render_template("my_matches.html")

#Join Match , Post
@app.route("/matches/<int:match_id>/join")
def join_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Leave Match , Post
@app.route("/matches/<int:match_id>/leave")
def leave_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Delete Match , Post, NUR HOST
@app.route("/matches/<int:match_id>/delete")
def delete_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Nach Aufbau der Seite wird zum Schluss noch die Betragsfunktion, in welcher die Aufteilung des Preises noch geleistet wird