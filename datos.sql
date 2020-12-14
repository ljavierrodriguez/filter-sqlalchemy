-- SQLite
SELECT id, name, lastname, email, phone, gender
FROM users;

INSERT INTO users (name, lastname, email, phone)
VALUES 
('Martina', 'Ojeda', 'mojeda@gmail.com', '55555551'),
('Lilian', 'Ceballo', 'lceballo@gmail.com', '55555552'),
('Diego', 'de la Vega', 'dlavega@gmail.com', '55555553'),
('Cecilia', 'Mujica', 'cmujica@gmail.com', '55555554');


UPDATE users SET gender = 'Female' WHERE id in (1, 2, 4);
UPDATE users SET gender = 'Male' WHERE id in (3);


INSERT INTO addresses (address, user_id) VALUES 
('Av Americo Vespucio Norte', 1),
('Grecia 451', 2),
('Manuel Montt 1274', 3),
('Clark 729', 4);