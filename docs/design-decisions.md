---
title: Design Decisions
nav_order: 3
---

{: .label }
[Leon Terencio Otte, Ayten Teshome]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Frontend Styling Framework - Bootstrap & AI Support

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 28-01-2026

### Problem statement

Unser Projektfokus liegt klar auf der Implementierung der Backend-Logik (Python mit Flask). Da wir begrenzte Zeit haben, wollen wir das Design nicht als Priorität definieren. Gleichzeitig soll die App aber nicht wie eine 08/15 Standard Vorlage aussehen, sondern durch und durch nach Fußball aussehen, ohne dass wir wochenlang CSS schreiben müssen.

### Decision

**Wir kombinieren Bootstrap 5 mit KI-gestützter Anpassung.**

1.  **Basis (Bootstrap):** Wir nutzen das Framework für das grobe Layout und funktionale Komponenten (Forms, Buttons, Navigationsleiste). Das spart uns die Arbeit für die Grundstruktur.
2.  **Anpassung (KI-Support):** Um Zeit zu sparen, haben wir KI-Tools genutzt (Gemini), um spezifische CSS-Anpassungen (Custom CSS) zu generieren. Anstatt CSS-Klassen manuell nachzuschlagen, ließen wir uns Code-Snippets für Farbschemata und das Styling erstellen. [[[Link zur kompletten Chatverlauf mit Gemini](https://gemini.google.com/share/3d6b13052522)]]

**Vorteil:** Wir konnten uns auf den Python-Code konzentrieren, haben aber trotzdem ein sauber gestyltes Frontend, das über den Standard-Look hinausgeht.

**Decision was taken by:** github/leongit11

### Regarded options

1.  **Custom CSS (Alles selbst schreiben)**
2.  **Bootstrap Standard (Ohne Anpassung)**
3.  **Bootstrap + KI-Assistenz**

| Criterion | Custom CSS | Bootstrap Standard | Bootstrap + KI |
| :--- | :--- | :--- | :--- |
| **Entwicklungsdauer** | ❌ Langsam | ✔️ Sehr schnell | ✔️ Sehr schnell |
| **Individualität** | ✔️ Hoch | ❌ Niedrig (Generisch) | ✔️ Mittel/Gut |
| **Aufwand** | ❌ Hoch | ✔️ Minimal | ✔️ Gering |

---

## 02: Umgang mit vergangenen Matches – Zeit- & rollenbasierte Sichtbarkeit

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-01-2026

### Problem statement

Problemstellung

Sollte ein Match vergangen sein, sollte es die All Matches Seite nicht unnötig "zumüllen". Der Host müsste jedoch weiterhin die Möglichkeit haben auf das Match zugriff zu haben, um z.B. offene Rechnungen zu begleichen. Es wurde in betracht gezogen die Matches automatisch zu stornieren, jedoch erwis sich diese Lösung als unötig komplex und würde das Spiel immer noch anzeigen. 


Ziel war daher:

•	Eine aufgeräumte öffentliche Match-Übersicht

•	Planungssicherheit für Teilnehmer

•	Volle Kontrolle für Hosts über ihre erstellten Matches



### Decision

Wir haben uns gegen ein automatisches Löschen oder kurzfristiges Stornieren entschieden und stattdessen eine zeit- und rollenbasierte Sichtbarkeitslogik implementiert.

Konkret:

•	Mindestens 2 Stunden vor Start muss das Match erstellt werden

•	2 Stunden nach Beginn werden Matches:

•	aus Match Details entfernt

•	aus der Liste der beigetretenen Matches entfernt

•	Der Host hat jedoch immer noch die Möglichkeit das Match mit allen Teilnehmern anzurufen bei "erstellten Matches", dort kann er sie manuell löschen 

Diese Lösung sorgt für eine saubere Nutzeroberfläche, ohne dem Host wichtige Informationen oder Kontrolle zu entziehen.

**Decision was taken by:** github/yten27


### Regarded options

Folgende Optionen wurden evaluiert:

•   Automatisches Löschen von Matches nach Spielende

•   Automatisches Stornieren kurz vor Spielbeginn (z. B. bei zu wenigen Teilnehmern)

•   Zeit- und rollenbasierte Sichtbarkeit (gewählte Lösung)


## 03: Forms & Validation - FLASK-WTF & CSRF Protection

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 29-01-2026

### Problem statement

Unsere App hat Eingabeformulare wie z.B. Register, Login und Create Match. Diese sollen möglichst schnell und ordentlich validiert werden. Dazu gehört die Überprüfung für das Email-Format, Passwortlänge oder die Passwort Bestätigung. Wir wollen keine Eingaben aus dem HTML-Formular manuell auslesen und selbst verarbeiten und trotzdem ein gewissen Sicherheitsstandard in die App mit integrieren. Der CSRF Token schützt uns vor CSRF Angriffe bei POST anfragen.

### Decision

**Wir nutzen FLASK-WTF (WTForms) für Formulare und Validierung und aktiven zustätzlich CSRF Schutz**

Wir nutzen als Basis FLASK-WTF mithilfe von WTForms. Das bringt uns ein standardmäßigen CSRF Schutz für Forms über den Token. Unser Vorteil ist damit, dass ein Angreifer nicht im Hintergrund mit einem fremden POST Anfrage, während der User eingeloggt ist, auslösen kann ohne Token.  

**Vorteil:** Damit können wir hier ebenfalls Zeit sparen, da Validierung und Fehlerhandling in einem erledigt werde.

**Decision was taken by:** github/leongit11


### Regarded options

+ Manuelles Handling
+ WTForms / FLASK ohne CSRF
+ FLASK-WTF mit CSRF

Criterion                     | Manuell (request.form) | Flask-WTF ohne CSRF | Flask-WTF + CSRF
-----------------------------|-------------------------|---------------------|-----------------
Entwicklungsdauer            | ❌ Langsam              | ✔️ Schnell          | ✔️ Schnell
Code-Übersichtlichkeit       | ❌ Eher unübersichtlich | ✔️ Gut              | ✔️ Gut
Validierung/Fehlermeldungen  | ❌ Viel Handarbeit      | ✔️ Gut              | ✔️ Gut
Sicherheit (CSRF bei POST)   | ❌ Extra Aufwand        | ❌ Fehlend           | ✔️ Standardmäßig dabei
