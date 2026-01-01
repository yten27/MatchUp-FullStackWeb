---
title: Design Decisions
nav_order: 3
---

{: .label }
[Leon Terencio Otte]

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

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

---
