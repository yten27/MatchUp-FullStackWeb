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

## 01: [Frontend Styling Framework - Bootstrap & AI Support]

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 23-12-2025

### Problem statement

[Describe the problem to be solved or the goal to be achieved. Include relevant context information.]

Unser Projektfokus liegt klar auf der Implementierung der Backend-Logik (Python mit Flask). Da wir begrenzte Zeit haben, wollen wir das Design nicht als Priorität definieren. Gleichzeitig soll die App aber nicht wie eine 08/15 Standard Vorlage aussehen, sondern durch und durch nach Fußball aussehen, ohne dass wir wochenlang CSS schreiben müssen.

### Decision

[Describe **which** design decision was taken for **what reason** and by **whom**.]

*Wir kombinieren Bootstrap 5 mit KI-gestützter Anpassung.**

1.  **Basis (Bootstrap):** Wir nutzen das Framework für das grobe Layout und funktionale Komponenten (Forms, Buttons, Navigationsleiste). Das spart uns die Arbeit für die Grundstruktur.
2.  **Anpassung (KI-Support):** Um Zeit zu sparen, haben wir KI-Tools genutzt (Gemini), um spezifische CSS-Anpassungen (Custom CSS) zu generieren. Anstatt CSS-Klassen manuell nachzuschlagen, ließen wir uns Code-Snippets für Farbschemata und das Styling erstellen. [[Link zur kompletten Chatverlauf mit Gemini]]

**Vorteil:** Wir konnten uns auf den Python-Code konzentrieren, haben aber trotzdem ein sauber gestyltes Frontend, das über den Standard-Look hinausgeht.

**Decision was taken by:** github/leongit11

### Regarded options

[Describe any possible design decision that will solve the problem. Assess these options, e.g., via a simple pro/con list.]

1.  **Custom CSS (Alles selbst schreiben)**
2.  **Bootstrap Standard (Ohne Anpassung)**
3.  **Bootstrap + KI-Assistenz**

| Criterion | Custom CSS | Bootstrap Standard | Bootstrap + KI |
| :--- | :--- | :--- | :--- |
| **Entwicklungsdauer** | ❌ Langsam | ✔️ Sehr schnell | ✔️ Sehr schnell |
| **Individualität** | ✔️ Hoch | ❌ Niedrig (Generisch) | ✔️ Mittel/Gut |
| **Aufwand** | ❌ Hoch | ✔️ Minimal | ✔️ Gering |

---

## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

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
	•	Der Host hat jedoch immer noch die Möglichkeit das Match mit allen Teilnehmern anzurufen bei "erstellten
    Matches", dort kann er sie manuell löschen 

Diese Lösung sorgt für eine saubere Nutzeroberfläche, ohne dem Host wichtige Informationen oder Kontrolle zu entziehen.
**Decision was taken by:** github/yten27


### Regarded options

Folgende Optionen wurden evaluiert:
	1.	Automatisches Löschen von Matches nach Spielende
	2.	Automatisches Stornieren kurz vor Spielbeginn (z. B. bei zu wenigen Teilnehmern)
	3.	Zeit- und rollenbasierte Sichtbarkeit (gewählte Lösung)
