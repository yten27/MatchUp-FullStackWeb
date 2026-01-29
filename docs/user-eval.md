---
title: User Evaluation
nav_order: 4
---

{: .label }
[Ayten Teshome]

{: .no_toc }
# User evaluation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: [Title]

### Meta

Status
: Done 

Updated
: 26-Jan-2026

### Goal

Ziel der Evaluation war es zu untersuchen,
wie gut Nutzer Matches erstellen, finden und ihnen beitreten können,
und ob zeitliche Regeln (z. B. Mindestvorlauf von 2 Stunden) verständlich sind oder zu Frustration führen.

Konkret wollten wir beantworten:
	•	Wie lange benötigen Nutzer, um ein Match zu erstellen?
	•	Werden zeitliche Einschränkungen korrekt verstanden?
	•	Gibt es Abbrüche oder Verwirrung im Erstellungs- oder Beitrittsprozess?



### Method

Wir haben eine moderierte Usability-Session mit sechs Testpersonen gemacht – Studierende, 20 bis 26 Jahre, technisch affin, aber nichts von dem Projekt gehört.

Jede Person hat diese Aufgaben durchlaufen:
- Neues Konto registrieren
- Ein neues Match anlegen
- Versuch, ein Match mit zu frühem Startzeitpunkt zu erstellen
- Bei einem bestehenden Match beitreten
- Eigene Matches aufrufen (Host- und Teilnehmer-Ansicht)

Währenddessen wurde gemessen:
- Bearbeitungszeiten
- Abbrüche dokumentiert
- Verständnisprobleme laut ausgesprochen (Think-Aloud)

Zum Schluss gab es ein kurzes, offenes Interview.


### Results

•   Registrierung:
- Dauer im Schnitt 1–2 Minuten
- Keine Abbrüche

Match-Erstellung:
- Dauer ca. 2–3 Minuten
- 4 von 6 Nutzern haben zuerst versucht, ein Match weniger als 2 Stunden vorher anzulegen
- Alle vier Nutzer verstanden nach der Fehlermeldung sofort, worum es ging

Beitritt zu Matches:
- Erfolgsquote 100 %
- Keine Missverständnisse zu Kosten oder Teilnahme

Vergangene Matches:
- Nutzer fanden positiv, dass vergangene Matches nicht mehr öffentlich sichtbar sind
- Hosts verstehen intuitiv, wieso sie ihre eigenen Matches weiterhin sehen können

Häufig genannte Rückmeldungen:
- „Gut, dass alte Spiele nicht alles vollmüllen.“
- „Dass der Host alte Matches noch sieht, macht Sinn.“
- „Die Zeitregel ist streng, aber fair.“



### Implications

Aus der Evaluation ziehen wir Folgendes:
- Zeitliche Regeln geben Planungssicherheit und werden akzeptiert, wenn sie klar kommuniziert sind
- Automatisches Löschen hätte zu Verwirrung geführt, besonders bei Hosts
- Die Trennung zwischen öffentlich sichtbaren Matches und Host-Sicht ist verständlich und sinnvoll

Darauf basierend haben wir umgesetzt:
- Die 2-Stunden-Regel ist fest implementiert
- Vergangene Matches sind nur noch für Teilnehmer sichtbar, öffentlich bleiben sie ausgeblendet
- Der Host behält die volle Kontrolle über alte Matches