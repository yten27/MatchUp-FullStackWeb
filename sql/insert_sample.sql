_BEGIN TRANSACTION;

DELETE FROM match_participant;
DELETE FROM note;
DELETE FROM match;
DELETE FROM user;

DELETE FROM sqlite_sequence;

-- 1) USERS
INSERT INTO user (email, password) VALUES ("player1@mail.com", "12345");
INSERT INTO user (email, password) VALUES ("player2@mail.com", "12345");
INSERT INTO user (email, password) VALUES ("player3@mail.com", "12345");
INSERT INTO user (email, password) VALUES ("player4@mail.com", "12345");
INSERT INTO user (email, password) VALUES ("player5@mail.com", "12345");
INSERT INTO user (email, password) VALUES ("player6@mail.com", "12345");

-- 2) MATCHES
INSERT INTO match (title, location, match_time, price, info, status, host_user_id)
VALUES ("5 gegen 5 – Feierabendkick", "Berlin Mitte – Bolzplatz A", "2026-02-02 18:30", 20,
        "Bring helle + dunkle Shirts mit.", "active", 1);

INSERT INTO match (title, location, match_time, price, info, status, host_user_id)
VALUES ("Hallenfußball 4 gegen 4", "Prenzlauer Berg – Halle 2", "2026-02-05 20:00", 40,
        "Halle ist gebucht, bitte 10 Min vorher da sein.", "active", 2);

INSERT INTO match (title, location, match_time, price, info, status, host_user_id)
VALUES ("7 gegen 7 – Sonntag", "Tempelhofer Feld", "2026-02-07 11:00", 0,
        "Gratis – Fokus auf Spaß.", "active", 3);

INSERT INTO match (title, location, match_time, price, info, status, host_user_id)
VALUES ("Training: Abschluss", "Friedrichshain – Sportplatz", "2026-02-03 19:15", 10,
        "Standards + Abschluss. Kurzes Warmup.", "cancelled", 4);

-- 3) MATCH_PARTICIPANT

-- Match 1
INSERT INTO match_participant (user_id, match_id) VALUES (1, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (2, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (3, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (4, 1);
INSERT INTO match_participant (user_id, match_id) VALUES (5, 1);

-- Match 2 
INSERT INTO match_participant (user_id, match_id) VALUES (2, 2);
INSERT INTO match_participant (user_id, match_id) VALUES (1, 2);
INSERT INTO match_participant (user_id, match_id) VALUES (3, 2);
INSERT INTO match_participant (user_id, match_id) VALUES (6, 2);

-- Match 3 
INSERT INTO match_participant (user_id, match_id) VALUES (3, 3);
INSERT INTO match_participant (user_id, match_id) VALUES (4, 3);
INSERT INTO match_participant (user_id, match_id) VALUES (5, 3);

-- Match 4 
INSERT INTO match_participant (user_id, match_id) VALUES (4, 4);
INSERT INTO match_participant (user_id, match_id) VALUES (2, 4);

-- 4) NOTES

INSERT INTO note (user_id, content) VALUES (1, "Host-Notiz: Bälle + Leibchen einpacken.");
INSERT INTO note (user_id, content) VALUES (2, "Halle: Schlüssel 19:45 abholen.");
INSERT INTO note (user_id, content) VALUES (5, "Nächstes Mal früher zusagen.");

COMMIT;
