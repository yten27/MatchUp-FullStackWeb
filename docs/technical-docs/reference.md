---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
MatchUP

{: .no_toc }
# Reference documentation


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

## Route References:

--- Home 

**Route:** `/`
**Route:** `/home`

**Methods:** `GET`

**Purpose:** Weiterleitung auf Home Page

**Sample output:** Kommt noch

Browser shows: `Browser zeigt das Template `home.html` welches als Einstieg für MatchUP UI dient.`

--- Authentifizieren

**Route:** `/register`

**Methods:** `GET`, `POST`

**Purpose:** Regestrierungsformular anzeigen, Regestrierungsdaten verarbeiten & neuen User anlegen

**Sample output:** Kommt noch
--

**Route:** `/login`

**Methods:** `GET`, `POST`

**Purpose:** Login-Formular anzeigen, Login Daten prüfen & Session setzen

**Sample output:** Kommt noch

--- Match Management

**Route:** `/allmatches`

**Methods:** `GET`

**Purpose:** Anzeige einer Übersicht aller Matches

**Sample output:** Kommt noch
--

**Route:** `/match_detail/<int:match_id>`

**Methods:** `GET`

**Purpose:** Anzeige der Detailinformation zu einem einzelnen Match. In finalen Version soll hier dann auch ein Match beigetreten, verlassen oder gelöscht werden. 

**Sample output:** Kommt noch
--

Browser zeigt das Template `allmatches.html` mit einer Liste von Matches 

**Route:** `/matches/create`

**Methods:** `GET`, `POST`

**Purpose:** Erstellen eines neuen Matches durch den eingeloggten User. Anzeige eines Formulates zum Erstellen eines Matches und Speichern der Formulardaten in die Datenbank.

**Sample output:** Kommt noch
--

**Route:** `/my-matches`

**Methods:** `GET`

**Purpose:** Anzeige aller Matches des von den User erstellten und den Matches, welchen er beigetreten ist.

**Sample output:** Kommt noch
--

**Route:** `/matches/<int:match_id>/join`

**Methods:** `POST`

**Purpose:** Fügt den aktuell eingeloggten User als Teilnehmer zu einem Match dazu. 

**Sample output:** Kommt noch
--

**Route:** `/matches/<int:match_id>/join`

**Methods:** `POST`

**Purpose:** Entfernt den aktuell eingeloggten aus der Teilnehmerliste von dem Match.

**Sample output:** Kommt noch
--

**Route:** `/matches/<int:match_id>/delete`

**Methods:** `POST`

**Purpose:** Löscht das Match aus der gesamten Datenbank. Nur der Host des Matches soll dazu berechtigt sein

**Sample output:** Kommt noch
--
