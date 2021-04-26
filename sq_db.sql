CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);