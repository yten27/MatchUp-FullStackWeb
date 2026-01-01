---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Leon Terencio Otte]

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

[Give a high-level overview of what your app does and how it achieves it: similar to the value proposition, but targeted at a fellow developer who wishes to contribute.]

MatchUP ist eine Webanwendung, die auf dem **Python Flask** Framework basiert. Ziel der Architektur ist eine strikte Trennung von Datenhaltung (SQLite) und Präsentation (HTML und Nutzung von Bootstrap), gesteuert mit den Flask-Routen.

Die App funktioniert wie folgt: 

1.  **Anfrage:** Der Browser des Nutzers sendet eine HTTP-Anfrage (z.B. Login oder "Match erstellen") an den Server.
2.  **Verarbeitung:** Die Flask-App (`app.py`) nimmt die Anfrage entgegen und prüft die Berechtigungen (Session).
3.  **Daten:** Falls nötig, fragt der Server Daten aus der SQLite-Datenbank ab oder speichert neue Einträge.
4.  **Antwort:** Die Daten werden in HTML-Templates (Jinja2) eingefügt und als fertige Webseite an den Nutzer zurückgeschickt.
   

## Codemap

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

### 1. Business Logic (`app.py`)
Dies ist der Einstiegspunkt der Anwendung.
* **Routing:** Hier sind alle URLs definiert (z.B. `/login`, `/allmatches`).
* **View-Funktionen:** Funktionen verarbeiten die Formulareingaben (GET und POST) und steuern den Zugriff auf die Datenbank.

### 2. Database (`db.py`)
Kapselt die Verbindung zur Datenbank.
* `get_db_con()`: Stellt sicher, dass pro Request eine frische Verbindung geöffnet wird.
* `close_db_con()`: Schließt die Verbindung sauber nach der Anfrage.
* `schema.sql` (im SQL Ordner): Definiert die Tabellenstruktur.

### 3. Templates (`/templates`)
Das Frontend basiert auf **Jinja2** Template-Vererbung.
* **`base.html`:** Das Master-Template mit Navigation.
* **`match_*.html` / `*match.html`:** Alles rund um Matches (Liste, Details, Erstellen).

## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]

Diese Konzepte ziehen sich durch den gesamten Code und sorgen für Sicherheit und Stabilität:

### Session-Based Authentication
Die Authentifizierung erfolgt über Server-Sessions.
* **Login: / Registrieren: ** Wenn Email und Passwort korrekt sind, speichern wir die `user_id` in der Session des Browsers.
* **Zugriffsschutz:** Routen wie `create_match` prüfen am Anfang: `if 'user_id' not in session`. Ist der Nutzer nicht eingeloggt, wird er sofort zur Login-Seite umgeleitet und die Funktion bricht ab.

### Resource Management (Datenbank)
Die Datenbankanbindung folgt dem empfohlenen Flask-Muster (`g` object).
* **Verbindung:** Bei jeder Anfrage wird eine neue Verbindung zur SQLite-Datenbank geöffnet.
* **Cleanup:** Sobald die Anfrage fertig ist, schließt Flask die Verbindung automatisch. Dies verhindert Ressourcen-Probleme.

### User Feedback (Flash Messages)
Um dem Nutzer Rückmeldung zu geben, nutzen wir das `flash()`-System von Flask.
* **Erfolg:** Bei Aktionen wie "Match erstellt" senden wir eine Nachricht mit der Kategorie `success` (grüne Box).
* **Fehler:** Bei falschem Passwort oder Datenbankfehlern senden wir `danger` (rote Box).
Diese Nachrichten werden im Base-Template einmalig abgefangen und angezeigt.