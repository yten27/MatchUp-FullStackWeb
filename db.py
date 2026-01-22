import click
import os
import sqlite3
from flask import current_app, g

def get_db_con(pragma_foreign_keys = True):
    if 'db_con' not in g:
        g.db_con = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db_con.row_factory = sqlite3.Row
        if pragma_foreign_keys:
            g.db_con.execute('PRAGMA foreign_keys = ON;')
    return g.db_con

def close_db_con(e=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

@click.command('init-db')
def init_db():
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass
    db_con = get_db_con()
    with current_app.open_resource('sql/drop_matches.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    with current_app.open_resource('sql/create_matches.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    click.echo('Database has been initialized.')


# Neue Funktion zum Abrufen aller Matches
def get_all_matches():
    db_con = get_db_con()
    return db_con.execute(
        """
        SELECT id, title, location, match_time, price, host_user_id
        FROM match
        ORDER BY match_time DESC
        """
    ).fetchall()
    return matches

def get_user_note(user_id: int) -> str:
    db_con = get_db_con()
    #öffnet db verbingung mit user_id und gibt string(text) wieder
    row = db_con.execute(
        "SELECT content FROM note WHERE user_id = ?",
        (user_id,)
    ).fetchone()#eine zeile oder none
    #sucht in tabelle Note nur den Text(content) für spezifischen spieler
    return row["content"] if row else ""
    #text zurückgeben wenn da, leeren text wenn nicht

def upsert_user_note(user_id: int, content: str) -> None:
    #Notize speichern oder umschreiben, rückgabe None -> nur DB Operation
    db_con = get_db_con()
    db_con.execute(
        """
        INSERT INTO note (user_id, content, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id)
        DO UPDATE SET content = excluded.content, updated_at = CURRENT_TIMESTAMP
        """,
        #wenn keine notiz, neue zeile wird angelegt, updated_at für aktualisierung (INSERT oder UPDATE)
        # ON CONFLICT: user_id unique, bei neuer notiz kein neuer eintrag sondern aktualisierung(text/zeit überschreibung)
        (user_id, content)
    )
    db_con.commit()
    # änderung dauerhaft speichern