CREATE TABLE guests(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE rooms(id INTEGER PRIMARY KEY, number TEXT UNIQUE NOT NULL, rate INT);
CREATE TABLE bookings(id INTEGER PRIMARY KEY, guest_id INT REFERENCES guests(id), room_id INT REFERENCES rooms(id), night TEXT, UNIQUE(room_id, night));
INSERT INTO guests(name) VALUES ('Asha'), ('Ravi');
INSERT INTO rooms(number, rate) VALUES ('101', 3000), ('102', 3500);
INSERT INTO bookings(guest_id, room_id, night) VALUES (1,1,'2026-12-01'), (1,2,'2026-12-02'), (2,1,'2026-12-03');
