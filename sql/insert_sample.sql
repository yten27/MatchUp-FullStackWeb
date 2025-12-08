BEGIN TRANSACTION;

-- Beispiel-User 
INSERT INTO user (email, password)
VALUES ("leon@example.com", "pass123");

INSERT INTO user (email, password)
VALUES ("ayten@example.com", "pass123");

INSERT INTO user (email, password)
VALUES ("mario@example.com", "pass123");

-- Beispiel-Matches
INSERT INTO match (title, location, match_time, host_user_id)
VALUES ("Late Night im Käfig", "Berlin-Mitte Cage", "2025-12-10 18:00", 1);

INSERT INTO match (title, location, match_time, host_user_id)
VALUES ("Sonntag Morgen Kick", "Tempelhofer Feld", "2025-12-14 11:00", 2);

-- Teilnehmer-Zuordnungen
-- Match 1: alle drei dabei
INSERT INTO match_participant (user_id, match_id) VALUES (1, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (2, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (3, 1);

-- Match 2: Ayten + Mario
INSERT INTO match_participant (user_id, match_id) VALUES (2, 2);
INSERT INTO match_participant (user_id, match_id) VALUES (3, 2);

COMMIT;
