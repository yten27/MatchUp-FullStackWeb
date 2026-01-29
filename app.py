import os
import db
import forms
from flask import Flask, render_template, redirect, url_for, flash, session, request
from datetime import datetime, timedelta
#
def is_visible_for_public(match_time_str: str, hours_after: int = 2) -> bool:
    # match_time wird als String aus db gelesen
    match_time = datetime.strptime(match_time_str, "%Y-%m-%d %H:%M")
    #Zeitpunkt ab dem match nicht angezeigt werden soll
    cutoff = datetime.now() - timedelta(hours=hours_after)
    #true oder false
    return match_time > cutoff

#Grundgerüst
app = Flask(__name__)
app.config["DEBUG"] = True

#Für Datenbankanbindung:
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'matchup.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)


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
    all_matches = db.get_all_matches()
    #Nut matches anzeigen die 2h im vorraus erstellt wurden, daten bleiben in db vorhanden
    matches = [m for m in all_matches if is_visible_for_public(m["match_time"], hours_after=2)]
    return render_template("allmatches.html", matches = matches)

#Match-Details:
#  Läd ein einzeldes macht
# läd alle teilnehmer
# unterscheidet owner oder joined
# berechnet preis pro person
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    db_con = db.get_db_con()

# match anhand von der id laden + durch JOIN wird auf User Tabelle die email des Host angezeigt
    match = db_con.execute(
        """
        SELECT
            m.*,
            u.email AS host_email
        FROM match m
        JOIN user u ON m.host_user_id = u.id
        WHERE m.id = ?
        """,
        (match_id,)
    ).fetchone()

    if not match:
        return "Match not found", 404

# Teilnehmenr abrufen 
    participants = db_con.execute(
        """
        SELECT u.id, u.email
        FROM user u
        JOIN match_participant mp ON u.id = mp.user_id
        WHERE mp.match_id = ?
        """,
    #Durch join email echte user-infos anzeigen
        (match_id,)
    ).fetchall()

# Preis pro Person berechnen, price / anzahl der Spieler für faire Aufteilung 
    participant_count = len(participants)
    price_per_person = (
        match["price"] / participant_count
        if participant_count > 0 else match["price"]
    )
# Überprüfung des User Status (Host oder User )
    current_user_id = session.get("user_id")
    is_owner = current_user_id == match["host_user_id"]
    is_joined = any(p["id"] == current_user_id for p in participants)

    return render_template(
        "match_detail.html",
        match=match,
        participants=participants,
        is_owner=is_owner,
        is_joined=is_joined,
        price_per_person=price_per_person
    )


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
                INSERT INTO match (title, location, match_time, price, info, host_user_id) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, [form.title.data, form.location.data, time_str, form.price.data, form.info.data, current_user_id])
            
            db_con.commit()
            print("MATCH SAVED TO DATABASE")
            flash("Match erfolgreich erstellt!", "success")
            
            flash('Match angepfiffen! Dein Spiel wurde erstellt.', 'success')
            # Leitet weiter zur Übersicht
            return redirect(url_for('allmatches'))
            
        except Exception as e:
            flash(f'Foulspiel in der Datenbank: {e}', 'danger')
    return render_template("create_match.html", form = form)

#My Matches anzeigen:
# zeigt erstellte und beigetretene Matches 
@app.route("/my-matches")
def my_matches():
    # Zugriff nur bei eingelogten Usern, eigentlich nicht nötig da nicht angezeigt
    if "user_id" not in session:
        flash("Bitte einloggen, um deine Matches zu sehen.", "warning")
        return redirect(url_for("login"))

    db_con = db.get_db_con()
    current_user_id = session["user_id"]
# Alle Matches werden aus DB geladen in denen User Host oder Teilnehmer ist 
    rows = db_con.execute(
        """
        SELECT DISTINCT m.* 
        FROM match m
        LEFT JOIN match_participant mp ON m.id = mp.match_id
        WHERE m.host_user_id = ? OR mp.user_id = ?
        """,
        # DISTINCT = nur ein Match anzeigen egal wie viele Teilnehmer
        # left join stellt sicher das auch matches ohne teilnehmer angezeigt werden (FROM Tabelle voll angezeigt)
        (current_user_id, current_user_id)
    ).fetchall()

    created_matches = []
    joined_matches = []

# Matches aufteilen in erstellte und beigetretene 
    for match in rows:
        if match["host_user_id"] == current_user_id:
            #host sieht alle matches, falls geld nicht ausgezahlt wurde kann weiterhin kontakt durch mail aufgenommen werden
            created_matches.append(match)
        else:
            if is_visible_for_public(match["match_time"], hours_after=2):
                #teilnehmer sehen nur noch aktuelle, besser übersichtlich
                joined_matches.append(match)
# append. fügt element in liste hinzu, matches werden entweder zu erstellt und beigetreten sortiert
    return render_template(
        "my_matches.html",
        created_matches=created_matches,
        joined_matches=joined_matches
    )


@app.route("/notes", methods=["GET", "POST"])
def notes():
    #GET zeigt Notiz Seite, POST speichert die Notiz
    user_id = session["user_id"]
    #notiz des passenden user geladen 

    if request.method == "POST": # Auslöser wenn spieler auf speichern drückt
        content = request.form.get("content", "") # hollt den text aus <textareaname= "content">
        db.upsert_user_note(user_id, content) # übergibt notiz an DB, entscheidet insert oder update in einem durch upsert
        flash("Notizen gespeichert.", "success")
        return redirect(url_for("notes"))

    content = db.get_user_note(user_id) # läd bestehende notiz, string oder leer
    return render_template("notes.html", content=content) # übergibt content an html 


#Buttons für match interaktion

# Join Match

@app.route("/matches/<int:match_id>/join", methods=["POST"])
def join_match(match_id):
#debug wenn nicht eingeloggt kein join möglich
    if "user_id" not in session:
        flash("Bitte einloggen, um einem Match beizutreten.", "warning")
        return redirect(url_for("login"))
    db_con = db.get_db_con()
    current_user_id = session["user_id"]
# fügt Teilnehmner in Match hinzu 
    db_con.execute(
        "INSERT INTO match_participant (user_id, match_id) VALUES (?, ?)",
        (current_user_id, match_id)
    )
    db_con.commit()

    return redirect(url_for("match_detail", match_id=match_id))
# Leave Match
@app.route("/matches/<int:match_id>/leave", methods=["POST"])
def leave_match(match_id):
    db_con = db.get_db_con()
    current_user_id = session["user_id"]
# entfernt Teilnehmer aus Match 
    db_con.execute(
        "DELETE FROM match_participant WHERE user_id = ? AND match_id = ?",
        (current_user_id, match_id)
    )
    db_con.commit()

    return redirect(url_for("match_detail", match_id=match_id))
# Cancel Match (nur Host)
@app.route("/matches/<int:match_id>/cancel", methods=["POST"])
def cancel_match(match_id):
    db_con = db.get_db_con()
    current_user_id = session["user_id"]
# löscht Match aus DB 
    db_con.execute(
        "DELETE FROM match WHERE id = ? AND host_user_id = ?",
        (match_id, current_user_id)
    )
    db_con.commit()

    return redirect(url_for("my_matches"))